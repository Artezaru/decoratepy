import unittest
from decoratepy import TimerCounterLogger
from decoratepy import class_propagate  # Replace `mymodule` with the actual module name containing `class_propagate`

class TestClassPropagateWithTimesDecorator(unittest.TestCase):
    def test_class_propagate_times_decorator(self):
        # Create a Times decorator instance
        decorator = TimerCounterLogger()  # Repeat the decorated method 3 times

        # Define a class with methods to decorate
        @class_propagate(decorator, names=["method1", "method2"])
        class TestClass:
            def method1(self):
                return "method1 called"

            def method2(self):
                return "method2 called"

            def method3(self):
                return "method3 called (not decorated)"

        # Instantiate the decorated class
        obj = TestClass()

        # Test method1 is repeated 3 times
        self.assertEqual(obj.method1(), "method1 called")

        # Test method2 is repeated 3 times
        self.assertEqual(obj.method2(), "method2 called")

        # Test method3 remains undecorated
        self.assertEqual(obj.method3(), "method3 called (not decorated)")

        print(decorator)

    def test_class_propagate_all_methods(self):
        # Apply Times decorator to all methods
        decorator = TimerCounterLogger()  # Repeat the decorated method 2 times

        @class_propagate(decorator)
        class TestClass:
            def method1(self):
                return "method1 called"

            def method2(self):
                return "method2 called"

        obj = TestClass()

        # Test all methods are repeated twice
        self.assertEqual(obj.method1(), "method1 called")
        self.assertEqual(obj.method2(), "method2 called")

        print(decorator)

if __name__ == "__main__":
    unittest.main()
