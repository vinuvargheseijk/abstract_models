import matplotlib.pyplot as plt
import numpy

loc=[100,150,200,250,300,350,400]
d1conc1p1=[13.4,12.6,0.0,14.1,17.6,11.4,11.1]
d1conc1p2=[39.8,39.7,0.0,36.8,39.9,38.6,37.2]
d1conc2p1=[14.7,17.9,11.5,14.1,16.4,0.0,10.5]
d1conc2p2=[40.5,42.2,34.3,37.0,39.3,0.0,36.0]
d1conc5p1=[15.9,0.0,11.7,13.9,16.0,18.6,9.6]
d1conc5p2=[41.2,0.0,35.0,37.2,39.4,41.9,34.5]
d1conc10p1=[17.3,8.8,11.4,13.6,15.8,18.1,0.0]
d1conc10p2=[42.0,32.7,35.3,37.4,39.7,42.1,0.0]


d3conc1p1=[11.1,12.1,0.0,0.0,19.9,11.7,10.6]
d3conc1p2=[38.8,39.5,0.0,0.0,42.7,39.4,35.9]
d3conc2p1=[16.5,11.5,10.4,12.9,16.4,0.0,10.2]
d3conc2p2=[41.1,39.8,34.2,38.5,40.5,0.0,35.4]
d3conc5p1=[18.2,8.7,11.2,13.0,14.7,17.5,9.5]
d3conc5p2=[42.1,33.3,36.5,38.3,40.0,42.3,34.3]
d3conc10p1=[0.0,9.3,10.9,12.8,14.7,17.1,7.9]
d3conc10p2=[0.0,34.8,36.6,38.4,40.3,42.4,31.9]

d5conc1p1=[12.1,12.1,12.2,12.1,12.1,11.8,12.6]
d5conc1p2=[39.2,39.2,39.4,39.2,39.2,39.3,40.2]
d5conc2p1=[11.5,11.6,12.0,12.2,19.9,20.2,10.2]
d5conc2p2=[39.0,39.5,39.7,39.3,42.9,43.9,35.2]
d5conc5p1=[11.4,8.2,11.5,12.4,13.7,17.3,9.6]
d5conc5p2=[39.6,32.7,38.6,39.1,40.3,42.5,34.5]
d5conc10p1=[11.0,10.2,11.0,12.3,14.0,16.9,8.8]
d5conc10p2=[34.0,36.7,38.0,39.1,40.7,42.5,32.1]

d7conc1p1=[12.2,12.1,12.1,12.2,12.3,11.9,12.5]
d7conc1p2=[39.2,39.2,39.2,39.3,39.4,39.3,39.9]
d7conc2p1=[11.7,11.7,11.9,12.1,12.4,19.6,10.1]
d7conc2p2=[39.0,39.2,39.4,39.6,40.0,43.5,35.1]
d7conc5p1=[11.2,0.0,11.5,12.2,13.4,17.3,9.7]
d7conc5p2=[39.4,0.0,39.4,39.6,40.5,42.7,34.7]
d7conc10p1=[0.0,10.8,11.2,12.0,13.8,16.9,9.1]
d7conc10p2=[0.0,39.1,39.1,39.7,40.9,42.5,33.6]

plt.plot(loc,numpy.array(d1conc1p2)-numpy.array(d1conc1p1),'*-',label='Conc = 1')
plt.plot(loc,numpy.array(d1conc2p2)-numpy.array(d1conc2p1),'*-',label='Conc = 2')
plt.plot(loc,numpy.array(d1conc5p2)-numpy.array(d1conc5p1),'*-',label='Conc = 5')
plt.plot(loc,numpy.array(d1conc10p2)-numpy.array(d1conc10p1),'*-',label='Conc = 10')
plt.legend()
plt.show()

plt.figure(2)
plt.plot(loc,numpy.array(d3conc1p2)-numpy.array(d3conc1p1),'^-',label='Conc = 1')
plt.plot(loc,numpy.array(d3conc2p2)-numpy.array(d3conc2p1),'^-',label='Conc = 2')
plt.plot(loc,numpy.array(d3conc5p2)-numpy.array(d3conc5p1),'^-',label='Conc = 5')
plt.plot(loc,numpy.array(d3conc10p2)-numpy.array(d3conc10p1),'^-',label='Conc = 10')
plt.legend()
plt.show()

plt.figure(3)
plt.plot(loc,numpy.array(d5conc1p2)-numpy.array(d5conc1p1),'^-',label='Conc = 1')
plt.plot(loc,numpy.array(d5conc2p2)-numpy.array(d5conc2p1),'^-',label='Conc = 2')
plt.plot(loc,numpy.array(d5conc5p2)-numpy.array(d5conc5p1),'^-',label='Conc = 5')
plt.plot(loc,numpy.array(d5conc10p2)-numpy.array(d5conc10p1),'^-',label='Conc = 10')
plt.legend()
plt.show()

plt.figure(4)
plt.plot(loc,numpy.array(d7conc1p2)-numpy.array(d7conc1p1),'^-',label='Conc = 1')
plt.plot(loc,numpy.array(d7conc2p2)-numpy.array(d7conc2p1),'^-',label='Conc = 2')
plt.plot(loc,numpy.array(d7conc5p2)-numpy.array(d7conc5p1),'^-',label='Conc = 5')
plt.plot(loc,numpy.array(d7conc10p2)-numpy.array(d7conc10p1),'^-',label='Conc = 10')
plt.legend()
plt.show()
