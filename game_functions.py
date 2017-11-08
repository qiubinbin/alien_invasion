import sys
from bullet import Bullet
from alien import Alien
from enemy_bullets import EnemyBullet
import json

"""
系统相关的信息模块 import sys 
    sys.argv是一个list,包含所有的命令行参数. 
    sys.stdout sys.stdin sys.stderr 分别表示标准输入输出,错误输出的文件对象. 
    sys.stdin.readline() 从标准输入读一行 sys.stdout.write("a") 屏幕输出a 
    sys.exit(exit_code) 退出程序 
    sys.modules 是一个dictionary，表示系统中所有可用的module 
    sys.platform 得到运行的操作系统环境 
    sys.path 是一个list,指明所有查找module，package的路径
"""
import pygame


def check_events(all_settings, screen, ship, aliens, bullets, stats, play_button, score_get, enemy_bullets):
	"""事件管理器：相应按键和鼠标"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			with open('history/hightest.json', 'w') as temp:
				json.dump(stats.hightest_score, temp)
				print('Remember!')
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, all_settings, screen, ship, bullets, stats)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship, stats)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(all_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y,
							  score_get, enemy_bullets)


def check_play_button(all_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, score_get,
					  enemy_bullets):
	"""点击Play按钮重新开始游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		all_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		# 清空外星人和子弹列表
		aliens.empty()
		bullets.empty()
		enemy_bullets.empty()
		# 初始化计分板
		score_get.prep_ships()
		score_get.prep_level()
		score_get.prep_score()
		score_get.prep_hightest()
		# 创建外星人，飞船居中
		creat_fleet(all_settings, screen, ship, aliens, enemy_bullets)
		ship.update_center()


def check_keydown_events(event, all_settings, screen, ship, bullets, stats):
	"""相应按键"""
	if event.key == pygame.K_RIGHT:
		# 飞船右移
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		# 飞船左移
		ship.moving_left = True
	if event.key == pygame.K_UP:
		# 飞船上移
		ship.moving_up = True
	if event.key == pygame.K_DOWN:
		# 飞船下移
		ship.moving_down = True
	if event.key == pygame.K_SPACE:
		# 发射子弹
		fire_bullets(bullets, all_settings, screen, ship)
	if event.key == pygame.K_s:
		stats.shield_active = True
	if event.key == pygame.K_q:
		with open('history/hightest.json', 'w') as temp:
			json.dump(stats.hightest_score, temp)
			print('Remember!')
		sys.exit()


def fire_bullets(bullets, all_settings, screen, ship):
	"""发射子弹"""
	if len(bullets) < all_settings.bullets_allowed:
		# 创建一颗子弹，并将其加入到编组bullets中
		new_bullet = Bullet(all_settings, screen, ship)
		bullets.add(new_bullet)


def check_keyup_events(event, ship, stats):
	"""相应松开"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	elif event.key == pygame.K_UP:
		ship.moving_up = False
	elif event.key == pygame.K_DOWN:
		ship.moving_down = False
	elif event.key == pygame.K_s:
		stats.shield_active = False


def update_screen(all_settings, screen, ship, aliens, bullets, play_button, stats, score_get, shield, enemy_bullets):
	"""更新屏幕上的图像，并切换到新的窗口"""
	screen.fill(all_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	for bullet in enemy_bullets.sprites():
		bullet.draw()
	aliens.draw(screen)
	if stats.shield_active and stats.game_active:
		shield.draw_shield()
	ship.blitme()  # 此处注意飞船必须在背景上面，因此此条语句放在screen.fill()之后
	score_get.show_score()
	# 如果游戏处于非活动状态，就绘制Play按钮
	if stats.game_active == False:
		play_button.draw_button()
	pygame.display.flip()


def update_bullets(bullets, aliens, all_settings, screen, ship, stats, score_get, enemy_bullets):
	# 更新子弹的位置
	bullets.update()
	# 删除消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom < 0:
			bullets.remove(bullet)
	check_bullets_aliens_collides(all_settings, screen, ship, bullets, aliens, stats, score_get, enemy_bullets)


def check_hightest_score(stats, score_get):
	if stats.score > stats.hightest_score:
		stats.hightest_score = stats.score
		score_get.prep_hightest()


def check_bullets_aliens_collides(all_settings, screen, ship, bullets, aliens, stats, score_get, enemy_bullets):
	"""响应子弹和外星人碰撞"""
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		# print(collisions)
		for aliens_group in collisions.values():
			stats.score += all_settings.alien_points * len(aliens_group)
			check_hightest_score(stats, score_get)
			score_get.prep_score()
	"""
	函数原型：
