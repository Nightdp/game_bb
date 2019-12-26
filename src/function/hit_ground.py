# -*- coding: utf-8 -*-

import src.assistant as assistant
import src.event as event
import src.s3_config as config
import src.time as time
import src.util as util


# 撞地升级模块

class HitGround(object):

    def __init__(self, hwnd):
        self.hwnd = hwnd

        # 武将体力
        self.hero_physical_list = [1000, 1000, 1000]

        # 武将索引
        self.leveling_hero_index = 0

    # 定位跳转
    def location_jump(self, point):
        print("点击地图菜单")
        event.click_map_menu(self.hwnd)
        print("输入坐标")
        event.location_input(self.hwnd, point)
        print("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd)

    # 获取武将信息
    def init_army_hero_info(self, army_index):
        print("点击武将队伍")
        event.click_city_army_even(self.hwnd, army_index)

        for i in range(2):
            print("点击队伍 武将大营")
            event.click_army_hero(self.hwnd, i)

            physical = assistant.get_hero_physical(self.hwnd)
            print("获取武将体力值：%d" % physical)

            self.hero_physical_list[i] = physical

            print("关闭武将属性页面")
            event.click_page_close(self.hwnd)

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

    # 武将放置
    def hero_placeholder(self, hero, index, is_first):
        print("点击武将筛选按钮")
        event.click_hero_screen_button(self.hwnd)
        print("筛选武将")
        if not is_first:
            event.click_hero_screen_reset(self.hwnd)
        event.click_hero_screen_reset(self.hwnd)
        event.click_hero_screen_item(self.hwnd, hero[1], hero[2], hero[3])
        event.click_outside(self.hwnd)
        try_index = 0
        while True:
            print("点击武将")
            event.click_hero_select(self.hwnd, try_index)
            print("判断首个武将是否是：" + hero[0])
            hero_name = assistant.get_hero_name(self.hwnd)
            print(hero_name)
            physical = assistant.get_hero_physical(self.hwnd)
            print("体力：" + str(physical))
            print("返回上一页")
            event.click_page_close(self.hwnd)
            if util.is_similar(hero_name, hero[0]) and physical >= 10:
                print("放置武将")
                event.drag_hero_placeholder(self.hwnd, try_index, index)
                break
            else:
                print("不是该武将，或者体力不够")
                try_index += 1
                if try_index >= 3:
                    break
                if hero_name.isspace():
                    break

    # 进入城池页面
    def enter_city_page(self):
        print("点击标记定位菜单")
        event.click_mark_location_menu(self.hwnd)
        print("点击主城项")
        event.click_mark_location_main_city(self.hwnd)
        print("点击城池菜单")
        event.click_city_menu(self.hwnd)

    # 替换体力不足的武将单个部队
    def tired_hero_replace_single(self, army_index, multi):
        # 第一个放置帮助升级的武将
        click_setting = False
        print("获取武将体力信息")
        self.init_army_hero_info(army_index)
        if self.hero_physical_list[0] < 10:
            print("点击武将配置按钮")
            event.click_army_setting_menu(self.hwnd)
            if assistant.is_setting_tip(self.hwnd):
                print("返回上一页")
                event.click_page_return(self.hwnd)
                return
            click_setting = True
            # 有重复的需要，取下后再放上去
            if multi:
                print("取下第一个武将")
                event.drag_hero_down(self.hwnd, 0)
            print("放置第一个武将")
            if multi:
                self.hero_placeholder(config.help_hero, 0, True)
            else:
                self.hero_placeholder(config.leveling_hero_dict[self.leveling_hero_index], 1, True)
                self.leveling_hero_index = (self.leveling_hero_index + 1) % len(config.leveling_hero_dict)
        if self.hero_physical_list[1] < 10:
            print("放置第二个武将")
            if not click_setting:
                print("点击武将配置按钮")
                event.click_army_setting_menu(self.hwnd)
                if assistant.is_setting_tip(self.hwnd):
                    print("返回上一页")
                    event.click_page_return(self.hwnd)
                    return
                click_setting = True
            self.hero_placeholder(config.leveling_hero_dict[self.leveling_hero_index], 1, False)
            self.leveling_hero_index = (self.leveling_hero_index + 1) % len(config.leveling_hero_dict)
        print("返回上一页")
        event.click_page_return(self.hwnd)
        if click_setting:
            print("返回上一页")
            event.click_page_return(self.hwnd)

    # 替换体力不足的武将
    def tired_hero_replace(self):

        print("循环判断和替换")
        for index in range(3, 4):
            print("判断是否能配置武将状态")
            if assistant.is_city_army_enable_setting(self.hwnd, index):
                self.tired_hero_replace_single(index, index == 3)
            else:
                print("武将队伍不能配置状态")

        print("返回上一页")
        event.click_page_return(self.hwnd)

    # 撞地
    def hit_the_ground(self):
        for army_index in range(3, 4):
            # 一是带撞地武将的
            if army_index == 3:
                self.army_expedition(config.leveling_land_help)
            else:
                self.army_expedition(config.leveling_land)
            print("判断武将灰度状态")
            if assistant.is_expedition_hero_gray(self.hwnd, army_index):
                print("武将是灰色状态，无法出征")
                print("点击外部区域回到上一页")
                event.click_outside(self.hwnd)
            else:
                print("武将可以出征")
                event.click_expedition_army(self.hwnd, army_index)
                print("武将开始出征了")
                event.click_wipe_out_button(self.hwnd)
                time.sleep(2)

    # 运行
    def run(self):
        while True:
            print("进入城池页面")
            self.enter_city_page()
            print("疲倦武将替换")
            self.tired_hero_replace()
            print("武将循环出征")
            self.hit_the_ground()
            print("睡眠等待下次循环")
            time.sleep(60)
