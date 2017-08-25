import moose
import numpy as np
import rdesigneur as rd
import matplotlib.pyplot as plt
import os.path
import xml.etree.ElementTree as ET

params={
        #'diffusionL':1,
        'diffusionL':1e-07,
        #'diffA':1000,
       'diffA':0, 
       #'diffB':0,
       'diffB':0,
       'dendDia':10e-06,
        #'dendDia':10,
        #'dendL':100,
       #'dendL':100e-06,
       }
       
numDendSegments=10
comptLenBuff=14.4e-06
comptLen=1e-6

#comptDia=1e-06
RM=1.0
RA=10.0
CM=0.001

def makePassiveSoma(name,length,diamater):
	elecid=moose.Neuron('/library/'+name)
        dend=moose.Compartment(elecid.path+'/soma')
        dend.diameter=params['dendDia']
        dend.length=params['dendL']
        dend.x=params['dendL']
        return elecid
        
def writeXML(storeAvec,trialNum,fileName):
    if os.path.isfile(fileName):
       tree = ET.parse(fileName)
       root = tree.getroot()
       for i in range(len(storeAvec)):
          avec = ET.SubElement(root, 'avec'+str(i)+trialNum)
          avec.text = ''.join(str(j)+' ' for j in storeAvec[i])+'\n'
       #times = ET.SubElement(root, 'times')
       #times.text = ''.join(str(j)+' ' for j in timeArr)+'\n'
       #xmaxFWHH = ET.SubElement(root, 'xmaxFWHH'+trialNum)
       #xmaxFWHH.text = ''.join(str(k)+' ' for k in maxFWHH)+'\n'
       #tree = ET.ElementTree(root)
       tree.write(fileName) 
    else:
       root = ET.Element('Data')
       for i in range(len(storeAvec)):
          avec = ET.SubElement(root, 'avec'+str(i)+trialNum)
          avec.text = ''.join(str(j)+' ' for j in storeAvec[i])+'\n'
       #times = ET.SubElement(root, 'times')
       #times.text = ''.join(str(j)+' ' for j in timeArr)+'\n'
       #xmaxFWHH = ET.SubElement(root, 'xmaxFWHH'+trialNum)
       #xmaxFWHH.text = ''.join(str(k)+' ' for k in maxFWHH)+'\n'
       tree = ET.ElementTree(root)
       tree.write(fileName)
 
def makeDendProto():
    dend=moose.Neuron('/library/dend')
    #prev=rd.buildCompt(dend,'soma',RM=RM,RA=RA,CM=CM,dia=0.3e-06,x=0,dx=comptLenBuff)
    prev=rd.buildCompt(dend,'soma',RM=RM,RA=RA,CM=CM,dia=10e-06,x=0,dx=comptLen)
    #x=comptLenBuff
    x=comptLen
    y=0.0
    comptDia=10e-06

    for i in range(numDendSegments-1):
      dx=comptLen
      dy=0
      #comptDia +=1.7e-08
      compt=rd.buildCompt(dend,'dend'+str(i),RM=RM,RA=RA,CM=CM,x=x,y=y,dx=dx,dy=dy,dia=comptDia)
      moose.connect(prev,'axial',compt,'raxial')
      prev=compt
      x+=dx
      y+=dy
      
    #compt=rd.buildCompt(dend,'dendL',RM=RM,RA=RA,CM=CM,x=x,y=y,dx=comptLenBuff,dy=dy,dia=comptDia)
    #moose.connect(prev,'axial',compt,'raxial')

    return dend


def makeChemProto(name='hydra'):
        maxs=0.05
        chem=moose.Neutral('/library/'+name)
        compt=moose.CubeMesh('/library/'+name + '/' + name)
        A=moose.Pool(compt.path+'/A')
        B=moose.Pool(compt.path+'/B')
        S=moose.Pool(compt.path+'/S')
        space=moose.Pool(compt.path+'/space')
        #C=moose.Pool(compt.path+'/C')
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
        Sdot = moose.Function( S.path + '/Sdot' )
        spacedot = moose.Function( space.path + '/spacedot' )
        #Cdot = moose.Function( C.path + '/Cdot' )
        #Adot.expr="0.001*((x0^2/x1)+1)-1*x0+0.5*x0"
        #Bdot.expr="0*x0+0.001*x0^2-1*x1+1*x1"
        #Adot.expr="-x0+x1(0.067+(1*x0^2)/(1+x0^2))"
        #Bdot.expr="x0-x1(0.067+(1*x0^2)/(1+x0^2))"
        Adot.expr="-x0+x1*(0.067+(1*x0^2)/(1+x0^2))+(t<=20)*(0.05/2)*(1+cos("+str(np.pi)+"*x3))*x1*x2+(t>20)*(t<25)*(0.05/4)*(1+cos("+str(np.pi)+"*(t-20)/5))*(1+cos("+str(np.pi)+"*x3))*x1*x2"
        Bdot.expr="x0-x1*(0.067+(1*x0^2)/(1+x0^2))-(t<=20)*(0.05/2)*(1+cos("+str(np.pi)+"*x3))*x1*x2-(t>20)*(t<25)*(0.05/4)*(1+cos("+str(np.pi)+"*(t-20)/5))*(1+cos("+str(np.pi)+"*x3))*x1*x2"
        Sdot.expr="0"
        spacedot.expr="0"
        #Cdot.expr="0*x0+0.11*x1-0.11*x2+0.1*x0^2-0.1*(x1+x2)"
 
        
        print "$$$$> ", Adot, Bdot
        print Adot.expr, Bdot.expr
        print moose.showmsg(Adot)
        Adot.x.num = 4 #2
        Bdot.x.num = 4 #2
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        moose.connect( S, 'nOut', Adot.x[2], 'input' )
        moose.connect( space, 'nOut', Adot.x[3], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )

        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
        moose.connect( S, 'nOut', Bdot.x[2], 'input' )
        moose.connect( space, 'nOut', Bdot.x[3], 'input' )
        moose.connect( Bdot, 'valueOut', B, 'increment' )
        
        return compt

