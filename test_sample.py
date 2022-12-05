import unittest


class SampleTest(unittest.TestCase):
    def test_sum_should_succeed(self):
        self.assertEqual(6, 6, "Should be 6")

    def test_sum_should_fail(self):
        self.assertNotEqual(3, 6, "Should not ge the same")


if __name__ == "__main__":
    unittest.main()
