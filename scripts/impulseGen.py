import sys
import math

f = open('impulse.conf', 'w')
begin = 0
end = 48
beginExp = 0
endExp = 3
m = 1.5
sigma = 0.25
delta = 0.012
cur = begin
while cur <= end:
	if cur > endExp:
		f.write('0\n')
	else:
		f.write(str(math.exp(-(cur - m)*(cur - m)/sigma)))
		f.write('\n')
	cur += delta