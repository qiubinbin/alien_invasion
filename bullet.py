import pygame
from pygame.sprite import Sprite  # 导入精灵


class Bullet(Sprite):
	"""管理子弹类"""

	def __init__(self, all_settings, screen, ship):
		"""在飞船所处位置创建一个子弹"""
		super().__init__()
		self.screen = screen
		# 在(0,0)处创建一个表示子弹的矩形，再设置正确的位置
		self.rect = pygame.Rect(0, 0, all_settings.bullet_width, all_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		# 存储用小数表示的子弹位置
		self.y = float(self.rect.y)
		self.color = all_settings.bullet_color
		self.speed_factor = all_settings.bullet_speed_factor

	def update(self):
		"""向上移动子弹"""
		self.y -= self.speed_factor
		self.rect.y = self.y

	def draw_bullet(self):
		"""绘制子弹"""
		pygame.draw.rect(self.screen, self.color, self.rect)
