import sys
import math

def get_shift_pos(pos, dir, step):
	newPos = {}
	newPos['x'] = pos['x']
	newPos['y'] = pos['y']
	newPos['z'] = pos['z']
	if dir == 'x':
		newPos['x'] += step
	if dir == 'y':
		newPos['y'] += step
	if dir == 'z':
		newPos['z'] += step
	return newPos

def get_config(param):
	text = get_initial(param)
	text += get_end()
	return text


def get_initial(param):
	text = "verbose = true\n"
	text += "dt = 0.012\n"
	text += "steps = 4001\n"
	text += get_grids(param)
	return text

def get_grids(param):
	size = {}
	size['x'] = 371
	size['y'] = 161
	size['z'] = 41
	origin = {}
	origin['x'] = 0
	origin['y'] = 0
	origin['z'] = 0
	text = "[grids]\n"
	text += get_grid("bottom", param, size, origin, 5000, 2900, 2600, True, False)
	size['z'] = 21
	origin['z'] = 4000
	text += get_grid("middle", param, size, origin, 3500, 2000, 2600, False, False)
	size['z'] = 11
	origin['z'] = 6000
	text += get_grid("top", param, size, origin, 1100, 600, 2000, False, True)
	text += "[/grids]\n"
	return text


def get_grid(id, param, size, origin, c1, c2, rho, isGridWithSource, isTop):
	text = "	[grid]\n"
	text += "		id = " + id + "\n"
	text += "		[node]\n"
	text += "			name = ElasticMetaNode3D\n"
	text += "		[/node]\n"
	text += "		[material_node]\n"
	text += "			name = ElasticMaterialMetaNode\n"
	text += "		[/material_node]\n"
	text += "		[material]\n"
	text += "			c1 = " + str(c1) + "\n" #"3500\n"
	text += "			c2 = " + str(c2) + "\n" #2000\n"
	text += "			rho = " + str(rho) + "\n" #2600\n"
	text += "		[/material]\n"
	text += "		[factory]\n"
	text += "			name = RectGridFactory\n"
	text += "			size = " + str(size['x']) + ", " + str(size['y']) + ", " + str(size['z']) + "\n" #" 371, 161, 71\n"
	text += "			origin = " + str(origin['x']) + ", " + str(origin['y']) + ", " + str(origin['z']) + "\n" #" 0, 0, 0\n"
	text += "			spacing = " +  str(param['step']) + ", " + str(param['step']) + ", " +  str(param['step']) + "\n"
	text += "		[/factory]\n"
	text += "		[schema]\n"
	text += "			name = ElasticMatRectSchema3DRusanov3\n"
	text += "		[/schema]\n"
	text += "		[fillers]\n"
	text += "			[filler]\n"
	text += "				name = RectNoReflectFiller\n"
	text += "				axis = 0\n"
	text += "				side = 0\n"
	text += "			[/filler]\n"
	text += "			[filler]\n"
	text += "				name = RectNoReflectFiller\n"
	text += "				axis = 0\n"
	text += "				side = 1\n"
	text += "			[/filler]\n"
	text += "			[filler]\n"
	text += "				name = RectNoReflectFiller\n"
	text += "				axis = 1\n"
	text += "				side = 0\n"
	text += "			[/filler]\n"
	text += "			[filler]\n"
	text += "				name = RectNoReflectFiller\n"
	text += "				axis = 1\n"
	text += "				side = 1\n"
	text += "			[/filler]\n"
	text += "			[filler]\n"
	text += "				name = RectNoReflectFiller\n"
	text += "				axis = 2\n"
	text += "				side = 0\n"
	text += "			[/filler]\n"
	text += "			[filler]\n"
	text += "				name = RectNoReflectFiller\n"
	text += "				axis = 2\n"
	text += "				side = 1\n"
	text += "			[/filler]\n"
	text += "		[/fillers]\n"
	if isGridWithSource:
		text += get_correctors(param)
	if isTop:
		text += get_correctors_boundary()


	text += "	[/grid]\n"
	return text



def get_correctors(param):
	text = "		[correctors]\n"

	mxx = param['mxx']
	myy = param['myy']
	mzz = param['mzz']
	mxy = param['mxy']
	mxz = param['mxz']
	myz = param['myz']
	step = param['step']
	center = param['center']
	r = float(step)/2

	fxp = {}
	fxp['x'] = mxx
	fxp['y'] = mxy
	fxp['z'] = mxz

	text += get_corrector(fxp, get_shift_pos(center, 'x', step), r)

	fxn = {}
	fxn['x'] = -mxx
	fxn['y'] = -mxy
	fxn['z'] = -mxz

	text += get_corrector(fxn, get_shift_pos(center, 'x', -step), r)

	fyp = {}
	fyp['x'] = mxy
	fyp['y'] = myy
	fyp['z'] = myz

	text += get_corrector(fyp, get_shift_pos(center, 'y', step), r)

	fyn = {}
	fyn['x'] = -mxy
	fyn['y'] = -myy
	fyn['z'] = -myz

	text += get_corrector(fyn, get_shift_pos(center, 'y', -step), r)

	fzp = {}
	fzp['x'] = mxz
	fzp['y'] = myz
	fzp['z'] = mzz

	text += get_corrector(fzp, get_shift_pos(center, 'z', step), r)

	fzn = {}
	fzn['x'] = -mxz
	fzn['y'] = -myz
	fzn['z'] = -mzz

	text += get_corrector(fzn, get_shift_pos(center, 'z', -step), r)
	text += "		[/correctors]\n"
	return text


