import pygame as pg
import numpy as np
import random

# ----------------------[기본값]----------------------
pg.init()

Window = pg.display.set_mode((1280, 720))
pg.display.set_caption("Jot Mang Game")

playNow = True
fps = pg.time.Clock()
# 키와 맵에 관한 값
keys = [False, False, False, False]  # W,S,A,D
playerPos = [50, 47]
mapData = []
cursorDelay = 200
menuStatus = [(500, 497), (500, 547), (500, 597)]
menuSelect = 0
pauseStatus = [(35, 30), (35, 80), (35, 130), (35, 180), (35, 240), (35, 290)]
pauseSelect = 0
characterStatus = [(35, 90), (35, 140), (35, 190)]
characterSelect = 0
# 상태 저장 값
startMenu = True
selectCharacter = False
playMap = False
pauseGame = False
battleFlag = False
mapOrBattle = False
runningChat = False
# 플레이어 저장 값
playerGold = 0
playerSelect = 0
playerHealth = [50, 75, 90]
playerAck = [4, 6, 9]
playerDef = [1, 1, 2]
playerCost = [20, 20, 30]
playerLv = [0,60,85,110,135,160,185,210,235,260,285,310,335,360,385,410]
playerLevelNow = 0
playerExp = 0
playerStat = 0

playerBattleHealth = 0
playerNowHealth = 0
playerNowAtk = 0
playerNowDef = 0
playerBattleCost = 0
playerNowCost = 0
playerWalk = 0
randomPlayerWalk = 0
# 몬스터 저장 값
mobData = {0: '슬라임', 1: '고블린', 2: '킹 슬라임'}
mobSelect = 0
mobHealth = [15, 21, 35]
mobAck = [4, 5, 7]
mobDropGold = [5, 7, 15]
mobExp = [5, 7, 20]
bossMobDrop = []

mobNowHealth = 0
# 아이템 저장 값
playerItem = [False, False, False]
playerEquip = [False, False, False]
itemSelect = 0
# 전투 저장
appearMob = True
battleCommand = False
battleCommandStatus = [(1240, 550), (1240, 592), (1240, 634), (1240, 676)]
battleCommandSelect = 0
battleCommandList = [False, False, False, False]

# 사진 저장된 곳
cursor = pg.image.load('picture/cursor.png')
player = pg.image.load('picture/player.png')
grass = pg.image.load('picture/grass.png')
wall = pg.image.load('picture/wall.png')
# 몬스터 사진
slime = pg.image.load('picture/slime.png')
goblin = pg.image.load('picture/goblin.png')
kingSlime = pg.image.load('picture/kingslime.png')

# 음악 저장된 곳
# mainBGM = pg.mixer.Sound('music/main.mp3')


