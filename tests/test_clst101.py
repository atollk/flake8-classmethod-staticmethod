from flake8_classmethod_staticmethod.checker import PYTHON_38
from tests.util import BaseTest


class Test_CLST101(BaseTest):
    def error_code(self) -> str:
        return "CLST101"

    def test_pass_1(self):
        code = """
        class Foo:
            def bar(self):
                self.__name__

            @classmethod
            def baz(cls):
                cls.__name__
        """
        result = self.run_flake8(code)
        assert result == []

    def test_pass_2(self):
        code = """
        class Foo:
            @staticmethod
            def bar():
                return 123
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        class Foo:
            @staticmethod
            def bar():
                return Foo.__name__
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "CLST101", 3 if PYTHON_38 else 2, 5)
