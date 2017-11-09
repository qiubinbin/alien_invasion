import math
import pygame
from pygame.sprite import Sprite

"""外星人发射子弹"""


class EnemyBullet(Sprite):
	def __init__(self, ship, alien, screen):
		super().__init__()
		self.ship = ship
		self.screen = screen
		self.alien = alien
		self.speed = 2
		self.radius = 2
		self.color = (72, 61, 139)
		self.x = self.alien.rect.centerx
		self.y = self.alien.rect.bottom
		self.angle = math.atan2(self.ship.rect.centery - self.alien.rect.bottom,
								self.ship.rect.centerx - self.alien.rect.centerx)

	def update(self):
		self.y += self.speed
		self.x += int(self.speed / math.tan(self.angle))

	def draw(self):
		pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius, 0)
