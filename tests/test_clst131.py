from flake8_classmethod_staticmethod.checker import PYTHON_38
from tests.util import BaseTest


class Test_CLST131(BaseTest):
    def error_code(self) -> str:
        return "CLST131"

    def test_pass_1(self):
        code = """
        class FooX:
            def bar(self):
                self.__name__
                
            def baz(self):
                return 123

            @staticmethod
            def qux():
                return 456
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        class FooX:
            @classmethod
            def bar(cls):
                print(cls.__name__)
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        class FooX:
            @classmethod
            def bar(cls):
                return 123
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "CLST131", 3 if PYTHON_38 else 2, 5)
