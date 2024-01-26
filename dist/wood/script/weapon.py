import pygame
import math,random

class Bullet():
	def __init__(self,game,entity_pos,target,image):
		self.game = game
		self.pos = [entity_pos[0],entity_pos[1]]
		self.target = target
		self.image = image
		self.alive = True
		self.shoot = False
		if self.target.__class__.__name__ == 'Player':
			self.angle = math.atan2(self.pos[1] - self.target.pos[1],self.pos[0] - self.target.pos[0])
			rel_center = (self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1])
		else:
			self.angle = math.atan2(self.pos[1] - self.target[1],self.pos[0] - self.target[0])
			rel_center = (self.target[0] - self.pos[0], self.target[1] - self.pos[1])
		self.speed = 15
		self.vel_x = math.cos(self.angle)
		self.vel_y = math.sin(self.angle)
		angle = (1 if self.game.player.flip else -1)*math.degrees(math.atan2(rel_center[1], rel_center[0]))
		self.image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(90 if self.game.player.flip else -90)),angle),self.game.player.flip,False)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		self.alive = True
		self.alive_time = 60
		self.active = True
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1],self.image.get_width(),self.image.get_height())
	def perfect_collision(self,target):
		if target.__class__.__name__ == 'Player':
			mask1 = pygame.mask.from_surface(self.image)
			mask2 = pygame.mask.from_surface(target.animation.img())
			if mask2.overlap(mask1,(self.rotate_rect.x - target.rect().x,self.rotate_rect.y - target.rect().y + 24)) and self.speed:
				target.damage_get = 5
				# target.pos[0] -= self.vel_x * 20
				# target.pos[1] -= self.vel_y * 20
				self.speed = 0
				self.game.screen_shake = 10
				# self.game.slashs.remove(self)
		else:
			for enemy in self.game.enemies:
				mask1 = pygame.mask.from_surface(self.image)
				mask2 = pygame.mask.from_surface(enemy.animation.img())
				if mask2.overlap(mask1,(self.rotate_rect.x - enemy.rect().x,self.rotate_rect.y - enemy.rect().y + 24)) and self.speed:
					self.speed = 0
					enemy.damage_get = 5

	def update(self,tile_map):
		for rect in tile_map.get_rect_tile(self.rotate_rect.center):
			if rect.collidepoint(self.rotate_rect.center):
				self.speed = 0
		self.alive_time = max(0,self.alive_time - 1)
		if self.alive_time == 0:
			self.alive = False
	def render(self,surf,offset,object_to_draw,tile_map):
		self.pos[0] -= (self.vel_x*self.speed)
		self.pos[1] -= (self.vel_y*self.speed)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		self.update(tile_map)
		# pygame.draw.rect(surf,'red',(self.rotate_rect.x - offset[0],self.rotate_rect.y - offset[1],self.rotate_rect.width,self.rotate_rect.height))
		object_to_draw.append([self.image, self.rotate_rect])
class Arrow(Bullet):
	def __init__(self,game,entity_pos,target_pos):
		super().__init__(game,entity_pos,target_pos,game.assets['bullet'][0])
	
	def render(self,surf,offset,object_to_draw,tile_map):
		self.speed = max(0,self.speed - 0.25)
		super().render(surf,offset,object_to_draw,tile_map)
class Pistol_bullet(Bullet):
	def __init__(self,game,entity_pos,target_pos):
		super().__init__(game,entity_pos,target_pos,game.assets['bullet'][1])
	
	def render(self,surf,offset,object_to_draw,tile_map):
		super().render(surf,offset,object_to_draw,tile_map)

