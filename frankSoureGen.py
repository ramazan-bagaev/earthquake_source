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

koef = M0/(2*step*step*step)
mxx = koef*2*n['x']*d['x']
myy = koef*2*n['y']*d['y']
mzz = koef*2*n['z']*d['z']
mxy = koef*(n['x']*d['y'] + n['y']*d['x'])
mxz = koef*(n['x']*d['z'] + n['z']*d['x'])
myz = koef*(n['y']*d['z'] + n['z']*d['y'])

file = open("config", 'w')

fxp = {}
fxp['x'] = mxx
fxp['y'] = mxy
fxp['z'] = mxz

file.write(get_corrector(fxp, get_shift_pos(center, 'x', step), step/2))

fxn = {}
fxn['x'] = -mxx
fxn['y'] = -mxy
fxn['z'] = -mxz

file.write(get_corrector(fxn, get_shift_pos(center, 'x', -step), step/2))

fyp = {}
fyp['x'] = mxy
fyp['y'] = myy
fyp['z'] = myz

file.write(get_corrector(fyp, get_shift_pos(center, 'y', step), step/2))

fyn = {}
fyn['x'] = -mxy
fyn['y'] = -myy
fyn['z'] = -myz

file.write(get_corrector(fyn, get_shift_pos(center, 'y', -step), step/2))

fzp = {}
fzp['x'] = mxz
fzp['y'] = myz
fzp['z'] = mzz

file.write(get_corrector(fzp, get_shift_pos(center, 'z', step), step/2))

fzn = {}
fzn['x'] = -mxz
fzn['y'] = -myz
fzn['z'] = -mzz

file.write(get_corrector(fzn, get_shift_pos(center, 'z', -step), step/2))