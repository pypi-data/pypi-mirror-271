class Method:
    def __init__(self, method_name: str) -> None:
        self.fn = self._generate_function(method_name)

    def _generate_function(self, method: str) -> str:
        method = method.strip()
        method_id = method.replace("_", "-")
        return f"<strong id='{method_id}'>{method}</strong>("

    def _fmt_function(self) -> str:
        fn = self.fn.removesuffix(", ") + ")"
        return fn