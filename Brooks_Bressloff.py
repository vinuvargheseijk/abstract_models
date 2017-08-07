import moose
import numpy as np
import rdesigneur as rd
import matplotlib.pyplot as plt


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
comptLenBuff=14.4e-06
comptLen=0.216e-06
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
        
def makeDendProto():
    dend=moose.Neuron('/library/dend')
    prev=rd.buildCompt(dend,'soma',RM=RM,RA=RA,CM=CM,dia=0.3e-06,x=0,dx=comptLenBuff)
    x=comptLenBuff
    y=0.0
    comptDia=0.3e-06

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
        Adot.expr="-0.1*x0+((0.1*x0^2)/(x1+x2))"
        Bdot.expr="0*x0-0.1*x1+0.1*x2+0.1*x0^2-0.1*(x1+x2)"
        Cdot.expr="0*x0+0.1*x1-0.1*x2+0.1*x0^2-0.1*(x1+x2)"
 
        
        print "$$$$> ", Adot, Bdot, Cdot
        print Adot.expr, Bdot.expr, Cdot.expr
        print moose.showmsg(Adot)
        Adot.x.num = 3 #2
        Bdot.x.num = 3 #2
        Cdot.x.num = 3
        #A.nInit=10
        #B.nInit=5
        A.nInit=1
        B.nInit=1
        C.nInit=1
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
    C = moose.element('/model/chem/dend/C')
    A.diffConst=1e-13
    B.diffConst=0
    C.diffConst=0
    B.motorConst=1e-06
    C.motorConst=-1e-06
#    A.concInit=1
#    B.concInit=10
    moose.element('/model/chem/dend/A').vec[200].nInit=1.2
    moose.element('/model/chem/dend/A').vec[100].nInit=1.2
    #moose.element('/model/chem/dend/A').vec[95].nInit=1.2
    #moose.element('/model/chem/dend/A').vec[127].nInit=1.2
    #moose.element('/model/chem/dend/B').vec[244].nInit=1.2
    #moose.element('/model/chem/dend/C').vec[400].nInit=1.2
    #moose.element('/model/chem/dend/A').vec[105].nInit=1.2
    #moose.element('/model/chem/dend/B').vec[105].nInit=1.2
    
    #moose.element('/model/chem/dend/B').vec[25].nInit=0
    #A.nInit=1
    #B.nInit=15
    #for i in range(0,499):
        #moose.element('/model/chem/dend/A').vec[i].diffConst=9.45e-12
        #moose.element('/model/chem/dend/A').vec[i].diffConst=1e-13
        #moose.element('/model/chem/dend/B').vec[i].diffConst=1e-13
        #moose.element('/model/chem/dend/B').vec[i].diffConst=0.27e-09
        
    #for i in range(500,999):
        #moose.element('/model/chem/dend/A').vec[i].diffConst=9.45e-12
        #moose.element('/model/chem/dend/A').vec[i].diffConst=1e-13
        #moose.element('/model/chem/dend/B').vec[i].diffConst=1e-13
        #moose.element('/model/chem/dend/B').vec[i].diffConst=0.27e-09
        
    #for i in range(0,200):
        #moose.element('/model/chem/dend/A').vec[i].diffConst=1e-13
        
    #for i in range(700,999):
        #moose.element('/model/chem/dend/A').vec[i].diffConst=1e-13
        
    moose.reinit()
    #moose.start(2)
    for t in range(0,2000,200):
        moose.start(200)
        avec=moose.vec('/model/chem/dend/A').n
        plt.plot(avec)
        
    avec = moose.vec( '/model/chem/dend/A' ).n
    bvec = moose.vec( '/model/chem/dend/B' ).n
    cvec = moose.vec( '/model/chem/dend/C' ).n
    #plt.plot(bvec) 
    

        

    
    return bvec,avec,cvec

if __name__ == '__main__':
    bvec,avec,cvec = main()
     
 

                   
