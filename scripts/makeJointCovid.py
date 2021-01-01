
PD = 0.05
PS_D = 1 - 0.3
PS_ND = 1- 0.03

PF_NONE_D = 0.4
PF_LOW_D = 0.3
PF_HIGH_D = 0.3

PF_NONE_ND = 0.85
PF_LOW_ND = 0.10
PF_HIGH_ND = 0.05

def main():
	joint('none',0,1)
	joint('none',1,1)
	joint('low',0,1)
	joint('low',1,1)
	joint('high',0,1)
	joint('high',1,1)

def joint(f, s, d):
	p = 1
	if(d == 0):
		p = joint_d0(f, s)
	else:
		p = joint_d1(f, s)
	print(f,s,d,p)   

def joint_d0(f, s):
	p = 1 - PD
	# smell
	if(s == 1):
		p *= PS_ND
	else:
		p *= 1- PS_ND
	# fever
	if(f == 'none'):
		p *= PF_NONE_ND
	elif(f == 'low'):
		p *= PF_LOW_ND
	else:
		p *= PF_HIGH_ND
	return p

def joint_d1(f, s):
	p = PD
	# smell
	if(s == 1):
		p *= PS_D
	else:
		p *= 1- PS_D
	# fever
	if(f == 'none'):
		p *= PF_NONE_D
	elif(f == 'low'):
		p *= PF_LOW_D
	else:
		p *= PF_HIGH_D
	return p


if __name__ == '__main__':
	main()