import sys
import math

def get_shift_pos(pos, shift, step):
	newPos = {}
	newPos['x'] = pos['x'] + step * shift['x']
	newPos['y'] = pos['y'] + step * shift['y']
	newPos['z'] = pos['z'] + step * shift['z']
	return newPos

def get_corrector(force, pos, r):
	text = "[corrector]\n"
	text += "	name = RightSideForceCorrector3D\n"
	text += "	axis = 2\n"
	text += "	[function]\n"
	text += "		name = RIFunction\n"
	text += "		magnitude = " + str(force['x']) + ", " + str(force['y']) + ", " + str(force['z']) + "\n"
	text += "		time_from = 0\n"
	text += "		time_to = 0.045\n"
	text += "		[region]\n"
	text += "			name = CircleRegion\n"
	text += "			center = " + str(pos['x']) + ", " + str(pos['y']) + ", " + str(pos['z']) + "\n"
	text += "			r = " + str(r) + "\n"
	text += "		[/region]\n"
	text += "		[impulse]\n"
	text += "			name = Gauss2Impulse\n"
	text += "		[/impulse]\n"
	text += "	[/function]\n"
	text += "[/corrector]\n"
	return text


n = {}
d = {}
center = {}

n['x'] = float(sys.argv[1])
n['y'] = float(sys.argv[2])
n['z'] = float(sys.argv[3])

d['x'] = float(sys.argv[4])
d['y'] = float(sys.argv[5])
d['z'] = float(sys.argv[6])

center['x'] = float(sys.argv[7])
center['y'] = float(sys.argv[8])
center['z'] = float(sys.argv[9])

step = float(sys.argv[10])

M0 = 10000

koef = M0/(step*step*step)
mxx = koef*2*n['x']*d['x']
myy = koef*2*n['y']*d['y']
mzz = koef*2*n['z']*d['z']
mxy = koef*(n['x']*d['y'] + n['y']*d['x'])
mxz = koef*(n['x']*d['z'] + n['z']*d['x'])
myz = koef*(n['y']*d['z'] + n['z']*d['y'])

file = open("config", 'w')

## x direction

f = {}
f['x'] = mxx
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 0, 'z': 0}, step), step/2))

f = {}
f['x'] = -mxx
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 0, 'z': 0}, step), step/2))

f = {}
f['x'] = mxy/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 2, 'z': 0}, step), step/2))

f = {}
f['x'] = mxy/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 2, 'z': 0}, step), step/2))

f = {}
f['x'] = -mxy/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -1, 'y': -2, 'z': 0}, step), step/2))

f = {}
f['x'] = -mxy/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 1, 'y': -2, 'z': 0}, step), step/2))

f = {}
f['x'] = mxz/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 0, 'z': 2}, step), step/2))

f = {}
f['x'] = mxz/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 0, 'z': 2}, step), step/2))

f = {}
f['x'] = -mxz/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -1, 'y': 0, 'z': -2}, step), step/2))

f = {}
f['x'] = -mxz/4
f['y'] = 0
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 1, 'y': 0, 'z': -2}, step), step/2))

# y direction

f = {}
f['x'] = 0
f['y'] = myy
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 1	, 'z': 0}, step), step/2))

f = {}
f['x'] = 0
f['y'] = -myy
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -1	, 'z': 0}, step), step/2))

f = {}
f['x'] = 0
f['y'] = mxy/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 2, 'y': -1	, 'z': 0}, step), step/2))

f = {}
f['x'] = 0
f['y'] = mxy/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 2, 'y': 1	, 'z': 0}, step), step/2))


f = {}
f['x'] = 0
f['y'] = -mxy/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -2, 'y': -1	, 'z': 0}, step), step/2))

f = {}
f['x'] = 0
f['y'] = -mxy/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': -2, 'y': 1	, 'z': 0}, step), step/2))


f = {}
f['x'] = 0
f['y'] = myz/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -1	, 'z': 2}, step), step/2))

f = {}
f['x'] = 0
f['y'] = myz/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 1	, 'z': 2}, step), step/2))


f = {}
f['x'] = 0
f['y'] = myz/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -1	, 'z': -2}, step), step/2))

f = {}
f['x'] = 0
f['y'] = -myz/4
f['z'] = 0

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 1	, 'z': -2}, step), step/2))

# z direction

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = mzz

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 0	, 'z': 1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = -mzz

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 0	, 'z': -1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = mxz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': 2, 'y': 0	, 'z': -1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = mxz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': 2, 'y': 0	, 'z': 1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = -mxz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': -2, 'y': 0	, 'z': -1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = -mxz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': -2, 'y': 0	, 'z': 1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = myz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 2	, 'z': -1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = myz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': 2	, 'z': 1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = myz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -2	, 'z': -1}, step), step/2))

f = {}
f['x'] = 0
f['y'] = 0
f['z'] = -myz/4

file.write(get_corrector(f, get_shift_pos(center, {'x': 0, 'y': -2	, 'z': 1}, step), step/2))