def main():
    library=moose.Neutral('/library')
    #makePassiveSoma( 'cell', params['dendL'], params['dendDia'] )
    makeDendProto()
    makeChemProto()
    rdes=rd.rdesigneur(
        turnOffElec=True,
        chemPlotDt = 0.1, 
        diffusionLength=params['diffusionL'],
        #cellProto=[['cell','soma']],
        cellProto=[['elec','dend']],
        chemProto=[['hydra','hydra']],
        chemDistrib=[['hydra', '#soma#,#dend#', 'install', '1']],
        #stimList=[['soma','1','.','inject','(t>0.01&&t<0.2)*1e-10']],
        plotList=[
            ['soma', '1', 'dend/A', 'n', '# of A'],
            ['soma', '1', 'dend/B', 'n', '# of B']],
        )
    moose.le( '/library' )
    moose.le( '/library/hydra' )
    rdes.buildModel()
    
    A = moose.element('/model/chem/dend/A')
    B = moose.element('/model/chem/dend/B')
    S = moose.element('/model/chem/dend/S')
    space = moose.element('/model/chem/dend/space')
    A.diffConst=1e-13 
    B.diffConst=1e-11
    S.diffConst=0
    space.diffConst = 0
    #moose.element('/model/chem/dend/A').vec[50].nInit=1.2
    #moose.element('/model/chem/dend/B').vec[50].nInit=1.2
    totLen = len(moose.vec('/model/chem/dend/A').n)
    sourceApply = range(int(totLen*0.1)+1)
    xl=0
    for j in range(totLen): 
        moose.element('/model/chem/dend/A').vec[j].concInit = 0.268331
        moose.element('/model/chem/dend/B').vec[j].concInit = 2.0
    
    
    for i in sourceApply:
        #moose.element('/model/chem/dend/A').vec[i].concInit=0.268331
        #moose.element('/model/chem/dend/B').vec[i].concInit=2
        moose.element('/model/chem/dend/S').vec[i].concInit=1
        moose.element('/model/chem/dend/space').vec[i].concInit=xl*0.1
        print moose.element('/model/chem/dend/space').vec[i].concInit,xl
        print moose.element('/model/chem/dend/S').vec[i].concInit
        xl=xl+1
    
    #randper=np.random.uniform(1,2,savec)
    print 'simulation start'
    dtSol = 0.01    
    moose.setClock(16,dtSol)
    moose.setClock(10,dtSol)
    moose.reinit()
    #avec=moose.vec('/model/chem/dend/A').n
    #bvec=moose.vec('/model/chem/dend/B').n
    #source=moose.vec('/model/chem/dend/S').n
    storeAvec=[]
    numSteps = 2500
    time=0
    t1=20
    t2=25
    maxs = 0.05
    space=moose.vec('/model/chem/dend/space').n
   # print 'coordinates are', space, np.cos(np.pi)
    
    for i in range(0,numSteps):
       #if t<20: 
       #  source = maxs/2
       #elif t > 20 and t < 25:
       #  s = (maxs/4)*(1+np.cos(np.pi*(t-t1)/(t2-t1)))
       #else:
       #  s = 0
       avec=moose.vec('/model/chem/dend/A').conc
       #print moose.vec('/model/chem/dend/S').n
       bvec=moose.vec('/model/chem/dend/B').conc
       source=moose.vec('/model/chem/dend/S').conc
       space=moose.vec('/model/chem/dend/space').conc
       moose.start(dtSol)
       storeAvec.append(avec)    
       time = time+dtSol
       print time
    
    #plt.ion()
    #fig = plt.figure(figsize=(6,6))
    trialNum = '1'
    fileName = 'Mori.xml'
    writeXML(storeAvec, trialNum, fileName)
    plt.plot(avec)
    plt.show()
    raw_input()
    print 'press any key to exit'
        

    
    return bvec,avec,source,space,storeAvec

if __name__ == '__main__':
    bvec,avec,source,space,storeAvec = main()
    
     
 

                   
