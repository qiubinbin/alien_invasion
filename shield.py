import pygame
import math

"""护盾"""


class Shield():
	def __init__(self, ship, screen):
		self.ship = ship
		self.rect = self.ship.rect
		self.screen = screen
		self.radius = int((math.sqrt(self.ship.rect.width ** 2 + self.ship.rect.height ** 2)) / 2)-5
		self.colors = ((174, 221, 129),(107,194,53),(6,128,67),(38,157,128))
		self.set_pos()

	def set_pos(self):
		self.x = self.ship.rect.centerx
		self.y = self.ship.rect.centery

	def draw_shield(self):
		radius_temp=self.radius
		for color in self.colors:
			pygame.draw.circle(self.screen, color, (self.x, self.y), radius_temp, 0)
			radius_temp-=20
