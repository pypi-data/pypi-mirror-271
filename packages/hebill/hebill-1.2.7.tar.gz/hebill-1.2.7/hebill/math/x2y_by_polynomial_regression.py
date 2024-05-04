import numpy


def x2y_by_polynomial_regression(x, x_list, y_list, degree: int = 2):
    """
    :param x: 获取y需要对应的x
    :param x_list: 基础x数组
    :param y_list: 基础y数组
    :param degree: 幂
    :return: 返回 x对应的y
    """
    cs = numpy.polyfit(x_list, y_list, degree)
    r = 0.0
    for i in range(degree, 0, -1):
        r += pow(x, i) * cs[degree - i]
    r += cs[-1]
    return r