# ----------------------[함수]--------------------------
def printText(msg, color='WHITE', Size=12, pos=(50, 50)):
    font = pg.font.Font('font/H2SA1M.ttf', Size)

    textSurface = font.render(msg, True, pg.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos

    Window.blit(textSurface, textRect)


def random_data(data='walk'):
    if data == "walk":
        return random.randint(70, 100)

    elif data == "mob":
        randomMobList = [None for i in range(100)]
        for i in range(70):
            randomMob = random.randint(0, 99)
            while randomMobList[randomMob] is not None:
                randomMob = random.randint(0, 99)
            randomMobList[randomMob] = 0
        for i in range(25):
            randomMob = random.randint(0, 99)
            while randomMobList[randomMob] is not None:
                randomMob = random.randint(0, 99)
            randomMobList[randomMob] = 1
        for i in range(5):
            randomMob = random.randint(0, 99)
            while randomMobList[randomMob] is not None:
                randomMob = random.randint(0, 99)
            randomMobList[randomMob] = 2
        return randomMobList[random.randint(0,99)]

    elif data == 'run':
        runningList = [None for i in range(100)]
        for i in range(60):
            running = random.randint(0, 99)
            while runningList[running] is not None:
                running = random.randint(0,99)
            runningList[running] = 0
        for i in range(40):
            running = random.randint(0, 99)
            while runningList[running] is not None:
                running = random.randint(0,99)
            runningList[running] = 1
        return runningList[random.randint(0,99)]


def random_select(arr):
    return arr[random.randint(0, len(arr) - 1)]


def get_around(cur, Map):
    next = []
    h = Map.shape[0]
    w = Map.shape[1]
    if cur[0] > 0 and Map[cur[0] - 1, cur[1]][0] < 0:
        next.append([cur[0] - 1, cur[1]])
    if cur[0] < h - 1 and Map[cur[0] + 1, cur[1]][0] < 0:
        next.append([cur[0] + 1, cur[1]])
    if cur[1] > 0 and Map[cur[0], cur[1] - 1][0] < 0:
        next.append([cur[0], cur[1] - 1])
    if cur[1] < w - 1 and Map[cur[0], cur[1] + 1][0] < 0:
        next.append([cur[0], cur[1] + 1])
    return next


def go_next(cur, Map, Visited):
    nexts = get_around(cur, Map)
    if len(nexts) > 0:
        Visited.append(cur)
        next = random_select(nexts)
        Map[next[0], next[1]] = cur
        return next
    else:
        if cur in Visited:
            Visited.remove(cur)
        if len(Visited) == 0:
            return None
        return random_select(Visited)


def drawMap(Map):
    h = Map.shape[0] * 2 - 1
    w = Map.shape[1] * 2 - 1
    draw = np.ndarray([w, h], np.int)
    draw[::] = 0

    for y in range(Map.shape[0]):
        for x in range(Map.shape[1]):
            pos = Map[y, x]
            draw[y * 2, x * 2] = 1
            draw[pos[0] * 2, pos[1] * 2] = 1
            draw[y + pos[0], x + pos[1]] = 1

    return draw


def printMap(Map):
    assert len(Map.shape) is 2
    for i in range(Map.shape[0] + 2):
        for j in range(Map.shape[1] + 2):
            if i == 0 or i == Map.shape[1] + 1 or j == 0 or j == Map.shape[0] + 1:
                Window.blit(wall, (i * 40, j * 40))
            else:
                pass
    for x in range(Map.shape[0]):
        for y in range(Map.shape[1]):
            if Map[y][x] == 0:
                Window.blit(wall, (x * 40 + 40, y * 40 + 40))
            elif Map[y][x] == 1:
                Window.blit(grass, (x * 40 + 40, y * 40 + 40))


# ----------------------[작동]----------------------
# 미로의 크기 2n+1
w = 7
h = 7

map = np.ndarray([w, h, 2], np.int)
map[::] = -1
current = [0, 0]
visited = []

randomPlayerWalk = random_data()

while True:
    map[0, 0, :] = 0
    current = go_next(current, map, visited)
    if current is None:
        break

mapData = drawMap(map)

while playNow:
    fps.tick(30)
    Window.fill((0, 0, 0))
    if playerWalk == randomPlayerWalk and playMap:
        battleCommandSelect = 0
        battleFlag = True
        appearMob = True
        playMap = False
        randomPlayerWalk = random_data()
        playerWalk = 0
        mobSelect = random_data('mob')

    if startMenu:
        Window.blit(cursor, menuStatus[menuSelect])
        printText("Test Game", "WHITE", 100, (420, 130))
        printText("게임 시작", "WHITE", 30, (530, 500))
        printText("불러오기", "WHITE", 30, (530, 550))
        printText("종료", "WHITE", 30, (530, 600))

    if selectCharacter:
        Window.blit(cursor, characterStatus[characterSelect])
        printText("캐릭터를 골라주세요!", "WHITE", 40, (30, 30))
        printText("궁수", "RED", 30, (70, 90))
        printText("전사", "WHITE", 30, (70, 140))
        printText("방패병", "skyblue", 30, (70, 190))

    if playMap:
        printMap(mapData)
        Window.blit(player, playerPos)
        printText("캐릭터 상태", "WHITE", 45, (620, 10))
        printText("체력: {0}/{1}".format(playerBattleHealth,playerNowHealth), "RED", 30, (620, 75))
        printText("마나: {0}/{1}".format(playerBattleCost,playerNowCost),"skyblue", 30, (620, 115))
        printText("공격력: {0}".format(playerNowAtk), "red4", 30, (620, 155))
        printText("방어력: {0}".format(playerNowDef), "aquamarine2", 30, (620, 195))
        printText("Lv: {0}".format(playerLevelNow + 1), "WHITE", 30, (620, 580))
        printText("소지금: {0}".format(playerGold), "YELLOW", 30, (1200, 580))
        printText("경험치: {0}/{1}".format(playerExp,playerLv[playerLevelNow]), "aquamarine2", 20, (0, 600))

    if pauseGame:
        Window.blit(cursor, pauseStatus[pauseSelect])
        printText("돌아가기", "WHITE", 30, (70, 30))
        printText("저장", "WHITE", 30, (70, 80))
        printText("스텟", "WHITE", 30, (70, 130))
        printText("인벤토리", "WHITE", 30, (70, 180))
        printText("상점", "GOLD", 30, (70, 240))
        printText("메인 화면", "WHITE", 30, (70, 290))

    if battleFlag:
        pg.draw.line(Window, (255, 255, 255), [10, 540], [1270, 540], 2)
        pg.draw.line(Window, (255, 255, 255), [10, 540], [10, 710], 2)
        pg.draw.line(Window, (255, 255, 255), [1270, 540], [1270, 710], 2)
        pg.draw.line(Window, (255, 255, 255), [10, 710], [1270, 710], 2)
        if mobSelect == 0:
            Window.blit(slime, (1020, 110))
        elif mobSelect == 1:
            Window.blit(goblin, (1020, 110))
        elif mobSelect == 2:
            Window.blit(kingSlime, (1020, 110))

        if appearMob:
            pg.draw.polygon(Window, (255, 255, 255), [[1252, 700], [1242, 680], [1262, 680]])
            printText("야생의 " + mobData[mobSelect] + "이 나타났다", "WHITE", 30, (20, 550))
        elif battleCommand:
            printText("무엇을 할까?", "WHITE", 30, (20, 550))
            pg.draw.line(Window, (255,255,255), [1080, 540], [1080, 710], 2)
            printText("공격", "WHITE", 20, (1100, 550))
            pg.draw.line(Window, (255, 255, 255), [1080, 582], [1270, 582], 2)
            printText("스킬", "WHITE", 20, (1100, 592))
            pg.draw.line(Window, (255, 255, 255), [1080, 624], [1270, 624], 2)
            printText("아이템", "WHITE", 20, (1100, 634))
            pg.draw.line(Window, (255, 255, 255), [1080, 666], [1270, 666], 2)
            printText("도주", "WHITE", 22, (1100, 676))
            Window.blit(cursor, battleCommandStatus[battleCommandSelect])
        elif battleCommandList[0]:
            pass
        elif battleCommandList[3]:
            if random_data('run') == 0:
                printText("도주에 실패했습니다", "WHITE", 30, (20, 550))
                pg.time.delay(500)
                battleCommandList[3] = False
                battleCommand = True
            elif random_data('run') == 1:
                printText("도주에 성공하셨습니다!", "WHITE", 30, (20, 550))
                pg.time.delay(500)
                battleCommandList[3] = False
                battleCommand = False
                battleFlag = False
                playMap = True

    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                keys[0] = True
            elif event.key == pg.K_DOWN:
                keys[1] = True
            elif event.key == pg.K_LEFT:
                keys[2] = True
            elif event.key == pg.K_RIGHT:
                keys[3] = True
            elif event.key == pg.K_z:
                if startMenu:
                    if menuSelect == 0:
                        startMenu = False
                        selectCharacter = True
                    elif menuSelect == 1:
                        pass  # 불러오기
                    elif menuSelect == 2:
                        playNow = False
                elif selectCharacter:
                    if characterSelect == 0:
                        playerBattleHealth = playerNowHealth = playerHealth[0]
                        playerNowAtk = playerAck[0]
                        playerNowDef = playerDef[0]
                        playerBattleCost = playerNowCost = playerCost[0]
                        selectCharacter = False
                        playMap = True
                    elif characterSelect == 1:
                        playerBattleHealth = playerNowHealth = playerHealth[1]
                        playerNowAtk = playerAck[1]
                        playerNowDef = playerDef[1]
                        playerBattleCost = playerNowCost = playerCost[1]
                        selectCharacter = False
                        playMap = True
                    elif characterSelect == 2:
                        playerBattleHealth = playerNowHealth = playerHealth[2]
                        playerNowAtk = playerAck[2]
                        playerNowDef = playerDef[2]
                        playerBattleCost = playerNowCost = playerCost[2]
                        selectCharacter = False
                        playMap = True
                elif pauseGame:
                    if pauseSelect == 0:
                        if not mapOrBattle:
                            playMap = True
                            pauseGame = False
                        else:
                            pauseGame = False
                            battleFlag = True
                    elif pauseSelect == 1:
                        pass  # 저장 조건
                    elif pauseSelect == 2:
                        pass  # 스텟
                    elif pauseSelect == 3:
                        pass  # 인벤토리
                    elif pauseSelect == 4:
                        pass  # 상점
                    elif pauseSelect == 5:
                        startMenu = True
                        playMap = False
                        pauseGame = False
                        pauseSelect = 0
                        playerPos = [50, 47]
                elif battleFlag:
                    if appearMob:
                        appearMob = False
                        battleCommand = True
                    if battleCommand:
                        if battleCommandSelect == 0:
                            pass
                        if battleCommandSelect == 3:
                            battleCommandList[3] = True
                            battleCommand = False

            elif event.key == pg.K_ESCAPE:
                if not startMenu and not mapOrBattle and not battleFlag:
                    playMap = not playMap
                    pauseGame = not pauseGame
                elif not startMenu and not playMap:
                    mapOrBattle = True
                    battleFlag = not battleFlag
                    pauseGame = not pauseGame

        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                keys[0] = False
            elif event.key == pg.K_DOWN:
                keys[1] = False
            elif event.key == pg.K_LEFT:
                keys[2] = False
            elif event.key == pg.K_RIGHT:
                keys[3] = False

        elif event.type == pg.QUIT:
            playNow = False

    if keys[0]:
        if playerPos[1] >= 42 and mapData[(playerPos[1] - 4) // 40 - 1][(playerPos[0] + 22) // 40 - 1] and \
                mapData[(playerPos[1] - 4) // 40 - 1][(playerPos[0] + 5) // 40 - 1] and playMap:
            playerPos[1] -= 3
            playerWalk += 1
        elif startMenu:
            if menuSelect - 1 > -1:
                menuSelect -= 1
                pg.time.wait(cursorDelay)
            else:
                menuSelect = 2
                pg.time.wait(cursorDelay)
        elif selectCharacter:
            if characterSelect - 1 > -1:
                characterSelect -= 1
                pg.time.wait(cursorDelay)
            else:
                characterSelect = 2
                pg.time.wait(cursorDelay)
        elif pauseGame:
            if pauseSelect - 1 > -1:
                pauseSelect -= 1
                pg.time.wait(cursorDelay)
            else:
                pauseSelect = 5
                pg.time.wait(cursorDelay)
        elif battleCommand:
            if battleCommandSelect + 1 > -1:
                battleCommandSelect -= 1
                pg.time.wait(cursorDelay)
            else:
                battleCommandSelect = 3
                pg.time.wait(cursorDelay)

    elif keys[1]:
        if playerPos[1] <= 535 and mapData[(playerPos[1] + 24) // 40 - 1][(playerPos[0] + 22) // 40 - 1] and \
                mapData[(playerPos[1] + 24) // 40 - 1][(playerPos[0] + 5) // 40 - 1] and playMap:
            playerPos[1] += 3
            playerWalk += 1
        elif startMenu:
            if menuSelect + 1 < 3:
                menuSelect += 1
                pg.time.wait(cursorDelay)
            else:
                menuSelect = 0
                pg.time.wait(cursorDelay)
        elif selectCharacter:
            if characterSelect + 1 < 3:
                characterSelect += 1
                pg.time.wait(cursorDelay)
            else:
                characterSelect = 0
                pg.time.wait(cursorDelay)
        elif pauseGame:
            if pauseSelect + 1 < 6:
                pauseSelect += 1
                pg.time.wait(cursorDelay)
            else:
                pauseSelect = 0
                pg.time.wait(cursorDelay)
        elif battleCommand:
            if battleCommandSelect + 1 < 4:
                battleCommandSelect += 1
                pg.time.wait(cursorDelay)
            else:
                battleCommandSelect = 0
                pg.time.wait(cursorDelay)

    elif keys[2]:
        if playerPos[0] >= 42 and mapData[(playerPos[1] + 17) // 40 - 1][(playerPos[0]) // 40 - 1] and \
                mapData[(playerPos[1]) // 40 - 1][(playerPos[0]) // 40 - 1] and playMap:
            playerPos[0] -= 3
            playerWalk += 1

    elif keys[3]:
        if playerPos[0] <= 535 and mapData[(playerPos[1] + 17) // 40 - 1][(playerPos[0] + 25) // 40 - 1] and \
                mapData[(playerPos[1]) // 40 - 1][(playerPos[0] + 25) // 40 - 1] and playMap:
            playerPos[0] += 3
            playerWalk += 1
