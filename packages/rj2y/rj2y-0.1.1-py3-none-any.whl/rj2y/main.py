import json
import sys
import textwrap
import typing as t
from abc import ABC, abstractmethod

import click

YamlGeneralValueType: t.TypeAlias = int | str | bool | float | t.Mapping[t.Any, t.Any] | t.Iterable[t.Any]

T = t.TypeVar("T", str, int, float, bool, dict[str, YamlGeneralValueType], list[YamlGeneralValueType])


class YamlNode(ABC):
    indent_size = 2

    @property
    def tag(self) -> str | None:
        return None

    @abstractmethod
    def dump(self) -> str:
        pass


class StrYamlNode(YamlNode):
    def __init__(self, value: str):
        self.value = value

    @property
    def tag(self) -> str:
        if len(self.value.split("\n")) > 1:
            return "!!str |-"
        return "!!str"

    def dump(self) -> str:
        return self.value


class IntYamlNode(YamlNode):
    def __init__(self, value: int):
        self.value = value

    @property
    def tag(self) -> str:
        return "!!int"

    def dump(self) -> str:
        return str(self.value)


class FloatYamlNode(YamlNode):
    def __init__(self, value: float):
        self.value = value

    @property
    def tag(self) -> str:
        return "!!float"

    def dump(self) -> str:
        return f"{self.value}"


class BoolYamlNode(YamlNode):
    def __init__(self, value: bool):  # noqa: FBT001
        self.value = value

    @property
    def tag(self) -> str:
        return "!!bool"

    def dump(self) -> str:
        return "true" if self.value else "false"


class MappingYamlNode(YamlNode):
    def __init__(self, value: dict[str, YamlNode]):
        self.value = value

    @classmethod
    def parse(cls, obj: dict[str, YamlGeneralValueType]) -> "MappingYamlNode":
        root: dict[str, YamlNode] = {}
        for k, v in obj.items():
            root[k] = parse_to_yaml_node(v)
        return cls(root)

    def dump(self) -> str:
        return "\n".join(
            [
                "\n".join(
                    [
                        f"{k}:" + ("" if v.tag is None else f" {v.tag}"),
                        textwrap.indent(v.dump(), " " * self.indent_size),
                    ]
                )
                for k, v in self.value.items()
            ]
        )


class ListYamlNode(YamlNode):
    def __init__(self, value: list[YamlNode]):
        self.value = value

    @classmethod
    def parse(cls, obj: list[YamlGeneralValueType]) -> "ListYamlNode":
        root: list[YamlNode] = []
        for v in obj:
            root.append(parse_to_yaml_node(v))
        return cls(root)

    def dump(self) -> str:
        return "\n".join(
            [
                "\n".join(
                    [
                        "-" + ("" if v.tag is None else f" {v.tag}"),
                        textwrap.indent(v.dump(), " " * self.indent_size),
                    ]
                )
                for v in self.value
            ]
        )


def parse_embedded_json_string(obj: str) -> "StrYamlNode | MappingYamlNode | ListYamlNode":
    if ((stripped_str := obj.strip()).startswith("{") and stripped_str.endswith("}")) or (
        stripped_str.startswith("[") and stripped_str.endswith("]")
    ):  # if encoded json string, parse it
        decoded_json: list[t.Any] | dict[str, t.Any] | None = None
        try:  # json check
            decoded_json = json.loads(obj)
        except json.JSONDecodeError:  # return raw string if json decode error
            click.echo(f"Failed to decode JSON string: {str(obj)!r}", err=True)
            pass

        if isinstance(decoded_json, dict):
            return MappingYamlNode.parse(decoded_json)
        elif isinstance(decoded_json, list):
            return ListYamlNode.parse(decoded_json)
    return StrYamlNode(obj)


def parse_to_yaml_node(v: YamlGeneralValueType) -> YamlNode:
    if isinstance(v, str):
        return parse_embedded_json_string(v)
    if isinstance(v, bool):  # note: bool should be checked before int because bool is a subclass of int
        return BoolYamlNode(v)
    if isinstance(v, int):
        return IntYamlNode(v)
    if isinstance(v, float):
        return FloatYamlNode(v)
    if isinstance(v, dict):
        return MappingYamlNode.parse(v)
    if isinstance(v, list):
        return ListYamlNode.parse(v)
    er_msg = f"Invalid type: {v}"
    raise ValueError(er_msg)


@click.command()
@click.argument("json_file", type=click.File("r"), default=sys.stdin)
def main(json_file: t.TextIO) -> None:
    """Parse JSON file to YAML. This command can also parse JSON string embedded in a string."""
    data: YamlGeneralValueType
    with json_file as f:
        data = json.load(f)

    parsed_data = parse_to_yaml_node(data)
    click.echo(parsed_data.dump())


if __name__ == "__main__":
    main()
