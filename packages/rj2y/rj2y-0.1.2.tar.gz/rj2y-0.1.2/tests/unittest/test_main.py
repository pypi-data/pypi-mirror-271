from rj2y.main import parse_embedded_json_string


def test_yaml_node_dump() -> None:
    sample_json = r"""
{
  "aaa": "AAA",
  "bbb": true,
  "ccc": 123,
  "ccc2": "123",
  "ddd": 123.456,
  "ddd2": "123.456",
  "eee": [
    "e",
    "ee",
    "eee"
  ],
  "fff": {
    "f": "f",
    "ff": "ff",
    "fff": "fff"
  },
  "ggg": [
    {
      "g": "g",
      "gg": "gg",
      "ggg": "ggg"
    },
    {
      "g": "g",
      "gg": "gg",
      "ggg": "ggg"
    }
  ],
  "hhh": "{\"h\":\"h\",\"hh\":\"hh\",\"hhh\":\"hhh\"}",
  "iii": "{\"i\":\"{\\\"ii\\\": \\\"ii\\\"}\",\"ii\":\"ii\"}",
  "jjj": "jj1\njj2\njj3",
  "kkk": "{\"k\": \"{\\\"kk\\\": \\\"kk1\\\\nkk2\\\\nkk3\\\\n\\\"}\"}"
}
"""

    parsed_data = parse_embedded_json_string(sample_json)
    assert (
        parsed_data.dump()
        == r"""aaa: !!str
  AAA
bbb: !!bool
  true
ccc: !!int
  123
ccc2: !!str
  123
ddd: !!float
  123.456
ddd2: !!str
  123.456
eee:
  - !!str
    e
  - !!str
    ee
  - !!str
    eee
fff:
  f: !!str
    f
  ff: !!str
    ff
  fff: !!str
    fff
ggg:
  -
    g: !!str
      g
    gg: !!str
      gg
    ggg: !!str
      ggg
  -
    g: !!str
      g
    gg: !!str
      gg
    ggg: !!str
      ggg
hhh:
  h: !!str
    h
  hh: !!str
    hh
  hhh: !!str
    hhh
iii:
  i:
    ii: !!str
      ii
  ii: !!str
    ii
jjj: !!str |-
  jj1
  jj2
  jj3
kkk:
  k:
    kk: !!str |-
      kk1
      kk2
      kk3
"""
    )
