from flake8_classmethod_staticmethod.checker import PYTHON_38
from tests.util import BaseTest


class Test_CLST132(BaseTest):
    def error_code(self) -> str:
        return "CLST132"

    def test_pass_1(self):
        code = """
        class Foo:
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
        class Foo:
            @classmethod
            def bar(cls):
                print(1)
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        class Foo:
            @classmethod
            def bar(cls):
                cls.__name__
                return Foo.__name__
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "CLST132", 3 if PYTHON_38 else 2, 5)
