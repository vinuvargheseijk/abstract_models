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
       'r':1.4,
       'b':0.001,
       'c1':3,
       'c2':0.2,
       'c3':6,
       'K1':6,
       'K2':3,
       'K3':3,
       'df':1,
       'lambda':0.95,
       'mt0':0.2,
       'Kf':1,
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
        C=moose.Pool(compt.path+'/C')
        fvec = moose.vec(compt.path+'/C').n
        numf = np.sum(fvec)
        r=params['r']
        b=params['b']
        c1=params['c1']
        c2=params['c2']
        c3=params['c3']
        K1=params['K1']
        K2=params['K2']
        K3=params['K3']
        df=params['df']
        lambdap=params['lambda']
        mt0=params['mt0']
        Kf=params['Kf']
        
        
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
        Cdot = moose.Function( C.path + '/Cdot' )

       
        Adot.expr=str(-r)+"*x0+("+str(b)+"+("+str(c1)+"*x0^2/(x0^2+"+str(K1^2)+"))+("+str(c2)+"*x2^2/(x2^2+"+str(K2^2)+")))*x1"
        Bdot.expr=str(r)+"*x0-("+str(b)+"+("+str(c1)+"*x0^2/(x0^2+"+str(K1^2)+"))+("+str(c2)+"*x2^2/(x2^2+"+str(K2^2)+")))*x1"
        Cdot.expr=str(-df)+"*x2+(("+str(c3)+"*x0^2/(x0^2+"+str(K3^2)+"))*("+str(Kf)+"/("+str(Kf)+"+("+str(mt0)+"*(1+"+str(lambdap)+"*"+str(numf*1e-07)+")))))"

 
        
        print Adot.expr
        print Bdot.expr
        print Cdot.expr
        print 'totalF-actin', numf
        Adot.x.num = 3 #2
        Bdot.x.num = 3 #2
        Cdot.x.num = 3
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        moose.connect( C, 'nOut', Adot.x[2], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )

        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
        moose.connect( C, 'nOut', Bdot.x[2], 'input' )
        moose.connect( Bdot, 'valueOut', B, 'increment' )
        
        moose.connect( A, 'nOut', Cdot.x[0], 'input' )
        moose.connect( B, 'nOut', Cdot.x[1], 'input' )
        moose.connect( C, 'nOut', Cdot.x[2], 'input' )
        moose.connect( Cdot, 'valueOut', C, 'increment' )
        
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
    C = moose.element('/model/chem/dend/C')
    
    A.diffConst=1e-13
    B.diffConst=50*1e-12
    C.diffConst=0.8*1e-12
    avec = moose.vec('/model/chem/dend/A').n
    savec = avec.size
    randper = np.random.uniform(1,2,savec)
    #for i in range(0,savec-1,1):
      #moose.element('/model/chem/dend/A').vec[i].nInit = randper[i]

    
    moose.element('/model/chem/dend/A').vec[50].nInit=100
    moose.element('/model/chem/dend/B').vec[50].nInit=100
    moose.element('/model/chem/dend/C').vec.nInit=0
    storeAvec=[]
    storeBvec=[]
    storeCvec=[]
        
    moose.reinit()
    for i in range(1,4000,10):
       moose.start(10)
       avec = moose.vec( '/model/chem/dend/A' ).n
       bvec = moose.vec( '/model/chem/dend/B' ).n
       cvec = moose.vec( '/model/chem/dend/C' ).n
       storeAvec.append(avec)
       storeBvec.append(bvec)
       storeCvec.append(cvec)

    trialNum = '1'
    fileName = 'mechano.xml'
    writeXML(storeAvec,trialNum,fileName)
        
    
    return storeAvec,storeBvec,storeCvec

if __name__ == '__main__':
    storeAvec,storeBvec,storeCvec = main()
    #plt.ion()
     
 

                   
