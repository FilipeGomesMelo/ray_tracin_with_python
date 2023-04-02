
from components import Vector3
import unittest

class TestVector(unittest.TestCase):
    def setUp(self) -> None:
        self.v1 = Vector3(1., -2., -2.)
        self.v2 = Vector3(3., 6., 9.)
    
    def testMagnitude(self):
        self.assertEqual(self.v1.magnitude(), 3)
    
    def testAddition(self):
        result = self.v1 + self.v2
        self.assertEqual(result, Vector3(4, 4, 7))
    
    def testSubtraction(self):
        result = self.v2 - self.v1
        self.assertEqual(result, Vector3(2, 8, 11))

    def testMultiplication(self):
        result = self.v1 * 2
        self.assertEqual(result, Vector3(2, -4, -4))

    def testcross_product(self):
        result = self.v1.cross_product(self.v2)
        self.assertEqual(result, Vector3(-6., -15., 12))

    
    def testDivision(self):
        result = self.v1 / 2
        self.assertEqual(result, Vector3(0.5, -1, -1))
    
    def testUnaryNeg(self):
        result = -self.v1
        self.assertEqual(result, Vector3(-1, 2, 2))
    
    def testdot_product(self):
        result = self.v1 ^ self.v2, self.v1.dot_product(self.v2)
        self.assertEqual(result, (-27, -27))
    
    def testNormalize(self):
        result = self.v1.normalize()
        self.assertEqual(result, Vector3(1/3, -2/3, -2/3))

if __name__ == '__main__':
    unittest.main()
    