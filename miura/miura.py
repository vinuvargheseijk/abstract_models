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
       
numDendSegments=400
comptLenBuff=14.4e-06
comptLen=0.5e-6

#comptDia=1e-06
RM=1.0
RA=10.0
CM=0.001

        
def makeDendProto():
    dend=moose.Neuron('/library/dend')
    #prev=rd.buildCompt(dend,'soma',RM=RM,RA=RA,CM=CM,dia=0.3e-06,x=0,dx=comptLenBuff)
    prev=rd.buildCompt(dend,'soma',RM=RM,RA=RA,CM=CM,dia=0.3e-06,x=0,dx=comptLen)
    #x=comptLenBuff
    x=comptLen
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
      
    #compt=rd.buildCompt(dend,'dendL',RM=RM,RA=RA,CM=CM,x=x,y=y,dx=comptLenBuff,dy=dy,dia=comptDia)
    #moose.connect(prev,'axial',compt,'raxial')

    return dend


def makeChemProto(name='hydra'):
        chem=moose.Neutral('/library/'+name)
        compt=moose.CubeMesh('/library/'+name + '/' + name)
        A=moose.Pool(compt.path+'/A')
        B=moose.Pool(compt.path+'/B')
        #C=moose.Pool(compt.path+'/C')
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
        #Cdot = moose.Function( C.path + '/Cdot' )
        #Adot.expr="0.001*((x0^2/x1)+1)-1*x0+0.5*x0"
        #Bdot.expr="0*x0+0.001*x0^2-1*x1+1*x1"
        Adot.expr="0.6*x0-x0^3-x1"
        Bdot.expr="1.5*x0-2*x1"
        #Cdot.expr="0*x0+0.11*x1-0.11*x2+0.1*x0^2-0.1*(x1+x2)"
 
        
        print "$$$$> ", Adot, Bdot
        print Adot.expr, Bdot.expr
        print moose.showmsg(Adot)
        Adot.x.num = 3 #2
        Bdot.x.num = 3 #2
        #Cdot.x.num = 3
        #A.nInit=10
        #B.nInit=5
        A.nInit=1
        B.nInit=1
        #C.nInit=1
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        #moose.connect( C, 'nOut', Adot.x[2], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )

        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
        #moose.connect( C, 'nOut', Bdot.x[2], 'input' )
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
        #moogList=[['#','1','.','Vm','Vm']]
    #    moogList = [['soma', '1', 'dend/A', 'n', 'num of A (number)']]
        )
    moose.le( '/library' )
    moose.le( '/library/hydra' )
    #moose.showfield( '/library/soma/soma' )
    rdes.buildModel()
    #moose.element('/model/chem/dend/B').vec[50].nInit=15.5
    
    A = moose.element('/model/chem/dend/A')
    B = moose.element('/model/chem/dend/B')
    A.diffConst=0.005
    B.diffConst=0.25
#    A.concInit=1
#    B.concInit=10
    avec=moose.vec('/model/chem/dend/A').n
    savec=avec.size
    randper=np.random.uniform(1,2,savec)
    print randper, randper.size
    
    for i in range(0,savec-1,1):
        moose.element('/model/chem/dend/A').vec[i].nInit=randper[i]
        print moose.element('/model/chem/dend/A').vec[i].nInit
    
    print moose.element('/model/chem/dend/A').vec.nInit.size
    print 'simulation start'    
    moose.reinit()
    #moose.start(2)
    storeAvec=[]
    for t in range(0,500,100):
        #if t>900 and t<1100:
         #   print 'before loop',moose.element('/model/chem/dend/A').vec[5].n
          #  for i in range(0,savec-1,1):
           #     moose.element('/model/chem/dend/A').vec[i].n +=2*randper[i]
                #print 2*randper[5]
                #print 'in second loop'
                
            #print 'after loop',moose.element('/model/chem/dend/A').vec[5].n
            
        moose.start(100)
        print 'in loop', t
        avec=moose.vec('/model/chem/dend/A').n
        storeAvec.append(avec)
        #print storeAvec
        plt.plot(avec)
        
    avec = moose.vec( '/model/chem/dend/A' ).n
    bvec = moose.vec( '/model/chem/dend/B' ).n
    #rdes.displayMoogli(0.00005, 0.05, 0.0)
    #plt.plot(bvec) 
    target=open('mod.txt','w')
    for item in storeAvec[3]:
        print>>target,item
    

        

    
    return bvec,avec,storeAvec

if __name__ == '__main__':
    bvec,avec,storeAvec = main()
    
     
 

                   
