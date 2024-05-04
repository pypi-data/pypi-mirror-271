import dataclasses
import decimal


@dataclasses.dataclass
class Foo:
    name: str
    v: decimal.Decimal
