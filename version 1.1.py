## Food class##
from tkinter import *
import math, random

class Food(object):
	# Model
	def __init__(self, cx, cy, r):
		self.cx = cx
		self.cy = cy
		self.r = r

	def __repr__(self):
		return 'food'

	# View
	def draw(self, canvas, color="green1"):
		canvas.create_oval(self.cx - self.r, self.cy - self.r,
						   self.cx + self.r, self.cy + self.r,
						   fill=color)

	# Controller
	# nothing yet
###################################################
# main framework repurposed from HW8 Asteroids game https://www.cs.cmu.edu/~112/notes/hw8.html
###################################################
## Creature class ##
class Creature(object):
	# Model
	def __init__(self, cx, cy, speed, health, fov):
		# A creature has a position and a current direction it faces
		self.cx = cx
		self.cy = cy
		self.speed = speed
		self.health = health
		self.r = health
		self.fov = fov
		self.direction = random.randint(0,359)

	# View
	def draw(self, canvas):
		# Draws a cool-looking triangle-ish shape
		if self.health > 100: health = 100
		else: health = self.health
		color = getCreatureColor(health)
		size = 10
		direction = math.radians(self.direction)
		angleChange = 2*math.pi/3
		numPoints = 3
		points = []
		for point in range(numPoints):
			points.append((self.cx + size*math.cos(direction + point*angleChange),
						   self.cy - size*math.sin(direction + point*angleChange)))
		points.insert(numPoints-1, (self.cx, self.cy))
		
		canvas.create_polygon(points, fill=color)


	def showFOV(self, canvas):
		canvas.create_oval(self.cx-self.fov, self.cy-self.fov, self.cx+self.fov,self.cy+self.fov, fill=None,outline='white')

	# Controller
	def rotate(self, numDegrees):
		self.direction = (self.direction + numDegrees) % 360

	def detectFood(self, foodList):
		foodInSight = []
		for food in foodList:
			#food = foodList[foodI]
			if distance(self.cx, self.cy, food.cx, food.cy) < self.fov + food.r:
				foodInSight.append(food)
			else:
				try: foodInSight.remove(food)
				except: pass
		try:
			foodInSight.sort(key = lambda food: distance(self.cx, self.cy, food.cx, food.cy))		
			food = foodInSight[0]
		except: return []
		foodAngle = math.atan2(self.cy-food.cy, food.cx-self.cx)
		foodAngle = math.degrees(foodAngle)%360
		deltaAngle = foodAngle - self.direction

		#self.direction = foodAngle
		#print(deltaAngle)
		#print(self.direction,foodAngle)

		if foodAngle > self.direction:
			if foodAngle - self.direction > 180:
				self.rotate(-2)
			elif foodAngle - self.direction < 180:
				self.rotate(2)
			return foodInSight
		elif foodAngle < self.direction:
			if self.direction - foodAngle > 180:
				self.rotate(2)
			elif self.direction - foodAngle < 180:
				self.rotate(-2)
			return foodInSight
		return []

	def move(self):
		self.rotate(random.randint(-1,1)/2)
		self.cx += math.cos(math.radians(self.direction))*self.speed
		self.cy -= math.sin(math.radians(self.direction))*self.speed

	def collidesWithFood(self, other):
		# Check if the creature and food overlap at all
		if(not isinstance(other, Food)): # Other must be an Food
			return False
		else:
			dist = ((other.cx - self.cx)**2 + (other.cy - self.cy)**2)**0.5
			return dist < other.r

	def collidesWithWallY(self, width, height):
		# Check if the food hits the wall or overlaps it at all
		return self.cy <= 0 or self.cy >= height

	def collidesWithWallX(self, width, height):
		# Check if the food hits the wall or overlaps it at all
		return self.cx <= 0 or self.cx >= width 

	# TODO: add code here
	def reactToWallHit(self, screenWidth, screenHeight):
		if self.collidesWithWallY(screenWidth, screenHeight):
			self.cx -= math.cos(math.radians(self.direction))*self.speed
			self.cy += math.sin(math.radians(self.direction))*self.speed
			self.direction = (360 - self.direction)%360
		elif self.collidesWithWallX(screenWidth, screenHeight):
			self.cx -= math.cos(math.radians(self.direction))*self.speed
			self.cy += math.sin(math.radians(self.direction))*self.speed
			self.direction = (180 - self.direction)%360

	def isOffscreen(self, width, height):
		# Check if the creature has moved fully offscreen
		return (self.cx <= 0 or self.cx >= width) or \
			   (self.cy <= 0 or self.cy >= height)

	def wrapAround(self, width, height):
		if self.isOffscreen(width, height):
			self.cx %= width
			self.cy %= height


#### Graphics Functions ####

from tkinter import *

def init(data):
	data.mode = "splashScreen"
	data.creatureList = []
	data.score = 0
	data.foodCount = 0
	# TODO: add code here
	data.shrinkFoodList = []
	data.explosiveFoodList = []
	data.foodList = []
	data.timerCount = 0
	data.rotateAngle = 15
	data.speed = 3
	data.health = 5
	data.sex = 3
	data.selection = 1
	data.firstTime = True
	data.tracking = {}
	data.showInfo = True
	
