import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self, screen, all_settings):
		super().__init__()
		"""初始化设置及其位置"""
		self.screen = screen
		# 加载飞船外形并获取其外接矩形
		self.image = pygame.image.load('images/ship_alpha.png')
		self.rect = self.image.get_rect()
		self.screen_rect = self.screen.get_rect()
		# 将每艘新飞船放在屏幕底部
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.moving_right = False  # 右移标志
		self.moving_left = False  # 左移标志
		self.moving_up = False  # 上移标志
		self.moving_down = False  # 下移标志
		self.all_settings_temp = all_settings
		self.center_x = float(self.rect.centerx)
		self.center_bottom = float(self.rect.bottom)

	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""根据移动标志调整飞船的位置
		特别注意pygame的坐标原点在左上角，所以上下移动的时候要注意坐标变换"""
		if self.moving_right and self.rect.right < self.screen_rect.right:  # 同时测试是否到边
			self.center_x += self.all_settings_temp.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center_x -= self.all_settings_temp.ship_speed_factor
		if self.moving_up and self.rect.top > 0:
			self.center_bottom -= self.all_settings_temp.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.center_bottom += self.all_settings_temp.ship_speed_factor
		self.rect.centerx = self.center_x
		self.rect.bottom = self.center_bottom

	def update_center(self):
		self.rect.bottom = self.screen_rect.bottom
		self.rect.centerx = self.screen_rect.centerx
		"""复位时记得把计数恢复初始值"""
		self.center_x = float(self.rect.centerx)
		self.center_bottom = float(self.rect.bottom)

