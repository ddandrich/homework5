# tests/test_ideal.py
import importlib
import math
import pytest

#
# Import the public API from the package top-level (as required).
# This assumes your package is named 'rocket_relations' and that
# __init__.py re-exports c_star and thrust_coefficient.
#
from rocket_relations import c_star, thrust_coefficient


# ---------------------------
# Package / module docstrings
# ---------------------------

def test_package_docstring_present():
    pkg = importlib.import_module("rocket_relations")
    assert isinstance(pkg.__doc__, str) and pkg.__doc__.strip() != ""


def test_module_docstring_present():
    ideal = importlib.import_module("rocket_relations.ideal")
    assert isinstance(ideal.__doc__, str) and ideal.__doc__.strip() != ""


def test_top_level_exports_exist():
    # Ensure the re-exported names are actually present at the package root
    pkg = importlib.import_module("rocket_relations")
    assert hasattr(pkg, "c_star")
    assert hasattr(pkg, "thrust_coefficient")


# ---------------------------
# Correctness: numeric checks
# ---------------------------

def test_c_star_value():
    gamma = 1.2
    R = 350.0
    T0 = 3500.0
    expected = 1706.6214101221442
    assert c_star(gamma, R, T0) == pytest.approx(expected, rel=1e-12)


def test_thrust_coefficient_value():
    gamma = 1.2
    pe_p0 = 0.0125
    pa_p0 = 0.02
    area_ratio = 10.0
    expected = 1.5423078989789598
    assert thrust_coefficient(gamma, pe_p0, pa_p0, area_ratio) == pytest.approx(expected, rel=1e-12)


# ---------------------------
# Validation: domain errors
# ---------------------------

@pytest.mark.parametrize(
    "gamma,R,T0",
    [
        (1.0, 350.0, 3500.0),   # gamma <= 1
        (1.2, 0.0, 3500.0),     # R <= 0
        (1.2, 350.0, 0.0),      # T0 <= 0
    ],
)
def test_c_star_invalid_domain(gamma, R, T0):
    with pytest.raises(ValueError):
        c_star(gamma, R, T0)


@pytest.mark.parametrize(
    "gamma,pe_p0,pa_p0,area_ratio",
    [
        (1.0, 0.2, 0.01, 10.0),   # gamma <= 1
        (1.2, -0.01, 0.01, 10.0), # pe/p0 < 0
        (1.2, 1.0, 0.01, 10.0),   # pe/p0 >= 1
        (1.2, 0.2, -0.01, 10.0),  # pa/p0 < 0
        (1.2, 0.2, 1.0, 10.0),    # pa/p0 >= 1
        (1.2, 0.2, 0.01, 0.999),  # area_ratio < 1
    ],
)
def test_thrust_coefficient_invalid_domain(gamma, pe_p0, pa_p0, area_ratio):
    with pytest.raises(ValueError):
        thrust_coefficient(gamma, pe_p0, pa_p0, area_ratio)


# ---------------------------
# Validation: type errors
# (Your simple implementation will raise TypeError naturally
# when comparing non-numeric to numbers.)
# ---------------------------

@pytest.mark.parametrize(
    "gamma,R,T0",
    [
        ("1.2", 350.0, 3500.0),
        (1.2, "350", 3500.0),
        (1.2, 350.0, "3500"),
    ],
)
def test_c_star_non_numeric_types(gamma, R, T0):
    with pytest.raises(TypeError):
        c_star(gamma, R, T0)


@pytest.mark.parametrize(
    "gamma,pe_p0,pa_p0,area_ratio",
    [
        ("1.2", 0.2, 0.01, 10.0),
        (1.2, "0.2", 0.01, 10.0),
        (1.2, 0.2, "0.01", 10.0),
        (1.2, 0.2, 0.01, "10"),
    ],
)
def test_thrust_coefficient_non_numeric_types(gamma, pe_p0, pa_p0, area_ratio):
    with pytest.raises(TypeError):
        thrust_coefficient(gamma, pe_p0, pa_p0, area_ratio)
