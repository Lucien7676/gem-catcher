import pgzrun
from pgzrun import *
from pgzero.builtins import *
import random
import pygame

# 配置画面框的大小
WIDTH = 800
HEIGHT = 600

# 创建一个飞船
# 下面将会实现进行创建对应颜色的飞船

ship = Actor("playership1_" + input("请输入您想要的颜色\t"))
ship.x = 370
ship.y = 550

# 首先设置宝石的颜色(这里我们将会设置4个宝石的颜色)
gem_color = [
    "gemgreen",
    "gemred",
    "gemblue",
    "gemyellow"
]

# # 创建一个宝石
# gem = Actor(random.choice(gem_color))
# gem.x = random.randint(20,780)
# gem.y = 10

# 创建一个宝石list
gems = []
gem_timeout = 0
# 创建一个子弹的列表
bullets = []
bullet_holdoff = 0 # 这个变量表示的是键盘发射子弹的冷却时间,当这个变量小于0 的时候，我们将能够进行发射子弹，但是当这个变量大于0的时候表示的是有这么多个帧数的冷却时间

# 创建一个分数变量
score = 0
game_over = False
life = 3 # 设置生命
b = 4

def update():
    global score, game_over,life, gem_timeout, bullet_holdoff,bullets # 将其进行全局化

    # 每一次更新刷新一次
    gem_timeout += 1

    # # 使用键盘进行操作
    # if keyboard.left:
    #     ship.x -= 5
    # if keyboard.right:
    #     ship.x += 5

    # 使用鼠标进行操作
    mouse = pygame.mouse.get_pos()
    ship.x = mouse[0] # 得到对应的位置
    a = random.randint(1,5)
    if gem_timeout >= 50 - score: # 随着速度的增大 那生成宝石的时间也越短
        if a > b: # 表示的是少数的情况，这个时候我们将会生成rock
            gem = Actor("rock")
        else: # 这个表示的是大部份的请情况，我们将会生成宝石
            gem = Actor(random.choice(gem_color))
        gem.x = random.randint(20,780)
        gem.y = 10
        gems.append(gem)
        gem_timeout = 0

    for gem in gems:
        gem.y += 4 + score/3 # 实现宝石加速

        # 下面我们要先进性判断是不是rock
        if gem.image == 'rock':
            # 有两种情况
            if gem.y >= 600:
                gems.remove(gem)
            
            if ship.collidelist(gems) != -1: # 表示的是撞上了
                if life > 0 :
                    life -= 1
                else:
                    game_over = True
                gems.remove(gem)

        else:
            # 下面是控制每次下落
            if gem.y >= 600:
                if life > 0:
                    life -= 1
                    # # 重新刷新宝石(这里可以实现生成别的颜色的宝石)
                    # gem = Actor(random.choice(gem_color))
                    # gem.y = 10
                    # gem.x = random.randint(20,780)
                else: # 当生命值全部用完的时候，这里将会结束游戏
                    game_over = True
                gems.remove(gem)

            # 控制飞船碰撞宝石
            # if ship.colliderect(gem): # 这个是判断一个一个撞
            if ship.collidelist(gems) != -1: # 表示的是撞上了

                # # 碰撞到之后可以进行重新刷新宝石的颜色
                # gem = Actor(random.choice(gem_color))
                # gem.x = random.randint(20,780)
                # gem.y = 10
                score += 1
                gems.remove(gem)


        if bullet_holdoff < 0:
            if keyboard.space:
                bullet = Actor("bulletdark2")
                bullet.angle =90 # 默认的子弹的图像是往右的，我们应该进行旋转90度
                # 这里设置的原因是因为飞船进行
                bullet.x = ship.x 
                bullet.y = ship.y
                bullets.append(bullet)
                bullet_holdoff = 60 # 发射完一个子弹之后，需要1s的时间进行更新
        else: # 如果这个冷却时间还是大于等于0的话进行减一的操作
            bullet_holdoff -= 1
        
        for bullet in bullets:
            bullet.y -= 10 # 每一次更新，子弹列表中的所有子弹位置进行更新
            if bullet.y < 0:
                bullets.remove(bullet)

        for bullet in bullets:
            if bullet.colliderect(gem):
                gems.remove(gem)
                bullets.remove(bullet)
                 

def draw():
    global gems
    screen.fill((153,255,204))
    if game_over:
        gems = []
        screen.draw.text("Game over", (WIDTH/2 - 140,HEIGHT/2 - 60), fontsize = 60, color = "red")
        screen.draw.text(f"Final Score: {score}", (WIDTH/2 - 140,HEIGHT / 2),fontsize = 60, color = "red")
        # print(len(bullets))
    else:
        # gem.draw()
        for gem in gems:
            gem.draw()

        for bullet in bullets:
            bullet.draw()

        ship.draw()
        # 在右上角的位置显示生命数目
        screen.draw.text(f"Life: {life}",(500,10),fontsize = 30, color = "purple")
        # 在左上角的位置显示分数
        screen.draw.text(f"Score：{score}",(15,10),fontsize=30,color = 'purple')


pgzrun.go()