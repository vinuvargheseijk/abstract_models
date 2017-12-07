import matplotlib.pyplot as plt
import numpy
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

loc=[100,150,200,250,300,350,400]
d1conc1p1=[12.7,14.1,14.5,14.5,10.6,11.1,11.8]
d1conc1p2=[39.4,40.2,40.6,35.1,36.6,37.2,38.4]
d1conc2p1=[12.9,13.4,14.3,14.1,18.9,11.4,11.6]
d1conc2p2=[39.6,40.0,40.8,36.7,40.8,38.2,38.1]
d1conc5p1=[14.5,17.6,11.4,14.1,16.5,8.1,10.6]
d1conc5p2=[40.4,42.0,34.1,37.0,39.3,31.7,36.2]
d1conc10p1=[14.9,18.3,11.7,14.0,16.3,19.6,10.3]
d1conc10p2=[40.6,42.5,34.6,37.1,39.2,42.4,35.7]


d3conc1p1=[12.6,12.5,12.4,11.9,11.9,12.0,12.2]
d3conc1p2=[39.4,39.4,39.5,39.4,39.1,39.0,39.4]
d3conc2p1=[11.5,12.2,12.4,25.2,24.6,11.9,12.6]
d3conc2p2=[39.0,39.5,40.0,25.2,24.6,39.2,40.2]
d3conc5p1=[10.9,11.8,10.2,12.8,16.7,25.7,12.6]
d3conc5p2=[39.0,39.9,33.9,38.7,40.7,25.7,35.4]
d3conc10p1=[17.5,27.0,11.2,13.0,14.8,17.9,9.8]
d3conc10p2=[41.7,27.0,36.2,38.3,39.9,42.3,34.9]

d5conc1p1=[12.5,12.5,12.4,12.2,12.2,12.1,12.2]
d5conc1p2=[39.4,39.4,39.2,39.3,39.4,38.9,38.9]
d5conc2p1=[12.4,12.2,12.2,12.1,12.1,11.9,12.5]
d5conc2p2=[39.2,39.1,39.3,39.3,39.3,39.2,39.7]
d5conc5p1=[11.6,11.7,12.0,12.2,11.7,20.1,10.1]
d5conc5p2=[39.1,39.4,39.6,39.3,39.6,43.8,35.1]
d5conc10p1=[11.4,26.6,28.7,12.4,13.0,17.6,9.9]
d5conc10p2=[39.3,26.6,28.7,39.3,39.9,42.6,34.8]

d7conc1p1=[12.4,12.4,12.4,12.3,12.3,12.1,12.2]
d7conc1p2=[39.2,39.1,39.1,39.1,39.1,38.9,38.9]
d7conc2p1=[12.4,12.2,12.2,12.2,12.3,12.0,12.4]
d7conc2p2=[39.3,39.1,39.1,39.1,39.3,39.1,39.5]
d7conc5p1=[11.8,11.8,11.9,12.1,12.5,19.3,10.1]
d7conc5p2=[39.1,39.1,39.3,39.5,39.7,43.3,34.8]
d7conc10p1=[11.4,11.2,11.6,12.1,12.9,17.6,9.9]
d7conc10p2=[39.1,39.3,39.6,39.4,40.1,42.7,34.8]
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.plot(loc,numpy.array(d1conc1p1),'*-',label='Conc = 1')
ax1.plot(loc,numpy.array(d1conc2p1),'*-',label='Conc = 2')
ax1.plot(loc,numpy.array(d1conc5p1),'*-',label='Conc = 5')
ax1.plot(loc,numpy.array(d1conc10p1),'*-',label='Conc = 10')
ax1.title.set_text(r'Source at d=1e-07 $\mu$m')
ax1.legend()
#plt.show()

ax2 = fig.add_subplot(222)
ax2.plot(loc,numpy.array(d3conc1p1),'^-',label='Conc = 1')
ax2.plot(loc,numpy.array(d3conc2p1),'^-',label='Conc = 2')
ax2.plot(loc,numpy.array(d3conc5p1),'^-',label='Conc = 5')
ax2.plot(loc,numpy.array(d3conc10p1),'^-',label='Conc = 10')
ax2.title.set_text(r'Source at d=3e-07 $\mu$m')
ax2.legend()
#plt.show()

ax3 = fig.add_subplot(223)
ax3.plot(loc,numpy.array(d5conc1p1),'^-',label='Conc = 1')
ax3.plot(loc,numpy.array(d5conc2p1),'^-',label='Conc = 2')
ax3.plot(loc,numpy.array(d5conc5p1),'^-',label='Conc = 5')
ax3.plot(loc,numpy.array(d5conc10p1),'^-',label='Conc = 10')
ax3.title.set_text(r'Source at d=5e-07 $\mu$m')
ax3.legend()
#plt.show()

ax4 = fig.add_subplot(224)
ax4.plot(loc,numpy.array(d7conc1p1),'^-',label='Conc = 1')
ax4.plot(loc,numpy.array(d7conc2p1),'^-',label='Conc = 2')
ax4.plot(loc,numpy.array(d7conc5p1),'^-',label='Conc = 5')
ax4.plot(loc,numpy.array(d7conc10p1),'^-',label='Conc = 10')
ax4.title.set_text(r'Source at d=7e-07 $\mu$m')
ax4.legend()
plt.show()
