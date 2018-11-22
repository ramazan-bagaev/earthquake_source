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
	text = get_initial()
	text += get_correctors(param)
	text += get_end()
	return text


def get_initial():
	text = "verbose = true\n"
	text += "dt = 0.00125\n"
	text += "steps = 501\n"
	text += "[global]\n"
	text += "	[mpi]\n"
	text += "		name = RectMPIGrid\n"
	text += "		dims = 0, 0, 1\n"
	text += "	[/mpi]\n"
	text += "[/global]\n"
	text += "[grids]\n"
	text += "	[grid]\n"
	text += "		id = crystalline_basement\n"
	text += "		[node]\n"
	text += "			name = ElasticMetaNode3D\n"
	text += "		[/node]\n"
	text += "		[material_node]\n"
	text += "		[/material_node]\n"
	text += "		[material]\n"
	text += "			c1 = 4000\n"
	text += "			c2 = 2500\n"
	text += "			rho = 2500\n"
	text += "		[/material]\n"
	text += "		[factory]\n"
	text += "			name = RectGridFactory\n"
	text += "			size = 200, 200, 200\n"
	text += "			origin = -2000, -2000, -1500\n"
	text += "			spacing = 5, 5, 5\n"
	text += "		[/factory]\n"
	text += "		[schema]\n"
	text += "			name = ElasticRectSchema3DRusanov3\n"
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
	text += "					time_to = 0.020\n"
	text += "					[region]\n"
	text += "						name = CircleRegion\n"
	text += "						center = " + str(pos['x']) + ", " + str(pos['y']) + ", " + str(pos['z']) + "\n"
	text += "						r = " + str(r) + "\n"
	text += "					[/region]\n"
	text += "					[impulse]\n"
	text += "						name = SinImpulse\n"
	text += "						periods = 0.080\n"
	text += "					[/impulse]\n"
	text += "				[/function]\n"
	text += "			[/corrector]\n"
	return text

def get_end():
	text = "	[/grid]\n"
	text += "[/grids]\n"
	text += "[contacts]\n"
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
	text += "[/initials]\n"
	text += "[savers]\n"
	text += "	[saver]\n"
	text += "		name = StructuredVTKSaver\n"
	text += "		path = ./vtk-frankel/%g_%s.vtk\n"
	text += "		order = 0\n"
	text += "		save = 50\n"
	text += "		params = v\n"
	text += "		norms = 1\n"
	text += "	[/saver]\n"
	text += "[/savers]\n"
	return text


n = {}
d = {}
center = {}
param = {}

n['x'] = float(sys.argv[1])
n['y'] = float(sys.argv[2])
n['z'] = float(sys.argv[3])

d['x'] = float(sys.argv[4])
d['y'] = float(sys.argv[5])
d['z'] = float(sys.argv[6])

center['x'] = int(sys.argv[7])
center['y'] = int(sys.argv[8])
center['z'] = int(sys.argv[9])

param['center'] = center

param['step'] = int(sys.argv[10])
step = param['step']

M0 = 100000000000/2*17

koef = M0/(2*step*step*step*step)

param['mxx'] = koef*2*n['x']*d['x']
param['myy'] = koef*2*n['y']*d['y']
param['mzz'] = koef*2*n['z']*d['z']
param['mxy'] = koef*(n['x']*d['y'] + n['y']*d['x'])
param['mxz'] = koef*(n['x']*d['z'] + n['z']*d['x'])
param['myz'] = koef*(n['y']*d['z'] + n['z']*d['y'])

file = open("../conf/conf", 'w')

file.write(get_config(param))
