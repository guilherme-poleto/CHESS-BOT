import pyautogui as pg
import time
import sys
from stockfish import Stockfish
from win10toast import ToastNotifier
import PySimpleGUI as ps
import keyboard

# try:
ps.theme('Reddit')
im2 = pg.screenshot('my_screenshot.png', region=(300, 138, 825, 825))
layout = [
    # [ps.Text('Skill level: '), ps.Input(key='skill')],
    [ps.Text('Tempo (s): '), ps.Input(key='tempo')],
    [ps.Button('Play')],
]
janela = ps.Window('CHESS BOT', layout)

while True:
    eventos, valores = janela.read()
    if eventos == ps.WINDOW_CLOSED:
        break
    if eventos == 'Play':
        time = valores['tempo']
        if time == "":
            time = 0.4
        janela.close()

stockfish = Stockfish("/Users/guilh/stockfish/stockfish-windows-2022-x86-64-avx2")
stockfish.set_skill_level(20)
toast = ToastNotifier()
move = ""


def getMove(playing):
    c = 0
    n = 1

    startFen = "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000X"
    listFen = []
    listFen[:0] = startFen
    area = (324, 138, 777, 777)
    confidence = 0.8

    for pos in pg.locateAllOnScreen('torreW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "R"

    for pos in pg.locateAllOnScreen('damaW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "Q"

    for pos in pg.locateAllOnScreen('reiW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "K"

    for pos in pg.locateAllOnScreen('cavaloW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "N"

    for pos in pg.locateAllOnScreen('bispoW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "B"

    for pos in pg.locateAllOnScreen('peaoW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "P"

    # -------------------------------------------- BLACK PIECES ----------------------------

    for pos in pg.locateAllOnScreen('peaoB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "p"

    for pos in pg.locateAllOnScreen('torreB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "r"

    for pos in pg.locateAllOnScreen('cavaloB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "n"

    for pos in pg.locateAllOnScreen('bispoB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "b"

    for pos in pg.locateAllOnScreen('damaB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "q"

    for pos in pg.locateAllOnScreen('reiB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - 1
        coluna = int(x / 100) - 3
        listFen[9 * linha + coluna] = "k"

    for elementos in listFen:
        if elementos == "0":
            index = getIndex(listFen)
            while listFen[index + 1] == "0":
                n += 1
                index += 1
            for x in range(0, n):
                listFen.pop(c)
            listFen.insert(c, str(n))
            n = 1
        c += 1

    listFen.pop()
    if playing == "b":
        listFen.reverse()
    strFen = listToString(listFen)
    fen = strFen + " " + playing + " - - 0 1"
    stockfish.set_fen_position(fen)
    value = float(time)
    m = stockfish.get_best_move_time(value * 1000)
    e = stockfish.get_evaluation()
    return m, e


def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1


def getIndex(lst):
    c = 0
    for e in lst:
        if e == "0":
            return c
        c += 1


cordenadasColunasW = {"a": 373, "b": 473, "c": 573, "d": 673, "e": 773, "f": 873, "g": 973, "h": 1073}
cordenadasLinhasW = {"1": 875, "2": 775, "3": 675, "4": 575, "5": 475, "6": 375, "7": 275, "8": 175}
cordenadasColunasB = {"a": 1050, "b": 950, "c": 850, "d": 750, "e": 650, "f": 550, "g": 450, "h": 350}
cordenadasLinhasB = {"1": 190, "2": 290, "3": 390, "4": 490, "5": 590, "6": 690, "7": 790, "8": 890}

while True:

    if keyboard.is_pressed(',') == True:
        move, e = getMove("b")
        print(move)
        pg.moveTo(cordenadasColunasB[move[0]], cordenadasLinhasB[move[1]])
        pg.mouseDown();
        pg.moveTo(cordenadasColunasB[move[2]], cordenadasLinhasB[move[3]])
        pg.mouseUp();

    if keyboard.is_pressed('.') == True:
        move, evaluation = getMove()
        toast.show_toast("Move:", f"Lance: {move} - Barrinha: {evaluation['value']}", duration=3)

    if keyboard.is_pressed(';') == True:
        move, e = getMove("w")
        print(move)
        pg.moveTo(cordenadasColunasW[move[0]], cordenadasLinhasW[move[1]])
        pg.mouseDown();
        pg.moveTo(cordenadasColunasW[move[2]], cordenadasLinhasW[move[3]])
        pg.mouseUp();

    if keyboard.is_pressed('z') == True:
        stockfish.__del__()
        sys.exit()

