from flake8_classmethod_staticmethod.checker import PYTHON_38
from tests.util import BaseTest


class Test_CLST100(BaseTest):
    def error_code(self) -> str:
        return "CLST100"

    def test_pass_1(self):
        code = """
        class Foo:
            def bar(self):
                pass
            
            @classmethod
            def baz(cls):
                pass
        """
        result = self.run_flake8(code)
        assert result == []

    def test_fail_1(self):
        code = """
        class Foo:
            @staticmethod
            def bar():
                pass
        """
        result = self.run_flake8(code)
        self.assert_error_at(result, "CLST100", 3 if PYTHON_38 else 2, 5)
