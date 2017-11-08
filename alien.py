import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	def __init__(self, all_settings, screen):
		"""初始化外星人的起始位置"""
		super(Alien, self).__init__()
		self.screen = screen
		self.all_setting = all_settings
		# 加载外星人图像，获取其rect
		self.image = pygame.image.load('images/alien_alpha.png')
		self.rect = self.image.get_rect()
		# 每个外星人的初始位置都在左上角附近
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		# 存储外星人精准位置
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def check_edges(self):
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left < 0:
			return True

	def update(self):
		"""右移外星人"""
		self.x += self.all_setting.alien_apeed_factor * self.all_setting.fleet_direction
		self.rect.x = self.x