#############################
# copied from course website "mode demo": https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
############################
def mousePressed(event, data):
	if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
	elif (data.mode == "playGame"):   playGameMousePressed(event, data)
	elif (data.mode == "setting"):       settingMousePressed(event, data)

def keyPressed(event, data):
	if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
	elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
	elif (data.mode == "setting"):       settingKeyPressed(event, data)

def timerFired(data):
	if (data.mode == "splashScreen"): splashScreenTimerFired(data)
	elif (data.mode == "playGame"):   playGameTimerFired(data)
	elif (data.mode == "setting"):       settingTimerFired(data)

def redrawAll(canvas, data):
	if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
	elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
	elif (data.mode == "setting"):       settingRedrawAll(canvas, data)
#############################

def splashScreenMousePressed(event, data):
	pass

def splashScreenKeyPressed(event, data):
	data.mode = "setting"

def splashScreenTimerFired(data):
	pass

def splashScreenRedrawAll(canvas, data):
	canvas.create_rectangle(0,0,data.width,data.height,fill='black')
	canvas.create_text(data.width/2, data.height/2-20,
					   text="Evolution Game", font="Arial 44 bold", fill = 'white')
	canvas.create_text(data.width/2, data.height/2+20,
					   text="Press any key to play", font="Arial 20", fill = 'white')

#############################
#############################
def playGameKeyPressed(event, data):
	if event.keysym == "Right":
		for creature in data.creatureList:
			creature.rotate(-data.rotateAngle)
	elif event.keysym == "Left":
		for creature in data.creatureList:
			creature.rotate(data.rotateAngle)
	elif event.keysym == "q":
		init(data)
	elif event.keysym == "space":
		pass
	elif (event.keysym == 's'):
		data.mode = "setting"
	elif (event.keysym == 'h'):
		data.showInfo = not data.showInfo
	# TODO: add code here

def playGameTimerFired(data):
	if data.firstTime:
		spawnNewCreatures(data, data.width/2, data.height/2)
		for i in range(6):
			createNewFoods(data)
		data.firstTime = False
	# TODO: add code here
	if data.foodCount < 6: 
		createNewFoods(data)

	for creature in data.creatureList:
		if creature.health > 0: creature.health -= 0.4/data.health
		if creature.health > 300:
			creature.health -= 225
			spawnNewCreatures(data, creature.cx, creature.cy)
		creatureI = data.creatureList.index(creature)
		creature.wrapAround(data.width, data.height)
		#creature.reactToWallHit(data.width, data.height)
		data.tracking[creature] = creature.detectFood(data.foodList)
		creature.move()
	hitDetection(data)

	i = 0
	while i < len(data.creatureList):
		creature = data.creatureList[i]
		if creature.health <= 0:
			data.creatureList.remove(creature)
		else:
			i += 1
	if data.creatureList == []: init(data)


def playGameMousePressed(event, data):
	rLow, rHigh = 10, 40
	r = random.randint(rLow, rHigh)
	data.foodList.append(Food(event.x, event.y, r))
	data.foodCount += 1

def playGameRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
	for creature in data.creatureList:	
		creature.draw(canvas)
		if data.showInfo: creature.showFOV(canvas)
	# TODO: add code here
	canvas.create_text(data.width/2, data.height, anchor="s", fill="yellow",
					   font="Arial 24 bold", text="Food Eaten: " + str(data.score))
	for food in data.foodList:
		food.draw(canvas)

	if not data.showInfo: return
	for creature in data.creatureList:
		foodInSight = data.tracking.get(creature, None)
		if foodInSight != None and foodInSight != []: 
			food = foodInSight[0]
			cx, cy = creature.cx, creature.cy
			fx, fy = food.cx, food.cy
			canvas.create_line(cx, cy, fx, fy, fill='red')
'''
	#for food in data.foodList:
		#for creature in data.creatureList:
			#foodAngle = math.atan2(creature.cy-food.cy, food.cx-creature.cx)
			#canvas.create_text(500,500,text=str(180+math.degrees(foodAngle)),fill='white')
'''
#####################################################
#####################################################
def settingMousePressed(event, data):
	pass

def settingKeyPressed(event, data):
	if data.selection < 3 and event.keysym == "Right":
		data.selection += 1
	elif data.selection > 1 and event.keysym == "Left":
		data.selection -= 1
	elif event.keysym == "Up" and data.speed + data.health + data.sex < 13:
		if data.selection == 1: data.speed += 1
		elif data.selection == 2: data.health += 1
		elif data.selection == 3: data.sex += 1
	elif event.keysym == "Down":
		if data.selection == 1 and data.speed > 1: data.speed -= 1
		elif data.selection == 2 and data.health > 1: data.health -= 1
		elif data.selection == 3 and data.sex > 1: data.sex -= 1
	elif event.keysym == "space":
		data.mode = "playGame"

