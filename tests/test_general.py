import textwrap


class Test_General:
    def test_pass_1(self, flake8dir):
        code = """
        class Foo:
            @some_decorator(123)  # noqa
            def bar(self):
                pass
                
            @other.decorator(key=123)  # noqa
            def baz(self):
                pass
        
        """
        flake8dir.make_example_py(textwrap.dedent(code))
        result = flake8dir.run_flake8()
        assert result.exit_code == 0