def get_corrector(force, pos, r):
	text = "			[corrector]\n"
	text += "				name = RightSideForceCorrector3D\n"
	text += "				axis = 2\n"
	text += "				[function]\n"
	text += "					name = RIFunction\n"
	text += "					magnitude = " + str(force['x']) + ", " + str(force['y']) + ", " + str(force['z']) + "\n"
	text += "					time_from = 0\n"
	text += "					time_to = 3\n"
	text += "					[region]\n"
	text += "						name = CircleRegion\n"
	text += "						center = " + str(pos['x']) + ", " + str(pos['y']) + ", " + str(pos['z']) + "\n"
	text += "						r = " + str(r) + "\n"
	text += "					[/region]\n"
	text += "					[impulse]\n"
	text += "						name = FileImpulse\n"
	text += "						file_name = source_earthquake/conf/impulse.conf\n"
	text += "						points_number = 250\n"
	text += "					[/impulse]\n"
	text += "				[/function]\n"
	text += "			[/corrector]\n"
	return text

def get_correctors_boundary():
	text =	"		[correctors]\n"
	text += "			[corrector]\n"
	text += "				name = ForceRectElasticBoundary3D\n"
	text += "				axis = 2\n"
	text += "				side = 1\n"
	text += "			[/corrector]\n"	
	text += "		[/correctors]\n"
	return text

def get_end():
	text = "[contacts]\n"
	text += "	[contact]\n"
	text += "		name = GlueRectElasticContact3D\n"
	text += "		grid1 = bottom\n"
	text += "		grid2 = middle\n"
	text += "		axis1 = 2\n"
	text += "		side1 = 1\n"
	text += "		axis2 = 2\n"
	text += "		side2 = 0\n"
	text += "	[/contact]\n"
	text += "	[contact]\n"
	text += "		name = GlueRectElasticContact3D\n"
	text += "		grid1 = middle\n"
	text += "		grid2 = top\n"
	text += "		axis1 = 2\n"
	text += "		side1 = 1\n"
	text += "		axis2 = 2\n"
	text += "		side2 = 0\n"
	text += "	[/contact]\n"
	text += "[/contacts]\n"
	text += "[initials]\n"
#	[initial]
#		name = ElasticEarthquakeInitial3D
#		order = 0
#		strik_angle = 45
#		dip_angle = 45
#		rake_angle = 45
#		height = 50
#		widht = 150
#		length = 150
#		center = 0, 0, -1150
#		velocity_magnitude = 30
#		[impulse]
#			name = ConstImpulse
#		[/impulse]
#	[/initial]

	text += "[savers]\n"
	text += "	[saver]\n"
	text += "		name = SinglePointSaver\n"
	text += "		path = ./vtk-frankel/result_1.txt\n"
	text += "		order = 0\n"
	text += "		save = 1\n"
	text += "		params = vx, vy, vz\n"
	text += "		norms = 0, 0, 0\n"
	text += "		coord = 20000, 6000, 7000\n"
	text += "		eps = 75\n"
	text += "	[/saver]\n"
	text += "	[saver]\n"
	text += "		name = SinglePointSaver\n"
	text += "		path = ./vtk-frankel/result_s.txt\n"
	text += "		order = 0\n"
	text += "		save = 1\n"
	text += "		params = vx, vy, vz\n"
	text += "		norms = 0, 0, 0\n"
	text += "		coord = 14000, 7000, 7000\n"
	text += "		eps = 75\n"
	text += "	[/saver]\n"
	text += "[/savers]\n"

	return text


n = {}
d = {}
center = {}
param = {}

n['x'] = 0
n['y'] = -1
n['z'] = 0

d['x'] = 1
d['y'] = 0
d['z'] = 0

center['x'] = 2000
center['y'] = 14000
center['z'] = 1000

param['center'] = center

param['step'] = 100
step = param['step']

M0 = float(100000000000000*4/30)

koef = float(M0/(2*step*step*step))

param['mxx'] = koef*2*n['x']*d['x']
param['myy'] = koef*2*n['y']*d['y']
param['mzz'] = koef*2*n['z']*d['z']
param['mxy'] = koef*(n['x']*d['y'] + n['y']*d['x'])
param['mxz'] = koef*(n['x']*d['z'] + n['z']*d['x'])
param['myz'] = koef*(n['y']*d['z'] + n['z']*d['y'])

file = open("config", 'w')

file.write(get_config(param))
