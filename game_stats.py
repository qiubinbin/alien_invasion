import json


class Gamestats():
	"""跟踪游戏统计信息"""

	def __init__(self, all_settings):
		self.all_setting = all_settings
		self.reset_stats()
		self.game_active = False
		self.shield_active=False
		# 读取历史数据
		with open('history/hightest.json', 'r') as temp:
			self.hightest_score = int(json.load(temp))

	def reset_stats(self):
		self.ship_left = self.all_setting.ship_limit
		self.score = 0
		self.level = 1
