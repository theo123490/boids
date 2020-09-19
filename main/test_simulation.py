from unittest import TestCase
import simulation as sim

class Testindividual(TestCase):

    def test_move(self):
        point_a = sim.individual(5, 5)
        point_a.move(5, 10)
        self.assertEqual(point_a.x, 10)
        self.assertEqual(point_a.y, 15)
