import pyautogui as pg
import time
import sys
from stockfish import Stockfish
import PySimpleGUI as ps
import keyboard
import timeit
import Komodo

# try:
ps.theme('Reddit')
area = (308, 153, 810, 810)
im2 = pg.screenshot('my_screenshot.png', region=area)
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

# stockfish = Stockfish("/Users/Guilherme Poleto/Desktop/komodo-14_224afb/Windows/komodo-14.1-64bit")
stockfish = Stockfish("/Users/Guilherme Poleto/Desktop/CHESS BOT/stockfish-windows-x86-64-avx2")
stockfish.set_skill_level(20)
move = ""


def getMove(playing):
    c = 0
    n = 1

    startFen = "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000X"
    listFen = []
    listFen[:0] = startFen
    confidence = 0.85
    corretorLinha = 2
    corretorColuna = 3

    start = timeit.default_timer()
    print("Start read board")

    for pos in pg.locateAllOnScreen('torreW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "R"

    for pos in pg.locateAllOnScreen('damaW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "Q"

    for pos in pg.locateAllOnScreen('reiW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "K"

    for pos in pg.locateAllOnScreen('cavaloW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "N"

    for pos in pg.locateAllOnScreen('bispoW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "B"

    for pos in pg.locateAllOnScreen('peaoW.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "P"

    # -------------------------------------------- BLACK PIECES ----------------------------

    for pos in pg.locateAllOnScreen('peaoB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "p"

    for pos in pg.locateAllOnScreen('torreB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "r"

    for pos in pg.locateAllOnScreen('cavaloB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "n"

    for pos in pg.locateAllOnScreen('bispoB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "b"

    for pos in pg.locateAllOnScreen('damaB.png', confidence=0.5, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
        listFen[9 * linha + coluna] = "q"

    for pos in pg.locateAllOnScreen('reiB.png', confidence=confidence, region=area):
        x, y = pg.center(pos)
        linha = int(y / 100) - corretorLinha
        coluna = int(x / 100) - corretorColuna
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

    stop = timeit.default_timer()
    print('Time read board: ', stop - start)

    listFen.pop()
    if playing == "b":
        listFen.reverse()
    strFen = listToString(listFen)
    fen = strFen + " " + playing + " - - 0 1"
    print(fen)
    stockfish.set_fen_position(fen)
    value = float(time)

    start = timeit.default_timer()
    print("Start getting best move")

    m = stockfish.get_best_move_time(value * 1000)
    e = stockfish.get_evaluation()

    stop = timeit.default_timer()
    print('Time to get best move: ', stop - start)
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

aW = 357
W1 = 912
aB = aW + 700
B1 = W1 - 700
cordenadasColunasW = {"a": aW, "b": aW+100, "c": aW+200, "d": aW+300, "e": aW+400, "f": aW+500, "g": aW+600, "h": aW+700}
cordenadasLinhasW = {"1": W1, "2": W1-100, "3": W1-200, "4": W1-300, "5": W1-400, "6": W1-500, "7": W1-600, "8": W1-700}
cordenadasColunasB = {"a": aB, "b": aB-100, "c": aB-200, "d": aB-300, "e": aB-400, "f": aB-500, "g": aB-600, "h": aB-700}
cordenadasLinhasB = {"1": B1, "2": B1+100, "3": B1+200, "4": B1+300, "5": B1+400, "6": B1+500, "7": B1+600, "8": B1+700}

while True:

    if keyboard.is_pressed(','):
        move, e = getMove("b")
        print(move)
        pg.moveTo(cordenadasColunasB[move[0]], cordenadasLinhasB[move[1]])
        pg.click()
        pg.moveTo(cordenadasColunasB[move[2]], cordenadasLinhasB[move[3]])
        pg.click()

    if keyboard.is_pressed(';'):
        move, e = getMove("w")
        print(move)
        pg.moveTo(cordenadasColunasW[move[0]], cordenadasLinhasW[move[1]])
        pg.click()
        pg.moveTo(cordenadasColunasW[move[2]], cordenadasLinhasW[move[3]])
        pg.click()

    if keyboard.is_pressed('z'):
        stockfish.__del__()
        sys.exit()