def settingTimerFired(data):
	pass

def settingRedrawAll(canvas, data):
	canvas.create_rectangle(0,0,data.width, data.height,fill='black')
	canvas.create_text(data.width/2, 40,
					   text="Settings", font="Arial 30 bold", fill='white')
	canvas.create_text(data.width/2, data.height-80,
					   text="Distribute the points wisely!", font="Arial 20",fill='white')
	canvas.create_text(data.width/2, data.height-55,
					   text="Make your creature unique", font="Arial 20",fill='white')
	canvas.create_text(data.width/2, data.height-30,
					   text="Press space bar to start simulation", font="Arial 20",fill='white')

	canvas.create_text(data.width/4, data.height/2 - 60,
					   text="Speed", font="Arial 30 bold",fill='white')
	canvas.create_text(data.width/4, data.height/2,
					   text=str(data.speed), font="Arial 40 bold",fill='white')

	canvas.create_text(data.width/2, data.height/2 - 60,
					   text="Health", font="Arial 30 bold",fill='white')
	canvas.create_text(data.width/2, data.height/2,
					   text=str(data.health), font="Arial 40 bold",fill='white')

	canvas.create_text(data.width*3/4, data.height/2 - 60,
					   text="Children", font="Arial 30 bold",fill='white')
	canvas.create_text(data.width*3/4, data.height/2,
					   text=str(data.sex), font="Arial 40 bold",fill='white')
	if data.selection == 1:
		x, y, r = data.width/4, data.height/2 - 30, 65
	elif data.selection == 2:
		x, y, r = data.width/2, data.height/2 - 30, 65
	elif data.selection == 3:
		x, y, r = data.width*3/4, data.height/2 - 30, 65

	canvas.create_rectangle(x-r,y-r,x+r,y+r, outline='white')
################################

# creates either a new regular food or a shrinking food with 50/50
# chance every 2 seconds
def spawnNewCreatures(data, cx, cy):
	for i in range(data.sex):
		data.creatureList.append(Creature(cx, cy, data.speed, 100, 200))

def createNewFoods(data):
	data.timerCount += 1
	if data.timerCount == 50:
		data.foodList.append(makeFood(data))
		data.foodCount += 1	
		data.timerCount = 0

def makeFood(data):
	# Generates a normal food heading in a random direction
	rLow, rHigh = 5, 10
	r = random.randint(rLow, rHigh)
	x = random.randint(r+1, data.width-r-1) 
	y = random.randint(r+1, data.height-r-1)
	return (Food(x, y, r))

# updates each creature's location

# detects whether any bullets hit any asteroids, if so destroy the
# corresponding asteroids and adds score
def hitDetection(data):
	## deals with creature and food collision##
	detectRegularCollision(data)

def detectRegularCollision(data):
	index = 0
	while index < len(data.foodList):
		hit = False
		food = data.foodList[index]
		for creature in data.creatureList:
			if creature.collidesWithFood(food):
				hit = True
				creature.health += 50
				data.foodCount -= 1
				data.score += 1
				creatureI = data.creatureList.index(creature) 
		if hit: data.foodList.remove(food)
		else: index += 1

def distance(a, b, c, d):
	return math.sqrt((a-c)**2 + (b-d)**2)
# repurposed from an earlier homework
def color(r, g, b):
	return "#%02x%02x%02x" % (r, g, b)

def getCreatureColor(health): 
	rgb = int(255 * health / 100)
	return color(rgb, rgb, rgb)

# run function copied fron HW8 starter file: https://www.cs.cmu.edu/~112/notes/hw8.html
def run(width=300, height=300):
	def redrawAllWrapper(canvas, data):
		canvas.delete(ALL)
		canvas.create_rectangle(0, 0, data.width, data.height,
								fill='white', width=0)
		redrawAll(canvas, data)
		canvas.update()

	def mousePressedWrapper(event, canvas, data):
		mousePressed(event, data)
		redrawAllWrapper(canvas, data)

	def keyPressedWrapper(event, canvas, data):
		keyPressed(event, data)
		redrawAllWrapper(canvas, data)

	def timerFiredWrapper(canvas, data):
		timerFired(data)
		redrawAllWrapper(canvas, data)
		# pause, then call timerFired again
		canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
	# Set up data and call init
	class Struct(object): pass
	data = Struct()
	data.width = width
	data.height = height
	data.timerDelay = 10 # milliseconds
	root = Tk()
	init(data)
	# create the root and the canvas
	canvas = Canvas(root, width=data.width, height=data.height)
	canvas.configure(bd=0, highlightthickness=0)
	canvas.pack()
	# set up events
	root.bind("<Button-1>", lambda event:
							mousePressedWrapper(event, canvas, data))
	root.bind("<Key>", lambda event:
							keyPressedWrapper(event, canvas, data))
	timerFiredWrapper(canvas, data)
	# and launch the app
	root.mainloop()  # blocks until window is closed
	print("bye!")

run(800, 800)
