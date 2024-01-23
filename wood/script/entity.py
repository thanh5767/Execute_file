import pygame,random
from math import sin

test_storage =  ['fence_stake','weapon','water'] #+ ['stone','water','fence','wood_slab','wood_wall','grass','fence_stake','sand','sand_stone','chest','wood_block']
can_stack_item = ['stone','water','fence','wood_slab','wood_wall','grass','fence_stake','sand','sand_stone','chest','wood_block','item','solid_stone']
tool_item = ['weapon']
craft_recipy = {
	'wood_sword':{'item','item','item'}
}
class Inventory():
	def __init__(self,game,pos,size,item_size):
		self.size = size
		self.item_size = item_size
		# self.pos = pos
		self.game = game
		self.storage = {}
		self.x_move = pos[0]
		self.y_move = pos[1]
		# self.hold = None
		self.range_x = self.size[0]//self.item_size
		self.range_y = self.size[1]//self.item_size
		for j in range(self.range_x):
			for i in range(self.range_y):
				self.storage[(self.x_move + i,self.y_move + j)] = {'type':0,'pos':(self.x_move + i,self.y_move + j),'quantity':200,'variant':0}
	def rect(self):
		return pygame.Rect(self.x_move*self.item_size,self.y_move*self.item_size,self.size[1],self.size[0])
	def random_item(self):
		for j in range(self.range_x):
			for i in range(self.range_y):
				type_item = random.choice(test_storage)
				variant = 0
				if type_item in tool_item:
					t  = random.randint(0,3)
					variant = (t if t != 6 else 0)
				self.storage[(self.x_move + i,self.y_move + j)] = {'type':type_item,'pos':(self.x_move + i,self.y_move + j),'quantity':200,'variant':variant}
	def sorted_storage(self):
		type_item = set()
		item_quantity = {}
		for i in self.storage:
			if self.storage[i]['type'] in can_stack_item:
				item_ = self.storage[i]['type']
				type_item.add(item_)
		for i in type_item:
			item_quantity[i] = [0,False]
		for i in type_item:
			for j in self.storage:
				if self.storage[j]['type'] == i:
					item_quantity[i][0] += self.storage[j]['quantity']
					# self.storage[j]['quantity'] = 0
					self.storage[j]['type'] = 0

		for j in self.storage:
			for i,index in enumerate(item_quantity):
				if self.storage[j]['type'] == 0 and item_quantity[index][1] == False:
					self.storage[j]['type'] = list(item_quantity.keys())[i]
					self.storage[j]['quantity'] = list(item_quantity.values())[i][0]
					item_quantity[index][1] = True

	def add_item(self,item_type,variant):
		have = False
		for i in self.storage:
			if self.storage[i]['type'] == item_type and self.storage[i]['variant'] == variant:
				self.storage[i]['quantity'] += 1
				have = True
		for i in self.storage:
			if self.storage[i]['type'] == 0 and have == False:
				self.storage[i]['type'] = item_type
				self.storage[i]['variant'] = variant
				self.storage[i]['quantity'] = 1
				break
			
	def replace_item(self,pos,event,surf):
		loc = (pos[0]//self.item_size,pos[1]//self.item_size)
		if loc in self.storage:
			if event.button == 1:
				item_type = self.storage[loc]
				if item_type['type'] != 0 and self.game.hold == None:
					self.game.hold = [item_type['type'],item_type['quantity'],item_type['variant']]
					item_type['type'] = 0
					item_type['quantity'] = 0
				else:
					if self.game.hold != None:
						if item_type['type'] == self.game.hold[0] and item_type['type'] in can_stack_item:
							item_type['quantity'] += self.game.hold[1]
							self.game.hold = None
						elif item_type['type'] == 0:
							item_type['type'] = self.game.hold[0]
							item_type['quantity'] = self.game.hold[1]
							item_type['variant'] = self.game.hold[2]

							self.game.hold = None
	def convert_size(self,img,ne):
		return pygame.transform.scale(img,(self.item_size - ne,self.item_size - ne))
	def render(self,surf):
		for i in self.storage:
			item = self.storage[i]
			item_quantity = item['quantity']
			# pygame.draw.rect(surf,'red',(item['pos'][0]*self.item_size,item['pos'][1]*self.item_size,self.item_size,self.item_size),1)
			surf.blit(self.convert_size(self.game.assets['box'][0],0),(item['pos'][0]*self.item_size,item['pos'][1]*self.item_size))
			if item['type'] != 0:
				surf.blit(self.convert_size(self.game.assets[item['type']][item['variant']],10),(item['pos'][0]*self.item_size + 5,item['pos'][1]*self.item_size + 5))
				self.game.draw_text(f'{item_quantity}',self.game.font,'white',surf,(item['pos'][0]*self.item_size + 5,item['pos'][1]*self.item_size + 5)) if item['type'] in can_stack_item else True
		if self.game.hold != None:
			mouse_pos = pygame.mouse.get_pos()
			item_image = self.convert_size(self.game.assets[self.game.hold[0]][self.game.hold[2]],10).copy()
			item_image.set_alpha(150)
			surf.blit(item_image,(mouse_pos[0]//2 - self.item_size//2,mouse_pos[1]//2 - self.item_size//2))
			self.game.draw_text(f'{self.game.hold[1]}',self.game.font,'white',surf,(mouse_pos[0]//2 - self.item_size//2,mouse_pos[1]//2 - self.item_size//2)) if self.game.hold[0] in can_stack_item else True

class Craft_table(Inventory):
	def __init__(self, game):
		super().__init__(game,(3,7),(60,60),30)
		self.storage[(6,7)] = {'type':0,'pos':(6,7),'quantity':20,'variant':0}
	# def craft_item(self,event):
		
	def render(self,surf):
		super().render(surf)
class Player_inventory(Inventory):
	def __init__(self,game):
		super().__init__(game,(3,3),(90,120),30)
		self.update = False
	def check_on(self):
		if self.update == False:
			self.update = True
		else:
			self.update = False
	def render(self,surf):
		# surf.blit(self.game.assets['box'][1],(self.x_move*self.item_size - 48,self.y_move*self.item_size -80))
		super().render(surf)
class Player_tool_bar(Inventory):
	def __init__(self,game):
		super().__init__(game,((game.monitorsize[0]//4 - 180//4)//30,(game.monitorsize[1]//2.15 - 30//4)//30),(30,180),30)
		self.hold_num = 0
		super().random_item()
	# def get_box(self,pos,event):
	# 	# loc = (pos[0]//self.item_size,pos[1]//self.item_size)
	# 	if event.unicode in ['1','2','3','4','5','6']:
	# 		self.hold_num =  int(event.unicode) - 1
	# 	for i,loc in enumerate(self.storage):
	# 		if i == self.hold_num:
	# 			return self.storage[loc]
	def get_box(self,pos,event):
		check_loc = (pos[0]//self.item_size,pos[1]//self.item_size)
		for i,loc in enumerate(self.storage):
			if check_loc == loc:
				if event.button == 1:
					self.hold_num = i
		for i,loc in enumerate(self.storage):
			if i == self.hold_num:
				return self.storage[loc]		
		
	def render(self,surf):
		super().render(surf)
		for i,loc in enumerate(self.storage):
			if i == self.hold_num:
				item = self.storage[loc]
				surf.blit(self.game.assets['box'][2],(item['pos'][0]*self.item_size,item['pos'][1]*self.item_size))

class Chest_inventory(Inventory):
	def __init__(self,game):
		super().__init__(game,[(game.monitorsize[0]//4 - 180//4)//30,3],[90,180],30)
		# super().random_item()
	def render(self,surf):
		super().render(surf)
		
class Physical_Entity():
	def __init__(self,game,type_e,pos,size,hp):
		self.type_e = type_e
		self.game = game 
		self.pos = pos
		self.size = size
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
	def render(self,surf,offset,object_to_draw):
		object_to_draw.append([pygame.transform.flip(self.animation.img(),self.flip,False),pygame.Rect(self.rect().x,self.rect().y - self.animation.img().get_width()//1.31,self.animation.img().get_width(),self.animation.img().get_height())])

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
		object_to_draw.append([pygame.transform.flip(self.animation.img(),self.flip,False),pygame.Rect(self.rect().x,self.rect().y - 24,self.animation.img().get_width(),self.animation.img().get_height())])

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
						self.weapon.charge = 20
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
		object_to_draw.append([pygame.transform.flip(self.animation.img(),self.flip,False),pygame.Rect(self.rect().x,self.rect().y - 24,self.animation.img().get_width(),self.animation.img().get_height())])

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
		object_to_draw.append([self.convert_size(self.game.assets[self.type_e[0]][self.type_e[1]]),
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
		self.drop_item = ('item',0)
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
		self.drop_item = (self.type_t,0)
	def rect(self):
		return pygame.Rect(self.pos[0],self.pos[1] - self.game.tile_map.tile_size,self.image.get_width(),self.image.get_height())
	def drop_item_type(self, id, item_class):
		item = item_class(self.game,id,[self.pos[0] + 4,self.pos[1]],[16,16])
		item.move = 0
		self.game.item_group.append(item)
	def render(self,surf,object_to_draw):
		self.alive = False
		super().render(surf,object_to_draw)
