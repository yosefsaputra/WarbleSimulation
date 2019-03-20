import json

import numpy as np

from WarbleSimulation import settings
from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function.Powered import PowerOutput
from WarbleSimulation.System.Entity.Task import TaskResponse, Command, Status
from WarbleSimulation.System.SpaceFactor import MatterType


class PowerSupply(Concrete):
    identifier = 'PowerSource'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.METAL)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.runnable = True
        self.task_active = False

        self.power_management.power_outputs.append(PowerOutput(self))

    def get_default_shape(self):
        matter = self.matter_type.value
        shape = np.array([[[matter]]])

        return shape

    def run(self, result_queue, mp_task_pipe):
        if result_queue is None and mp_task_pipe is None:
            return

        while True:
            # TODO still need much definition and design decisions

            # TODO do the actuator action
            if result_queue is not None:
                pass

            # Do the submitted Task
            if mp_task_pipe is not None and mp_task_pipe.poll(settings.ENTITY_TASK_POLLING_DURATION):
                task = mp_task_pipe.recv()
                if task.command == Command.END:
                    self.task_active = False
                    mp_task_pipe.send(TaskResponse(Status.OK, None))
                    mp_task_pipe.close()
                    break

                elif task.command == Command.ACTIVE:
                    self.task_active = True
                    for power_output in self.power_management.power_outputs:
                        power_output.voltage = 110

                elif task.command == Command.DEACTIVATE:
                    self.task_active = False
                    for power_output in self.power_management.power_outputs:
                        power_output.voltage = 0

                else:
                    if self.task_active:
                        mp_task_pipe.send(self.handle_task(task))

    def handle_task(self, task):
        if task.command == Command.GET_INFO:
            response = {
                'uuid': str(self.uuid),
                'identifier': type(self).identifier,
                'type': {
                    'actuator': [
                        'LUMINOSITY'
                    ],
                    'sensor': [],
                    'accessor': []
                },
            }
            return json.dumps(response)
        else:
            return None