　　groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict
　　参数：
　　group1：精灵组1。
　　group2：精灵组2。
　　dokill1：发生碰撞时，是否销毁精灵组1中的发生碰撞的精灵。
　　dokill2：发生碰撞时，是否销毁精灵组2中的发生碰撞的精灵。
　　collided：自定义的回调函数，你可以自己编写碰撞检测函数。碰撞检测函数的参数是两个精灵，返回值是True/False。
　　返回值：
　　返回一个字典，键是精灵组1中发生碰撞的精灵，值是精灵组2中与该精灵发生碰撞的精灵的列表。
	"""
	if len(aliens) == 0:
		all_settings.increase_speed()
		stats.level += 1
		score_get.prep_level()
		bullets.empty()
		creat_fleet(all_settings, screen, ship, aliens, enemy_bullets)


def check_fleet_edges(all_settings, aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(all_settings, aliens)
			break


def check_aliens_bottom(all_settings, stats, screen, ship, aliens, bullets, score_get, enemy_bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(all_settings, stats, screen, ship, aliens, bullets, score_get, enemy_bullets)
			break


def change_fleet_direction(all_settings, aliens):
	"""将整群外星人下移，并改变它们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += all_settings.fleet_drop_apeed
	all_settings.fleet_direction *= -1


def update_enemy_bullets(enemy_bullets, all_settings):
	for bullet in enemy_bullets.sprites():
		bullet.update()
		if bullet.y > all_settings.screen_height:
			enemy_bullets.remove(bullet)


def update_aliens(all_settings, aliens, ship, stats, screen, bullets, score_get, shield, enemy_bullets):
	"""更新外星人群中所有外星人的位置"""
	check_fleet_edges(all_settings, aliens)
	aliens.update()
	# 检测外星人和飞船的碰撞
	if stats.shield_active:
		pygame.sprite.spritecollide(shield, aliens, True)
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(all_settings, stats, screen, ship, aliens, bullets, score_get, enemy_bullets)
	check_aliens_bottom(all_settings, stats, screen, ship, aliens, bullets, score_get, enemy_bullets)


def ship_hit(all_settings, stats, screen, ship, aliens, bullets, score_get, enemy_bullets):
	if stats.ship_left > 0:
		stats.ship_left -= 1
		aliens.empty()
		bullets.empty()
		creat_fleet(all_settings, screen, ship, aliens, enemy_bullets)
		ship.update_center()
		score_get.prep_ships()
	# 暂停
	# sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)


def get_number_alien_x(all_settings, alien_width):
	"""计算每行可容纳多少个外星人"""
	available_space_x = all_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (7 * alien_width))
	return number_aliens_x


def creat_alien(all_settings, screen, aliens, alien_number, row_number, ship, enemy_bullets):
	"""创建一个外星人并将其放在当前行"""
	alien = Alien(all_settings, screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = alien_width + 7 * alien_width * alien_number
	alien.y = alien_height + 3 * alien_height * row_number
	alien.rect.x = alien.x
	alien.rect.y = alien.y
	aliens.add(alien)
	enemy_bullet_temp = EnemyBullet(ship, alien, screen)
	enemy_bullets.add(enemy_bullet_temp)


def creat_fleet(all_settings, screen, ship, aliens, enemy_bullets):
	"""创建外星群"""
	alien = Alien(all_settings, screen)
	number_aliens_x = get_number_alien_x(all_settings, alien.rect.width)
	# 创建第一行外星人
	number_rows = get_number_rows(all_settings, ship.rect.height, alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			# 创建一个外星人并将其加入当前行
			creat_alien(all_settings, screen, aliens, alien_number, row_number, ship, enemy_bullets)


def get_number_rows(all_settings, ship_heigt, alien_height):
	"""计算屏幕可容纳多少行外星人"""
	available_space_y = all_settings.screen_height - (2 * alien_height) - ship_heigt
	number_rows = int(available_space_y / (3 * alien_height))
	return number_rows
