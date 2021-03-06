import os
import sys
import random
import pygame
from pygame import *

'''
setting.py : 게임 구성의 기본 기능(게임창크기,사운드,폰트,RGB값 등 설정)
'''
#게이밍 사운드 믹서 초기화(주파수,크기,채널,버퍼,장치이름)
pygame.mixer.pre_init(44100, -16, 2, 2048)

#1.게임 초기화
pygame.init()

gamername=''

#2.게임창 옵션 설정

#2-1.게임창 크기 설정
scr_size = (width, height) = (800, 400)
#FPS 설정(반복문에서 1초에 몇번 이미지를 업데이트를 하는지, 높을수록 화면 부드럽지만 연산 많아짐)
FPS = 60
gravity = 0.65
# 폰트 타입 및 크기 설정
font = pygame.font.Font('DungGeunMo.ttf', 32)
full_screen=False
# 현재 그래픽 너비, 높이 환경 정보 받아와 모니터 사이즈 설정
monitor_size = (monitor_width, monitor_height) = (pygame.display.Info().current_w, pygame.display.Info().current_h)

# 화면 RGB값 설정
black = (0,0,0)
white = (255,255,255)
background_col = (235,235,235)
green = (0,200,0)
orange = (255,127,0)
blue = (0,0,225)
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_orange = (255,215,0)

high_score = 0

#위 2-1 로 게임창 크기 적용
resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)
# screen 변수에 크기옵션 집어넣어 앞으로 그릴 내용 담음
screen = resized_screen.copy()


resized_screen_centerpos = (0,0)
rwidth = resized_screen.get_width()
rheight = resized_screen.get_height()
button_offset = 0.18

#2-2.게임 제목 설정
pygame.display.set_caption("J-Dragon's Adventure by_JiwooKids")

# 3. 게임 내 필요한 설정
# 3-1. 시계 생성(향후 FPS 생성시 활용)
clock = pygame.time.Clock()


bgm_on=True
on_pushtime=0
off_pushtime=0
jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')
# background_music = pygame.mixer.Sound('t-rex_let-the-games-begin-21858.mp3')
#background_music = pygame.mixer.Sound('sprites/t-rex_bgm1.mp3')

# HERE: REMOVE SOUND!!
# pygame.mixer.music.load('sprites/t-rex_let-the-games-begin-21858.mp3')
background_m=pygame.mixer.Sound("sprites/t-rex_let-the-games-begin-21858.mp3")
ingame_m=pygame.mixer.Sound("sprites/t-rex_man-is-he-mega-glbml-22045.mp3")
gameclear_m=pygame.mixer.Sound("sprites/t-rex_happy-birthday-funk-spot-16197.mp3")


dino_size = [44, 47]
object_size = [40, 40]
ptera_size = [46, 40]
collision_immune_time = 500
shield_time = 2000
speed_up_limit_count = 700

# 게임 내에 text를 넣을때 쓰는 함수
def draw_text(text,font,surface,x,y,main_color) :
    text_obj = font.render(text,True,main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj,text_rect)

def text_objects(text, font):
    textSurface = font.render(text, True, (black))
    return textSurface, textSurface.get_rect()

# 게임 내 image를 넣을 때 쓰는 함수
def load_image(
    name,
    sizex=-1,
    sizey=-1,
    colorkey=None,
    ):

    fullname = os.path.join('sprites', name)
    # 이미지 불러옴
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return (image, image.get_rect())

