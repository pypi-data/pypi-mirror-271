import math

from math import ceil


class TestClass:
    def __init__(self):
        pass

    def print_x(self):
        print('x')


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


if __name__ == '__main__':
    assert gcd(40, 100)


def main():
    assert gcd(40, 100)
