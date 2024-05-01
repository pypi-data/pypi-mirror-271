import pytest
from tdi_rust_python_tools import add_chemical_formula_subscript

from chemical_formulae import add_chemical_formula_subscript_python


@pytest.mark.parametrize(
    argnames=("value",),
    argvalues=(
        ("",),
        ("H2O",),
        ("C6H12O6",),
        ("This product contains H2O and O2",),
    ),
)
def test_add_chemical_formula_subscript(value: str) -> None:
    assert add_chemical_formula_subscript(value) == add_chemical_formula_subscript_python(value)
