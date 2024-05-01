from gcd import gcd

x = type(dict().keys())


class test_class:
    def __init__(self):
        self.x = 0

    def add(self, num):
        self.x += num


class my_int(int):
    def trolol(self):
        pass


class my_dict(dict):
    pass


class my_super_int(my_int):
    pass


def main():

    gcd(5, 6)

    dict_ = {1: 1, 2: 2, 3: 3}
    1 in dict_

    dict_[1]

    del dict_[1]

    dict_[2] = 5

    list_ = [0, 1, 2]

    del list_[1]

    list_[1]

    list_[1] = 0
    set_ = {0, 1, 2}

    del set_

    b_ = bytearray(b"example data")
    b_[0]
    del b_[0]

    b_[0] = 3

    x = range(1, 10)

    x.start


main()

# testing_func()
