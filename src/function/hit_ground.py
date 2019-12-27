# -*- coding: utf-8 -*-

import src.assistant as assistant
import src.assert_event as event
import src.s3_config as config
import src.time as time
import src.util as util
import src.log as log


# 撞地升级模块

class HitGround(object):

    def __init__(self, hwnd):
        self.hwnd = hwnd

        # 武将体力
        self.hero_physical_list = [1000, 1000, 1000]

        # 武将索引
        self.leveling_hero_index = 0

        # 最短等待时间列表
        self.min_wait_duration_list = [12 * 60 * 60, 12 * 60 * 60, 12 * 60 * 60, 12 * 60 * 60, 12 * 60 * 60]

    # 重置数据
    def reset_data(self):
        self.min_wait_duration_list = [12 * 60 * 60, 12 * 60 * 60, 12 * 60 * 60, 12 * 60 * 60, 12 * 60 * 60]

    # 定位跳转
    def location_jump(self, point):
        log.info("点击地图菜单")
        event.click_map_menu(self.hwnd)
        log.info("输入坐标")
        event.location_input(self.hwnd, point)
        log.info("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd)

    # 获取武将信息
    # army_index：部队索引
    def init_army_hero_info(self, army_index):

        log.info("获取等待时间：")
        wait_duration = assistant.get_wait_duration(self.hwnd, army_index)

        if assistant.is_city_army_enable_conscription(self.hwnd, army_index):
            log.info("兵力不够，并且不在不可征兵状态，不计算等待时长")
        else:
            self.min_wait_duration_list[army_index] = wait_duration
            log.info("兵力足够，设置等待时间，否则不计算")

        log.info("最小等待时间：" + str(wait_duration) + "秒")

        log.info("点击武将队伍：第 %d 个部队" % army_index)
        # 双数的
        event.click_city_army_even(self.hwnd, army_index)

        log.info("循环遍历武将，获取武将信息：")
        for index in range(2):
            log.info("点击部队->武将大营")
            event.click_army_hero(self.hwnd, index)

            physical = assistant.get_hero_physical(self.hwnd)
            log.info("获取武将体力值：%d" % physical)

            # 暂存体力信息
            self.hero_physical_list[index] = physical

            log.info("关闭武将属性页面")
            event.click_page_close(self.hwnd)

    # 队伍出征
    def army_expedition(self, point):
        log.info("定位到指定位置")
        self.location_jump(point)
        log.info("地图放大")
        event.map_enlarge(self.hwnd)
        log.info("点击土地")
        event.click_center(self.hwnd)
        log.info("地图还原")
        event.map_reduction(self.hwnd)
        log.info("点击出征菜单按钮")
        event.click_army_expedition_menu(self.hwnd)

    # 武将放置
    # hero：武将信息
    # index: 武将在队伍的索引
    # is_first：是否是大营
    def hero_placeholder(self, hero, index, is_first):
        log.info("点击武将筛选按钮（第一次）")
        event.click_hero_screen_button(self.hwnd)
        log.info("筛选武将配置：（重置后选择武将信息）")
        if not is_first:
            event.click_hero_screen_reset(self.hwnd)
        event.click_hero_screen_reset(self.hwnd)
        event.click_hero_screen_item(self.hwnd, hero[1], hero[2], hero[3])
        event.click_outside(self.hwnd)
        # 武将池武将索引
        try_index = 0
        while True:
            log.info("点击武将：第 %d 个" % try_index)
            event.click_hero_select(self.hwnd, try_index)
            log.info("判断首个武将是否是：" + hero[0])
            hero_name = assistant.get_hero_name(self.hwnd)
            log.info("武将识别名称：" + hero_name)
            physical = assistant.get_hero_physical(self.hwnd)
            log.info("武将体力：" + str(physical))
            log.info("返回上一页：（配置页）")
            event.click_page_close(self.hwnd)
            if util.is_similar(hero_name, hero[0]) and physical >= 10:
                log.info("武将名一致，放置武将")
                event.drag_hero_placeholder(self.hwnd, try_index, index)
                break
            else:
                log.info("不是该武将，或者体力不够")
                try_index += 1
                if try_index >= 3:
                    log.info("武将索引大于 3 放弃替换武将")
                    break
                if hero_name.isspace():
                    log.info("武将名称未识别到，放弃替换武将")
                    break

    # 进入城池页面
    def enter_city_page(self):
        log.info("点击标记定位菜单")
        event.click_mark_location_menu(self.hwnd)
        log.info("点击主城项")
        event.click_mark_location_main_city(self.hwnd)
        log.info("点击城池菜单")
        event.click_city_menu(self.hwnd)

    # 替换体力不足的武将单个部队
    # 第一个放置帮助升级的武将
    # army_index：主城 部队索引
    # multi：是否有多个相同武将
    def tired_hero_replace_single(self, army_index, multi):
        click_setting = False
        log.info("获取武将体力信息：")
        self.init_army_hero_info(army_index)
        if self.hero_physical_list[0] < 10:
            log.info("大营武将体力小于 10 -> 点击武将配置按钮")
            event.click_army_setting_menu(self.hwnd)
            if assistant.is_setting_tip(self.hwnd):
                log.info("当前部队处于非待命状态，返回上一页")
                event.click_page_return(self.hwnd)
                return
            click_setting = True
            # 有重复的需要，取下后再放上去
            if multi:
                log.info("取下大营武将")
                event.drag_hero_down(self.hwnd, 0)
            log.info("放置大营武将：")
            # 多个武将（帮助撞地武将）
            if multi:
                self.hero_placeholder(config.help_hero, 0, True)
            else:
                self.hero_placeholder(config.leveling_hero_dict[self.leveling_hero_index], 1, True)
                self.leveling_hero_index = (self.leveling_hero_index + 1) % len(config.leveling_hero_dict)
        if self.hero_physical_list[1] < 10:
            log.info("中军武将体力小于 10 -> 点击武将配置按钮")
            if not click_setting:
                log.info("点击武将配置按钮")
                event.click_army_setting_menu(self.hwnd)
                if assistant.is_setting_tip(self.hwnd):
                    log.info("当前部队处于非待命状态，返回上一页")
                    event.click_page_return(self.hwnd)
                    return
                click_setting = True
            self.hero_placeholder(config.leveling_hero_dict[self.leveling_hero_index], 1, click_setting)
            self.leveling_hero_index = (self.leveling_hero_index + 1) % len(config.leveling_hero_dict)
        log.info("返回上一页：（未点击配置按钮）")
        event.click_page_return(self.hwnd)
        if click_setting:
            log.info("返回上一页：（首页）")
            event.click_page_return(self.hwnd)

    # 替换体力不足的武将
    def tired_hero_replace(self):

        log.info("循环判断和替换体力不足的武将")
        for index in range(3, 4):
            log.info("判断是否能配置武将状态：第 %d 个部队" % index)
            if assistant.is_city_army_enable_setting(self.hwnd, index):
                self.tired_hero_replace_single(index, index == 3)
            else:
                log.info("武将队伍不能配置状态：1->征兵；2->行军；3->返回；4->练兵；")

        log.info("返回上一页：主页")
        event.click_page_return(self.hwnd)

    # 撞地
    def hit_the_ground(self):
        for army_index in range(3, 4):
            if army_index == 3:
                log.info("撞地武将撞地：")
                self.army_expedition(config.leveling_land_help)
            else:
                log.info("普通武将撞地：")
                self.army_expedition(config.leveling_land)
            log.info("判断武将灰度状态：")
            if assistant.is_expedition_hero_gray(self.hwnd, army_index):
                log.info("武将是灰色状态，无法出征")
                log.info("点击外部区域回到上一页")
                event.click_outside(self.hwnd)
            else:
                log.info("武将可以出征")
                event.click_expedition_army(self.hwnd, army_index)
                log.info("武将开始出征了")
                event.click_wipe_out_button(self.hwnd)
                time.sleep(2)

    # 运行
    def run(self):
        while True:
            # 数据重置
            self.reset_data()

            log.info("进入城池页面")
            self.enter_city_page()
            log.info("疲倦武将替换")
            self.tired_hero_replace()
            log.info("武将循环出征")
            self.hit_the_ground()
            log.info("睡眠" + str(max(min(self.min_wait_duration_list), 20)) + "秒")
            time.sleep(max(min(self.min_wait_duration_list), 20))
