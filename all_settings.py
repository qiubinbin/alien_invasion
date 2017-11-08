class AllSettings():
	"""存储《外星人入侵》的所有设置的类"""

	def __init__(self):
		"""初始化游戏的设置"""
		# 屏幕设置
		self.screen_width = 1280
		self.screen_height = 960
		self.bg_color = (255, 255, 255)
		self.speed_scale = 1.1
		self.initialize_dynamic_settings()
		self.bullet_width = 100
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		self.fleet_drop_apeed = 10
		self.ship_limit = 3

	def initialize_dynamic_settings(self):
		"""初始化随游戏变化而变化的设置"""
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 5
		self.alien_apeed_factor = 1
		# fleet_direction为1表示向右；为-1表示向左
		self.fleet_direction = 1
		self.alien_points = 50

	def increase_speed(self):
		"""提高速度"""
		self.ship_speed_factor *= self.speed_scale
		self.bullet_speed_factor *= self.speed_scale
		self.alien_apeed_factor *= self.speed_scale
		self.alien_points = int(self.alien_points * self.speed_scale)
		print(self.alien_points)