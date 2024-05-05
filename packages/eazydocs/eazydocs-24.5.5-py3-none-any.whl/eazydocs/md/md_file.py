from pathlib import Path


class MDFile:
    def __init__(self, filename: str = None, to_append: str = None, filepath: Path | str = None) -> None:
        if to_append == None:
            raise ValueError("Markdown() missing 1 required positional argument: 'to_append'")
        else:
            self.to_append = to_append

        self._set_path_attr(filepath)

        if filename != None:
            filename = self._check_filename(filename)
        else:
            filename = self._set_filename()

        self.filename = filename
        self.filepath = Path(self.cwd, filename)

    def append(self) -> None:
        to_append = f"\n\n{self.to_append}"
        with open(self.filepath, "+a") as f:
            f.write(to_append)

        print(f"Succesfully updated '{self.filename}' ({self.filepath})")

    def append_to_param(self, method_name: str) -> None:
        before, after = self._slice_contents_at_insert_position(method_name)
        to_append = self._generate_output_str(before, after)

        with open(self.filepath, "w") as f:
            f.write(to_append)

        print(f"Succesfully updated '{method_name}' in '{self.filename}' ({self.filepath})")

    def _set_path_attr(self, path: None | Path = None) -> None:
        if type(path) == str:
            path = Path(path)

        if path != None:
            self.p = path
            self.cwd = path
        else:
            p = Path()
            self.p = p
            self.cwd = p.cwd()

    def _check_filename(self, filename: str) -> str:
        filename = filename.strip()

        if filename[-3:] != ".md":
            filename += ".md"

        return filename

    def _set_filename(self) -> str:
        if Path(self.cwd, "README.md").exists():
            md_files = list(self.p.glob("README_*.md"))

            try:
                last_file = str(md_files.pop())
                last_filename = last_file.replace(".md", "").split("_")
                last_file_num = int(last_filename[-1])
                filename = f"README_{last_file_num+1}.md"
            except IndexError:
                filename = "README_2.md"

        else:
            filename = "README.md"

        self._create_file(filename)

        return filename

    def _create_file(self, filename: str) -> None:
        with open(filename, "w") as f:
            f.write("")

        print(f"Created markdown file: '{filename}'.")

    def _slice_contents_at_insert_position(self, method_name: str) -> tuple[str, str]:
        with open(self.filepath, "r+") as f:
            contents = f.read()

            if contents == "":
                raise ValueError(f"Unable to append to '{method_name}' - '{self.filename}' is empty")
            if contents.__contains__(method_name) is False:
                raise ValueError(f"Unable to find {method_name} in {self.filename}. Confirm '{method_name}' is found in '{self.filepath}'")

            method_start = contents.find(f">{method_name}<")
            next_method_start = contents.find("<strong", method_start)

            before = contents[0:next_method_start].strip()
            after = contents[next_method_start:-1].strip()

            return (before, after)

    def _generate_output_str(self, s1: str, s2: str) -> str:
        output = s1 + "\n\n> Example\n\n" + self.to_append + "\n" + s2
        return output
