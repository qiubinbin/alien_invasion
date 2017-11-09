import pygame
from pygame.sprite import Group
# 测试push
from all_settings import AllSettings
from ship import Ship
import game_functions as gf
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard
from shield import Shield


def run_game():
	# 初始化游戏并创建一个屏幕对象
	all_setting = AllSettings()
	stats = Gamestats(all_setting)
	pygame.init()  # 初始化pygame
	# 创建屏幕
	screen = pygame.display.set_mode((all_setting.screen_width, all_setting.screen_height))
	pygame.display.set_caption("Alien Invation")
	# 创建飞船对象
	ship = Ship(screen, all_setting)
	# 创建一个用于存储子弹，外星人，外星人子弹的编组
	bullets = Group()
	aliens = Group()
	enemy_bullets = Group()
	shield = Shield(ship, screen)
	# gf.creat_fleet(all_setting, screen, ship, aliens)
	play_button = Button(all_setting, screen, "Play")
	score_get = Scoreboard(all_setting, screen, stats)
	# 开始游戏主循环
	while True:
		gf.check_events(all_setting, screen, ship, aliens, bullets, stats, play_button, score_get, enemy_bullets)
		if stats.game_active:
			ship.update()
			shield.set_pos()
			gf.update_bullets(bullets, aliens, all_setting, screen, ship, stats, score_get, enemy_bullets)
			gf.update_aliens(all_setting, aliens, ship, stats, screen, bullets, score_get, shield, enemy_bullets)
			gf.update_enemy_bullets(enemy_bullets, all_setting)
		gf.update_screen(all_setting, screen, ship, aliens, bullets, play_button, stats, score_get, shield,
						 enemy_bullets)


run_game()
#加强了碰撞测试