import battlecode as bc
import random
import sys
import traceback
import os

gc = bc.GameController()
directions = [bc.Direction.North, bc.Direction.Northeast, bc.Direction.East, bc.Direction.Southeast, bc.Direction.South, bc.Direction.Southwest, bc.Direction.West, bc.Direction.Northwest]
tryRotate = [0,-1,1,-2,2]
random.seed(6137)
my_team = gc.team()

def invert(loc):#assumes Earth
	newx = earthMap.width-loc.x
	newy = earthMap.height-loc.y
	return bc.MapLocation(bc.Planet.Earth,newx,newy)

def locToStr(loc):
	return '('+str(loc.x)+','+str(loc.y)+')'

if gc.planet() == bc.Planet.Earth:
	oneLoc = gc.my_units()[0].location.map_location()
	earthMap = gc.starting_map(bc.Planet.Earth)
	enemyStart = invert(oneLoc);
	print('worker starts at '+locToStr(oneLoc))
	print('enemy worker presumably at '+locToStr(enemyStart))

def rotate(dir,amount):
	ind = directions.index(dir)
	return directions[(ind+amount)%8]

def goto(unit,dest):
	d = unit.location.map_location().direction_to(dest)
	if gc.can_move(unit.id, d):
		gc.move_robot(unit.id,d)
		
def fuzzygoto(unit,dest):
	toward = unit.location.map_location().direction_to(dest)
	for tilt in tryRotate:
		d = rotate(toward,tilt)
		if gc.can_move(unit.id, d):
			gc.move_robot(unit.id,d)
			break

while True:
	try:
		#count things: unfinished buildings, workers
		numWorkers = 0
		blueprintLocation = None
		blueprintWaiting = False
		for unit in gc.my_units():
			if unit.unit_type== bc.UnitType.Factory:
				if not unit.structure_is_built():
					ml = unit.location.map_location()
					blueprintLocation = ml
					blueprintWaiting = True
			if unit.unit_type== bc.UnitType.Worker:
				numWorkers+=1
		
		for unit in gc.my_units():
			if unit.unit_type == bc.UnitType.Worker:
				d = random.choice(directions)
				if numWorkers<5 and gc.can_replicate(unit.id,d):
					gc.replicate(unit.id,d)
					continue
				if gc.karbonite() > bc.UnitType.Factory.blueprint_cost():#blueprint
					if gc.can_blueprint(unit.id, bc.UnitType.Factory, d):
						gc.blueprint(unit.id, bc.UnitType.Factory, d)
						continue
				adjacentUnits = gc.sense_nearby_units(unit.location.map_location(), 2)
				for adjacent in adjacentUnits:#build
					if gc.can_build(unit.id,adjacent.id):
						gc.build(unit.id,adjacent.id)
						continue
				#head toward blueprint location
				if blueprintWaiting:
					if gc.is_move_ready(unit.id):
						ml = unit.location.map_location()
						bdist = ml.distance_squared_to(blueprintLocation)
						if bdist>2:
							fuzzygoto(unit,blueprintLocation)
			
			if unit.unit_type == bc.UnitType.Factory:
				garrison = unit.structure_garrison()
				if len(garrison) > 0:#ungarrison
					d = random.choice(directions)
					if gc.can_unload(unit.id, d):
						gc.unload(unit.id, d)
						continue
				elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):#produce Knights
					gc.produce_robot(unit.id, bc.UnitType.Knight)
					continue
					
			if unit.unit_type == bc.UnitType.Knight:
				if unit.location.is_on_map():#can't move from inside a factory
					if gc.is_move_ready(unit.id):
						if gc.round()>50:
							fuzzygoto(unit,enemyStart)
					
			# attack
			# if other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
				# gc.attack(unit.id, other.id)
			
			# movement
			# elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
				# gc.move_robot(unit.id, d)

	except Exception as e:
		print('Error:', e)
		traceback.print_exc()

	# send the actions we've performed, and wait for our next turn.
	gc.next_turn()

	# these lines are not strictly necessary, but it helps make the logs make more sense.
	# it forces everything we've written this turn to be written to the manager.
	sys.stdout.flush()
	sys.stderr.flush()