def load_sprite_sheet(
        sheetname,
        nx,
        ny,
        scalex = -1,
        scaley = -1,
        colorkey = None,
        ):
    fullname = os.path.join('sprites', sheetname)
    # sheet = pygame.image.load(fullname)
    # sheet = sheet.convert()
    sheet, sheet_rect = alpha_image(sheetname, -1, -1, -1)

    sheet_rect = sheet.get_rect()

    sprites = []

    sizex = sheet_rect.width/nx
    sizey = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*sizex,i*sizey,sizex,sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            #이미지 어느 위치에 넣을지
            image.blit(sheet,(0,0),rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey,RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect

def disp_gameOver_msg(gameover_image):

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(gameover_image, gameover_rect)

def disp_intro_buttons(btn_gamestart, btn_board, btn_option):
    btn_gamestart_rect = btn_gamestart.get_rect()
    btn_board_rect = btn_board.get_rect()
    btn_option_rect = btn_option.get_rect()

    btn_gamestart_rect.centerx, btn_board_rect.centerx, btn_option_rect.centerx = width * 0.72, width * 0.72, width * 0.72
    btn_gamestart_rect.centery, btn_board_rect.centery, btn_option_rect.centery = height * 0.5, height * (0.5+button_offset), height * (0.5+2*button_offset)
    
    screen.blit(btn_gamestart, btn_gamestart_rect)
    screen.blit(btn_board, btn_board_rect)
    screen.blit(btn_option, btn_option_rect)


def checkscrsize(eventw, eventh):
    if (eventw < width and eventh < height) or eventw < width or eventh < height: #최소해상도
        resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)
    else:
        if eventw/eventh!=width/height: #고정화면비
            adjusted_height=int(eventw/(width/height))
            resized_screen = pygame.display.set_mode((eventw,adjusted_height), RESIZABLE)

def full_screen_issue():
    global scr_size
    resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)
    resized_screen = pygame.display.set_mode((scr_size), RESIZABLE)

def extractDigits(number):
    if number > -1:
        digits = []
        i = 0
        while(number/10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits

def resize(name, w, h, color):
        global width, height, resized_screen
        print("resized_screen: (",resized_screen.get_width(),",",resized_screen.get_height(),")")
        return (name, w*resized_screen.get_width()//width, h*resized_screen.get_height()//height, color)

def textsize(size):
    font = pygame.font.Font('DungGeunMo.ttf', size)
    return font

# 투명한 이미지 불러오기
def alpha_image(name, sizex=-1, sizey=-1,color_key=None):
    full_name = os.path.join('sprites', name)
    #ubuntu ver : full_name = os.path.join('/home/q202-14/2022-1-OSSProj-JiwooKids-5/sprites', name)
    img = pygame.image.load(full_name)
    if color_key is not None:
        if color_key == -1:
            color_key = img.get_at((0, 0))
        img.set_colorkey(color_key, RLEACCEL)
    if sizex != -1 or sizey != -1:
        img = transform.scale(img, (sizex, sizey))
    img.convert_alpha()
    return (img, img.get_rect())

def disp_store_buttons(btn_restart, btn_save, btn_exit, btn_back, btn_true):
    width_offset=0.2
    resized_screen_center = (0, 0)
    btn_restart_rect = btn_restart.get_rect()
    btn_save_rect = btn_save.get_rect()
    btn_exit_rect = btn_exit.get_rect()
    btn_back_rect = btn_back.get_rect()
    btn_true_rect = btn_true.get_rect()
    # btn_start_rect = btn_start.get_rect()

    btn_restart_rect.centerx = width * 0.2
    btn_save_rect.centerx = width * (0.2 + width_offset)
    btn_exit_rect.centerx = width * (0.2 + 2 * width_offset)
    btn_back_rect.centerx = width * 0.1
    btn_true_rect.centerx = width * (0.2 + 3 * width_offset)
    # btn_start_rect.centerx = width * 0.9

    btn_restart_rect.centery = height * 0.6
    btn_save_rect.centery = height * 0.6
    btn_exit_rect.centery = height * 0.6
    btn_back_rect.centery = height * 0.1
    btn_true_rect.centery = height * 0.6
    # btn_start_rect.centery = height * 0.1

    screen.blit(btn_restart, btn_restart_rect)
    screen.blit(btn_save, btn_save_rect)
    screen.blit(btn_exit, btn_exit_rect)
    screen.blit(btn_back, btn_back_rect)
    screen.blit(btn_true, btn_true_rect)
    # screen.blit(btn_start, btn_start_rect)

def disp_ind_img(index, image):
    width_offset=0.2
    image_rect = image.get_rect()
    if index==0:
        image_rect.centerx = width * 0.2
        image_rect.centery = height * 0.6
    elif index==1:
        image_rect.centerx = width * (0.2 + width_offset)
        image_rect.centery = height * 0.6
    elif index==2:
        image_rect.centerx = width * (0.2 + 2 * width_offset)
        image_rect.centery = height * 0.6
    elif index==3:
        image_rect.centerx = width * (0.2 + 3 * width_offset)
        image_rect.centery = height * 0.6
    screen.blit(image, image_rect)