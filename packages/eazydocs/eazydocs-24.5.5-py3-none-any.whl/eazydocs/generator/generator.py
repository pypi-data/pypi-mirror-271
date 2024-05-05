from inspect import getmembers, signature, isfunction, ismethod

from eazydocs.generator.parameters import Parameters


class Generator:
    def __init__(self, cls: object, skip_private: bool) -> None:
        self.skip_private = skip_private
        self.name = cls.__name__

        self.generate_docs(cls)

    def generate_docs(self, cls: object) -> None:
        docs = str()

        for name, member in getmembers(cls):
            if ismethod(member) or isfunction(member):
                if self._check_member(member):
                    params = Parameters(member, self.skip_private).params
                    docs += f"\n{params}\n"

        self.docs = docs
        self._fmt_class_name()

    def __repr__(self) -> str:
        return self.docs

    def _check_member(self, method: object) -> bool:
        method_name = method.__name__
        if self.skip_private:
            if method_name[0] == "_" or method_name[0:2] == "__" and method_name != "__init__":
                return False

        return self._check_params(method)

    def _check_params(self, method) -> bool:
        params = signature(method).parameters
        params = [param for param in params.keys() if param != "self"]
        if params == []:
            return False

        return True

    def _fmt_class_name(self) -> None:
        if self.docs.__contains__("__init__"):
            docs = self.docs.replace("--init--", self.name.lower())
            docs = docs.replace("__init__", self.name)
            self.docs = docs
