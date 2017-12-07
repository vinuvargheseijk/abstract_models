import matplotlib.pyplot as plt
import numpy

from matplotlib import rc

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

loc=[100,150,200,250,300,350,400]
d1conc1p1=[12.9,13.8,14.3,14.1,19.2,11.4,11.6]
d1conc1p2=[39.6,40.1,40.8,36.7,40.9,38.2,38.9]
d1conc2p1=[14.2,17.3,10.9,14.1,16.9,11.3,10.8]
d1conc2p2=[40.2,41.7,33.2,36.9,39.5,39.1,36.5]
d1conc5p1=[15.3,19.5,11.8,14.0,16.1,19.7,10.0]
d1conc5p2=[40.9,43.3,34.9,37.1,39.3,42.4,35.3]
d1conc10p1=[16.4,8.8,11.5,13.8,15.9,18.3,9.1]
d1conc10p2=[41.5,32.1,35.1,37.3,39.5,41.9,33.8]


d3conc1p1=[11.6,12.3,12.4,25.3,11.2,11.9,12.5]
d3conc1p2=[39.0,39.4,39.6,25.3,39.1,39.2,40.1]
d3conc2p1=[11.0,12.0,27.8,12.6,17.9,26.8,10.4]
d3conc2p2=[39.0,39.4,27.8,39.1,41.4,26.8,35.6]
d3conc5p1=[17.4,26.5,11.2,13.0,14.9,18.1,9.9]
d3conc5p2=[41.7,26.5,36.1,38.3,39.9,42.4,34.9]
d3conc10p1=[19.2,9.1,11.1,12.9,14.7,17.2,9.1]
d3conc10p2=[42.7,34.3,36.6,38.3,40.1,42.3,33.7]

d5conc1p1=[12.4,12.2,12.2,12.1,12.1,12.0,12.4]
d5conc1p2=[39.2,39.2,39.2,39.2,39.1,39.1,39.6]
d5conc2p1=[11.7,11.9,12.1,12.1,12.0,25.2,10.2]
d5conc2p2=[39.2,39.2,39.4,39.3,39.4,25.2,35.2]
d5conc5p1=[11.4,26.5,29.3,12.4,13.0,17.7,9.9]
d5conc5p2=[39.4,26.5,29.3,39.1,39.9,42.7,34.9]
d5conc10p1=[26.0,9.0,11.3,12.3,13.9,17.0,9.3]
d5conc10p2=[26.0,34.2,38.2,39.1,40.5,42.5,34.0]

d7conc1p1=[12.4,12.2,12.2,12.2,12.3,12.0,12.3]
d7conc1p2=[39.2,39.2,39.2,39.1,39.2,39.0,39.3]
d7conc2p1=[11.9,11.9,12.0,12.1,12.4,24.8,12.6]
d7conc2p2=[39.1,39.2,39.2,39.4,39.5,24.8,40.4]
d7conc5p1=[11.4,11.2,11.7,12.1,12.9,11.8,9.9]
d7conc5p2=[39.2,39.5,39.4,39.4,39.4,42.8,34.9]
d7conc10p1=[25.6,27.2,11.3,12.1,13.6,17.0,9.5]
d7conc10p2=[25.6,27.2,39.3,39.5,40.7,42.6,34.3]

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.plot(loc,numpy.array(d1conc1p2)-numpy.array(d1conc1p1),'*-',label='Conc = 1')
ax1.plot(loc,numpy.array(d1conc2p2)-numpy.array(d1conc2p1),'*-',label='Conc = 2')
ax1.plot(loc,numpy.array(d1conc5p2)-numpy.array(d1conc5p1),'*-',label='Conc = 5')
ax1.plot(loc,numpy.array(d1conc10p2)-numpy.array(d1conc10p1),'*-',label='Conc = 10')
ax1.title.set_text(r'Source at d=1e-07 $\mu$m')
ax1.legend()

ax2=fig.add_subplot(222)
ax2.plot(loc,numpy.array(d3conc1p2)-numpy.array(d3conc1p1),'^-',label='Conc = 1')
ax2.plot(loc,numpy.array(d3conc2p2)-numpy.array(d3conc2p1),'^-',label='Conc = 2')
ax2.plot(loc,numpy.array(d3conc5p2)-numpy.array(d3conc5p1),'^-',label='Conc = 5')
ax2.plot(loc,numpy.array(d3conc10p2)-numpy.array(d3conc10p1),'^-',label='Conc = 10')
ax2.title.set_text(r'Source at d=3e-07 $\mu$m')
ax2.legend()

ax3=fig.add_subplot(223)
ax3.plot(loc,numpy.array(d5conc1p2)-numpy.array(d5conc1p1),'^-',label='Conc = 1')
ax3.plot(loc,numpy.array(d5conc2p2)-numpy.array(d5conc2p1),'^-',label='Conc = 2')
ax3.plot(loc,numpy.array(d5conc5p2)-numpy.array(d5conc5p1),'^-',label='Conc = 5')
ax3.plot(loc,numpy.array(d5conc10p2)-numpy.array(d5conc10p1),'^-',label='Conc = 10')
ax3.title.set_text(r'Source at d=5e-07 $\mu$m')
ax3.legend()

ax4 = fig.add_subplot(224)
ax4.plot(loc,numpy.array(d7conc1p2)-numpy.array(d7conc1p1),'^-',label='Conc = 1')
ax4.plot(loc,numpy.array(d7conc2p2)-numpy.array(d7conc2p1),'^-',label='Conc = 2')
ax4.plot(loc,numpy.array(d7conc5p2)-numpy.array(d7conc5p1),'^-',label='Conc = 5')
ax4.plot(loc,numpy.array(d7conc10p2)-numpy.array(d7conc10p1),'^-',label='Conc = 10')
ax4.title.set_text(r'Source at d=7e-07 $\mu$m')
ax4.legend()
plt.show()
