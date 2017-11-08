import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
	def __init__(self, all_settings, screen, stats):
		self.screen = screen
		self.all_settings = all_settings
		self.stats = stats
		self.screen_rect = self.screen.get_rect()
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont('华文仿宋', 20)
		# 准备初始得分图像
		self.prep_score()
		self.prep_hightest()
		self.prep_level()
		self.prep_ships()

	def prep_score(self):
		rounded_score = round(self.stats.score, -1)  # 圆整到十的整数倍
		score_str = "分数：" + "{:,}".format(rounded_score)  # 添加千位分隔符
		self.score_image = self.font.render(score_str, True, self.text_color, self.all_settings.bg_color)
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_hightest(self):
		rounded_hightest_score = round(self.stats.hightest_score, -1)  # 圆整到十的整数倍
		hightest_score_str = "最高分：" + "{:,}".format(rounded_hightest_score)  # 添加千位分隔符
		self.hightest_score_image = self.font.render(hightest_score_str, True, self.text_color,
													 self.all_settings.bg_color)
		self.hightest_score_rect = self.hightest_score_image.get_rect()
		self.hightest_score_rect.right = self.score_rect.right
		self.hightest_score_rect.top = self.score_rect.bottom

	def prep_level(self):
		level_str = "等级：" + "{:,}".format(self.stats.level)
		self.level_image = self.font.render(level_str, True, self.text_color, self.all_settings.bg_color)
		self.level_rect = self.level_image.get_rect()
		# self.level_rect.centerx = self.hightest_score_rect.centerx
		self.level_rect.right = self.hightest_score_rect.right
		self.level_rect.top = self.hightest_score_rect.bottom

	def show_score(self):
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.hightest_score_image, self.hightest_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		# for ships in self.ships_left.sprites():
		# 	ships.blitme()
		self.ships_left.draw(self.screen)

	def prep_ships(self):
		self.ships_left = Group()
		# number_ships = self.stats.ship_left
		# while number_ships > 0:
		for number_ships in range(self.stats.ship_left):
			ship_temp = Ship(self.screen, self.all_settings)
			# ship_temp.rect.top = self.screen_rect.top
			# ship_temp.rect.left = ship_temp.rect.width * number_ships
			ship_temp.rect.x = 10 + ship_temp.rect.width * number_ships
			ship_temp.rect.y = 10
			self.ships_left.add(ship_temp)
			number_ships -= 1
