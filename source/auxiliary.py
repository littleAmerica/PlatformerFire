__author__ = 'Swallow'
import math
import operator

#Vector operation
def magnitude(v):
    return math.sqrt(sum(v[i] * v[i] for i in range(len(v))))


def add(u, v):
    assert len(v) == len(u)
    return [u[i] + v[i] for i in range(len(u))]


def sub(u, v):
    assert len(v) == len(u)
    return [u[i] - v[i] for i in range(len(u))]


def dot(u, v):
    assert len(v) == len(u)
    return sum(u[i] * v[i] for i in range(len(u)))


def multiply(u, v):
    """
    multiply vector on another vector or a number
    :param u: vector1
    :param v: vector2 or constant
    :return: u[0] * v[0], u[1] * v[1], ...
    """
    #vector on constant
    if isinstance(v, (float, int)) and isinstance(u, (list, tuple)):
        c = v
        return [c * elem for elem in v]
    #vector on vector
    elif isinstance(v, (list, tuple)) and isinstance(u, (list, tuple)):
        return [u[i]*v[i] for i in range(len(u))]

    def class_name(a):
        return a.__class__.__name__

    raise TypeError("TypeError: unsupported operand type(s) for multiply function: {} and {}",
                    class_name(u), class_name(v))


def normalize(v):
    vmag = magnitude(v)
    return [v[i]/vmag for i in range(len(v))]


def division(u, v):
    return [u[i] / v[i] for i in range(len(u))]


def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)


def dict_union(d1, d2):
    return dict(d1, **d2)