class Slash():
	def __init__(self,game,size,color,alive_time,entity_pos,target):
		self.game = game
		self.entity_pos = entity_pos
		self.pos = self.entity_pos.rect(target)[1].center
		self.target = target
		self.size = size
		self.color = color
		if target.__class__.__name__ == 'Player':
			self.angle = math.atan2(self.pos[1] - self.target.pos[1],self.pos[0] - self.target.pos[0])
			rel_center = (self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1])
		else:
			self.angle = math.atan2(self.pos[1] - self.target[1],self.pos[0] - self.target[0])
			rel_center = (self.target[0] - self.pos[0], self.target[1] - self.pos[1])
		self.speed = 10
		self.vel_x = math.cos(self.angle)
		self.vel_y = math.sin(self.angle)
		self.image = pygame.Surface((self.size,self.size))
		self.img_size = self.image.get_size()
		pygame.draw.circle(self.image,self.color,(self.img_size[0]//2,self.img_size[1]//2),self.img_size[0]//2)
		pygame.draw.circle(self.image,'black',(self.img_size[0]//2,self.img_size[1]//2 + self.img_size[1]//4),self.img_size[0]//2)
		self.image.set_colorkey((0,0,0))
		angle = (1 if self.game.player.flip else -1)*math.degrees(math.atan2(rel_center[1], rel_center[0]))
		self.image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(90 if self.game.player.flip else -90)),angle),self.game.player.flip,False)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		self.alive = True
		self.alive_time = alive_time
		self.damage = 10
		self.counter_bullet = False
		self.push = False
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1],self.image.get_width(),self.image.get_height())
	def update(self,tile_map):
		for rect in tile_map.get_rect_tile(self.rotate_rect.center):
			if rect.collidepoint(self.rotate_rect.center):
				self.speed = 0
	def perfect_collision(self,target):
		if target.__class__.__name__ == 'Player':
			mask1 = pygame.mask.from_surface(self.image)
			mask2 = pygame.mask.from_surface(target.animation.img())
			if mask2.overlap(mask1,(self.rotate_rect.x - target.rect().x,self.rotate_rect.y - target.rect().y + 24)):
				target.damage_get = 2
				self.game.screen_shake = 10
				if self.push:
					target.update(self.game.tile_map,movement = (-self.vel_x * 20,-self.vel_y * 20))
				# self.game.slashs.remove(self)
			if self.counter_bullet:
				for bullet in self.game.bullets:
					if bullet.active:
						mask1 = pygame.mask.from_surface(self.image)
						mask2 = pygame.mask.from_surface(bullet.image)
						if mask2.overlap(mask1,(self.rotate_rect.x - bullet.rotate_rect.x,self.rotate_rect.y - bullet.rotate_rect.y)):
							bullet.target = self.target
							bullet.speed = 20
							bullet.vel_x = -bullet.vel_x
							bullet.vel_y = -bullet.vel_y
		else:
			for enemy in self.game.enemies:
				if enemy.active:
					mask1 = pygame.mask.from_surface(self.image)
					mask2 = pygame.mask.from_surface(enemy.animation.img())
					if mask2.overlap(mask1,(self.rotate_rect.x - enemy.rect().x,self.rotate_rect.y - enemy.rect().y + 24)):
						enemy.damage_get = 2
						if self.push:
							enemy.update(self.game.tile_map,movement = (-self.vel_x * 20,-self.vel_y * 20))
			if self.counter_bullet:
				for bullet in self.game.bullets:
					mask1 = pygame.mask.from_surface(self.image)
					mask2 = pygame.mask.from_surface(bullet.image)
					if mask2.overlap(mask1,(self.rotate_rect.x - bullet.rotate_rect.x,self.rotate_rect.y - bullet.rotate_rect.y)):
						bullet.target = self.game.mouse_pos
						bullet.speed = 2
						bullet.vel_x = -bullet.vel_x
						bullet.vel_y = -bullet.vel_y
			
	def render(self,surf,offset,object_to_draw,tile_map):
		self.pos = list(self.entity_pos.rect(self.target)[1].center)
		self.rotate_rect = self.image.get_rect(center=self.pos)
		# self.update(tile_map)
		object_to_draw.append([self.image, self.rotate_rect])
		if self.alive:
			self.alive_time = max(0,self.alive_time-0.25)
			self.image.set_alpha(200 * self.alive_time + 50)
		if self.alive_time == 0:
			self.alive = False

