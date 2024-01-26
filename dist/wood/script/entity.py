import pygame,random
from script.setting import no_stack_item,item_id,tool_item
from script.inventory import Player_inventory,Player_tool_bar,Craft_table
from math import sin
		
class Physical_Entity():
	def __init__(self,game,type_e,pos,size,hp):
		self.type_e = type_e
		self.game = game 
		self.pos = pos
		self.size = size
		self.image = None
		self.action = ''
		self.flip = False
		self.set_action('idle')
		self.collision = {'up':False,'down':False,'left':False,'right':False}
		self.direct = (0,-1)
		self.hp = hp 
		self.max_hp = hp 
		self.energy = 20
		self.max_energy = 20
		self.health_bar = None
		self.energy_bar = None
		self.weapon = None
		self.have_animate = False
		self.active = True
		self.damage_get = 0
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
	def set_action(self,action):
		if action!=self.action:
			self.action = action
			self.animation = self.game.assets[self.type_e +'/' + self.action].copy()
	def update(self,tile_map,movement = (0,0)):
		self.move_direct = pygame.math.Vector2(movement[0],movement[1])
		self.pos[0] += self.move_direct.x
		entity_rect = self.rect()
		for rect in tile_map.get_rect_tile(self.pos):
			if entity_rect.colliderect(rect):
				if movement[0] > 0:
					entity_rect.right = rect.left
					self.direct = (1,0)
				if movement[0] < 0:
					entity_rect.left = rect.right
					self.direct = (-1,0)
				self.pos[0] = entity_rect.x
		self.pos[1] += self.move_direct.y
		entity_rect = self.rect()
		for rect in tile_map.get_rect_tile(self.pos):
			if entity_rect.colliderect(rect):
				if movement[1] > 0:
					entity_rect.bottom = rect.top
					self.direct = (0,1)
				if movement[1] < 0:
					entity_rect.top = rect.bottom
					self.direct = (0,-1)
				self.pos[1] = entity_rect.y
		if movement[0] > 0:
			self.flip = False
		if movement[0] < 0:
			self.flip = True
		if self.have_animate:
			self.animation.update()
		if self.energy < self.max_energy:
			self.energy += 0.01
	def wave_value(self):
		wave = sin(pygame.time.get_ticks())
		if wave > 0:
			return 120
		else:
			return 0
	def render(self,surf,offset,object_to_draw):
		object_to_draw.append([self.image,pygame.Rect(self.rect().x,self.rect().y - self.animation.img().get_width()//1.31,self.animation.img().get_width(),self.animation.img().get_height())])

class Player(Physical_Entity):
	def __init__(self,game,pos,size):
		super().__init__(game,'player2',pos,size,20)
		self.test = 0
		self.inventory = Player_inventory(self.game)
		self.tool_bar = Player_tool_bar(self.game)
		self.craft_table = Craft_table(self.game)
		self.have_animate = True
		
	def update(self,tile_map,movement = (0,0)):
		super().update(tile_map,movement = movement)
		if movement[0] != 0 or movement[1] != 0:
			self.set_action('run')
		else:
			self.set_action('idle')
	def render(self, surf, offset, object_to_draw):
		self.image = pygame.transform.flip(self.animation.img(),self.flip,False)
		if self.damage_get:
			mask = pygame.mask.from_surface(self.image)
			self.image = mask.to_surface(setcolor=(255,255,255,255),unsetcolor=(0,0,0,0))
			self.damage_get = max(0,self.damage_get - 1)
		object_to_draw.append([self.image,pygame.Rect(self.rect().x,self.rect().y - 24,self.animation.img().get_width(),self.animation.img().get_height())])

class Dafluffy(Physical_Entity):
	def __init__(self,game,pos,size):
		super().__init__(game,'dafluffy',pos,size,20)
		self.walking = 0
		self.move = [0,0]
		self.weapon = None
		self.have_animate = True
	def update(self,tile_map,movement = (0,0)):
		if self.walking:
			# if tile_map.check_solid([self.rect().centerx + (-5 if self.flip else 5),self.rect().centery + (-5 if self.flip else 5)]):
			# 	self.move[0] = -self.move[0]
			# 	self.move[1] = -self.move[1]
		
			# 	self.flip = tile_map.check_solid([self.rect().centerx + (-7 if self.flip else 7),self.rect().centery + (-7 if self.flip else 7)])
			movement = (movement[0] + self.move[0],movement[1] + self.move[1])
			self.walking = max(0,self.walking -1)
		else:
			self.move[0] = random.choice([-2,0,2])
			self.move[1] = random.choice([-2,0,2])
			self.walking = random.randint(30,120)
		super().update(tile_map,movement = movement)
		if movement[0] != 0 or movement[1] != 0:
			self.set_action('run')
		else:
			self.set_action('idle')
	def render(self, surf, offset, object_to_draw):

		object_to_draw.append([pygame.transform.flip(self.animation.img(),self.flip,False),pygame.Rect(self.rect().x,self.rect().y - 16,self.animation.img().get_width(),self.animation.img().get_height())])

class Pink(Physical_Entity):
	def __init__(self,game,pos,size):
		super().__init__(game,'pink',pos,size,20)
		self.walking = 0
		self.move = [0,0]
		self.weapon = None
		self.have_animate = True
		self.target = self
		self.reset = 0
		self.offset_x = random.randrange(-300,300)
		self.offset_y = random.randrange(-300,300)
		self.speed = 1
	def update(self,tile_map,movement = (0,0)):
		direct = (0,0)
		direct = (movement[0] + self.move[0],movement[1] + self.move[1])
		self.move = [0,0]
		if self.reset == 0:
			self.offset_x = random.randrange(-300,300)
			self.offset_y = random.randrange(-300,300)
			self.reset = random.randrange(30,50)
		else:
			self.reset -= 1
		distance = 200
		test_distance = abs(self.target.rect().centerx - self.rect().centerx) <= self.game.display.get_width()//2 and abs(self.target.rect().centery - self.rect().centery) <= self.game.display.get_height()//2
		if test_distance:	
			if self.target.rect().x + self.offset_x >= self.rect().x:
				self.move[0] = self.speed
			elif self.target.rect().x + self.offset_x <= self.rect().x:
				self.move[0] = -self.speed

			if self.target.rect().y + self.offset_y >= self.rect().y:
				self.move[1] = self.speed
			elif self.target.rect().y + self.offset_y <= self.rect().y:
				self.move[1] = -self.speed
		else:
			if self.walking > 0:
				self.walking = max(0,self.walking -1)
			else:
				self.move[0] = random.randint(-1,1)
				self.move[1] = random.randint(-1,1)
				self.walking = random.randint(30,120)
		super().update(tile_map,movement = direct)
		if direct[0] != 0 or direct[1] != 0:
			self.set_action('run')
		else:
			self.set_action('idle')
	def render(self, surf, offset, object_to_draw):
		object_to_draw.append([pygame.transform.flip(self.animation.img(),self.flip,False),pygame.Rect(self.rect().x,self.rect().y - 8,self.animation.img().get_width(),self.animation.img().get_height())])

class Homeless(Physical_Entity):
	def __init__(self,game,pos,size):
		super().__init__(game,'homeless',pos,size,20)
		self.walking = 0
		self.reset = 0
		self.offset_x = random.randrange(-300,300)
		self.offset_y = random.randrange(-300,300)
		self.move = [0,0]
		self.target = None
		self.attack = False
		self.attack_time = 0
		self.speed = 1.5
		self.have_animate = True
	def update(self,tile_map,movement = (0,0)):
		direct = (0,0)
		direct = (movement[0] + self.move[0],movement[1] + self.move[1])
		self.move = [0,0]
		if self.reset == 0:
			self.offset_x = random.randrange(-300,300)
			self.offset_y = random.randrange(-300,300)
			self.reset = random.randrange(30,50)
		else:
			self.reset -= 1
		distance = 200
		test_distance = abs(self.target.rect().centerx - self.rect().centerx) <= self.game.display.get_width()//2 and abs(self.target.rect().centery - self.rect().centery) <= self.game.display.get_height()//2
		if test_distance:	
			if self.target.rect().x + self.offset_x >= self.rect().x:
				self.move[0] = self.speed
			elif self.target.rect().x + self.offset_x <= self.rect().x:
				self.move[0] = -self.speed

			if self.target.rect().y + self.offset_y >= self.rect().y:
				self.move[1] = self.speed
			elif self.target.rect().y + self.offset_y <= self.rect().y:
				self.move[1] = -self.speed
			distance = self.weapon.distance
			test_distance = abs(self.target.rect().centerx - self.rect().centerx) <= distance and abs(self.target.rect().centery - self.rect().centery) <= distance
			if test_distance:
				if self.attack and self.attack_time == 0:
					if self.weapon.type == 'range':
						self.weapon.charge = 10
						self.weapon.shoot_arrow(1,self.target)
					else:
						self.weapon.slash(1,self.target)
					self.attack_time = self.weapon.cooldown
			self.attack_time = max(0,self.attack_time - 0.25)
			if self.attack_time == 0:
				self.attack = True
		else:
			if self.walking > 0:
				self.walking = max(0,self.walking -1)
			else:
				self.move[0] = random.randint(-1,1)
				self.move[1] = random.randint(-1,1)
				self.walking = random.randint(30,120)
		super().update(tile_map,movement = direct)
		if direct[0] != 0 or direct[1] != 0:
			self.set_action('run')
		else:
			self.set_action('idle')
	def render(self, surf, offset, object_to_draw):
		self.image = pygame.transform.flip(self.animation.img(),self.flip,False)
		if self.damage_get:
			mask = pygame.mask.from_surface(self.image)
			self.image = mask.to_surface(setcolor=(255,255,255,255),unsetcolor=(0,0,0,0))
			self.damage_get = max(0,self.damage_get - 1)
		object_to_draw.append([self.image,pygame.Rect(self.rect().x,self.rect().y - 24,self.animation.img().get_width(),self.animation.img().get_height())])

class Item(Physical_Entity):
	def __init__(self, game, type_e, pos,size):
		super().__init__(game, type_e, pos, size,1)
		self.size = size
		self.speed = 2
		self.direct = [random.random() * random.choice([-self.speed,self.speed]), random.random() * random.choice([-self.speed,self.speed])]
		self.move = 10
		self.swing = 0
	def set_action(self,action):
		if action!=self.action:
			self.action = action
	def update(self,tile_map,movement = [0,0]):
		self.collision = {'up':False,'down':False,'left':False,'right':False}
		
		if self.move > 0:
			movement[0] = self.direct[0] * self.move/4
			movement[1] = self.direct[1] * self.move/4
		else:
			movement = [0,sin(self.swing)*self.speed]
		self.swing += 0.5
		if self.swing >= 50:
			self.swing = 0
		self.move = max(0,self.move - 1)
		self.move_direct = pygame.math.Vector2(movement[0],movement[1])
		super().update(tile_map,movement=self.move_direct)
	def convert_size(self,surf):
		return pygame.transform.scale(surf,(self.size[0],self.size[1]))
	def render(self,surf,offset,object_to_draw):
		object_to_draw.append([(self.game.assets['item'][item_id[self.type_e]]),
						pygame.Rect(self.rect().x,self.rect().y,
						self.size[0],
						self.size[1])])
		# shadow_surf = pygame.Surface((self.game.display.get_size()),pygame.SRCALPHA)
		# pygame.draw.ellipse(shadow_surf,(0,0,0,50),(self.pos[0] - offset[0],self.pos[1] - offset[1] + self.size[0] // 1.5, self.size[0], self.size[1] // 3))
		# self.game.display.blit(shadow_surf,(0,0))
class Tile_func():
	def __init__(self,game,type_t,pos,hp,variant):
		self.game = game
		self.type_t = type_t
		self.pos = pos 
		self.hp = hp
		self.variant = variant
		self.image = self.game.assets[self.type_t][self.variant]
		self.angle = 0
		self.max_angle = random.choice([-90,90])
		self.alive = True
		self.drop_item = (self.type_t,0)
	def rect(self):
		return pygame.Rect(self.pos[0] - self.game.assets[self.type_t][self.variant].get_width() // 7,self.pos[1] - self.game.tile_map.tile_size * 2,self.image.get_width(),self.image.get_height())
	def drop_item_type(self,id,item_class):
		self.game.item_group.append(item_class(self.game,id,[self.pos[0],self.pos[1] - 8],[16,16]))
	def render(self,surf,object_to_draw):
		if self.hp == 0:
			if self.angle < self.max_angle and self.max_angle > 0:
				self.angle += 2
				self.pos[0] -= 1
				self.pos[1] += 0.5
			elif self.angle > self.max_angle and self.max_angle < 0:
				self.angle -= 2
				self.pos[0] += 1
				self.pos[1] += 0.5
		if self.angle == self.max_angle:
			self.alive = False
			
		self.rotate_image = pygame.transform.rotate(self.image,self.angle)
		self.rotate_rect = self.rotate_image.get_rect(center = self.rect().center)
		# self.mask = pygame.mask.from_surface(self.rotate_image)
		# self.outline = [(p[0] ,p[1]) for p in self.mask.outline()]
		# pygame.draw.lines(self.rotate_image,'white',True,self.outline,1)
		object_to_draw.append([self.rotate_image,self.rotate_rect])

class Tree(Tile_func):
	def __init__(self,game,pos,hp,variant):
		super().__init__(game,'tree',pos,hp,variant)
		self.drop_item = 'oak_wood'
	def rect(self):
		return pygame.Rect(self.pos[0] - self.game.assets[self.type_t][self.variant].get_width() // 7,self.pos[1] - self.game.tile_map.tile_size * 2,self.image.get_width(),self.image.get_height())
	def drop_item_type(self, id, item_class):
		for _ in range(0,random.randint(2,5)):
			item = item_class(self.game,id,[self.pos[0],self.pos[1] - 8],[16,16])
			self.game.item_group.append(item)
	def render(self,surf,object_to_draw): 
		super().render(surf,object_to_draw)
class Block(Tile_func):
	def __init__(self,game,type_t,pos,hp,variant):
		super().__init__(game,type_t,pos,hp,variant)
		self.drop_item = self.type_t
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1] - self.game.tile_map.tile_size,self.image.get_width(),self.image.get_height())
	def drop_item_type(self, id, item_class):
		item = item_class(self.game,id,[self.pos[0] + 4,self.pos[1]],[16,16])
		item.move = 0
		self.game.item_group.append(item)
	def render(self,surf,object_to_draw):
		self.alive = False
		super().render(surf,object_to_draw)
