import re

from tdi_rust_python_tools import add_chemical_formula_subscript

from shared.shared import timeit

TEST_VALUES: list[str] = [
    "",
    "H2O",
    "H20S4",
    "This product contains H2O and O2",
    "C6H12O6",
    "NaCl",
    "CO2",
    "CH4",
    "C12H22O11",
    "HCl",
    "NH3",
    "This product contains NaCl and CO2",
    "The reaction produced CH4 and H2O",
]

FORMULA_PATTERN = re.compile(r"([A-Za-z])(\d+)")


def add_chemical_formula_subscript_python(value: str) -> str:
    return FORMULA_PATTERN.sub(r"\1<sub>\2</sub>", value)


@timeit
def process_python() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = add_chemical_formula_subscript_python(value)


@timeit
def process_rust() -> None:
    for _ in range(1_000_000):
        for value in TEST_VALUES:
            _ = add_chemical_formula_subscript(value)


def main() -> None:
    process_python()
    process_rust()


if __name__ == "__main__":
    main()
