import textwrap


class Test_General:
    def test_pass_1(self, flake8_path):
        code = """
        class Foo:
            @some_decorator(123)  # noqa
            def bar(self):
                pass
                
            @other.decorator(key=123)  # noqa
            def baz(self):
                pass
        """
        (flake8_path / "example.py").write_text(textwrap.dedent(code))
        result = flake8_path.run_flake8()
        assert result.exit_code == 0
