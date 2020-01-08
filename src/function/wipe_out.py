# -*- coding: utf-8 -*-

import src.assistant as assistant
import src.assert_event as event
import src.s3_config as config
import src.time as time
import src.util as util
import src.log as log


# 扫荡模块

class WipeOut(object):

    def __init__(self, hwnd):
        self.hwnd = hwnd

        # 部队兵力列表
        self.army_troops_list = [0, 0, 0, 0, 0]

        # 土地的扫荡索引
        self.manor_index_list = [0, 0]

        # 最短等待时间列表
        self.min_wait_duration_list = [12 * 50 * 50, 12 * 50 * 50, 12 * 50 * 50, 12 * 50 * 50, 12 * 50 * 50]

    # 重置数据
    def reset_data(self):
        self.army_troops_list = [0, 0, 0, 0, 0]
        self.min_wait_duration_list = [12 * 50 * 50, 12 * 50 * 50, 12 * 50 * 50, 12 * 50 * 50, 12 * 50 * 50]

    # 定位跳转
    def location_jump(self, point):
        log.info("点击地图菜单")
        event.click_map_menu(self.hwnd)
        log.info("输入坐标")
        event.location_input(self.hwnd, point)
        log.info("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd)

    # 扫荡
    def wipe_out(self, point):
        log.info("定位到指定位置")
        self.location_jump(point)
        log.info("地图放大")
        event.map_enlarge(self.hwnd)
        log.info("点击土地")
        event.click_center(self.hwnd)
        log.info("地图还原")
        event.map_reduction(self.hwnd)
        log.info("点击扫荡菜单按钮")
        event.click_wipe_out_menu(self.hwnd)

    # 是否可以出征
    def is_enable_wipe_out(self, hero_index, manor_index, troops):
        threshold = config.wipe_out_threshold_dict[hero_index][manor_index]
        log.info("推荐兵力：{threshold}，当前兵力：{troops}".format(threshold=str(threshold), troops=str(troops)))
        return threshold <= troops

    # 武将扫荡分析
    def hero_wipe_out_analysis(self, hero_index, troops):
        manor_dict = config.wipe_out_threshold_dict[hero_index]
        enable_index = -1
        for index in range(0, 2):
            if manor_dict[index] <= troops:
                log.info(manor_dict[index])
                log.info(troops)
                enable_index = index
                break

        if enable_index >= 0:
            log.info("有能战胜的土地：%d 级地" % (6 - enable_index))
            log.info("寻找合适的土地：")
            manor_list = config.wipe_out_location_dict["manor_%d" % (6 - enable_index)]
            manor_index = self.manor_index_list[enable_index]
            point = manor_list[manor_index]
            log.info("合适的土地坐标：" + str(point))
            log.info("定位扫荡地点")
            self.wipe_out(point)
            log.info("判断武将灰度状态")
            if assistant.is_expedition_hero_gray(self.hwnd, hero_index) or not \
                    self.is_enable_wipe_out(hero_index, enable_index, assistant.is_troops_enough(self.hwnd,
                                                                                                 hero_index)):
                log.info("武将是灰色状态，无法出征")
                log.info("点击外部区域回到上一页")
                event.click_outside(self.hwnd)
            else:
                log.info("武将可以出征")
                event.click_expedition_army(self.hwnd, hero_index)
                log.info("武将开始出征了")
                event.click_wipe_out_button(self.hwnd)
                self.manor_index_list[enable_index] = (self.manor_index_list[enable_index] + 1) % len(
                    config.wipe_out_location_dict["manor_%d" % (6 - enable_index)])
                time.sleep(2)
        else:
            log.info("没有能战胜的土地")

    # 寻找合适的征兵时间
    def fit_conscription(self, physical):
        # 最大时长
        max_duration = 0
        max_index = -1

        for index in range(0, 3):
            max_index += 1
            duration = assistant.get_hero_conscription_duration(self.hwnd, index)
            log.info("武将 " + str(max_index + 1) + "征兵时长：" + str(duration))
            if duration > max_duration:
                max_duration = duration

        log.info("最大征兵时长：%d" % max_duration)
        # 可用时长，即体力满之前的时长
        enable_duration = (130 - physical) * 50 * 50 / 20
        log.info("可用征兵时长：%d" % enable_duration)
        # 总时长
        if max_duration > enable_duration and max_duration != 0:
            percent = enable_duration / max_duration
            log.info("征兵时间大于剩余体力恢复：占比：%s" % str(percent))
            event.click_hero_conscription_percent(self.hwnd, max_index, percent)
        else:
            log.info("征兵时间小于剩余体力恢复")

    # 单个武将征兵
    def hero_conscription(self, army_index):

        log.info("获取等待时间：")
        wait_duration = assistant.get_wait_duration(self.hwnd, army_index)

        self.army_troops_list[army_index] = assistant.get_city_army_troops(self.hwnd, army_index)
        log.info("获取武将兵力数量：%d" % self.army_troops_list[army_index])

        if self.army_troops_list[army_index] < config.wipe_out_threshold_dict[army_index][1] and \
                assistant.is_city_army_enable_conscription(self.hwnd, army_index):
            log.info("兵力不够，并且不在不可征兵状态，不计算等待时长")
        else:
            self.min_wait_duration_list[army_index] = wait_duration
            log.info("兵力足够，设置等待时间，否则不计算")

        log.info("最小等待时间：" + str(wait_duration) + "秒")

        log.info("判断武将是否是灰色状态：")
        if assistant.is_city_hero_gray(self.hwnd, army_index):
            log.info("武将灰色状态不能征兵")
            return
        if not assistant.is_city_army_enable_conscription(self.hwnd, army_index):
            log.info("武将不可征兵状态")
            return

        log.info("点击武将队伍")
        event.click_city_army(self.hwnd, army_index)

        log.info("点击队伍 武将大营")
        event.click_army_hero(self.hwnd, 0)

        physical = assistant.get_hero_physical(self.hwnd)
        log.info("获取武将体力值：%d" % physical)

        log.info("关闭武将属性页面")
        event.click_page_close(self.hwnd)

        log.info("判断兵力是否够最低的，不够就征兵：")

        log.info("判断体力是否不太满：")

        if physical < 130 - 110 or self.army_troops_list[army_index] < config.wipe_out_threshold_dict[army_index][1]:
            log.info("体力不太满：")

            log.info("点击征兵按钮")
            event.click_conscription_button(self.hwnd)

            log.info("判断是否还在原来的页面")
            if assistant.is_conscription_disable(self.hwnd):
                log.info("征兵不可用")
                log.info("返回上个页面")
                event.click_page_return(self.hwnd)
                return

            log.info("征兵数量拖动到最大")
            for index in range(0, 3):
                event.click_hero_conscription_max(self.hwnd, index)

            log.info("判断能否征兵")
            if assistant.is_conscription_button_gray(self.hwnd):
                log.info("征兵按钮是灰色的")
                event.click_outside(self.hwnd)
                log.info("再次点击返回")
                event.click_page_return(self.hwnd)
                return

            log.info("寻找合适的征兵数量")
            self.fit_conscription(physical)

            log.info("确认征兵")
            event.click_conscription_confirm_button(self.hwnd)
            log.info("弹框确认征兵")
            event.click_conscription_dialog_confirm_button(self.hwnd)
            log.info("回到上一页")
            event.click_page_return(self.hwnd)
        else:
            log.info("体力有点满：")
            log.info("回到上一页")
            event.click_page_return(self.hwnd)

    # 征兵操作
    def conscription(self):

        log.info("点击标记定位菜单")
        event.click_mark_location_menu(self.hwnd)
        log.info("点击主城项")
        event.click_mark_location_main_city(self.hwnd)
        log.info("点击城池菜单")
        event.click_city_menu(self.hwnd)

        # 遍历武将征兵
        for index in range(0, config.army_count):
            self.hero_conscription(index)

        log.info("返回上一页")
        event.click_page_return(self.hwnd)

    # 获取坐标列表
    def get_location_list(self):
        location_list = set()
        while True:
            item_list = assistant.get_one_page_land_location_list(self.hwnd)
            before_count = len(location_list) + len(item_list)
            location_list.update(item_list)
            after_count = len(location_list)
            # 比较是否有重复的有就认为是到底了
            if before_count < 8 or before_count != after_count:
                break
            time.sleep(1)
            event.scroll_one_page(self.hwnd)
        return location_list

    # 根据土地等级获取可出征列表
    def init_wipe_out_land_by_level(self, level):
        event.click_interior_detail_menu(self.hwnd)
        log.info("重置土地统计选项")
        event.reset_land_option(self.hwnd)
        log.info("选择图地选项")
        rect = assistant.get_land_option_rect(self.hwnd, level)
        if rect is None:
            log.info("无" + str(level) + "级地")
            return
        event.click(self.hwnd, rect)
        location_list = self.get_location_list()
        log.info("获取所有土地坐标" + str(location_list))
        log.info("移除主城坐标")
        location_list.remove(config.main_city_location)
        log.info("筛选合适的土地出征列表")
        wipe_out_land_list = util.calc_best_march_duration(config.main_city_location, location_list, 118)
        log.info(str(level) + "级地：" + str(wipe_out_land_list))
        config.wipe_out_location_dict['manor_%d' % level] = wipe_out_land_list

    # 初始化扫荡信息
    def init_wipe_out_land_info(self):
        log.info("打开内政页面")
        event.click_interior_menu(self.hwnd)
        log.info("打开内政详情页面")
        event.click_interior_detail_menu(self.hwnd)
        log.info("重置土地统计选项")
        event.reset_land_option(self.hwnd)

        for index in range(1, 10):
            self.init_wipe_out_land_by_level(index)

        log.info("返回上一页")
        event.click_page_close(self.hwnd)
        log.info("返回上一页")
        event.click_page_return(self.hwnd)

    def run(self):

        self.init_wipe_out_land_info()

        while True:

            # 数据重置
            self.reset_data()

            # 征兵
            self.conscription()

            log.info(self.army_troops_list)

            for index in range(0, config.army_count):
                self.hero_wipe_out_analysis(index, self.army_troops_list[index])

            min_value = min(self.min_wait_duration_list)
            if min_value == 12 * 50 * 50:
                sleep_duration = 20
            else:
                sleep_duration = max(min_value, 20)

            log.info("睡眠" + str(sleep_duration) + "秒")
            time.sleep(sleep_duration)
