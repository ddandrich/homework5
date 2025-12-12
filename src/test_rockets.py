# tests/test_ideal.py
import importlib
import pytest
import numpy as np

from rocket_relations import c_star, thrust_coefficient
from rocket_relations.ideal import (
    area_ratio,
    ve,
    Isp,
    m_dot,
    F_th,
    F,
)


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

    P0 = 5.0e6          # Pa (5 MPa chamber pressure)
    Pe = 0.0125 * P0   # exit pressure
    Pa = 0.02 * P0     # ambient pressure

    area_ratio_val = 10.0
    expected = 1.5423078989789598

    assert thrust_coefficient(gamma, Pe, Pa, P0, area_ratio_val) == pytest.approx(
        expected, rel=1e-12
    )


def test_ve_value():
    gamma = 1.2
    R = 350.0
    T0 = 3500.0

    P0 = 5.0e6
    Pe = 6.25e4

    expected = 2760.1322871571533
    assert ve(gamma, R, T0, Pe, P0) == pytest.approx(expected, rel=1e-12)


def test_Isp_value():
    cf = 1.5423078989789598
    g0 = 9.80665
    cstar = 1706.6214101221442

    expected = 268.4031429079241
    assert Isp(cf, g0, cstar) == pytest.approx(expected, rel=1e-12)


def test_m_dot_value():
    cstar = 1706.6214101221442
    a_star = 0.01
    P0 = 5.0e6

    expected = 29.297651900676357
    assert m_dot(cstar, a_star, P0) == pytest.approx(expected, rel=1e-12)


def test_F_th_value():
    P0 = 5.0e6
    a_star = 0.01
    cf = 1.5423078989789598

    expected = 77115.39494894799
    assert F_th(P0, a_star, cf) == pytest.approx(expected, rel=1e-12)


def test_F_value():
    m_dot = 29.297651900676357
    isp = 268.4031429079241
    g0 = 9.80665

    expected = 77115.394948948
    assert F(m_dot, isp, g0) == pytest.approx(expected, rel=1e-12)

# ---------------------------
# Validation: domain errors
# ---------------------------

@pytest.mark.parametrize(
    "gamma,R,T0",
    [
        (1.0, 350.0, 3500.0),
        (1.2, 0.0, 3500.0),
        (1.2, 350.0, 0.0),
    ],
)
def test_c_star_invalid_domain(gamma, R, T0):
    with pytest.raises(ValueError):
        c_star(gamma, R, T0)


@pytest.mark.parametrize(
    "gamma,Pe,Pa,P0,area_ratio_val",
    [
        (1.0, 1.0e5, 1.0e5, 5.0e6, 10.0),     # gamma <= 1
        (1.2, -1.0e5, 1.0e5, 5.0e6, 10.0),    # Pe < 0
        (1.2, 5.0e6, 1.0e5, 5.0e6, 10.0),     # Pe >= P0
        (1.2, 1.0e5, -1.0e5, 5.0e6, 10.0),    # Pa < 0
        (1.2, 1.0e5, 5.0e6, 5.0e6, 10.0),     # Pa >= P0
        (1.2, 1.0e5, 1.0e5, 5.0e6, 0.999),    # area_ratio < 1
    ],
)
def test_thrust_coefficient_invalid_domain(gamma, Pe, Pa, P0, area_ratio_val):
    with pytest.raises(ValueError):
        thrust_coefficient(gamma, Pe, Pa, P0, area_ratio_val)


@pytest.mark.parametrize(
    "gamma,Pe,P0",
    [
        (1.0, 1.0e5, 5.0e6),
        (1.2, 0.0, 5.0e6),
        (1.2, 1.0e5, 0.0),
    ],
)
def test_area_ratio_invalid_domain(gamma, Pe, P0):
    with pytest.raises(ValueError):
        area_ratio(gamma, Pe, P0)


@pytest.mark.parametrize(
    "gamma,R,T0,Pe,P0",
    [
        (1.0, 350.0, 3500.0, 1.0e5, 5.0e6),
        (1.2, 0.0, 3500.0, 1.0e5, 5.0e6),
        (1.2, 350.0, 0.0, 1.0e5, 5.0e6),
        (1.2, 350.0, 3500.0, -1.0e5, 5.0e6),
        (1.2, 350.0, 3500.0, 5.0e6, 5.0e6),
    ],
)

def test_ve_invalid_domain(gamma, R, T0, Pe, P0):
    with pytest.raises(ValueError):
        ve(gamma, R, T0, Pe, P0)