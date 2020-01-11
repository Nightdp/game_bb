# -*- coding: utf-8 -*-

import pymongo

import src.assert_event as event
import src.assistant as assistant
import src.log as log
import src.s3_config as config
import src.util as util
import time


# 土地信息获取探索


class Explore(object):

    def __init__(self, hwnd):
        self.map_info_dao = None
        self.hwnd = hwnd

        # 地图信息
        self.map_info = {}

    # 定位跳转
    def location_jump(self, point, duration=2):
        log.info("点击地图菜单")
        event.click_map_menu(self.hwnd)
        log.info("输入坐标")
        event.location_input(self.hwnd, point)
        log.info("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd, duration=duration)

    def init_db(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        game_db = client["game_bb"]
        self.map_info_dao = game_db["map_info"]

    # 运行
    def run(self):
        self.init_db()
        land_width = 10
        land_height = 10
        log.info("开始探索：宽->" + str(land_width) + "块  长->" + str(land_height) + "块：")
        is_first_jump = True
        for x in range(config.main_city_location[0] - land_width, config.main_city_location[0] + land_width + 1):
            for y in range(config.main_city_location[1] - land_height, config.main_city_location[1] + land_height + 1):
                # 跳过已经存在的
                item = self.map_info_dao.find_one({"x": x, "y": y})
                if item is not None and item['land_level'] > 0:
                    log.info(str(item) + "  已存在")
                    continue
                log.info("位置定位：" + str((x, y)))
                if y == config.main_city_location[1] - land_height or is_first_jump:
                    self.location_jump((x, y), duration=2)
                    is_first_jump = False
                else:
                    self.location_jump((x, y), duration=1)
                log.info("点击土地")
                event.click_center(self.hwnd)
                log.info("识别土地等级")
                land_level = assistant.get_land_level(self.hwnd)
                log.info("等级：%d" % land_level)
                try:
                    info = assistant.get_land_info(self.hwnd)
                    resource_name = util.get_resource_name(info)
                except:
                    resource_name = None
                if resource_name is None:
                    resource_name = ""
                log.info("资源类型：" + resource_name)
                self.map_info[(x, y)] = land_level
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                log.info("创建时间：" + create_time)
                land_dict = {"x": x, "y": y, "land_level": land_level, "resource_name": resource_name,
                             "create_time": create_time}
                self.map_info_dao.update({"x": x, "y": y}, land_dict, True)
