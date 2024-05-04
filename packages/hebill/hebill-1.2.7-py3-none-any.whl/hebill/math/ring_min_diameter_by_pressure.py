import math


def ring_min_diameter_by_pressure(inner_diameter: float = 0, weight: float = 1000000,
                                  safety_ratio: float = 5, yield_strength: float = 27.6):
    """
    :param inner_diameter: mm
    :param weight: kgs 默认按1000吨硫化机压力
    :param safety_ratio: num 安全系数 默认 5 倍
    :param yield_strength: kgs/mm^2 默认ZG 270-500 铸钢的 屈服强度 YIELD STRENGTH (/Mpa) 270 N/mm2 (27.6 kgf/mm2)
    :return: minimal_diameter: mm
    """
    area = weight / yield_strength * safety_ratio
    return pow(area / math.pi + pow(inner_diameter / 2, 2), 0.5) * 2
