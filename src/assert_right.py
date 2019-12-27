# -*- coding: utf-8 -*-

import src.image as image
import src.position_util as position_util
import src.s3_position as position
import src.string_util as string_util
import src.util as util


# 确认 -> 点击标记定位菜单按钮
def assert_click_mark_location_menu(hwnd):
    text = image.get_text_by_orc(hwnd, position.mark_location_menu_title_rect, 120)
    assert util.is_most_similar('标记定位', text)


# 确认 -> 点击标记定位->主城
def assert_click_mark_location_main_city(hwnd):
    value = image.is_image_similar(hwnd, '../res/location_icon.png', position.location_icon_rect)
    assert value > 0.975


# 确认 -> 是否在主城页面
def assert_enter_city_page(hwnd):
    value = image.is_image_similar(hwnd, '../res/army_overview_button.png', position.army_overview_button_rect)
    assert value > 0.975
