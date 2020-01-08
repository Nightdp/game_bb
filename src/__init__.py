# -*- coding: utf-8 -*-

import src.game_gui as game_gui

if __name__ == '__main__':
    try:
        file = open('../logs/all.log', 'w')
        file.write('')
        file.close()
    except FileNotFoundError:
        print('无需清理日志文件')
    game_gui.create()
