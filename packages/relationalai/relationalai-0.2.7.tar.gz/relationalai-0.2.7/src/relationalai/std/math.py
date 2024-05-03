import numbers

from .. import dsl

# Custom number type
Number = numbers.Number | dsl.Producer

# NOTE: Right now, common contains all Rel stdlib relations.
# If the stdlib is split into multiple namespaces, this will have to be updated.
_math_ns = dsl.global_ns.std.common


# ------------------------------
# Basics
# ------------------------------

def abs(value: Number) -> dsl.Expression:
    return _math_ns.abs(value)

def isclose(x: Number, y: Number, tolerance: Number = 1e-9) -> dsl.Expression:
    return _math_ns.approx_eq(tolerance, x, y)

def cbrt(value: Number) -> dsl.Expression:
    return _math_ns.cbrt(value)

def log(x: Number, base: Number | None = None) -> dsl.Expression:
    if isinstance(x, numbers.Number) and x <= 0:
        raise ValueError("Cannot take the logarithm of a negative number")
    if base is None:
        return _math_ns.natural_log(x)
    return _math_ns.log(base, x)

def sign(x: Number) -> dsl.Expression:
    return _math_ns.sign(x)

def sqrt(value: Number) -> dsl.Expression:
    if isinstance(value, numbers.Number) and value < 0:
        raise ValueError("Cannot take the square root of a negative number")
    return _math_ns.sqrt(value)

def trunc_divide(numerator: Number, denominator: Number) -> dsl.Expression:
    return _math_ns.trunc_divide(numerator, denominator)


# ------------------------------
# Rounding
# ------------------------------

def ceil(value: Number) -> dsl.Expression:
    return _math_ns.ceil(value)

def floor(value: Number) -> dsl.Expression:
    return _math_ns.floor(value)


# ------------------------------
# Exports
# ------------------------------

__all__ = [
    "abs",
    "isclose",
    "cbrt",
    "log",
    "sign",
    "sqrt",
    "trunc_divide",
    "ceil",
    "floor",
]
