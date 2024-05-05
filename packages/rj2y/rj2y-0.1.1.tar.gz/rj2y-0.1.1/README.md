# rj2y

This CLI tool is a simple utility to convert JSON to YAML. Especially useful when you want to convert JSON including embedded JSON as a string.

It may be convenient to reading server logs. Using with [`jq`](https://github.com/jqlang/jq) and [`yq`](https://github.com/mikefarah/yq) is recommended.

## Installation

```bash
pipx install rj2y
```

## Usage

```bash
cat some.json | rj2y
rj2y some.json
```

### Example

input json and output yaml

<https://github.com/pollenjp/rj2y-py/blob/d237729c54be84f1dd78542bf4bd2476c7a16e3a/tests/unittest/test_main.py#L6-L39>

<https://github.com/pollenjp/rj2y-py/blob/d237729c54be84f1dd78542bf4bd2476c7a16e3a/tests/unittest/test_main.py#L45-L109>
