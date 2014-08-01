__author__ = 'Swallow'
import math

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
    :param u: vector1
    :param v: vector2
    :return: u[0] * v[0], u[1] * v[1], ...
    """
    return [u[i]*v[i] for i in range(len(u))]


def multiplybyNumber(v, c):
    """
    :param v: vector
    :param c: constant
    :return: v[0] * c, v[1] * c, ...
    """
    return [c * elem for elem in v]


def normalize(v):
    vmag = magnitude(v)
    return [v[i]/vmag  for i in range(len(v))]

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)