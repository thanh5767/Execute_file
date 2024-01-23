import pygame,noise,random
AUTOTILES_RULE = {
	tuple():0,
	tuple(sorted([(1,0)])) : 1,
	tuple(sorted([(-1,0)])) :2,
	tuple(sorted([(-1,0),(1,0)])) :3,
	tuple(sorted([(0,1)])) :4,
	tuple(sorted([(0,-1)])) :5,
	tuple(sorted([(0,-1),(0,1)])) :6,
	tuple(sorted([(0,1),(1,0)])) :7,
	tuple(sorted([(0,1),(-1,0)])) :8,
	tuple(sorted([(0,-1),(1,0)])) :9,
	tuple(sorted([(0,-1),(-1,0)])) :10,
	tuple(sorted([(0,1),(-1,0),(1,0)])) :11,
	tuple(sorted([(0,-1),(-1,0),(1,0)])) :12,
	tuple(sorted([(0,-1),(0,1),(1,0)])) :13,
	tuple(sorted([(0,-1),(0,1),(-1,0)])) :14,
	tuple(sorted([(0,-1),(0,1),(-1,0),(1,0)])) :15,
}
NEIGHTBOUER_POINT = [(0,1),(0,-1),(1,0),(-1,0),(0,0),(-1,-1),(-1,1),(1,-1),(1,1)]
PHYSICAL_TILE = ['tree','stone','water','fence','wood_wall','rock','fence_stake','sand_stone','chest','wood_block','solid_stone','solid_water']
AUTOTILES_TYPES = ['stone','water','fence','wood_slab','wood_wall','fence_stake','sand_stone','wood_block','solid_stone','solid_water']
offgrid_tile = ['water','wood_slab','grass','sand','solid_dirt','solid_water']
light_tile = ['torch']
layer = {
	'grass':1,
	'sand':1,
	'wood_slab':2,
	'water':3,
	'solid_water':3,
	'stone':3,
	'fence':3,
	'fence_stake':3,
	'sand_stone':3,
	'wood_block':3,
	'chest':3,
	'rock':3,
	'wood_wall':3,
	'solid_stone':3,
	'reset':1,
}
object_hp = {
	'tree': 3,
	'stone':5,
	'flower':2,
	'water':5,
	'rock':4,
	'wood_slab':3,
	'reset':1,
	'chest':4,
}
class Tile_map():
	def __init__(self,game,tile_size):
		self.map_data = {}
		self.tile_size = tile_size
		self.game = game
		self.seed = 0
		self.modifier = 0.1
		self.auto = True
		self.offgrid = []
		self.chest_inventory = {}
		self.interact_tile = {}
	def generate_chunk(self, x, y):
		tile_type = 0
		variant = 0
		z = 3
		# Sử dụng Perlin Noise để tạo giá trị
		scale = 0.5  # Điều chỉnh scale để ảnh hưởng đến kích thước địa hình và rộng lớn của thế giới
		test_value = noise.pnoise2(
			x/self.tile_size*scale + self.seed,
			y/self.tile_size*scale + self.seed,
			octaves=1, persistence=0.5, lacunarity=2.0,
			# base=self.seed
		)
		water_noise = noise.pnoise2(x/self.tile_size*scale + 1 + self.seed, y/self.tile_size*scale + 1 + self.seed, base=self.seed)
		biom_noise = noise.pnoise2(x/self.tile_size*0.05 + self.seed, y/self.tile_size*0.05 + self.seed, base=self.seed)
		tree_noise = noise.pnoise2(x/self.tile_size*1.5 + self.seed, y * self.modifier + self.seed, base=random.randint(0, 100))
		flower_noise = noise.pnoise2(x * self.modifier + self.seed, y * self.modifier + self.seed, base=random.randint(0, 100))
		bush_noise = noise.pnoise2(x*0.1  + self.seed, y*0.1  + self.seed, base=self.seed)
		struct_noise = noise.pnoise2(x * self.modifier + self.seed, y * self.modifier + self.seed, base=random.randint(0, 100))
		if biom_noise > 0.2:
			if test_value > 0.2:
				tile_type = 'solid_stone'
			elif water_noise > 0.2:
				tile_type = 'solid_water'
			elif tree_noise > 0.5:
				tile_type = 'tree'
				variant = random.randint(2,3)
		else:
			if test_value > 0.2 and water_noise < 0.2:
				tile_type = 'stone'
			elif water_noise > 0.2:
				if water_noise > 0.3:
					tile_type = 'water'
			elif struct_noise > 0.7:
				self.place_struct([x + 1,y + 1])
			elif bush_noise > 0.5:
				tile_type = 'flower'
				variant = 2
			elif random.random() < 0.001:
				tile_type = 'rock'
			elif random.random() < 0.1:
				tile_type = 'flower'
				variant = random.randint(0, 4)
			elif tree_noise > 0.5:
				tile_type = 'tree'	
				variant = random.randint(0,2)
			
			# elif tree_noise <0.1:
			# 	self.place_struct((x,y))
			# tile_type = 'grass'
			# z= 2

		# elif random.random() < 0.01:
		# 	tile_type = 'stone'
		# 	for j,j_count in enumerate(house_shape):
		# 		for i,tile in enumerate(j_count):
		# 			self.map_data[str(x + i) + ';' + str(y + j)] = {'type':tile,'variant':0,'pos':(x + i,y +j)}
		return {'type':tile_type,'variant':variant,'pos':(x,y,z),'hp':object_hp[tile_type if tile_type in object_hp else 'reset']}
	def generate_chunk_base(self,x,y,z):
		variant = 0
		tile_type = 0
		z = 1
		scale = 0.5  # Điều chỉnh scale để ảnh hưởng đến kích thước địa hình và rộng lớn của thế giới
		test_value = noise.pnoise2(
			x/self.tile_size*scale + self.seed,
			y/self.tile_size*scale + self.seed,
			octaves=1, persistence=0.5, lacunarity=2.0,
			# base=self.seed
		)
		biom_noise = noise.pnoise2(x/self.tile_size*0.05 + self.seed, y/self.tile_size*0.05 + self.seed, base=self.seed)
		water_noise = noise.pnoise2(x/self.tile_size*scale + 1 + self.seed, y/self.tile_size*scale + 1 + self.seed, base=self.seed)

		if biom_noise > 0.2:
			tile_type = 'solid_dirt'
			variant = 0
			if water_noise > 0.6:
				variant = 0 
			elif water_noise > 0.55:
				variant = 1
		else:
			if test_value > -0.2 and water_noise < 0.2:
				tile_type = 'grass'
			else:
				tile_type = 'grass'
		return {'type':tile_type,'variant':variant,'pos':(x,y,z),'hp':object_hp[tile_type if tile_type in object_hp else 'reset']}
	def check_infor(self,pos):
		loc = (pos[0]//self.tile_size,pos[1]//self.tile_size)
		if loc in self.map_data:
			return (self.map_data[loc])

	def check_physical_tile(self,pos):
		tiles = []
		tile_loc = (int(pos[0]//self.tile_size),int(pos[1] // self.tile_size))
		for offset in NEIGHTBOUER_POINT:
			check_loc = (tile_loc[0] + offset[0],tile_loc[1] + offset[1],3)
			if check_loc in self.map_data:
				tiles.append(self.map_data[check_loc])
		return tiles
	def get_rect_tile(self,pos):
		rects = []
		for tile in self.check_physical_tile(pos):
			if tile['type'] in PHYSICAL_TILE:
				rects.append(pygame.Rect(tile['pos'][0] * self.tile_size,tile['pos'][1] * self.tile_size,self.tile_size,self.tile_size))
		return rects
	def auto_tile(self,pos):
		tile = self.map_data[pos]
		neighbors = set()
		for shift in [(-1,0),(1,0),(0,-1),(0,1)]:
			check_loc = (tile['pos'][0] + shift[0],tile['pos'][1] + shift[1],tile['pos'][2])
			if check_loc in self.map_data:
				if self.map_data[check_loc]['type'] == tile['type']:
					neighbors.add(shift)
		neighbors = tuple(sorted(neighbors))
		if (tile['type'] in AUTOTILES_TYPES) and (neighbors in AUTOTILES_RULE):
			tile['variant'] = AUTOTILES_RULE[neighbors]
	def place_block(self,pos,tile_type):
		num = self.check_layer(tile_type)
		check_loc = (int(pos[0]//self.tile_size),int(pos[1]//self.tile_size),num)
		if check_loc in self.map_data:
			if tile_type != 0:
				if self.map_data[check_loc]['type'] == 0:
					self.map_data[check_loc] = {'type':tile_type,'variant':0,'pos':(int(pos[0]//self.tile_size),int(pos[1]//self.tile_size),num),'hp': object_hp[tile_type if tile_type in object_hp else 'reset']}

			if tile_type == 0:
				if self.map_data[check_loc]['type'] != 0:
					self.map_data[check_loc] = {'type':0,'variant':0,'pos':(int(pos[0]//self.tile_size),int(pos[1]//self.tile_size),num),'hp': object_hp['reset']}
	def check_layer(self,tile_type):
		num = layer[tile_type if tile_type in layer else 'reset']
		return num
	def check_object(self,pos,object,direct):
		loc = (pos[0]//self.tile_size,pos[1]//self.tile_size,3)
		test = []
		if type(object) != tuple:
			for offset in [direct]:
				check_loc = (loc[0] + offset[0],loc[1] + offset[1],3)
				if check_loc in self.map_data:
					if self.map_data[check_loc]['type'] == object:
						test.append(self.map_data[check_loc])
		else:
			for offset in [direct]:
				check_loc = (loc[0] + offset[0],loc[1] + offset[1],3)
				if check_loc in self.map_data:
					if self.map_data[check_loc]['type'] in object:
						test.append(self.map_data[check_loc])
		return test
		

	def place_struct(self,pos):
		house_shape = [
		['stone','stone','stone','stone','stone','stone','stone'],
		['stone','chest','wood_slab','wood_slab','wood_slab','wood_slab','stone'],
		['stone','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','stone'],
		['stone','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','stone'],
		['stone','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','stone'],
		['stone','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','stone'],
		['stone','stone','stone','stone',0,0,'stone'],
		]
		barracks = [
		['fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake'],
		['fence_stake',0,0,0,0,0,0,0,0,0,'fence_stake'],
		['fence_stake',0,'wood_block','wood_block','wood_block','wood_block','wood_block','wood_block','wood_block',0,'fence_stake'],
		['fence_stake',0,'wood_block','chest','wood_slab','wood_slab','wood_slab','wood_slab','wood_block',0,'fence_stake'],
		['fence_stake',0,'wood_block','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','wood_block',0,'fence_stake'],
		['fence_stake',0,'wood_block','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','wood_block',0,'fence_stake'],
		['fence_stake',0,'wood_block','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','wood_block',0,'fence_stake'],
		['fence_stake',0,'wood_block','wood_slab','wood_slab','wood_slab','wood_slab','wood_slab','wood_block',0,'fence_stake'],
		['fence_stake',0,'wood_block','wood_block',0,'wood_block','wood_block','wood_block','wood_block',0,'fence_stake'],
		['fence_stake',0,0,0,0,0,0,0,0,0,'fence_stake'],
		['fence_stake','fence_stake','fence_stake','fence_stake',0,'fence_stake','fence_stake','fence_stake','fence_stake','fence_stake','fence_stake'],
		]
		x,y = pos
		tile_type = 'stone'
		random_struct = random.choice([barracks,house_shape])
		for j,j_count in enumerate(random_struct):
			for i,tile in enumerate(j_count):
				self.map_data[(x+i,y+j,layer[tile if tile in layer else 'reset' ])] = {'type':tile,'variant':0,'pos':(x + i,y +j,layer[tile if tile in layer else 'reset' ]),'hp':object_hp[tile if tile in object_hp else 'reset']}
	def check_solid(self,pos):
		check_loc = str(pos[0]//self.tile_size) +';' + str(pos[1]//self.tile_size)
		if check_loc in self.map_data:
			if self.map_data[check_loc]['type'] in PHYSICAL_TILE:
				return False
		return True
	def check_chest(self,pos,surf):
		loc = (pos[0]//self.tile_size,pos[1]//self.tile_size)
		for offset in [(0,-1),(0,1),(1,0),(-1,0)]:
			check_loc = (loc[0] + offset[0],loc[1] + offset[1],3)
			if check_loc in self.map_data:
				if self.map_data[check_loc]['type'] == 'chest':
					return check_loc
		return None
	def check_chest_use(self,pos):
		loc = (pos[0]//self.tile_size,pos[1]//self.tile_size,3)
		if loc in self.chest_inventory:
			if self.chest_inventory[loc]['used'] == False:
				self.chest_inventory[loc]['used'] = True
	def render(self, surf, offset, object_to_draw,invent):
		for x in range(offset[0] // self.tile_size - 1, (offset[0] + surf.get_width()) // self.tile_size + 2):
			for y in range(offset[1] // self.tile_size -1, (offset[1] + surf.get_height()) // self.tile_size + 3):
				for z in range(1,4):
					target_chunk = (x,y,z)
					if target_chunk not in self.map_data:
						if z == 1:
							self.map_data[target_chunk] = self.generate_chunk_base(x, y,z)
						elif z == 2:
							self.map_data[target_chunk] = {'type':0,'variant':0,'pos':(x,y,z),'hp':object_hp['reset']}
						elif z == 3:
							self.map_data[target_chunk] = self.generate_chunk(x, y)

					if target_chunk in self.map_data:
						tile = self.map_data[target_chunk]

						if tile['type'] != 0 and tile['type'] not in offgrid_tile and tile['type'] != 'tree' and target_chunk not in self.interact_tile:
							
							
							object_to_draw.append([self.game.assets[tile['type']][tile['variant']],
												pygame.Rect(tile['pos'][0] * self.tile_size,
															tile['pos'][1] * self.tile_size - self.tile_size,
															self.game.assets[tile['type']][tile['variant']].get_width(),
															self.game.assets[tile['type']][tile['variant']].get_height())])
							self.auto_tile(target_chunk)

						elif tile['type'] == 'tree' and target_chunk not in self.interact_tile:
							object_to_draw.append([self.game.assets[tile['type']][tile['variant']],
												   pygame.Rect(tile['pos'][0] * self.tile_size -
															   self.game.assets[tile['type']][tile['variant']].get_width() // 7,
															   tile['pos'][1] * self.tile_size - self.tile_size * 2,
															   self.game.assets[tile['type']][tile['variant']].get_width(),
															   self.game.assets[tile['type']][tile['variant']].get_height())])

						elif tile['type'] in offgrid_tile:
							surf.blit(self.game.assets[tile['type']][tile['variant']],
									  (tile['pos'][0] * self.tile_size - offset[0],
									   tile['pos'][1] * self.tile_size - offset[1]))
							self.auto_tile(target_chunk)

						elif tile['type'] in light_tile:
							self.game.daynight.display_surf.blit(self.game.assets['light'],
																 ((tile['pos'][0] * self.tile_size - offset[0] -
																   self.game.assets['light'].get_width() // 2 + 24,
																   tile['pos'][1] * self.tile_size - offset[1] -
																   self.game.assets['light'].get_height() // 2 + 24)),
																 special_flags=pygame.BLEND_RGB_ADD)
							
							
						if tile['type'] == 'chest':
							loc = (tile['pos'][0],tile['pos'][1],3)
							if  loc not in self.chest_inventory:
								self.chest_inventory[loc] = {'inventory': invent,'used':False}
						if tile['hp'] == 0:
							tile['type'] = 0
						
						loc = (tile['pos'][0],tile['pos'][1],3)
						if loc in self.map_data:
							if self.map_data[loc]['type'] == 0 and loc in self.chest_inventory:
								del self.chest_inventory[loc]
						# else:
						# 	pygame.draw.rect(surf,'white',(tile['pos'][0] * self.tile_size - offset[0],tile['pos'][1] * self.tile_size - offset[1],self.tile_size,self.tile_size),1)
