# EazyDocs

eazydocs looks to provide an easy way to generate code documentation by cutting down repetitive boilerplate input. By providing a class or method object, you can generate a markdown (MD) file that mixes markdown and html formatting to clearly define your code.

`eazydocs.generate_docs` will scrape a Class object for functions and methods, then scrape the parameter names, types, and default arguments for each, returning a string expression formatted for a MD file. Passing a Function or Method object will do the same, instead only for the desired object. Optionally, you can create a MD file from the output, or append it to an existing file.

`eazydocs.generate_example` will format a pandas.DataFrames to include as an example in your README file. Optionally, you can append the example to an existing MD file, with the ability to specify the specific function or method you would like to insert the string expression under.

## Table of Contents

- [Installation](#installation)
- `eazydocs.generate_docs`:
  - [Overview](#eazydocsgenerate_docs)
  - [Using a Class object](#using-a-class-object)
  - [Using a Method object](#using-a-method-object)
  - [Creating a MD File](#creating-a-md-file)
- `eazydocs.generate_example`:
  - [Overview](#eazydocsgenerate_example)
  - [Generating an Example](#creating-an-example-from-a-pandasdataframe)
  - [Appending to an Existing MD File](#appending-the-example-to-an-existing-md-file)

### Installation

- Install the eazydocs module using your preferred package manager:z
  ```
  pip install eazydocs
  ```
- Alternatively, the .whl can be downloaded and installed:
  ```
  pip install eazydocs-24.X.X-py3-none-any.whl
  ```

### eazydocs.generate_docs

<strong id='generate-docs'>generate_docs</strong>(<b>obj</b>, <b>append_to_file</b><i>=False</i>, <b>skip_private</b><i>=True</i>, <b>filename</b><i>=\_NoDefault.no_default</i>, <b>filepath</b><i>=\_NoDefault.no_default</i>)

> Parameters

<ul style='list-style: none'>
    <li>
        <b>obj : <i>object</i></b>
        <ul style='list-style: none'>
            <li>A Class or Method object.</li>
        </ul>
    </li>
    <li>
        <b>append_to_file : <i>bool, default False</i></b>
        <ul style='list-style: none'>
            <li>Append the output string expression to a MD file.</li>
        </ul>
    </li>
    <li>
        <b>skip_private : <i>bool, default True</i></b>
        <ul style='list-style: none'>
            <li>Skip functions or methods with the prefix '_' or '__'.</li>
        </ul>
    </li>
    <li>
        <b>filename : <i>str, optional</i></b>
        <ul style='list-style: none'>
            <li>String expression of the markdown file to append. Required argument if <code>append_to_file=True</code>.</li>
        </ul>
    </li>
    <li>
        <b>filepath : <i>str, optional</i></b>
        <ul style='list-style: none'>
            <li>String expression of the absolute path to the markdown file you are appending. If <code>append_to_file=True</code>, and <code>filepath=None</code>, the <code>filename</code> is expected to be in the current working directory.</li>
        </ul>
    </li>
</ul>

#### Using a Class object

- This example generates documents for the object `easydocs.Method`:

  ```
  >>> from eazydocs import generate_docs

  >>> docs = generate_docs(Method)
  >>> print(docs)

  <strong id='method'>Method</strong>(<b>method_name</b>)

  > Parameters

  <ul style='list-style: none'>
      <li>
          <b>method_name : <i>str</i></b>
          <ul style='list-style: none'>
              <li>{description}</li>
          </ul>
      </li>
  </ul>
  ```

- The resulting MD file, when rendered:
    <div style="border:1px solid gray; padding: 10px">
    <strong id='method'>Method</strong>(<b>method_name</b>)<br><br>

  > Parameters

    <ul style='list-style: none'>
        <li>
            <b>method_name : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>
    </div>

* Notice the placeholder generated under the method name: 'description'.

#### Using a Method object

- This example generates documents for the object `eazydocs.generate_docs`:

  ```
    >>> from eazydocs import generate_docs

    >>> docs = generate_docs(generate_docs)
    >>> print(docs)

    <strong id='generate-docs'>generate_docs</strong>(<b>obj</b>, <b>append_to_file</b><i>=False</i>, <b>filename</b><i>=_NoDefault.no_default</i>, <b>filepath</b><i>=_NoDefault.no_default</i>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>obj : <i>object</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>append_to_file : <i>bool, default False</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>filename : <i>str, optional</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>filepath : <i>str, optional</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>
  ```

- The resulting MD file when rendered:
    <div style="border:1px solid gray; padding: 10px">
    <strong id='generate-docs'>generate_docs</strong>(<b>obj</b>, <b>append_to_file</b><i>=False</i>, <b>filename</b><i>=_NoDefault.no_default</i>, <b>filepath</b><i>=_NoDefault.no_default</i>)

  > Parameters

    <ul style='list-style: none'>
        <li>
            <b>obj : <i>object</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>append_to_file : <i>bool, default False</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>filename : <i>str, optional</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>filepath : <i>str, optional</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>    
    </div>

#### Creating a MD file

- To create a MD file from `generate_docs` output, you can set its `append_to_file` to True. This will create a `README.md` file in your current working directory:

  ```
  >>> from eazydocs import generate_docs

  >>> generate_docs(Method, append_to_file=True)
  ```

- However, you may want to append the documents to an existing MD file, in which case you can provide the `filename`:

  ```
  >>> from eazydocs import generate_docs

  >>> generate_docs(
        Method,
        append_to_file=True,
        filename='METHOD'
      )
  ```

- Optionally, you can provide a `filepath` to the MD file, in addition to the `filename`:

  ```
  >>> from eazydocs import generate_docs

  >>> generate_docs(
        Method,
        append_to_file=True,
        filename='METHOD',
        filepath='~/$USER/eazydocs/output'
      )
  ```

  - The string argument provided to `filepath` is joined with `filename` as a pathlib.Path object

### eazydocs.generate_example

<strong id='generate-example'>generate_example</strong>(<b>df</b>, <b>df_shape</b><i>=[5, 5]</i>, <b>code</b><i>='df'</i>, <b>append_to_file</b><i>=False</i>, <b>filename</b><i>=\_NoDefault.no_default</i>, <b>filepath</b><i>=\_NoDefault.no_default</i>, <b>method_name</b><i>=\_NoDefault.no_default</i>)

> Parameters

<ul style='list-style: none'>
    <li>
        <b>df : <i>pandas.DataFrame</i></b>
        <ul style='list-style: none'>
            <li>Pandas DataFrame to format.</li>
        </ul>
    </li>
    <li>
        <b>df_shape : <i>list[int], default [5, 5]</i></b>
        <ul style='list-style: none'>
            <li>Integer list defining the desired shape of the <code>df</code>. First integer is the desired number of rows, while the second is the desired number of columns. Passing <code>df_shape=[-1, -1]</code> will generate the string expression without reshaping <code>df</code> - not recommended for large DataFrames.</li>
        </ul>
    </li>
    <li>
        <b>code : <i>str, default 'df'</i></b>
        <ul style='list-style: none'>
            <li>Line of code you would like displayed before the DataFrame example. This is useful if you are demonstrating how a method changes a DataFrame.</li>
        </ul>
    </li>
    <li>
        <b>append_to_file : <i>bool, default False</i></b>
        <ul style='list-style: none'>
            <li>Append output string expression to an existing MD file.</li>
        </ul>
    </li>
    <li>
        <b>filename : <i>str, optional</i></b>
        <ul style='list-style: none'>
            <li>String expression of the markdown file to append. Required argument if <code>append_to_file=True</code>.</li>
        </ul>
    </li>
    <li>
        <b>filepath : <i>str, optional</i></b>
        <ul style='list-style: none'>
            <li>String expression of the absolute path to the markdown file you are appending. If <code>append_to_file=True</code>, and <code>filepath=None</code>, the MD file is expected to be in the current working directory.</li>
        </ul>
    </li>
    <li>
        <b>method_name : <i>str, optional</i></b>
        <ul style='list-style: none'>
            <li>String expression of the specific method name you would like to insert this example under. If <code>method_name=None</code>, the string generated from the example is inserted at the end of the MD file.</li>
        </ul>
    </li>
</ul>

#### Creating an Example from a pandas.DataFrame

- Basic example using default parameters:

  ````
  >>> from eazydocs import generate_example
  >>> df = DataFrame({'col_1': [0, 1, 2, 3, 4, 5], 'col_2': [0, 1, 2, 3, 4, 5], 'col_3': [0, 1, 2, 3, 4, 5] ... 'col_10': [0, 1, 2, 3, 4, 5]})
  >>> df.shape
      (7, 10)

  >>> example = generate_example(df)
  >>> example
      ```
      >>> df
      col_1  col_2  col_3  col_4  col_5
      0      0      0      0      0      0
      1      1      1      1      1      1
      2      2      2      2      2      2
      3      3      3      3      3      3
      4      4      4      4      4      4
      ```
  ````

- Specifying the shape of the DataFrame before its formatted to a string expression:

  ````
      >>> df = DataFrame({'col_1': [0, 1, 2, 3, 4, 5], 'col_2': [0, 1, 2, 3, 4, 5], 'col_3': [0, 1, 2, 3, 4, 5] ... 'col_10': [0, 1, 2, 3, 4, 5]})
      >>> df.shape
          (7, 10)

      >>> example = generate_example(df, df_shape=(5,10))
      >>> example
          ```
          >>> df
          col_1  col_2  col_3  col_4  col_5
          0      0      0      0      0      0
          1      1      1      1      1      1
          2      2      2      2      2      2
          3      3      3      3      3      3
          4      4      4      4      4      4
          ```
  ````

- Specifying the code displayed before the string expression:

  ````
  >>> dff = DataFrame({'col_1': [0, 1, 2, 3, 4, 5], 'col_2': [0, 1, 2, 3, 4, 5], 'col_3': [0, 1, 2, 3, 4, 5] ... 'col_10': [0, 1, 2, 3, 4, 5]})

  >>> example = generate_example(dff, code = 'dff')
  >>> example
      ```
      >>> dff
      col_1  col_2  col_3  col_4  col_5
      0      0      0      0      0      0
      1      1      1      1      1      1
      2      2      2      2      2      2
      3      3      3      3      3      3
      4      4      4      4      4      4
      ```
  ````

#### Appending the example to an existing MD file:

```
>>> generate_example(df, append_to_file=True, filename='EXAMPLE')
Succesfully updated 'EXAMPLE.md' (~/$USER/easydocs/EXAMPLE.md)
```

- Appending the example to a method in an existing MD file:

  - **Note**: This requires the existing MD file to have been created, or at least the desired method, using `eazydocs.generate_docs()`.

    **cls.py**

    ```
    class Cls:
        def __init__(self, s1: str) -> None:
            ...

        def method_1(self, new_str: str) -> str:
            ...

        def method_2(self, another_str: str, optional_str: str) -> str:
            ...
    ```

    **~/\$USER/README.md**
    <div style="border:1px solid gray; padding: 10px">

    <strong id='cls'>Cls</strong>(<b>s1</b>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>s1 : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>

    <strong id='method-1'>method_1</strong>(<b>new_str</b>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>new_str : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>

    <strong id='method-2'>method_2</strong>(<b>another_str</b>, <b>optional_str</b>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>another_str : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>optional_str : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul><br>

    **~/\$USER/main.py**

        ```
        >>> df = DataFrame({'col_1': [0, 1, 2, 3, 4, 5], 'col_2': [0, 1, 2, 3, 4, 5], 'col_3': [0, 1, 2, 3, 4, 5] ... 'col_10': [0, 1, 2, 3, 4, 5]})

        >>> generate_example(df, df_shape=(5,10), append_to_file=True, filename='README', method_name='method_1')
        Successfully update 'method_1' in 'README.md' (~/$USER/README.md)
        ```

    **~/\$USER/README.md**
    <div style="border:1px solid gray; padding: 10px">
    <strong id='cls'>Cls</strong>(<b>s1</b>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>s1 : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>

    <strong id='method-1'>method_1</strong>(<b>new_str</b>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>new_str : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>

    > Example

    ```
    >>> df
    col_1  col_2  col_3  col_4  col_5
    0      0      0      0      0      0
    1      1      1      1      1      1
    2      2      2      2      2      2
    3      3      3      3      3      3
    4      4      4      4      4      4
    ```

    <strong id='method-2'>method_2</strong>(<b>another_str</b>, <b>optional_str</b>)

    > Parameters

    <ul style='list-style: none'>
        <li>
            <b>another_str : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
        <li>
            <b>optional_str : <i>str</i></b>
            <ul style='list-style: none'>
                <li>description</li>
            </ul>
        </li>
    </ul>
    </div>
