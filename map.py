class mmap():
	def __init__(self, width, height):
		self.width=width
		self.height=height
		self.arr=[[0]*self.height for i in range(self.width)]
	def get(self, mapLocation):
		if self.is_on_planet(Earth):
			return self.arr[mapLocation.x][mapLocation.y]
	def set(self, mapLocation, val):
		self.arr[mapLocation.x][mapLocation.y]=val
	def printout(self):
		print("printing map: ")
		for y in range(self.height):
			buildstr=''
			for x in range(self.width):
				buildstr+=format(self.arr[x][self.height-1-y], '2d')
				print(buildstr)


if gc.planet() == bc.Planet.Earth:
	gc.queue_research(bc.UnitType.Worker)
	gc.queue_research(bc.UnitType.Worker)
	gc.queue_research(bc.UnitType.Mage)
	oneLoc = gc.my_units()[0].location.map_location()
	earthMap = gc.starting_map(bc.Planet.Earth)
	enemyStart = invert(oneLoc);
	print('worker starts at '+locToStr(oneLoc))
	print('enemy worker presumably at '+locToStr(enemyStart))

	passableMap = mmap(earthMap.width, earthMap.height)
	kMap = mmap(earthMap.width, earthMap.height)
	for x in range(earthMap.width):
		for y in range(earthMap.height):
			m1 = bc.MapLocation(bc.Planet.Earth, x, y)
			passableMap.set(m1, earthMap.is_passable_terrain_at(m1))
			kMap.set(m1, earthMap.initial_karbonite_at(m1))
	passableMap.printout()
	kMap.printout()
