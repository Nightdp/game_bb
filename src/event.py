# -*- coding: utf-8 -*-

import src.keyboard as keyboard
import src.mouse as mouse
import src.s3_position as position
import src.time as time
import src.user_input as user_input
import src.window as window
import src.const as const


# 设置窗口标题
def set_title(hwnd, number):
    keyboard.set_text(hwnd, "率土之滨" + str(number))


def click(hwnd, rect):
    mouse.click(hwnd, rect)
    time.sleep(1)


# 点击外部区域
def click_outside(hwnd):
    mouse.click(hwnd, position.outside_rect)
    time.sleep(1)


# 点击中心点
def click_center(hwnd):
    mouse.click_point(hwnd, window.center_x, window.center_y)
    time.sleep(1)


# 点击标记定位菜单按钮
def click_mark_location_menu(hwnd):
    mouse.click(hwnd, position.mark_location_menu_rect)
    time.sleep(0.5)


# 点击地图菜单按钮
def click_map_menu(hwnd):
    mouse.click(hwnd, position.map_menu_rect)
    time.sleep(0.5)


# 点击标记定位->主城
def click_mark_location_main_city(hwnd):
    mouse.click(hwnd, position.mark_location_menu_main_city_rect)
    time.sleep(0.5)


# 点击城市菜单进入城池部队页面
def click_city_menu(hwnd):
    mouse.click(hwnd, position.city_menu_rect)
    time.sleep(1.5)


# 点击城池队伍头像
def click_city_army(hwnd, army_index):
    mouse.click(hwnd, position.city_army_list[army_index])
    time.sleep(0.5)


# 点击城池队伍头像（双数）
def click_city_army_even(hwnd, army_index):
    mouse.click(hwnd, position.city_army_even_list[army_index])
    time.sleep(0.5)


# 点击出征队伍头像
def click_expedition_army(hwnd, army_index):
    mouse.click(hwnd, position.expedition_army_rect_list[army_index])
    time.sleep(1)


# 点击出征队伍头像（双数）
def click_expedition_army_even(hwnd, army_index):
    mouse.click(hwnd, position.expedition_army_even_rect_list[army_index])
    time.sleep(1)


# 点击武将队伍大营
def click_army_hero(hwnd, hero_index):
    mouse.click(hwnd, position.army_hero_rect_list[hero_index])
    time.sleep(0.5)


# 点击出征按钮
def click_wipe_out_button(hwnd):
    mouse.click(hwnd, position.wipe_out_button_rect)
    time.sleep(1)


# 点击强行出征
def click_hero_force_expedition(hwnd):
    mouse.click(hwnd, position.hero_force_expedition_rect)
    time.sleep(1)


# 点击页面关闭按钮
def click_page_close(hwnd):
    mouse.click(hwnd, position.page_close_rect)
    time.sleep(2)


# 点击页面返回按钮
def click_page_return(hwnd):
    mouse.click(hwnd, position.page_return_rect)
    time.sleep(3)


# 点击征兵中心按钮
def click_conscription_button(hwnd):
    mouse.click(hwnd, position.conscription_button_rect)
    time.sleep(1)


# 点击武将征兵最大值
def click_hero_conscription_max(hwnd, hero_index):
    rect = position.hero_conscription_rect_list[hero_index]
    mouse.click_point(hwnd, rect[2] - window.seek_bar_limit, int((rect[1] + rect[3]) / 2))
    time.sleep(0.2)
    mouse.click_point(hwnd, rect[2], int((rect[1] + rect[3]) / 2))
    time.sleep(0.2)


# 点击征兵条的百分比
def click_hero_conscription_percent(hwnd, hero_index, percent):
    rect = position.hero_conscription_rect_list[hero_index]
    mouse.click_point(hwnd, int(rect[0] + (rect[2] - rect[0]) * percent), int((rect[1] + rect[3]) / 2))
    time.sleep(0.5)


# 点击确认征兵按钮
def click_conscription_confirm_button(hwnd):
    mouse.click(hwnd, position.conscription_confirm_button_rect)
    time.sleep(1)


# 点击确认征兵按钮
def click_conscription_dialog_confirm_button(hwnd):
    mouse.click(hwnd, position.conscription_dialog_confirm_button_rect)
    time.sleep(1)


# 点击坐标输入框并输入（单个）
def text_input(hwnd, rect, value):
    mouse.click(hwnd, rect)
    time.sleep(0.3)
    # 删除坐标内容
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.1)
    keyboard.press_key(hwnd, keyboard.backspace)
    time.sleep(0.2)
    # 输入坐标
    keyboard.type_string(hwnd, value)
    time.sleep(0.5)


