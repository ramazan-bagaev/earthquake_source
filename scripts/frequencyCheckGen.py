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
	text += get_correctors(param)
	text += get_end(param)
	return text


def get_initial(param):
	text = "verbose = true\n"
	text += "dt = 0.012\n"
	text += "steps = 500\n"
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
	text += "			name = ElasticMaterialMetaNode\n"
	text += "		[/material_node]\n"
	text += "		[material]\n"
	text += "			c1 = 3500\n"
	text += "			c2 = 2000\n"
	text += "			rho = 2600\n"
	text += "		[/material]\n"
	text += "		[factory]\n"
	text += "			name = RectGridFactory\n"
	text += "			size = 100, 100, 200\n"
	text += "			origin = 0, 0, 0\n"
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
	#text += get_corrector_boundary()
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
	text += "					time_to = 1\n"
	text += "					[region]\n"
	text += "						name = CircleRegion\n"
	text += "						center = " + str(pos['x']) + ", " + str(pos['y']) + ", " + str(pos['z']) + "\n"
	text += "						r = " + str(r) + "\n"
	text += "					[/region]\n"
	text += "					[impulse]\n"
	text += "						name = FileImpulse\n"
	text += "						file_name = source_earthquake/conf/freqImp.conf\n"
	text += "						points_number = 84\n"
	text += "					[/impulse]\n"
	text += "				[/function]\n"
	text += "			[/corrector]\n"
	return text

def get_corrector_boundary():
	text = "			[corrector]\n"
	text += "				name = ForceRectElasticBoundary3D\n"
	text += "				axis = 2\n"
	text += "				side = 0\n"
	text += "			[/corrector]\n"	
	return text

def get_end(params):
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
	text += "		name = SinglePointSaver\n"
	text += "		path = ./vtk-frankel3/result.txt\n"
	text += "		order = 0\n"
	text += "		save = 1\n"
	text += "		params = vx, vy, vz\n"
	text += "		norms = 0, 0, 0\n"
	text += "		coord = " + str(50*params['step']) + ", " + str(50*params['step']) + ", " + str(150*params['step']) + "\n"
	text += "		eps = " + str(3*params['step']/4) + "\n"
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

param['step'] = float(sys.argv[10])
step = param['step']

M0 = float(100000000000)

koef = float(M0/(2*step*step*step))

param['mxx'] = koef*2*n['x']*d['x']
param['myy'] = koef*2*n['y']*d['y']
param['mzz'] = koef*2*n['z']*d['z']
param['mxy'] = koef*(n['x']*d['y'] + n['y']*d['x'])
param['mxz'] = koef*(n['x']*d['z'] + n['z']*d['x'])
param['myz'] = koef*(n['y']*d['z'] + n['z']*d['y'])

file = open("config", 'w')

file.write(get_config(param))
