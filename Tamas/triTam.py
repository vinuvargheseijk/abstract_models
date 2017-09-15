import moose
import numpy as np
import rdesigneur as rd
import matplotlib.pyplot as plt
import os.path
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
       
numDendSegments=500
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
    print 'writing XML'
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
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
        Cdot = moose.Function( C.path + '/Cdot' )
        #Adot.expr="0.001*((x0^2/x1)+1)-1*x0+0.5*x0"
        #Bdot.expr="0*x0+0.001*x0^2-1*x1+1*x1"
        Adot.expr="4e-08-4e-06*x0+0.0004*x0^2*x1"
        Bdot.expr="6e-06-0.0004*x0^2*x1"
        print moose.showmsg(Adot)
        Adot.x.num = 2 #2
        Bdot.x.num = 2 #2
        #A.nInit=10
        #B.nInit=5
        A.nInit=0
        B.nInit=0
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )
        
        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
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
    moose.element('/model/chem/dend/A').vec[50].nInit=2
    moose.element('/model/chem/dend/B').vec[50].nInit=1
    moose.element('/model/chem/dend/A').vec[75].nInit=2
    moose.element('/model/chem/dend/B').vec[75].nInit=1
    moose.element('/model/chem/dend/A').vec[150].nInit=2
    moose.element('/model/chem/dend/B').vec[150].nInit=1
    moose.element('/model/chem/dend/A').vec[250].nInit=2
    moose.element('/model/chem/dend/B').vec[250].nInit=1
    moose.element('/model/chem/dend/A').vec[350].nInit=2
    moose.element('/model/chem/dend/B').vec[350].nInit=1
    moose.element('/model/chem/dend/A').vec[450].nInit=2
    moose.element('/model/chem/dend/B').vec[450].nInit=1
    storeAvec=[]
    avec = moose.vec( '/model/chem/dend/A' ).n
    savec=avec.size
    randper=np.random.uniform(1,2,savec)
    randper = randper/10
    print randper, randper.size

    #for i in range(0,savec-1,1):
    #    moose.element('/model/chem/dend/A').vec[i].nInit=randper[i]
    #    print moose.element('/model/chem/dend/A').vec[i].nInit
    
    moose.reinit()
    for i in range(1,4000,10):
       moose.start(10)
       avec = moose.vec( '/model/chem/dend/A' ).n
       storeAvec.append(avec)
    bvec = moose.vec( '/model/chem/dend/B' ).n
    avec = moose.vec( '/model/chem/dend/A' ).n
    
    trialNum = '1'
    fileName = 'Tamas.xml'

        
    writeXML(storeAvec, trialNum, fileName)

    
    return bvec,avec,storeAvec

if __name__ == '__main__':
    bvec,avec,storeAvec = main()
    #plt.ion()
    plt.figure(2)
    plt.plot(avec)
    plt.show()
    raw_input()
     
 

                   
