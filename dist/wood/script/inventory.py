import pygame,random
from script.setting import no_stack_item,item_id,tool_item

test_storage =  ['wood_sword','wood_axe','spear','bow','wood_pickaxe'] #+ ['stone','water','fence','wood_slab','wood_wall','grass','fence_stake','sand','sand_stone','chest','wood_block']

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
			if self.storage[i]['type'] not in no_stack_item:
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
						if item_type['type'] == self.game.hold[0] and item_type['type'] not in no_stack_item:
							item_type['quantity'] += self.game.hold[1]
							self.game.hold = None
						elif item_type['type'] != self.game.hold[0] and item_type['type']!=0:
							tmp = {'type': item_type['type'],'quantity':item_type['quantity']}
							item_type['type'] = self.game.hold[0]
							item_type['quantity'] = self.game.hold[1]
							self.game.hold[0] = tmp['type']
							self.game.hold[1] = tmp['quantity']
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
				surf.blit(self.convert_size(self.game.assets['item'][item_id[item['type']]],10),(item['pos'][0]*self.item_size + 5,item['pos'][1]*self.item_size + 5))
				self.game.draw_text(f'{item_quantity}',self.game.font,'white',surf,(item['pos'][0]*self.item_size + 5,item['pos'][1]*self.item_size + 5)) if item['type'] not in no_stack_item else True
		if self.game.hold != None:
			mouse_pos = pygame.mouse.get_pos()
			item_image = self.convert_size(self.game.assets['item'][item_id[self.game.hold[0]]],10).copy()
			item_image.set_alpha(150)
			surf.blit(item_image,(mouse_pos[0]//2 - self.item_size//2,mouse_pos[1]//2 - self.item_size//2))
			self.game.draw_text(f'{self.game.hold[1]}',self.game.font,'white',surf,(mouse_pos[0]//2 - self.item_size//2,mouse_pos[1]//2 - self.item_size//2)) if self.game.hold[0] not in no_stack_item else True

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