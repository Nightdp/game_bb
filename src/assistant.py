# -*- coding: utf-8 -*-

import src.image as image
import src.position_util as position_util
import src.s3_position as position
import src.string_util as string_util
import src.util as util


# 城池的武将是否是灰色状态（调动的）
def is_city_hero_gray(hwnd, hero_index):
    return image.is_gray_map(image.image_grab(hwnd, position_util.top_right(position.city_army_list[hero_index])))


# 出征的武将是否是灰色状态（调动的）
def is_expedition_hero_gray(hwnd, hero_index):
    return image.is_gray_map(
        image.image_grab(hwnd, position_util.top_right(position.expedition_army_rect_list[hero_index])))


# 出征的武将是否是灰色状态（调动的）(双数)
def is_expedition_hero_even_gray(hwnd, hero_index):
    return image.is_gray_map(
        image.image_grab(hwnd, position_util.top_right(position.expedition_army_even_rect_list[hero_index])))


# 城池的武将队伍是否可征兵状态
def is_city_army_enable_conscription(hwnd, army_index):
    # 是否在征兵
    is_conscription = image.is_image_similar(hwnd, '../res/conscription.png',
                                             position_util.hero_status(position.city_army_list[army_index])) > 0.975
    # 是否在行军
    is_march = image.is_image_similar(hwnd, '../res/march.png',
                                      position_util.hero_status(position.city_army_list[army_index])) > 0.975
    # 是否在返回
    is_return = image.is_image_similar(hwnd, '../res/return.png',
                                       position_util.hero_status(position.city_army_list[army_index])) > 0.975
    # 是否在练兵
    is_training = image.is_image_similar(hwnd, '../res/training.png',
                                         position_util.hero_status(position.city_army_list[army_index])) > 0.975
    return not is_conscription and not is_march and not is_return and not is_training


# 城池的武将队伍是否可配置武将状态
def is_city_army_enable_setting(hwnd, army_index):
    # 是否在征兵
    is_conscription = image.is_image_similar(hwnd, '../res/conscription.png',
                                             position_util.hero_status(position.city_army_list[army_index])) > 0.975
    # 是否在行军
    is_march = image.is_image_similar(hwnd, '../res/march.png',
                                      position_util.hero_status(position.city_army_list[army_index])) > 0.975
    # 是否在返回
    is_return = image.is_image_similar(hwnd, '../res/return.png',
                                       position_util.hero_status(position.city_army_list[army_index])) > 0.975
    # 是否在练兵
    is_training = image.is_image_similar(hwnd, '../res/training.png',
                                         position_util.hero_status(position.city_army_list[army_index])) > 0.975
    return not is_conscription and not is_march and not is_return and not is_training


# 获取武将队伍页面的兵力
def get_city_army_troops(hwnd, army_index):
    return image.get_number_by_orc(hwnd, position_util.hero_troops(position.city_army_list[army_index]), 180)


# 获取武将体力
def get_hero_physical(hwnd):
    number = image.get_number_tuple_by_orc(hwnd, position.hero_physical_value_rect, 80, '/')
    number_pair = string_util.get_number_pair_by_split(number, '/')
    return number_pair[0]


# 获取武将征兵时长
def get_hero_conscription_duration(hwnd, hero_index):
    text = image.get_number_tuple_by_orc(hwnd, position.hero_conscription_duration_rect_list[hero_index], 130, ':')
    duration = string_util.get_time_by_string(text)
    return duration


# 武将是否兵力足够
def is_troops_enough(hwnd, hero_index):
    return image.get_number_by_orc(hwnd, position_util.hero_troops(position.expedition_army_rect_list[hero_index]), 130)


# 征兵不可用
def is_conscription_disable(hwnd):
    return image.is_above_main_threshold(image.image_grab(hwnd, position.conscription_button_rect), 60)


# 征兵队列已满
def is_conscription_button_gray(hwnd):
    return image.is_gray_map(image.image_grab(hwnd, position.conscription_confirm_button_rect))


# 当前部队处于非待命状态
def is_setting_tip(hwnd):
    text = image.get_text_by_orc(hwnd, position.conscription_tip_rect, 120)
    return util.is_similar(text, '当前部队处于非待命状态')


