import math
from decimal import Decimal

from asce7.figure import Figure, Curve, _return_value
from asce7.interpolate import InterpolationError
import pytest
from pytest import approx


NAMES = list("ab")


# for building curve objects, testing lookups, testing errors
XY_LISTS, DEPENDENTS, ANSWERS, ERRORS = zip(
    ((["0.1", "0.6"], ["0.0", "5.0"]), "0.3", 2, "0.0"),
    ((["0.1", "-0.5"], ["5.0", "11.0"]), "-0.1", 7, "-0.6"),
)


# for testing figure objects
FIGURE_KWARGS, REPRS = zip(
    ({}, "Figure()"),
    ({"a": ([], [])}, "Figure(a=([], []))"),
    (dict(zip(NAMES, XY_LISTS)), "Figure(a=(['0.1', '0.6'], ['0.0', '5.0']), b=(['0.1', '-0.5'], ['5.0', '11.0']))"),
)


@pytest.fixture(scope = "module", params = [float, Decimal])
def curve_value_type(request):
    """Convert string values used to make curves (see above)"""
    return request.param


@pytest.fixture(scope = "module")
def curves(curve_value_type):
    """List of all the curve objects to be tested"""
    return [Curve(*([curve_value_type(v) for v in lst] for lst in tup)) for tup in XY_LISTS]


@pytest.fixture(scope = "module", params = range(len(XY_LISTS)))
def curve_no(request):
    """For running tests on each Curve object individually."""
    return request.param


@pytest.fixture(scope = "module", params = range(len(FIGURE_KWARGS)))
def figure_no(request):
    """For running tests on each Figure object individually."""
    return request.param


@pytest.fixture(scope = "module", params = range(2, len(FIGURE_KWARGS)))
def figure_no_nonempty(request):
    """For running tests only on the non-empty Figure objects individually."""
    return request.param


@pytest.fixture(scope = "module")
def figure(figure_no):
    """Figure objects to be tested"""
    return Figure(**FIGURE_KWARGS[figure_no])


@pytest.fixture(scope = "function")
def figure_nonempty(figure_no_nonempty):
    """Figure objects to be tested that have curve members"""
    return Figure(**FIGURE_KWARGS[figure_no_nonempty])


@pytest.fixture(scope = "module")
def fixture_repr(figure_no):
    """For checking the figure reprs"""
    return REPRS[figure_no]


@pytest.fixture(scope = "module")
def curve(curve_no, curves):
    """Curve objects to be tested"""
    return curves[curve_no]


@pytest.fixture(scope = "module")
def answer(curve_no):
    """Answers to be looked up"""
    return ANSWERS[curve_no]


@pytest.fixture(scope = "module")
def dependent(curve_no, curve_value_type):
    """Variable to be looked up"""
    return curve_value_type(DEPENDENTS[curve_no])


@pytest.fixture(scope = "module")
def error_value(curve_no, curve_value_type):
    """Lookups to be checked that results in errors"""
    return curve_value_type(ERRORS[curve_no])


def test_figure_repr(figure: Figure, fixture_repr: str):
    """Check figure display"""
    assert repr(figure) == fixture_repr


def test_lookup(curve, answer, dependent):
    """Check interpolation"""
    assert curve.lookup(dependent) == approx(answer)


def test_lookup_error(curve, error_value):
    """Check interpolation error"""
    with pytest.raises(InterpolationError):
        curve.lookup(error_value)


@pytest.fixture(params = [
    "from_dependent",
    "to_dependent",
    "from_independent",
    "to_independent",
])
def figure_conversion_method_name(request):
    """Method names for checking all the conversions"""
    return request.param


@pytest.fixture(params = NAMES)
def figure_attr(request):
    """Figure member names"""
    return request.param


@pytest.fixture
def figure_conversion_method(figure_conversion_method_name, figure_nonempty, figure_attr):
    """All the conversions to be checked"""
    curve = getattr(figure_nonempty, figure_attr)
    return getattr(curve, figure_conversion_method_name)


@pytest.fixture(params = [0.001234, 1.1, 3679, Decimal("123.456")])
def conversion_value(request):
    """A bunch of values to be converted"""
    return request.param


def test_figure_conversion(figure_conversion_method, conversion_value):
    """A bunch of conversion tests"""
    assert figure_conversion_method(conversion_value) == approx(conversion_value)


@pytest.fixture(params = [None, _return_value, math.log], ids = ["default", "unchanged", "log"])
def conversion_func(request):
    """A bunch of changes to the conversion test"""
    return request.param if request.param is not None else _return_value


@pytest.fixture
def modify_figure_conversion(figure_conversion_method_name, figure_nonempty, figure_attr, conversion_func):
    """Execute changes to conversion"""
    curve = getattr(figure_nonempty, figure_attr)
    setattr(curve, figure_conversion_method_name, conversion_func)


@pytest.fixture
def figure_conversion_modified(modify_figure_conversion, figure_conversion_method_name, figure_nonempty, figure_attr):
    """Already modified conversion methods"""
    curve = getattr(figure_nonempty, figure_attr)
    return getattr(curve, figure_conversion_method_name)


@pytest.fixture
def converted_value(conversion_value, conversion_func):
    """Correct answers for tested conversions"""
    return conversion_func(conversion_value)


def test_figure_conversion_modified(figure_conversion_modified, conversion_value, converted_value):
    """Check modified conversions for correctness"""
    assert figure_conversion_modified(conversion_value) == approx(converted_value)
