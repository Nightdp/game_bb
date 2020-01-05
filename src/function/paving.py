# -*- coding: utf-8 -*-

import src.assistant as assistant
import src.event as event
import src.path as path
import src.time as time
from src.db_manager import DBManager


# 铺路模块

class Paving(object):

    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.db = DBManager()

    # 选择部队
    def choose_army(self):
        for hero_index in range(5):
            print("判断武将灰度状态")
            # TODO 判断兵力
            if assistant.is_expedition_hero_gray(self.hwnd, hero_index):
                print("武将是灰色状态，无法出征")
                print("点击外部区域回到上一页")
            else:
                print("武将可以出征")
                event.click_expedition_army(self.hwnd, hero_index)
                print("武将开始出征了")
                duration = assistant.get_march_duration(self.hwnd)
                print("计算行军时长: " + str(duration))
                event.click_wipe_out_button(self.hwnd)
                time.sleep(duration * 2 + 30)
                return True
        return False

    # 队伍出征
    def army_expedition(self, point):
        print("定位到指定位置")
        self.location_jump(point)
        print("地图放大")
        event.map_enlarge(self.hwnd)
        print("点击土地")
        event.click_center(self.hwnd)
        print("地图还原")
        event.map_reduction(self.hwnd)
        print("点击出征菜单按钮")
        event.click_army_expedition_menu(self.hwnd)

    # 定位跳转
    def location_jump(self, point):
        print("点击地图菜单")
        event.click_map_menu(self.hwnd)
        print("输入坐标")
        event.location_input(self.hwnd, point)
        print("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd)

    # 占领下一个土地
    def occupy_next_land(self, start, end):
        next_location = path.get_better_next_possible_location(start, end)
        min_level = 10
        fit_location = None
        for location in next_location:
            print("从数据库中读取数据：")
            land_info = self.db.get_land_info(location)
            # 有该信息，并且土地信息等级不等于0
            if land_info is not None:
                if land_info['land_level'] == 0:
                    land_level = 10
                else:
                    land_level = land_info['land_level']
            else:
                print("土地：" + str(location))
                self.location_jump(location)
                print("点击土地")
                event.click_center(self.hwnd)
                print("识别土地等级")
                land_level = assistant.get_land_level(self.hwnd)
                print("等级：%d" % land_level)
            # 判断最小的土地等级
            if min_level > land_level:
                min_level = land_level
                fit_location = location
        return fit_location

    def run(self):
        start = (1092, 1377)
        end = (1103, 1384)
        while start != end:
            temp = self.occupy_next_land(start, end)
            print("武将出征")
            self.army_expedition(temp)
            print("选择合适的武将出征")
            while not self.choose_army():
                print("重新选择武将")
                time.sleep(60)
            start = temp
