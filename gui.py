import pygame

TILE_SIZE = 20

def draw_lines(screen, height, width):
    for i in range(0, height):
        pygame.draw.line(screen, [255, 255, 255], [0, i * TILE_SIZE], [width * TILE_SIZE, i * TILE_SIZE], 1)
    for i in range(0, width):
        pygame.draw.line(screen, [255, 255, 255], [i * TILE_SIZE, 0], [i * TILE_SIZE, height * TILE_SIZE], 1)
    pygame.display.flip()
def dist2(start,end):
	return (end[0]-start[0])**2+(end[1]-start[1])**2
def lineInd(start,end):
	currentPoint=start
	ptlist=[currentPoint]
	while(currentPoint!=end):
		closestDist=1000000
		for n in orthoNeighbors(currentPoint):
			ndist2=dist2(n,end)
			if ndist2<closestDist:
				closestDist=ndist2
				closestn=n
		currentPoint=closestn
		ptlist.append(currentPoint)
	return ptlist
def orthoNeighbors(pt):
	return [(pt[0]-1,pt[1]),(pt[0]+1,pt[1]),(pt[0],pt[1]-1),(pt[0],pt[1]+1)]
def getIndices(pt):
	return ((pt[0])//TILE_SIZE,(pt[1])//TILE_SIZE)

def create_pygame_earth_editor(h,w,windowname):
	global terrain,karbonite,robot_positions
	global height,width
	height=h
	width=w
	terrain = [[True for _ in range(height)] for _ in range(width)]
	karbonite = [[0 for _ in range(height)] for _ in range(width)]
	robot_positions = []
	pygame.init()
	screen = pygame.display.set_mode([width * TILE_SIZE, height * TILE_SIZE])
	pygame.display.set_caption(windowname)
	clock = pygame.time.Clock()
	prevPress=None
	try:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					raise StopIteration
			press=pygame.mouse.get_pressed()
			pressInd=getIndices(pygame.mouse.get_pos())
			keys=pygame.key.get_pressed()
			if press[0] or press[2]:
				if prevPress==None:
					processClick(press,pressInd,keys)
				else:
					for ind in lineInd(pressInd,prevPress): 
						processClick(press,ind,keys)
				prevPress=pressInd
			else:
				prevPress=None
			render(screen)
			pygame.display.flip()
			clock.tick(60)
	except StopIteration:
		pygame.quit()
		return rotateData()

def rotateData():
	global terrain,karbonite,robot_positions
	global height,width
	terrain2 = [[True for _ in range(width)] for _ in range(height)]
	karbonite2 = [[0 for _ in range(width)] for _ in range(height)]
	for x in range(width):
		for y in range(height):
			terrain2[y][x]=terrain[x][y]
			karbonite2[y][x]=karbonite[x][y]
	for i in range(len(robot_positions)):
		pos=robot_positions[i]
		print(str(pos))
		robot_positions[i]=[height-pos[1]-1,pos[0],pos[2]]
	print('----')
	for pos in robot_positions:print(str(pos))
	return terrain2, karbonite2, robot_positions
			
def render(screen):
	global terrain,karbonite,robot_positions,height,width
	#terrain map:
	for x in range(width):
		for y in range(height):
			if terrain[x][y]: color=[100, 255, 100]
			else: color=[100,100,255]
			pygame.draw.rect(screen, color, [x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE,TILE_SIZE], 0)
			#karbonite map
			if terrain[x][y]:
				color=(100,255-5*karbonite[x][y],100)
				pygame.draw.rect(screen, color, [x * TILE_SIZE+2, y * TILE_SIZE+2, TILE_SIZE-4,TILE_SIZE-4], 0)
	for pos in robot_positions:
		if pos[2]==0:color=[0,0,255]
		else:color=[255,0,0]
		pygame.draw.circle(screen, color, [pos[0] * TILE_SIZE+TILE_SIZE//2, pos[1] * TILE_SIZE+TILE_SIZE//2], TILE_SIZE//2)

def invertLoc(loc):
	global height,width
	return (width-loc[0]-1,height-loc[1]-1)

def karboniteKey(keys):
	if keys[pygame.K_0]:return True, 0
	if keys[pygame.K_1]:return True, 5
	if keys[pygame.K_2]:return True, 10
	if keys[pygame.K_3]:return True, 15
	if keys[pygame.K_4]:return True, 20
	if keys[pygame.K_5]:return True, 25
	if keys[pygame.K_6]:return True, 30
	if keys[pygame.K_7]:return True, 35
	if keys[pygame.K_8]:return True, 40
	if keys[pygame.K_9]:return True, 45
	return False, 0

def processClick(press,pressInd,keys):
	if press[0]:#lmb
		layKarbonite, amt = karboniteKey(keys)
		delete_robot_at(pressInd)
		delete_robot_at(invertLoc(pressInd))
		if layKarbonite:
			set_karbonite(pressInd,amt)
			set_karbonite(invertLoc(pressInd),amt)
		elif keys[pygame.K_w]:#place a worker
			make_robot_at(pressInd,0)
			make_robot_at(invertLoc(pressInd),1)
		else:
			set_terrain(pressInd,False)
			set_terrain(invertLoc(pressInd),False)
	elif press[2]:#rmb
		set_terrain(pressInd,True)
		set_terrain(invertLoc(pressInd),True)

def make_robot_at(loc,team):
	global robot_positions
	robot_positions.append([loc[0],loc[1],team])

def delete_robot_at(loc):
	global robot_positions
	for i in range(len(robot_positions)):
		pos=robot_positions[i]
		if loc[0]==pos[0] and loc[1]==pos[1]:
			del robot_positions[i]
			break

def set_karbonite(loc,val):
	global terrain,karbonite
	if terrain[loc[0]][loc[1]]:#only place karbonite on passable locations
		karbonite[loc[0]][loc[1]]=val
		
def set_terrain(loc,val):
	global terrain,karbonite,robot_positions
	terrain[loc[0]][loc[1]]=val
	karbonite[loc[0]][loc[1]]=0#painting terrain erases karbonite