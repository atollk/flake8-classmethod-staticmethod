# flake8-classmethod-staticmethod
flake8 plugin that checks rules regarding the staticmethod and classmethod decorators.

## Options

The plugin offers one flag, `--select_clst1`, accepting a list of error
codes (see below) to be enabled. By default, the enabled errors
are `CLST101` and `CLST131`.

## Error Codes

### CLST100

`@staticmethod` should not be used.

### CLST101

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

### CLST102

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

### CLST130

`@classmethod` should not be used.

### CLST131

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

### CLST132
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
