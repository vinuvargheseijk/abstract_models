import moose
import numpy as np
import rdesigneur as rd
import numpy as np
import matplotlib.pyplot as plt
import os.path
import sys
import xml.etree.ElementTree as ET


params={
        #'diffusionL':1,
        'diffusionL':1e-06,
        #'diffA':1000,
       'diffA':0, 
       #'diffB':0,
       'diffB':0,
       'dendDia':10e-06,
        #'dendDia':10,
        #'dendL':100,
       #'dendL':100e-06,
       }
       
numDendSegments=50
comptLenBuff=1e-06
comptLen=1e-06
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
    prev=rd.buildCompt(dend,'soma',RM=RM,RA=RA,CM=CM,dia=10e-06,x=0,dx=comptLenBuff)
    x=comptLenBuff
    y=0.0
    comptDia=10e-06

    for i in range(numDendSegments):
      dx=comptLen
      dy=0
      #comptDia +=1.7e-08
      compt=rd.buildCompt(dend,'dend'+str(i),RM=RM,RA=RA,CM=CM,x=x,y=y,dx=dx,dy=dy,dia=comptDia)
      moose.connect(prev,'axial',compt,'raxial')
      prev=compt
      x+=dx
      y+=dy
      
    compt=rd.buildCompt(dend,'dendL',RM=RM,RA=RA,CM=CM,x=x,y=y,dx=comptLenBuff,dy=dy,dia=comptDia)
    moose.connect(prev,'axial',compt,'raxial')

    return dend


def makeChemProto(name='hydra'):
        chem=moose.Neutral('/library/'+name)
        compt=moose.CubeMesh('/library/'+name + '/' + name)
        A=moose.Pool(compt.path+'/A')
        B=moose.Pool(compt.path+'/B')
        C=moose.Pool(compt.path+'/C')
        space=moose.Pool(compt.path+'/space')
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
        Cdot = moose.Function( C.path + '/Cdot' )
        #Adot.expr="0.001*((x0^2/x1)+1)-1*x0+0.5*x0"
        #Bdot.expr="0*x0+0.001*x0^2-1*x1+1*x1"
        #Adot.expr="0.5*exp(-1.5*x2/(50*1e-06))*x0^2*x1-(0.1+0.01)*x0+0.01*x1"
        #Bdot.expr="-0.5*exp(-1.5*x2/(50*1e-06))*x0^2*x1+0.1*x0-0.01*x1+0.01"
 
        Adot.expr="0.1*x0^2*x1-(0.1+0.01)*x0+0.01*x1"
        Bdot.expr="-0.1*x0^2*x1+0.1*x0-0.01*x1+0.01"
        
        print moose.showmsg(Adot)
        Adot.x.num = 2 #2
        Bdot.x.num = 2 #2
        #A.nInit=10
        #B.nInit=5
        A.nInit=0
        B.nInit=0
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        #moose.connect( space, 'nOut', Adot.x[2], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )

        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
        #moose.connect( space, 'nOut', Bdot.x[2], 'input' )
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
        plotList=[
            ['soma', '1', 'dend/A', 'n', '# of A'],
            ['soma', '1', 'dend/B', 'n', '# of B']
        ],
    #    moogList = [['soma', '1', 'dend/A', 'n', 'num of A (number)']]
        )
    moose.le( '/library' )
    moose.le( '/library/hydra' )
    #moose.showfield( '/library/soma/soma' )
    rdes.buildModel()
    #moose.element('/model/chem/dend/B').vec[50].nInit=15.5
    
    A = moose.element('/model/chem/dend/A')
    B = moose.element('/model/chem/dend/B')
    A.diffConst=1e-13
    B.diffConst=1e-12
    moose.element('/model/chem/dend/A').vec[25].nInit=0.1
    moose.element('/model/chem/dend/B').vec[25].nInit=0.1
    moose.element('/model/chem/dend/A').vec[30].nInit=0.1
    moose.element('/model/chem/dend/B').vec[30].nInit=0.1
    moose.element('/model/chem/dend/A').vec[45].nInit=0.1
    moose.element('/model/chem/dend/B').vec[45].nInit=0.1
    storeAvec=[]
    storeBvec=[]
    for i in range(50):
      moose.element('/model/chem/dend/space').vec[i].nInit=moose.element('/model/chem/dend/mesh').vec[i].Coordinates[0]
      print moose.element('/model/chem/dend/space').vec[i].nInit
        
    moose.reinit()
    pert_pos=int(sys.argv[1])
    print 'now perturbed at', pert_pos
    for i in range(1,20000,10):
       if i>10000 and i<10010:
          moose.element('/model/chem/dend/A').vec[pert_pos].n=3
          moose.element('/model/chem/dend/B').vec[pert_pos].n=3
          print moose.element('/model/chem/dend/A').vec[pert_pos].n
       moose.start(10)
       avec = moose.vec( '/model/chem/dend/A' ).n
       bvec = moose.vec( '/model/chem/dend/B' ).n
       storeAvec.append(avec)
       storeBvec.append(bvec)
    bvec = moose.vec( '/model/chem/dend/B' ).n
    avec = moose.vec( '/model/chem/dend/A' ).n
    svec = moose.vec( '/model/chem/dend/space').n
    trialNum = str(pert_pos)
    fileName = str(pert_pos)+'champneys.xml'
    writeXML(storeAvec, trialNum, fileName)


        

    
    return svec,bvec,avec,storeAvec,storeBvec

if __name__ == '__main__':
    svec,bvec,avec,storeAvec,storeBvec = main()
    #plt.ion()
    plt.figure(2)
    plt.plot(avec)
    plt.show()
    raw_input()
     
 

                   
