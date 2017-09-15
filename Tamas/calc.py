import math
a=0.1
b=1.5
gamma = 100
diffConstU = 1e-14
diffConstV = 1e-13
Length = 500e-06
k2=(diffConstU/Length**2)*gamma
orderv = 1
orderV = 0.1
k3=k2*(orderv/orderV)**2
k1=(k2*a)/math.sqrt(k3/k2)
k4=(k2*b)/math.sqrt(k3/k2)
print 'a',a,'b',b,'k1',k1,'k2',k2,'k3',k3,'k4',k4
