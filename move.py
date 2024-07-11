from random import choice as randomness
def move(self, data):

	####### Starting Variables #########
	shout, turn, test = '', data['turn']+1, ''
	up, down, left, right = 'up', 'down', 'left', 'right'
	directionlist = [up, down, left, right]

	####### Choosing Stuffs #######
	death, risky, totesOk = [],[],[]

	def newDeath(movement):	
		if movement not in death: death.append(movement)

	def newRisky(movement):
		if movement not in death: 
			if movement not in risky: risky.append(movement)

	def newTotesOk(movement):
		if movement not in death:
			if movement not in risky:
				if movement not in totesOk: totesOk.append(movement)

	###### Board ######
	headX, headY = data['you']['head']['x'], data['you']['head']['y']
	maxX, minX = data['board']['width']-1,0
	maxY, minY = data['board']['height']-1,0
	#hazardlist = data['hazards']

	###### Finding Immediate Dangers #######
	mybodylist, othersnakeslist = data['you']['body'], data['board']['snakes']
	#for snake in othersnakeslist:
		#if snake["name"] == "Stuffadids":
			#othersnakeslist.pop(othersnakeslist.index(snake))
	with open('teststuff.txt','a') as yeet:
		for snake in othersnakeslist:
			yeet.write(str(snake["name"])+'\n')
	
	if headY == minY: # bottom wall
		newDeath(down)
	if headX == minX: # left wall
		newDeath(left)
	if headY == maxY: # top wall
		newDeath(up)
	if headX == maxX: # right wall
		newDeath(right)

	def moveadids(thingX, thingY, daListFunction):
		if thingY==headY+1 and thingX==headX: # above
			daListFunction(up)
		elif thingY==headY-1 and thingX==headX: # below
			daListFunction(down)
		elif thingX==headX+1 and thingY==headY: # right
			daListFunction(right)
		elif thingX==headX-1 and thingY==headY: # left
			daListFunction(left) 

	for piece in mybodylist:		### My body
		moveadids(piece['x'], piece['y'], newDeath)
		
	for snake in othersnakeslist:		### Other Snakes
		for part in snake['body']:		# bodys
			moveadids(part['x'], part['y'], newDeath)
			
		enemyX, enemyY = snake['head']['x'], snake['head']['y']
		moveadids(enemyX, enemyY, newDeath)
		enemyHeadBox = [
			{'x':enemyX,'y':enemyY+1},
			{'x':enemyX,'y':enemyY-1},
			{'x':enemyX+1,'y':enemyY},
			{'x':enemyX-1,'y':enemyY}, ]
		for box in enemyHeadBox:
			moveadids(box['x'], box['y'], newRisky)

	####### Determine Food Importance #######
	health, foodlist = data['you']['health'], data['board']['food']

		### Need Food ###
	if health <= 50:
		shout = 'me dying'

		foodInfo = {}
		for food in foodlist:

			if food['x'] < headX:					# food to left
				horizontal = headX - food['x'], left
			elif food['x'] > headX:				# food to right
				horizontal = food['x'] - headX, right
			elif food['x'] == headX:			# food same level
				if food['y'] < headY:
					vertical = headY - food['y'], down
					horizontal = 0, down
				else: 
					vertical = headY - food['y'], up
					horizontal = 0, up

			if food['y'] < headY:					# food below
				vertical = headY - food['y'], down
			elif food['y'] > headY:				# food above
				vertical = food['y'] - headY, up
			elif food['y'] == headY:
				if food['x'] < headX:
					horizontal = food['x'] - headX, left
					vertical = 0, left
				else: 
					horizontal = food['x'] - headX, right
					vertical = 0, right
			foodInfo[horizontal[0]+vertical[0]] = horizontal[1], vertical[1]
		
		for food in sorted(foodInfo):
			if foodInfo[food][0] in death:
				if foodInfo[food][1] not in death:
					newTotesOk(foodInfo[food][1])
			else:
				newTotesOk(foodInfo[food][0])

	### Avoid Food ###
	else:
		for food in foodlist:
			moveadids(food['x'], food['y'], newRisky)

########### Finishing Touch ############
	if totesOk:
		move = randomness(totesOk)

	else: 
		for movement in directionlist:
			if movement not in death: 
				if movement not in risky: newTotesOk(movement)

		if totesOk:
			move = randomness(totesOk)
		else:
			move = randomness(risky)

	test += '---'+str(death)+" | "+str(risky)+' | '+str(totesOk)+"---"
	########## Gameplay Text File ##########
	with open('gameplay.txt', 'a') as file:
		file.write(
			str(turn)+'\t\t\t'+
			str(move)+'\t\t\t'+
			str(shout)+'\t\t\t'+
			str(test)+'\n')

	########## End ###########
	return {'move':move, 'shout':str(shout)}