import re
import token
import warnings
from pathlib import Path
from typing import List

from black.nodes import syms
from blib2to3.pytree import Node  # type: ignore

from refers.definitions import COMMENT_SYMBOL
from refers.errors import TagAlreadyExistsError
from refers.errors import TagNotFoundError
from refers.errors import TagNotInClass
from refers.errors import TagNotInFunction


class Tag:
    def __init__(
        self,
        name: str,
        line_num: int,
        line: str,
        file: Path,
        line_num_start: int,
        line_num_end: int,
        full_line: str,
        parent_node: Node,
    ):
        self._name = name
        self._line_num = line_num
        self._line = line
        self._file = file
        self._line_num_start = line_num_start
        self._line_num_end = line_num_end
        self._full_line = full_line

        current_parent, self._func_name = parent_node, None
        while self.func_name is None and current_parent.type != token.NT_OFFSET:
            if current_parent.type == syms.funcdef:
                self._func_name = re.sub(
                    r"\s*(\w+)\s*\n?", r"\1", str(current_parent.children[1])
                )
                break
            current_parent = current_parent.parent

        current_parent, self._class_name = parent_node, None
        while self._class_name is None and current_parent.type != token.NT_OFFSET:
            if current_parent.type == syms.classdef:
                self._class_name = re.sub(
                    r"\s*(\w+)\s*\n?", r"\1", str(current_parent.children[1])
                )
                break
            current_parent = current_parent.parent

    @property
    def name(self):
        return self._name

    @property
    def line_num(self):
        return self._line_num

    @property
    def line(self):
        return self._line

    @property
    def file(self):
        return self._file

    @property
    def line_num_start(self):
        return self._line_num_start

    @property
    def line_num_end(self):
        return self._line_num_end

    @property
    def full_line(self):
        return self._full_line

    @property
    def func_name(self):
        return self._func_name

    @property
    def class_name(self):
        return self._class_name

    def visit_name(self, *args, **kwargs) -> str:
        return self._name

    def visit_line_num(self, *args, **kwargs) -> str:
        return str(self._line_num)

    def visit_line(self, *args, **kwargs) -> str:
        return str(self._line_num)

    def visit_file(self, *args, **kwargs) -> str:
        return self._file.name

    def visit_line_num_start(self, *args, **kwargs) -> str:
        return str(self._line_num_start)

    def visit_line_num_end(self, *args, **kwargs) -> str:
        return str(self._line_num_end)

    def visit_full_line(self, *args, **kwargs) -> str:
        return self._full_line

    def visit_default(self, *args, **kwargs) -> str:
        return str(self.file.name) + " L" + str(self.line_num)

    def visit_quotecode(self, *args, **kwargs) -> str:
        """return code without comments"""
        if self.file.suffix.lower() not in COMMENT_SYMBOL.keys():
            warnings.warn(f"{self.file.suffix} not recognised. Using :quote option")
            return str(self.full_line)
        return re.sub(
            rf"{COMMENT_SYMBOL[self.file.suffix.lower()]}.*(\n?)",
            r"\1",
            self.full_line,
        ).strip()

    def visit_quote(self, *args, **kwargs) -> str:
        return str(self.full_line)

    def visit_fulllinkline(self, *args, **kwargs) -> str:
        return str(self.file.as_posix()) + "#L" + str(self.line_num)

    def visit_fulllink(self, *args, **kwargs) -> str:
        return str(self.file.as_posix())

    def visit_linkline(self, parent_dir: Path, *args, **kwargs) -> str:
        return (
            str(self.file.relative_to(parent_dir).as_posix())
            + "#L"
            + str(self.line_num)
        )

    def visit_link(self, parent_dir: Path, *args, **kwargs) -> str:
        return str(self.file.relative_to(parent_dir).as_posix())

    # def visit_p(self, num_parents, *args, **kwargs) -> str:
    #     return (
    #         self.file.parent.relative_to(self.file.parents[num_parents])
    #         / self.file.name
    #     ).as_posix()

    @staticmethod
    def visit_unknown_tag(*args, **kwargs) -> str:
        return "TAG-NOT-FOUND"

    def visit_func(self, *args, **kwargs):
        if self._func_name is None:
            raise TagNotInFunction
        return self._func_name

    def visit_class(self, *args, **kwargs):
        if self._class_name is None:
            raise TagNotInClass
        return self._class_name


class Tags:
    def __init__(self):
        self.all_tags: List[Tag] = []

    def is_tag(self, tag_name: str) -> Tag | None:
        """check if tag already exists"""
        for tag in self.all_tags:
            if tag._name == tag_name:
                return tag
        return None

    def add_tag(self, new_tag: Tag):
        """add new tag"""
        if self.is_tag(new_tag._name) is not None:
            raise TagAlreadyExistsError(f"""Tag {new_tag._name} is not unique.""")
        self.all_tags.append(new_tag)

    def get_tag(self, tag_name: str):
        tag = self.is_tag(tag_name)
        if tag is None:
            raise TagNotFoundError(f"Tag {tag_name} not found")
        return tag
