import pickle
import uuid
from pickle import PicklingError

from Mesh.System.Entity.Concrete.Light import Light
from Mesh.System.Space import Space
from Mesh.System.SpaceFactor import SpaceFactor
from Mesh.System.System import System
from MeshTest.AppTestCase import AppTestCase


class TestPickleable(AppTestCase):
    def test_space(self):
        space = Space((5, 5, 5), space_factor_types=[i for i in SpaceFactor])

        try:
            pickle.dumps(space)
        except PicklingError:
            self.fail('Space is NOT pickable')

    def test_light(self):
        light = Light(uuid=uuid.uuid4())

        self.assertRaises(TypeError, lambda: pickle.dumps(light))

        light.destroy()

    def test_system(self):
        system = System(name='MyNewSystem')
        system.put_space((5, 5, 5), space_factor_types=[i for i in SpaceFactor])

        light = Light(uuid=uuid.uuid4())
        system.put_entity(light, (0, 0, 0))

        self.assertRaises(TypeError, lambda: pickle.dumps(system))

        light.destroy()
