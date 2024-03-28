## Litepipe
Lightweight Python module for building modules using syntax similar to Apache Beam.

Pipelines can be created using two classes provided in this package - `Pipeline` and `Transform`.

A `Pipeline` is a one or more `Transforms` which are essentially functions cast as a `Transform` class so that they
can be easily chained together.

Once a `Pipeline` is defined, inputs can be passed through using the `run` functionality.
The output of the final step in the pipeline is returned from the `run` function.

As mentioned above `Transform` is basically a wrapper class for a function with an overloaded `__rshift__` method.
This allows `Transforms` to be chained together using a syntax like

```commandline
transform_one >> transform_two
```

This package was born from my curiosity to how packages like [Apache Beam](https://beam.apache.org/) and
[Apache Airflow](https://airflow.apache.org/) use the greater than operator to chain functions.

### Installation Instructions
```python
pip install litepipe
```

### Example Pipeline

#### Creating Transforms

Transforms can be easily created using multiple syntax

By first defining a function and passing it as a parameter to the Transform class

```
def add_two(x: int):
  return x + 2

add_two_transfrom = Transform(add_two)
```

By passing a lambda function as a parameter

```
add_transform = Transform(lambda x: x + 2)
```

Wrapping the function with a decorator function that can be imported from the Transform module

```
@t
def print_and_divide(input, divider=4):
    print(f"Input: {input} will be divided by {divider}")
    return input / divider
```

### Example Pipeline

```
add_transform = Transform(lambda x: x + 2)
hello_int = Transform(lambda x: f'Hello, {x}')

pipeline = Pipeline(add_transform >> hello_int)

result = pipeline.run(5)
# output - 'Hello, 7'
```