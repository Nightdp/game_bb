# -*- coding: utf-8 -*-

import tkinter as tk
from src.game_assistant import GameAssistant


def game_start(is_sand_box=False, game_type=0, name=""):
    game_assistant = GameAssistant(is_sand_box, game_type, name)
    game_assistant.run()


def create():
    window = tk.Tk()
    window.title("辅助")
    window.geometry("500x300+1414+100")
    win_1 = tk.Button(window, text="游戏A", command=lambda: game_start(False, 2, "一条小团团"))
    win_1.pack(side='left')
    win_2 = tk.Button(window, text="游戏B", command=lambda: game_start(False, 0, "团团小跟班"))
    win_2.pack(side='right')
    win_3 = tk.Button(window, text="游戏C", command=lambda: game_start(True, 0, "难搞哦"))
    win_3.pack()
    window.mainloop()
