# -*- coding: utf-8 -*-

import src.log as log
import src.s3_config as config
import src.assert_event as event
import src.assistant as assistant

import pymongo
import time


# 土地信息获取探索


class Explore(object):

    def __init__(self, hwnd):
        self.map_info_dao = None
        self.hwnd = hwnd

        # 地图信息
        self.map_info = {}

    # 定位跳转
    def location_jump(self, point):
        log.info("点击地图菜单")
        event.click_map_menu(self.hwnd)
        log.info("输入坐标")
        event.location_input(self.hwnd, point)
        log.info("点击坐标跳转按钮")
        event.click_location_jump_button(self.hwnd)

    def init_db(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        game_db = client["game_bb"]
        self.map_info_dao = game_db["map_info"]

    # 运行
    def run(self):
        self.init_db()
        land_width = 30
        land_height = 30
        log.info("开始探索：宽->" + str(land_width) + "块  长->" + str(land_height) + "块：")
        for x in range(config.main_city_location[0] - land_width, config.main_city_location[0] + land_width + 1):
            for y in range(config.main_city_location[1] - land_height, config.main_city_location[1] + land_height + 1):
                # 跳过已经存在的
                item = self.map_info_dao.find_one({"x": x, "y": y})
                if item is not None:
                    log.info(str(item) + "  已存在")
                    continue
                log.info("位置定位：" + str((x, y)))
                self.location_jump((x, y))
                log.info("点击土地")
                event.click_center(self.hwnd)
                log.info("识别土地等级")
                land_level = assistant.get_land_level(self.hwnd)
                log.info("等级：%d" % land_level)
                self.map_info[(x, y)] = land_level
                land_dict = {"x": x, "y": y, "land_level": land_level}
                self.map_info_dao.update({"x": x, "y": y}, land_dict, True)
