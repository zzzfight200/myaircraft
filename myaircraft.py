import pygame
import time
import random
from pygame.locals import *
import threading

# 全局变量双方比分
HEROSCORE = 0
ENEMYSCORE = 0

#定义了一个Base类，作为子弹和飞机的父类，通过构造函数定义了有4个属性，分别为坐标x,y，底板screen,和底板上加载的图片image
class Base(object):
    #构造方法，在当创建这个类的实例时就会调用该方法
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
#继承于Base类的BaseBullet类
class BaseBullet(Base):
    #如果在子类中需要父类的构造方法就需要显式地调用父类的构造方法，或者不重写父类的构造方法。
    #子类不重写__init__，实例化子类时，会自动调用父类定义的__init__。
    #BaseBullet类与Base类不一样的就是新增了一个display方法
    def display(self):
        #调用时screen_temp为通过pygame.display.set_mode函数加载的位图。
        #pygame.display.set_mode（）这个函数会返回一个Surface对象，他是位图的一种
        #Surface对象有一个名为blit（）的方法，它可以绘制位图
        # 第一个参数是加载完成的位图，第二个参数是绘制的起始坐标。
        self.screen.blit(self.image, (self.x, self.y))
class HeroBullet(BaseBullet):
    #定义了子弹类，继承于BaseBullet类
    #重写了__init__，在实例化子时就不会调用父类已经定义的 __init__
    def __init__(self, screen_temp, x, y):
    #如果重写了__init__ 后，还要继承父类的构造方法，则像如下这样写
        BaseBullet.__init__(self, screen_temp, x+70, y-20, './feiji/herobullet.png')
    def move(self):
        self.y -= 5
    # 判断子弹是否越界
    def judge(self):
        if self.y < 0:
            return True
        else:
            return False
class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x+25, y+40, './feiji/enemybullet.png')
    def move(self):
        self.y += 5
    def judge(self):
        if self.y > 685:
            return True
        else:
            return False
#定义了BasePlane类，BasePlane类继承于Base类
class BasePlane(Base):
    def __init__(self, screen_temp, x, y, image_name):
        # 继承父类的构造方法
        Base.__init__(self, screen_temp, x, y, image_name)
        self.bullet_list = []  # 存储发射出去的子弹对象的引用
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        #bullet是BaseBullet类，具有display()、judge()和move()方法
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge():#判断子弹是否越界
                self.bullet_list.remove(bullet)#删除越界的子弹对象
    '''我方飞机的类'''
class HeroAircraft(BasePlane):
    def __init__(self, screen_temp):
        #继承父类的构造方法
       BasePlane.__init__(self, screen_temp, 190, 585, './feiji/hero1.png')
    def move_left(self):
        if self.x>=-100:
            self.x -= 40
    def move_right(self):
        if self.x<=350:
            self.x += 40
        #在存储发射出去的子弹对象的列表中增加一个HeroBullet对象
    def fire(self):
        self.bullet_list.append(HeroBullet(self.screen, self.x, self.y))
class EnemyPlane(BasePlane):
    '''敌机的类'''
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, './feiji/enemy0.png')
        self.direction = 'right'#用来指示敌机的移动方向
    def move(self):
        if self.direction == 'right':
            self.x += 5
        elif self.direction == 'left':
            self.x -= 5
            #超出界面边界则变相
        if self.x > 350:
            self.direction = 'left'
            # 超出界面边界则变相
        elif self.x < -100:
            self.direction = 'right'
    def fire(self):
        self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))
        # 获取事件,比如按下键盘
def key_scan(hero_temp):
    for event in pygame.event.get():
        # 判断是否点击了退出按钮
        if event.type == QUIT:
            print('exit')
            exit()
        # 判断是否按下按键
        elif event.type == KEYDOWN:
            # 检测按键是否是left
            if event.key == K_LEFT:
                #print('left')
                hero_temp.move_left()
            # 检测按键是否是right
            elif event.key == K_RIGHT:
                #print('right')
                hero_temp.move_right()
            # 检测按键是否是空格键
            elif event.key == K_SPACE:
                #print('space')
                hero_temp.fire()
if __name__ == '__main__':
    pygame.init()
    # 1.创建游戏界面的窗口
    '''
    screen为通过pygame.display.set_mode函数加载的位图。
    pygame.display.set_mode（）这个函数会返回一个Surface对象，他是位图的一种
    https://www.cnblogs.com/msxh/p/4990435.html
    '''
    screen = pygame.display.set_mode((480, 800), 0, 32)
    # 2.创建一个背景图片
    background = pygame.image.load('./feiji/background.jpg')
    # 3. 创建一个飞机对象
    hero = HeroAircraft(screen)
    # 4. 创建一个敌机
    enemyplane = EnemyPlane(screen)
    #我方子弹
    herobullet = hero.bullet_list
    font = pygame.font.SysFont(None,25)
    def text_object(text,color):
        textsurface = font.render(text,True,color)
        return textsurface,textsurface.get_rect()
    def print_message(msg,color,place):
        tsurf,tsurf_rect = text_object(msg,color)
        tsurf_rect.center = place
        screen.blit(tsurf,tsurf_rect)

    def EnemyBulletDisapear():
        #敌机子弹击中我方飞机后消失
        global ENEMYSCORE
        for enemybullet in enemyplane.bullet_list:
            if enemybullet.y >= hero.y-40 and enemybullet.x <= hero.x+120 and enemybullet.x>=hero.x-70:
                enemyplane.bullet_list.remove(enemybullet)
                ENEMYSCORE += 1
    def HeroBulletDisapear():
        # 我方子弹击中敌机后消失
        global HEROSCORE
        for herobullet in hero.bullet_list:
            if herobullet.y <= enemyplane.y+170 and herobullet.x<=enemyplane.x+120 and herobullet.x>=enemyplane.x-70:
                hero.bullet_list.remove(herobullet)
                HEROSCORE +=1
    while True:
        '''
        blit()函数作用是把background的图案印章一样的印在screen上
        pygame的坐标体系中以左上角为原点，向右向下两个方向作x轴y轴，构成坐标（x，y），注意是被画的B对象的左上角，如果这个对象是屏幕，那就是屏幕的左上角了。
        '''
        screen.blit(background, (0, 0))
        hero.display()
        enemyplane.display()
        #打印分数
        print_message(f'Hero:{HEROSCORE} - Enemy:{ENEMYSCORE}',(0,255,0),(380,20))
        enemyplane.move()  # 调用敌机的移动方法
        pygame.display.update()
        key_scan(hero)
        random_num = random.randint(1, 70)
        if random_num == 1 or random_num == 70:
            enemyplane.fire()  # 敌机发射子弹
        # 通过多线程同时跑两个循环，同时实现子弹打敌机和子弹打我方飞机的效果
        t1 = threading.Thread(target=EnemyBulletDisapear)
        t2 = threading.Thread(target=HeroBulletDisapear)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # EnemyBulletDisapear()
        # HeroBulletDisapear()
        time.sleep(0.01)