# 坐标输入
def location_input(hwnd, point):
    # 输入X坐标
    text_input(hwnd, position.location_input_x_rect, str(point[0]))
    # 输入Y坐标
    text_input(hwnd, position.location_input_y_rect, str(point[1]))


# 坐标跳转按钮
def click_location_jump_button(hwnd):
    mouse.click(hwnd, position.location_jump_rect)
    time.sleep(2)


# 点击扫荡菜单按钮
def click_wipe_out_menu(hwnd):
    mouse.click(hwnd, position.wipe_out_menu_rect)
    time.sleep(1)


# 点击出征菜单按钮
def click_army_expedition_menu(hwnd):
    mouse.click(hwnd, position.army_expedition_menu_rect)
    time.sleep(1)


# 地图放大
def map_enlarge(hwnd):
    user_input.ctrl_scroll(hwnd, 120, window.center_x, window.center_y)
    time.sleep(1)


# 地图还原
def map_reduction(hwnd):
    user_input.ctrl_scroll(hwnd, -120, window.center_x, window.center_y)
    time.sleep(1)


# 滚动一页 TODO 放配置文件
def scroll_one_page(hwnd):
    mouse.press_move_point(hwnd, (300, 760 - window.top_space), (300, 760 - window.top_space - 581))


# 重置土地统计选项
def reset_land_option(hwnd):
    mouse.click(hwnd, position.land_option_all_rect)
    time.sleep(0.5)
    mouse.click(hwnd, position.land_option_all_rect)
    time.sleep(1)


# 点击内政菜单
def click_interior_menu(hwnd):
    mouse.click(hwnd, position.interior_menu_rect)
    time.sleep(1)


# 点击内政详情菜单
def click_interior_detail_menu(hwnd):
    mouse.click(hwnd, position.interior_detail_menu_rect)
    time.sleep(1)


# 点击武将队伍配置
def click_army_setting_menu(hwnd):
    mouse.click(hwnd, position.army_setting_menu_rect)
    time.sleep(1)


# 点击武将选择里的第（index + 1）个武将
def click_hero_select(hwnd, index):
    mouse.click(hwnd, position.hero_select_rect_list[index])
    time.sleep(1)


# 武将筛选按钮
def click_hero_screen_button(hwnd):
    mouse.click(hwnd, position.hero_screen_button_rect)
    time.sleep(1)


# 武将筛选星级重置
def click_hero_screen_star_reset(hwnd):
    mouse.click(hwnd, position.hero_screen_star_reset_rect)
    time.sleep(1)


# 武将筛选兵种重置
def click_hero_screen_arms_reset(hwnd):
    mouse.click(hwnd, position.hero_screen_arms_reset_rect)
    time.sleep(1)


# 武将筛选阵营重置
def click_hero_screen_camp_reset(hwnd):
    mouse.click(hwnd, position.hero_screen_camp_reset_rect)
    time.sleep(1)


# 武将筛选星级
def click_hero_screen_star_item(hwnd, star):
    mouse.click(hwnd, position.hero_screen_star_item_rect_list[const.hero_dict[star]])
    time.sleep(1)


# 武将筛选兵种
def click_hero_screen_arms_item(hwnd, arms):
    mouse.click(hwnd, position.hero_screen_arms_item_rect_list[const.hero_dict[arms]])
    time.sleep(1)


# 武将筛选阵营
def click_hero_screen_camp_item(hwnd, camp):
    mouse.click(hwnd, position.hero_screen_camp_item_rect_list[const.hero_dict[camp]])
    time.sleep(1)


# 武将筛选重置
def click_hero_screen_reset(hwnd):
    click_hero_screen_star_reset(hwnd)
    click_hero_screen_arms_reset(hwnd)
    click_hero_screen_camp_reset(hwnd)


# 武将筛选
def click_hero_screen_item(hwnd, star, arms, camp):
    click_hero_screen_star_item(hwnd, star)
    click_hero_screen_arms_item(hwnd, arms)
    click_hero_screen_camp_item(hwnd, camp)


# 武将拖拽放置
def drag_hero_placeholder(hwnd, index, target_index):
    mouse.press_move(hwnd, position.hero_select_rect_list[index], position.army_hero_raise_rect_list[target_index])
    time.sleep(2)


# 武将拖拽下架
def drag_hero_down(hwnd, index):
    mouse.press_move(hwnd, position.army_hero_raise_rect_list[index], position.hero_select_rect_list[0])
    time.sleep(2)