class Weapon():
	def __init__(self,game,number,entity,size,animate):
		self.game = game
		self.entity = entity
		self.size = size
		self.pos = [self.entity.rect().centerx,self.entity.rect().centery]
		self.number = number
		self.damage = False
		self.angle = 0
		self.image = pygame.Surface((self.game.assets['item'][self.number].get_width(),self.game.assets['item'][self.number].get_height()*2))
		mask = pygame.mask.from_surface(self.game.assets['item'][self.number])
		self.image.blit(self.game.assets['item'][self.number],(0,0))
		# self.image.blit(mask.to_surface(unsetcolor = (0,0,0,0),setcolor = (random.randint(0,100),60,120,60)),(0,0),special_flags=pygame.BLEND_RGB_ADD)
		# if self.number != 6:
		# 	pygame.draw.circle(self.image,'#61683a',(self.image.get_width()//2 - 1,self.image.get_height()//2 - 2),2)
		# 	pygame.draw.circle(self.image,'#0e0c0c',(self.image.get_width()//2 - 1,self.image.get_height()//2 - 2),3,1)
		self.image.set_colorkey((0,0,0))
		self.stop = False
		self.animate = animate
	def rect(self,target):
		# print(target)
		if target.__class__.__name__ == 'Player':
			rel_center = (target.pos[0] - self.pos[0],target.pos[1] - self.pos[1])
		else:
			rel_center = (target[0] - self.pos[0],target[1] - self.pos[1])
		if self.stop:
			pass
		else:
			self.angle = (1 if self.entity.flip else -1)*math.degrees(math.atan2(rel_center[1], rel_center[0]))
		if self.animate:
			self.rotated_image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(180 if self.entity.flip else 0)),self.angle),self.entity.flip,False)
		else:
			self.rotated_image = pygame.transform.flip(pygame.transform.rotate(pygame.transform.rotate(self.image,(90 if self.entity.flip else -90)),self.angle),self.entity.flip,False)
		self.rotated_rect = self.rotated_image.get_rect(center=self.pos)
		return [self.rotated_image, self.rotated_rect]
	def render(self,surf,offset,object_to_draw,target):
		object_to_draw.append(self.rect(target))
class Bare_hands(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,12,entity,size,True)
		self.time_slash = 0
		self.distance = 20
		self.cooldown = 10
		self.type = 'combat'
	def slash(self,event,target):
		if event and self.time_slash == 0 and self.cooldown == 0:
			test_slash = Slash(self.game,30,'white',2,self.entity.weapon,target)
			self.time_slash = test_slash.alive_time
			test_slash.speed = 1.3
			self.game.slashs.append(test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)
