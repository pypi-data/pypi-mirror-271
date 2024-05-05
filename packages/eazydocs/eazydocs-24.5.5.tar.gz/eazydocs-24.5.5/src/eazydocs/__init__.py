from inspect import isclass, ismethod, isfunction
from pandas import DataFrame

from eazydocs.generator.example import Example
from eazydocs.generator.generator import Generator
from eazydocs.generator.parameters import Parameters

from eazydocs.md.md_file import MDFile


def generate_docs(obj: object, skip_private: bool = True, append_to_file: bool = False, filename: str = None, filepath: str = None) -> str:
    if isclass(obj):
        docs = Generator(obj, skip_private).docs
    elif isfunction(obj) or ismethod(obj):
        docs = Parameters(obj, skip_private).params

    docs = docs.strip()

    if append_to_file != False:
        MDFile(filename, docs, filepath).append()

    return docs


def generate_example(
    df: DataFrame,
    df_shape: list[int] = [5, 5],
    code: str = "df",
    append_to_file: bool = False,
    filename: str = None,
    filepath: str = None,
    method_name: str = None,
) -> str:
    example = Example(code, df, df_shape).output

    if append_to_file != False:
        if filename == None:
            raise ValueError(
                "generate_example missing 1 required positional argument: 'filename'. Set 'append_to_file=False', if you would like the string output of this function."
            )

        if method_name != None:
            MDFile(filename, example, filepath).append_to_param(method_name)
        else:
            MDFile(filename, example, filepath)

    return example
