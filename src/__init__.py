# -*- coding: utf-8 -*-

import src.time as time
import tkinter as tk

import src.util as util

import threading
import win32api
import win32con
import win32gui
from pykeyboard import PyKeyboard
from pymouse import PyMouse

import src.assistant as assistant
import src.event as event
import src.s3_config as config
import src.path as path

from src.function.hit_ground import HitGround
from src.function.wipe_out import WipeOut
from src.function.paving import Paving
from src.function.explore import Explore
import src.thread_util as thread_util


class GameAuxiliaries(object):

    def __init__(self):
        self.wd_name = u'率土之滨'
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()

        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, self.wd_name)
        # 设置窗口显示（防止最小化问题）
        win32gui.ShowWindow(self.hwnd, win32con.SW_NORMAL)
        # 设置为最前显示
        win32gui.SetForegroundWindow(self.hwnd)

        # 调整目标窗口到坐标(0, 0), 大小设置为(1414, 824)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, 0, 0, 1414, 824,
                              win32con.SWP_SHOWWINDOW)
        # 屏幕宽高
        self.width_real = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.height_real = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.width_px = 1920
        self.height_px = 1080
        # 获取窗口尺寸信息
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.hwnd)
        # 设置窗口尺寸信息
        self.width = self.right - self.left
        self.height = self.bottom - self.top
        # 标题栏的高度
        self.title_bar_height = 30
        self.top = self.top + self.title_bar_height
        # 中心位置坐标
        self.center_x = int((self.right + self.left) / 2)
        self.center_y = int((self.bottom + self.top) / 2)
        print("窗口宽：%s" % (self.right - self.left))
        print("窗口高：%s" % (self.bottom - self.top))

        self.thread_start = None

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

    # 初始化扫荡信息
    def init_wipe_out_land_info(self):
        print("打开内政页面")
        event.click_interior_menu(self.hwnd)
        print("打开内政详情页面")
        event.click_interior_detail_menu(self.hwnd)
        print("重置土地统计选项")
        event.reset_land_option(self.hwnd)

        self.init_wipe_out_land_by_level(6)
        self.init_wipe_out_land_by_level(5)

        print("返回上一页")
        event.click_page_close(self.hwnd)
        print("返回上一页")
        event.click_page_return(self.hwnd)

    # 根据土地等级获取可出征列表
    def init_wipe_out_land_by_level(self, level):
        event.click_interior_detail_menu(self.hwnd)
        print("重置土地统计选项")
        event.reset_land_option(self.hwnd)
        print("选择图地选项")
        event.click(self.hwnd, assistant.get_land_option_rect(self.hwnd, level))
        print("获取所有土地坐标")
        location_list = self.get_location_list()
        print("筛选合适的土地出征列表")
        wipe_out_land_list = util.calc_best_march_duration((201, 1442), location_list, 118)
        print("移除最后一个")
        wipe_out_land_list.pop(len(wipe_out_land_list) - 1)
        print(wipe_out_land_list)
        config.wipe_out_location_dict['manor_%d' % level] = wipe_out_land_list

    # 铺路
    def paving(self):
        p = Paving(self.hwnd)
        p.run()

    # 撞地升级
    def hit_ground(self):
        hg = HitGround(self.hwnd)
        hg.run()

    # 扫荡
    def wipe_out(self):
        wo = WipeOut(self.hwnd)
        wo.run()

    def run_thread(self):
        self.thread_start = threading.Thread(target=lambda: self.paving())
        self.thread_start.setDaemon(True)
        self.thread_start.start()

    # 探索土地信息
    def explore(self):
        wo = Explore(self.hwnd)
        wo.run()

    # 创建GUI
    def run(self):
        window = tk.Tk()
        window.title(self.wd_name + "辅助")
        window.geometry("500x300+1414+100")
        start = tk.Button(window, text="开始", command=lambda: self.run_thread())
        start.pack()
        end = tk.Button(window, text="结束", command=lambda: thread_util.stop_thread(self.thread_start))
        end.pack(side='bottom')
        window.mainloop()


if __name__ == '__main__':
    try:
        file = open('../logs/all.log', 'w')
        file.write('')
        file.close()
    except FileNotFoundError:
        print('无需清理日志文件')
    ga = GameAuxiliaries()
    ga.run()