class Wood_sword(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,6,entity,size,True)
		self.time_slash = 0
		self.distance = 35
		self.cooldown = 10
		self.type = 'combat'

	def slash(self,event,target):
		if event and self.time_slash == 0 and self.cooldown == 0:
			test_slash = Slash(self.game,50,'white',2,self.entity.weapon,target)
			self.time_slash = test_slash.alive_time
			test_slash.speed = 2
			test_slash.push = True
			self.game.slashs.append(test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
			self.cooldown = 10
		else:
			self.stop = False
			self.cooldown = max(0,self.cooldown - 1)
		super().render(surf,offset,object_to_draw,target)
class Wood_axe(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,7,entity,size,True)
		self.time_slash = 0
		self.distance = 40
		self.cooldown = 20
		self.type = 'combat'

	def slash(self,event,target):
		if event == 1 and self.time_slash == 0 and not self.damage and self.cooldown == 0:
			test_slash = Slash(self.game,40,'white',2,self.entity.weapon,target)
			self.time_slash = 2
			test_slash.speed = 2
			test_slash.push = True
			self.game.slashs.append(test_slash)
			self.damage = True
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.damage = False
			self.angle += (-30 if self.entity.flip else -30)
			self.cooldown = 10
		else:
			self.stop = False
			self.cooldown = max(0,self.cooldown - 1)
		super().render(surf,offset,object_to_draw,target)
class Wood_pickaxe(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,8,entity,size,True)
		self.time_slash = 0
		self.distance = 40
		self.cooldown = 20
		self.type = 'combat'
	def slash(self,event,target):
		if event == 1 and self.time_slash == 0 and self.cooldown == 0:
			test_slash = Slash(self.game,40,'white',2,self.entity.weapon,target)
			self.time_slash = 2
			test_slash.speed = 2
			test_slash.push = True
			self.game.slashs.append(test_slash)
			self.damage = True
			self.cooldown = 10


	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.stop = True
			self.damage = False
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
			self.cooldown = max(0,self.cooldown - 1)
		super().render(surf,offset,object_to_draw,target)
class Bow(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,9,entity,size,False)
		self.charge = 0
		self.ratio = 0
		self.distance = 300
		self.cooldown = 40
		self.type = 'range'

	def charge_shoot(self):
		if pygame.mouse.get_pressed()[0]:
			self.charge = min(10,self.charge + 0.25)
			# pygame.draw.line(self.game.display,'green',(self.rect()[1].centerx - self.game.true_scroll[0],self.rect()[1].centery - self.game.true_scroll[1]),(self.game.mouse_pos[0] - self.game.true_scroll[0],self.game.mouse_pos[1] - self.game.true_scroll[1]),1)

		else: self.charge = 0
		self.ratio = self.charge/10
	def shoot_arrow(self,event,target):
		
		if event:
			arrow = Arrow(self.game,self.entity.weapon.rect(target)[1].center,target)
			arrow.speed = self.charge*2
			self.game.bullets.append(arrow)
			self.charge = 0

	def render(self,surf,offset,object_to_draw,target):
		super().render(surf,offset,object_to_draw,target)
		pygame.draw.rect(surf,'#C7CBD1',(self.entity.pos[0] - offset[0],self.entity.pos[1] - offset[1] - 20,self.entity.rect().width,2))
		pygame.draw.rect(surf,'#303841',(self.entity.pos[0] - offset[0],self.entity.pos[1] - offset[1] - 20,self.entity.rect().width*self.ratio,2))

class Spear(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,10,entity,size,False)
		self.charge = 0
		self.ratio = 0
		self.time_slash = 0
		self.test_slash = None
		self.cooldown = 30
		self.type = 'combat'
	def slash(self,event,target):
		if event and self.time_slash == 0 and self.cooldown == 0:
			self.test_slash = Slash(self.game,40,'red',2,self.entity.weapon,target)
			self.time_slash = self.test_slash.alive_time
			self.test_slash.push = True
			# test_slash.size = (self.charge * 4)
			self.game.slashs.append(self.test_slash)
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			self.pos = list(self.pos)
			self.pos[0] -= self.test_slash.vel_x*10
			self.pos[1] -= self.test_slash.vel_y*10
			self.cooldown = 10
		else:
			self.cooldown = max(0,self.cooldown - 1)
		super().render(surf,offset,object_to_draw,target)
class Katana(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,11,entity,size,True)
		self.time_slash = 0
		self.test_slash = None
		self.distance = 100
		self.cooldown = 20
		self.type = 'combat'
	def slash(self,event,target):
		if event and self.time_slash == 0:
			self.test_slash = Slash(self.game, 50, 'red', 5, self.entity.weapon.rect(target)[1].center, target)
			self.time_slash = 2
			self.test_slash.speed = 5
			self.test_slash.push = True
			self.game.slashs.append(self.test_slash)


	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			# self.entity.pos[0] -= self.test_slash.vel_x * 2
			# self.entity.pos[1] -= self.test_slash.vel_y * 2
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
		super().render(surf,offset,object_to_draw,target)

class Pistol(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,13,entity,size,False)
		self.charge = 0
		self.ratio = 0
		self.type = 'range'
	def charge_shoot(self):
		if pygame.mouse.get_pressed()[0]:
			self.charge = min(20,self.charge + 0.25)
			# pygame.draw.line(self.game.display,'green',(self.rect()[1].centerx - self.game.true_scroll[0],self.rect()[1].centery - self.game.true_scroll[1]),(self.game.mouse_pos[0] - self.game.true_scroll[0],self.game.mouse_pos[1] - self.game.true_scroll[1]),1)

		else: self.charge = 0
		self.ratio = self.charge/20
	def shoot_bullet(self,event,target):
		
		arrow = Pistol_bullet(self.game,self.rect(target)[1].center,self.game.mouse_pos)
		arrow.speed = 20
		self.game.bullets.append(arrow)

	def render(self,surf,offset,object_to_draw,target):
		super().render(surf,offset,object_to_draw,target)
class Energy_sword(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,14,entity,size,True)
		self.time_slash = 0
		self.test_slash = None
		self.distance = 300
		self.cooldown = 10
		self.type = 'combat'
	def slash(self,event,target):
		if event and self.time_slash == 0 and self.entity.energy >=1 and self.cooldown == 0:
			self.test_slash = Slash(self.game, 100, '#42f9f4', 7, self.entity.weapon.rect(target)[1].center, target)
			self.time_slash = 2
			self.test_slash.speed = 7
			self.test_slash.counter_bullet = True
			self.test_slash.push = True
			self.entity.energy -= 1
			self.game.slashs.append(self.test_slash)
			self.cooldown = 10
	def render(self,surf,offset,object_to_draw,target):
		self.time_slash = max(0,self.time_slash - 0.25)
		if self.time_slash > 0:
			# self.entity.pos[0] -= self.test_slash.vel_x * 2
			# self.entity.pos[1] -= self.test_slash.vel_y * 2
			self.stop = True
			self.angle += (-30 if self.entity.flip else -30)
		else:
			self.stop = False
			self.cooldown = max(0,self.cooldown - 1)
		super().render(surf,offset,object_to_draw,target)

class Energy_bow(Weapon):
	def __init__(self,game,entity,size):
		super().__init__(game,15,entity,size,False)
		self.charge = 0
		self.ratio = 0
		self.distance = 300
		self.cooldown = 40
		self.type = 'range'
	def charge_shoot(self):
		if pygame.mouse.get_pressed()[0]:
			self.charge = min(20,self.charge + 0.25)
		else: self.charge = 0
		self.ratio = self.charge/20
	def shoot_arrow(self,event,target):
		# pygame.draw.line(self.game.display,'green',(self.rect()[1].centerx - self.game.true_scroll[0],self.rect()[1].centery - self.game.true_scroll[1]),(target[0] - self.game.true_scroll[0],target[1] - self.game.true_scroll[1]),1)
		if event and self.entity.energy >= 1:
			line = pygame.Surface((24,24))
			pygame.draw.polygon(line,'#40E879',[(8,10),(12,0),(16,10)])
			pygame.draw.line(line,'#40E879',(12,10),(12,24),3)
			line.set_colorkey((0,0,0))
			for i in range(5):
				arrow = Bullet(self.game,(self.entity.weapon.rect(target)[1].centerx + random.randint(-50,50),self.entity.weapon.rect(target)[1].centery + random.randint(-50,50)),
				target,line)
				arrow.speed = 20
				self.game.bullets.append(arrow)
			self.charge = 0
	def render(self,surf,offset,object_to_draw,target):
		super().render(surf,offset,object_to_draw,target)
		pygame.draw.rect(surf,'#C7CBD1',(self.entity.pos[0] - offset[0],self.entity.pos[1] - offset[1] - 20,self.entity.rect().width,2))
		pygame.draw.rect(surf,'#303841',(self.entity.pos[0] - offset[0],self.entity.pos[1] - offset[1] - 20,self.entity.rect().width*self.ratio,2))