# 是否是五级地
def is_land_5_tone(hwnd):
    return image.is_image_similar(hwnd, image.open_image('../res/land_5_tone.png'), position.center_land_rect)


# 获取单页坐标列表
def get_one_page_land_location_list(hwnd):
    # 识别坐标
    text = image.get_multi_text(hwnd, position.land_list_location_rect, lang=image.english, threshold=120,
                                whitelist='0123456789(),').replace(" ", "")
    # 去除无用内容
    split = text.split('\n')
    # 倒序移除无用数据
    for i in range(len(split) - 1, -1, -1):
        if split[i].find('(') < 0:
            split.pop(i)
    # 坐标列表
    location_list = []
    for item_location in split:
        split_number = item_location.replace("(", "").replace(")", "").split(",")
        if len(split_number) == 2 and split_number[0].isdigit() and split_number[1].isdigit():
            location_list.append((int(split_number[0]), int(split_number[1])))
    return location_list


# 获取土地信息
def get_land_info(hwnd):
    text = image.get_multi_text(hwnd, position.center_land_info_rect, lang=image.chinese, threshold=100,
                                whitelist='')
    split = text.split('\n')
    # 循环移除前后无效字符
    for i in range(len(split)):
        split[i] = split[i].strip()
    # 倒序移除无用数据
    for i in range(len(split) - 1, -1, -1):
        if len(split[i]) == 0:
            split.pop(i)
    return split


# 获取土地等级
def get_land_level(hwnd):
    text = image.get_single_line_text(hwnd, position.center_land_level_rect, lang=image.chinese, threshold=150,
                                      whitelist='Lv.123456789')
    text = text.strip().replace(" ", "")
    index = text.find('Lv.')
    if index >= 0:
        number = text[(index + len('Lv.')):]
        if number.isdigit():
            return int(number)
    return 0


# 获取土地统计信息列表
def get_land_statistics_list(hwnd, left):
    if left:
        rect = position.land_statistics_left_list
    else:
        rect = position.land_statistics_right_list
    text = image.get_multi_text(hwnd, rect, lang=image.chinese, threshold=100,
                                whitelist='')
    split = text.split('\n')
    # 循环移除前后无效字符
    for i in range(len(split)):
        split[i] = split[i].strip()
    # 倒序移除无用数据
    for i in range(len(split) - 1, -1, -1):
        if len(split[i]) == 0:
            split.pop(i)
    return split


# 图地选项矩形位置
def get_land_option_rect(hwnd, level):
    left_rect = get_land_option_side_rect(hwnd, level, True)
    right_rect = get_land_option_side_rect(hwnd, level, False)
    if left_rect is None:
        return right_rect
    else:
        return left_rect


# 图地选项矩形位置(一侧)
def get_land_option_side_rect(hwnd, level, left):
    if left:
        option_list = get_land_statistics_list(hwnd, True)
    else:
        option_list = get_land_statistics_list(hwnd, False)
    # 寻找
    target_index = -1
    for i in range(len(option_list)):
        if option_list[i].find('领地Lv.%d' % level) >= 0:
            target_index = i
            break
    if target_index < 0:
        return None
    else:
        if left:
            return position_util.land_option(position.left_land_option_first_rect, position.land_option_item_height,
                                             target_index)
        else:
            return position_util.land_option(position.right_land_option_first_rect, position.land_option_item_height,
                                             target_index)


# 获取行军时长
def get_march_duration(hwnd):
    text = image.get_single_line_text(hwnd, position.march_duration_rect, lang=image.chinese, threshold=180,
                                      whitelist='0123456789:')
    duration = string_util.get_time_by_string(text)
    return duration


# 获取武将名称
def get_hero_name(hwnd):
    return image.get_column_text_by_orc(hwnd, position.hero_name_rect, 120).replace(" ", "").replace("\n", "")


# 获取等待时长（征兵，行军之类）
def get_wait_duration(hwnd, army_index):
    text = image.get_red_text_single_by_orc(hwnd, position_util.time_consuming(position.city_army_list[army_index]),
                                            'eng', '0123456789:')
    duration = string_util.get_time_by_string(text)
    return duration
