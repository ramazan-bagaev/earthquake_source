import sys
import math

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

def get_shift_pos(pos, shift, step):
	newPos = {}
	newPos['x'] = pos['x'] + step * shift['x']
	newPos['y'] = pos['y'] + step * shift['y']
	newPos['z'] = pos['z'] + step * shift['z']
	return newPos

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

	## x direction

	f = {}
	f['x'] = mxx
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 0, 'z': 0}, step), r)

	f = {}
	f['x'] = -mxx
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 0, 'z': 0}, step), r)

	f = {}
	f['x'] = mxy/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 2, 'z': 0}, step), r)

	f = {}
	f['x'] = mxy/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 2, 'z': 0}, step), r)

	f = {}
	f['x'] = -mxy/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -1, 'y': -2, 'z': 0}, step), r)

	f = {}
	f['x'] = -mxy/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 1, 'y': -2, 'z': 0}, step), r)

	f = {}
	f['x'] = mxz/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 0, 'z': 2}, step), r)

	f = {}
	f['x'] = mxz/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 0, 'z': 2}, step), r)

	f = {}
	f['x'] = -mxz/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 0, 'z': -2}, step), r)

	f = {}
	f['x'] = -mxz/4
	f['y'] = 0
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 0, 'z': -2}, step), r)

	# y direction

	f = {}
	f['x'] = 0
	f['y'] = myy
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 1	, 'z': 0}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = -myy
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -1	, 'z': 0}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = mxy/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 2, 'y': -1	, 'z': 0}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = mxy/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 2, 'y': 1	, 'z': 0}, step), r)


	f = {}
	f['x'] = 0
	f['y'] = -mxy/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -2, 'y': -1	, 'z': 0}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = -mxy/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': -2, 'y': 1	, 'z': 0}, step), r)


	f = {}
	f['x'] = 0
	f['y'] = myz/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -1	, 'z': 2}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = myz/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 1	, 'z': 2}, step), r)


	f = {}
	f['x'] = 0
	f['y'] = -myz/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -1	, 'z': -2}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = -myz/4
	f['z'] = 0

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 1	, 'z': -2}, step), r)

	# z direction

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = mzz

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 0	, 'z': 1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = -mzz

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 0	, 'z': -1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = mxz/4

	text += get_corrector(f, get_shift_pos(center, {'x': 2, 'y': 0	, 'z': -1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = mxz/4

	text += get_corrector(f, get_shift_pos(center, {'x': 2, 'y': 0	, 'z': 1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = -mxz/4

	text += get_corrector(f, get_shift_pos(center, {'x': -2, 'y': 0	, 'z': -1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = -mxz/4

	text += get_corrector(f, get_shift_pos(center, {'x': -2, 'y': 0	, 'z': 1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = myz/4

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 2	, 'z': -1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = myz/4

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 2	, 'z': 1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = -myz/4

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -2	, 'z': -1}, step), r)

	f = {}
	f['x'] = 0
	f['y'] = 0
	f['z'] = -myz/4

	text += get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -2	, 'z': 1}, step), r)
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
	text += "					time_to = 0.045\n"
	text += "					[region]\n"
	text += "						name = CircleRegion\n"
	text += "						center = " + str(pos['x']) + ", " + str(pos['y']) + ", " + str(pos['z']) + "\n"
	text += "						r = " + str(r) + "\n"
	text += "					[/region]\n"
	text += "					[impulse]\n"
	text += "						name = Gauss2Impulse\n"
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

center['x'] = float(sys.argv[7])
center['y'] = float(sys.argv[8])
center['z'] = float(sys.argv[9])

param['center'] = center

param['step'] = float(sys.argv[10])
step = param['step']

M0 = 100000

koef = M0/(step*step*step)

param['mxx'] = koef*2*n['x']*d['x']
param['myy'] = koef*2*n['y']*d['y']
param['mzz'] = koef*2*n['z']*d['z']
param['mxy'] = koef*(n['x']*d['y'] + n['y']*d['x'])
param['mxz'] = koef*(n['x']*d['z'] + n['z']*d['x'])
param['myz'] = koef*(n['y']*d['z'] + n['z']*d['y'])

file = open("config", 'w')

file.write(get_config(param))
