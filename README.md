# flake8-classmethod-staticmethod
[![Build Status](https://github.com/atollk/flake8-classmethod-staticmethod/workflows/tox/badge.svg)](https://github.com/atollk/flake8-classmethod-staticmethod/actions)
[![Build Status](https://github.com/atollk/flake8-classmethod-staticmethod/workflows/black/badge.svg)](https://github.com/atollk/flake8-classmethod-staticmethod/actions)


flake8 plugin that checks rules regarding the staticmethod and classmethod decorators.

## Options

The plugin offers one flag, `--select_csm1`, accepting a list of error
codes (see below) to be enabled. By default, the enabled errors
are `CSM101` and `CSM131`.

## Error Codes

### CSM100

`@staticmethod` should not be used.

### CSM101

A method marked as `@staticmethod` should not reference the class it
is defined in. Use `@classmethod` otherwise.

**Bad** 
```python
class MyClass:
    @staticmethod
    def my_name():
        return MyClass.__name__
```

**Good** 
```python
class MyClass:
    @classmethod
    def my_name(cls):
        return cls.__name__
```

### CSM102

Do not inherit and override a method marked as `@staticmethod`.

**Bad** 
```python
class MyClass:
    @staticmethod
    def my_name():
        return "MyClass"

class MyChild:
    @staticmethod
    def my_name():
        return "MyChild"
```

**Good** 
```python
class MyClass:
    @classmethod
    def my_name(cls):
        return cls.__name__
```

### CSM130

`@classmethod` should not be used.

### CSM131

A method marked as `@classmethod` should access the parameter `cls`.
Use `@staticmethod` otherwise.

**Bad** 
```python
class MyClass:
    @classmethod
    def my_name(cls):
        return "MyClass"
```

**Good** 
```python
class MyClass:
    @staticmethod
    def my_name():
        return "MyClass"
```

### CSM132
A method marked as `@classmethod` should not reference the class it
is defined in. Use the `cls` parameter.

```python
class MyClass:
    @classmethod
    def my_name(cls):
        return MyClass.__name__
```

**Good** 
```python
class MyClass:
    @classmethod
    def my_name(cls):
        return cls.__name__
```
