## Food and its subclasses, ShrinkingFood and SplittingFood ##
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
	def draw(self, canvas, color="green"):
		canvas.create_oval(self.cx - self.r, self.cy - self.r,
						   self.cx + self.r, self.cy + self.r,
						   fill=color)

	def collidesWithWall(self, width, height):
		# Check if the food hits the wall or overlaps it at all
		return self.cx - self.r <= 0 or self.cx + self.r >= width or \
			self.cy - self.r <= 0 or self.cy + self.r >= height

	def reactToWallHit(self, screenWidth, screenHeight):
		if self.collidesWithWall(screenWidth, screenHeight):
			self.direction *= -1
	# Controller
	

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
		self.direction = random.randint(0,360)

	# View
	def draw(self, canvas):
		# Draws a cool-looking triangle-ish shape
		size = 20
		direction = math.radians(self.direction)
		angleChange = 2*math.pi/3
		numPoints = 3
		points = []
		for point in range(numPoints):
			points.append((self.cx + size*math.cos(direction + point*angleChange),
						   self.cy - size*math.sin(direction + point*angleChange)))
		points.insert(numPoints-1, (self.cx, self.cy))
		
		canvas.create_polygon(points, fill="white")

	# Controller
	def rotate(self, numDegrees):
		self.direction += numDegrees

	def detectFood(self, food):
		if distance(self.cx, self.cy, food.cx, food.cy) < self.fov + food.r:
			foodAngle = math.atan2(food.cy-self.cy, food.cx-self.cx)
			degrees = abs(math.radians(self.direction) - math.radians(self.direction))
			self.rotate(degrees)

	def move(self):
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
			self.direction *= -1
		elif self.collidesWithWallX(screenWidth, screenHeight):
			self.cx -= math.cos(math.radians(self.direction))*self.speed
			self.cy += math.sin(math.radians(self.direction))*self.speed
			self.direction = 180 - self.direction

	def isOffscreen(self, width, height):
		# Check if the creature has moved fully offscreen
		return (self.cx + self.r <= 0 or self.cx - self.r >= width) or \
			   (self.cy + self.r <= 0 or self.cy - self.r >= height)


#### Graphics Functions ####

from tkinter import *

def init(data):
	data.mode = "splashScreen"
	data.creatureList = []
	spawnNewCreatures(data, data.width/2, data.height/2)
	data.score = 0
	data.foodCount = 0
	# TODO: add code here
	data.shrinkFoodList = []
	data.explosiveFoodList = []
	data.foodList = []
	data.timerCount = 0
	data.rotateAngle = 15
#############################
def mousePressed(event, data):
	if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
	elif (data.mode == "playGame"):   playGameMousePressed(event, data)
	elif (data.mode == "help"):       helpMousePressed(event, data)

def keyPressed(event, data):
	if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
	elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
	elif (data.mode == "help"):       helpKeyPressed(event, data)

def timerFired(data):
	if (data.mode == "splashScreen"): splashScreenTimerFired(data)
	elif (data.mode == "playGame"):   playGameTimerFired(data)
	elif (data.mode == "help"):       helpTimerFired(data)

def redrawAll(canvas, data):
	if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
	elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
	elif (data.mode == "help"):       helpRedrawAll(canvas, data)
#############################

def splashScreenMousePressed(event, data):
	pass

def splashScreenKeyPressed(event, data):
	data.mode = "playGame"

def splashScreenTimerFired(data):
	pass

def splashScreenRedrawAll(canvas, data):
	canvas.create_rectangle(0,0,data.width,data.height,fill='black')
	canvas.create_text(data.width/2, data.height/2-20,
					   text="Evolution Game", font="Arial 40 bold", fill = 'white')
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
	elif (event.keysym == 'h'):
		data.mode = "help"
	# TODO: add code here

def playGameTimerFired(data):
	# TODO: add code here
	if data.foodCount < 10: 
		createNewFoods(data)

	for creature in data.creatureList:
		creature.reactToWallHit(data.width, data.height)
		creature.move()
		for food in data.foodList:
			creature.detectFood(food)
	hitDetection(data)


def playGameRedrawAll(canvas, data):
	canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
	for creature in data.creatureList:	
		creature.draw(canvas)
	# TODO: add code here
	canvas.create_text(data.width/2, data.height, anchor="s", fill="yellow",
					   font="Arial 24 bold", text="Score: " + str(data.score))
	for food in data.foodList:
		food.draw(canvas)
#####################################################
#####################################################
def helpMousePressed(event, data):
	pass

def helpKeyPressed(event, data):
	data.mode = "playGame"

def helpTimerFired(data):
	pass

def helpRedrawAll(canvas, data):
	canvas.create_text(data.width/2, data.height/2-40,
					   text="This is help mode!", font="Arial 26 bold")
	canvas.create_text(data.width/2, data.height/2-10,
					   text="How to play:", font="Arial 20")
	canvas.create_text(data.width/2, data.height/2+15,
					   text="Do nothing and score points!", font="Arial 20")
	canvas.create_text(data.width/2, data.height/2+40,
					   text="Press any key to keep playing!", font="Arial 20")
################################

# creates either a new regular food or a shrinking food with 50/50
# chance every 2 seconds
def spawnNewCreatures(data, cx, cy):
	for i in range(5):
		data.creatureList.append(Creature(cx, cy, 5, 100, 200))

def createNewFoods(data):
	data.timerCount += 1
	if data.timerCount == 10:
		data.foodList.append(makeFood(data))
		data.foodCount += 1	
		data.timerCount = 0

def makeFood(data):
	# Generates a normal food heading in a random direction
	rLow, rHigh = 10, 40
	r = random.randint(rLow, rHigh)
	x = random.randint(r+1, data.width-r-1) 
	y = random.randint(r+1, data.height-r-1)
	return (Food(x, y, r))


# moves all the asteroids on screen
def moveAllFoods(data):
	pass

# updates each creature's location

# detects whether any bullets hit any asteroids, if so destroy/shrink the
# corresponding asteroids and adds score
def hitDetection(data):
	## deals with the shrinking asteroids ##
	## deals with the regular asteroids ##
	detectRegularCollision(data)
	## deals with the explosive asteroids ##
	detectExplosiveCollision(data)



def detectRegularCollision(data):
	index = 0
	while index < len(data.foodList):
		hit = False
		food = data.foodList[index]
		for creature in data.creatureList:
			if creature.collidesWithFood(food):
				hit = True
				data.foodCount -= 1
				data.score += 1
		if hit: data.foodList.remove(food)
		else: index += 1
		

def detectExplosiveCollision(data):
		eIndex = 0
		while eIndex < len(data.explosiveFoodList):
			hit = False
			food = data.explosiveFoodList[eIndex]
			creatureIndex = 0
			while creatureIndex < len(data.creatureList):
				creature = data.creatureList[creatureIndex]
				if creature.collidesWithFood(food):
					hit = True
					data.creatureList.remove(creature)
					data.explosiveFoodList.remove(food)
					data.creatureList.extend(food.explode())
					data.score += 1
					break
				else: creatureIndex += 1
			if not hit: eIndex += 1

def distance(a, b, c, d):
	return math.sqrt((a-c)**2 + (b-d)**2)




def runFoods(width=300, height=300):
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

runFoods(800, 800)