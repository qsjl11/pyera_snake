# -*- coding: UTF-8 -*-
import core.game as game
import script.base_lib as lib


def open_func():
    game.pl('pyera贪吃蛇游戏加载中')
    map_size = game.data['map']['map_size']
    game.pl('地图大小设置为 ' + str(map_size))
    game.pline()

    game.pcmd('[001]  读取游戏', 1, lib.load_func, arg=(open_func, main_func))
    game.pl()
    game.pcmd('[002]  开始游戏', 2, newgame_func)


def newgame_func():
    # 初始化地图数据dic，0是空地，1是苹果
    map_size = game.data['map']['map_size']
    game.data['mapdata'] = {}
    for y in range(0, map_size):
        for x in range(0, map_size):
            game.data['mapdata'][(x, y)] = 0

    # 初始化蛇list, 三格长度，靠左下角放置
    snake_list = []
    snake_list.append((0, 2))
    snake_list.append((0, 1))
    snake_list.append((0, 0))
    game.data['snake_list'] = snake_list

    main_func()


def create_apple():
    map_size = game.data['map']['map_size']

    # 随机苹果的位置，当位置与蛇重合的时候，重新随机
    import random
    apple_position = (random.randint(0, map_size - 1), random.randint(0, map_size - 1))
    while apple_position in game.data['snake_list']:
        apple_position = (random.randint(0, map_size - 1), random.randint(0, map_size - 1))

    # 将mapdata中的对应苹果位置改为1
    game.data['mapdata'][apple_position] = 1


def draw_map():
    map_size = game.data['map']['map_size']
    snake_list = game.data['snake_list']
    mapdata = game.data['mapdata']
    for y in range(0, map_size):
        for x in range(0, map_size):
            pos = (x, y)
            if pos in snake_list:
                game.p('❖', style='special')
                continue
            if mapdata[pos] == 1:
                game.p('❁')
                continue
            if mapdata[pos] == 0:
                game.p('﹒')
                continue
        game.pl()


direction = 'xia'

def next_step():
    # 方便调用
    global direction
    snake_list = game.data['snake_list']
    mapdata = game.data['mapdata']

    # 判断是否有苹果，没有就创造一个
    if 1 not in mapdata.values():
        create_apple()

    # 更新蛇身
    for i in range(len(snake_list) - 1, 0, -1):
        snake_list[i] = snake_list[i - 1]

    # 更新蛇头位置
    x_head = snake_list[0][0]
    y_head = snake_list[0][1]
    if direction == 'zuo':
        x_head = x_head - 1
    if direction == 'you':
        x_head = x_head + 1
    if direction == 'shang':
        y_head = y_head - 1
    if direction == 'xia':
        y_head = y_head + 1
    snake_list[0] = (x_head, y_head)

def main_func():
    # 新界面准备
    game.clr_cmd()
    game.pline()

    # 画图
    draw_map()

    def create_func(direction_name):
        def func():
            global direction
            direction = direction_name
            next_step()
            main_func()
        return func

    # 状态显示
    game.pline('--')
    game.pl('分数：')

    # 绘制命令按钮
    game.pline('--')
    game.pcmd('[1] 左  ', 1, create_func('zuo'))
    game.pcmd('[2] 上  ', 2, create_func('shang'))
    game.pcmd('[3] 右  ', 3, create_func('you'))
    game.pl()
    game.p('        ')
    game.pcmd('[4] 下  ', 4, create_func('xia'))
    game.pl('\n')
    game.pcmd('[5] 存储游戏  ', 5, lib.save_func, arg=main_func)
    game.pcmd('[6] 读取游戏  ', 6, lib.load_func, arg=(main_func, main_func))
