# -*- coding: utf-8 -*-

# 平局时长
draw_duration = 5 * 60
# 平局次数
draw_count = 1
# 误差时长
error_duration = 3 * 60

# 兵力增长系数
troops_increase_factor = 0.03

# 基础兵力列表
land_basics_troops_list = [0, 200, 750, 2100, 6000, 9000, 16500, 21000, 25500, 30000]

# 一次出征时长
one_wipe_out_duration = 60 * 60 - draw_duration * draw_count - error_duration

# 武将属性字典
hero_dict = {
    '5星': 0,
    "4星": 1,
    '3星': 2,
    "2星": 3,
    '1星': 4,

    "弓": 0,
    '步': 1,
    '骑': 2,

    '群': 0,
    '汉': 1,
    '魏': 2,
    '蜀': 3,
    '吴': 4
}

# 资源名称
resource_name_list = ['木材', '铁矿', '石料', '粮草']
