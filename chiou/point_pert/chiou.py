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
       
numDendSegments=100
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
        
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
       
        Adot.expr="-x0+(x0^2/(1+0.01*x0^2))*x1"
        Bdot.expr="x0-(x0^2/(1+0.01*x0^2))*x1"

 
        
        print moose.showmsg(Adot)
        Adot.x.num = 2 #2
        Bdot.x.num = 2 #2
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )

        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
        moose.connect( Bdot, 'valueOut', B, 'increment' )
        
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
            ['soma', '1', 'dend/B', 'n', '# of B'],
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
    
    A.diffConst=1e-13  #1e-14
    B.diffConst=1e-11  #1e-12
    avec = moose.vec('/model/chem/dend/A').n
    savec = avec.size
    randper = np.random.uniform(1,2,savec)
    #for i in range(0,savec-1,1):
      #moose.element('/model/chem/dend/A').vec[i].nInit = randper[i]

    
    moose.element('/model/chem/dend/A').vec[500].nInit=300
    moose.element('/model/chem/dend/A').vec[501].nInit=300
    moose.element('/model/chem/dend/B').vec[500].nInit=300
    moose.element('/model/chem/dend/B').vec[501].nInit=300
    moose.element('/model/chem/dend/A').vec[750].nInit=300
    moose.element('/model/chem/dend/A').vec[751].nInit=300
    moose.element('/model/chem/dend/B').vec[750].nInit=300
    moose.element('/model/chem/dend/B').vec[751].nInit=300
    storeAvec=[]
    storeBvec=[]
        
    moose.reinit()
    for i in range(1,10000,40):
       moose.start(40)
       if i > 5000 and i<5050:
           print 'perturbing'
           moose.element('/model/chem/dend/A').vec[650].n=350
           moose.element('/model/chem/dend/A').vec[651].n=350
       avec = moose.vec( '/model/chem/dend/A' ).n
       bvec = moose.vec( '/model/chem/dend/B' ).n
       storeAvec.append(avec)
       storeBvec.append(bvec)

    trialNum = '1'
    fileName = 'chio650651.xml'
    writeXML(storeAvec,trialNum,fileName)
        
    
    return storeAvec,storeBvec

if __name__ == '__main__':
    storeAvec,storeBvec = main()
    #plt.ion()
     
 

                   
