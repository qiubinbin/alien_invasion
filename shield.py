import pygame
import math

"""护盾"""


class Shield():
	def __init__(self, ship, screen):
		self.ship = ship
		self.rect = self.ship.rect
		self.screen = screen
		self.radius = int((math.sqrt(self.ship.rect.width ** 2 + self.ship.rect.height ** 2)) / 2)
		self.color = (254, 67, 101)
		self.set_pos()

	def set_pos(self):
		self.x = self.ship.rect.centerx
		self.y = self.ship.rect.centery

	def draw_shield(self):
		pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius, 0)
