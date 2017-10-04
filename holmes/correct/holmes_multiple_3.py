import moose
import numpy as np
import rdesigneur as rd
import matplotlib.pyplot as plt


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
        D=moose.Pool(compt.path+'/D')
        E=moose.Pool(compt.path+'/E')
        F=moose.Pool(compt.path+'/F')
        Z1=moose.Pool(compt.path+'/Z1')
        Z2=moose.Pool(compt.path+'/Z2')
        
        #A.diffConst=params['diffA']
        #B.diffConst=params['diffB']
        Adot = moose.Function( A.path + '/Adot' )
        Bdot = moose.Function( B.path + '/Bdot' )
        Cdot = moose.Function( C.path + '/Cdot' )
        Ddot = moose.Function( D.path + '/Ddot' )
        Edot = moose.Function( E.path + '/Edot' )
        Fdot = moose.Function( F.path + '/Fdot' )
        #Zdot = moose.Function( Z.path + '/Zdot' )
       
        #Adot.expr="x6*(1+x7)*(-x0+(5/(1+x1^3))*(2-x0-x3))"
        #Bdot.expr="x6*(1+x7)*(0*x0-x1+(3+2*(x2^3/(1+x1^3)))*(1/(1+x0^3))*(2-x1-x4))"
        #Cdot.expr="x6*(1+x7)*(0*x0+0*x1-0*x2+0.1*((0.2+0.3*(x0^3/(0.85^3+x0^3)))-x2^2*(0.2+1*x1^3/(0.85^3+x1^3))))"
        
        Adot.expr="x6*(1+x7)*(-x0+(4.5/(1+x1^3))*(2-x0-x3))"
        Bdot.expr="x6*(1+x7)*(0*x0-x1+(3+0.5*(x2^3/(1+x2^3)))*(1/(1+x0^3))*(2-x1-x4))"
        Cdot.expr="x6*(1+x7)*(0*x0+0*x1-0*x2+0.5*((0.2+0.3*(x0^3/(0.85^3+x0^3)))-x2^2*(0.2+1*x1^3/(0.85^3+x1^3))))"

        #Ddot.expr="(1+x6)*x7*(0*x0+0*x1+0*x2-x3+(5/(1+x4^3))*(2-x0-x3))"
        #Edot.expr="(1+x6)*x7*(0*x0+0*x1+0*x2+0*x3-x4+(3+2*(x5^3/(1+x4^3)))*(1/(1+x3^3))*(2-x1-x4))"
        #Fdot.expr="(1+x6)*x7*(0*x0+0*x1+0*x2+0*x3+0*x4-0*x5+0.1*((0.2+0.3*(x3^3/(0.85^3+x3^3)))-x5^2*(0.2+1*x4^3/(0.85^3+x4^3))))"
        
        Ddot.expr="(1+x6)*x7*(0*x0+0*x1+0*x2-x3+(4.5/(1+x4^3))*(2-x0-x3))"
        Edot.expr="(1+x6)*x7*(0*x0+0*x1+0*x2+0*x3-x4+(3+0.5*(x5^3/(1+x5^3)))*(1/(1+x3^3))*(2-x1-x4))"
        Fdot.expr="(1+x6)*x7*(0*x0+0*x1+0*x2+0*x3+0*x4-0*x5+0.5*((0.2+0.3*(x3^3/(0.85^3+x3^3)))-x5^2*(0.2+1*x4^3/(0.85^3+x4^3))))"
 
        
        print moose.showmsg(Adot)
        Adot.x.num = 8 #2
        Bdot.x.num = 8 #2
        Cdot.x.num = 8 #2
        Ddot.x.num = 8 #2
        Edot.x.num = 8 #2
        Fdot.x.num = 8 #2
        #A.nInit=10
        #B.nInit=5
        moose.connect( A, 'nOut', Adot.x[0], 'input' )
        moose.connect( B, 'nOut', Adot.x[1], 'input' )
        moose.connect( C, 'nOut', Adot.x[2], 'input' )
        moose.connect( D, 'nOut', Adot.x[3], 'input' )
        moose.connect( E, 'nOut', Adot.x[4], 'input' )
        moose.connect( F, 'nOut', Adot.x[5], 'input' )
        moose.connect( Z1, 'nOut', Adot.x[6], 'input' )
        moose.connect( Z2, 'nOut', Adot.x[7], 'input' )
        moose.connect( Adot, 'valueOut', A, 'increment' )

        moose.connect( A, 'nOut', Bdot.x[0], 'input' )
        moose.connect( B, 'nOut', Bdot.x[1], 'input' )
        moose.connect( C, 'nOut', Bdot.x[2], 'input' )
        moose.connect( D, 'nOut', Bdot.x[3], 'input' )
        moose.connect( E, 'nOut', Bdot.x[4], 'input' )
        moose.connect( F, 'nOut', Bdot.x[5], 'input' )
        moose.connect( Z1, 'nOut', Bdot.x[6], 'input' )
        moose.connect( Z2, 'nOut', Bdot.x[7], 'input' )
        moose.connect( Bdot, 'valueOut', B, 'increment' )
        
        moose.connect( A, 'nOut', Cdot.x[0], 'input' )
        moose.connect( B, 'nOut', Cdot.x[1], 'input' )
        moose.connect( C, 'nOut', Cdot.x[2], 'input' )
        moose.connect( D, 'nOut', Cdot.x[3], 'input' )
        moose.connect( E, 'nOut', Cdot.x[4], 'input' )
        moose.connect( F, 'nOut', Cdot.x[5], 'input' )
        moose.connect( Z1, 'nOut', Cdot.x[6], 'input' )
        moose.connect( Z2, 'nOut', Cdot.x[7], 'input' )
        moose.connect( Cdot, 'valueOut', C, 'increment' )
        
        moose.connect( A, 'nOut', Ddot.x[0], 'input' )
        moose.connect( B, 'nOut', Ddot.x[1], 'input' )
        moose.connect( C, 'nOut', Ddot.x[2], 'input' )
        moose.connect( D, 'nOut', Ddot.x[3], 'input' )
        moose.connect( E, 'nOut', Ddot.x[4], 'input' )
        moose.connect( F, 'nOut', Ddot.x[5], 'input' )
        moose.connect( Z1, 'nOut', Ddot.x[6], 'input' )
        moose.connect( Z2, 'nOut', Ddot.x[7], 'input' )
        moose.connect( Ddot, 'valueOut', D, 'increment' )


        moose.connect( A, 'nOut', Edot.x[0], 'input' )
        moose.connect( B, 'nOut', Edot.x[1], 'input' )
        moose.connect( C, 'nOut', Edot.x[2], 'input' )
        moose.connect( D, 'nOut', Edot.x[3], 'input' )
        moose.connect( E, 'nOut', Edot.x[4], 'input' )
        moose.connect( F, 'nOut', Edot.x[5], 'input' )
        moose.connect( Z1, 'nOut', Edot.x[6], 'input' )
        moose.connect( Z2, 'nOut', Edot.x[7], 'input' )
        moose.connect( Edot, 'valueOut', E, 'increment' )


        moose.connect( A, 'nOut', Fdot.x[0], 'input' )
        moose.connect( B, 'nOut', Fdot.x[1], 'input' )
        moose.connect( C, 'nOut', Fdot.x[2], 'input' )
        moose.connect( D, 'nOut', Fdot.x[3], 'input' )
        moose.connect( E, 'nOut', Fdot.x[4], 'input' )
        moose.connect( F, 'nOut', Fdot.x[5], 'input' )
        moose.connect( Z1, 'nOut', Fdot.x[6], 'input' )
        moose.connect( Z2, 'nOut', Fdot.x[7], 'input' )
        moose.connect( Fdot, 'valueOut', F, 'increment' )
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
            ['soma', '1', 'dend/B', 'n', '# of B'],
            ['soma', '1', 'dend/C', 'n', '# of C'],
            ['soma', '1', 'dend/D', 'n', '# of D'],
            ['soma', '1', 'dend/E', 'n', '# of E'],
            ['soma', '1', 'dend/F', 'n', '# of F']
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
    D = moose.element('/model/chem/dend/D')
    E = moose.element('/model/chem/dend/E')
    F = moose.element('/model/chem/dend/F')
    Z1 = moose.element('/model/chem/dend/Z1')
    Z2 = moose.element('/model/chem/dend/Z2')
    
    A.diffConst=1e-13
    B.diffConst=1e-13
    C.diffConst=1e-13
    D.diffConst=1e-13
    E.diffConst=1e-13
    F.diffConst=1e-13
    Z1.diffConst=0
    Z2.diffConst=0

    #moose.element('/model/chem/dend/Z1').vec.nInit = 0
    moose.element('/model/chem/dend/Z1').vec.nInit = 1
    #moose.element('/model/chem/dend/Z2').vec.nInit = 0
    moose.element('/model/chem/dend/Z2').vec.nInit = 1
    #for i in range(50,55):
     # moose.element('/model/chem/dend/Z1').vec[i].nInit = 1
     # moose.element('/model/chem/dend/Z2').vec[i].nInit = 1
    
    moose.element('/model/chem/dend/A').vec[20].nInit=1
    moose.element('/model/chem/dend/B').vec[20].nInit=1
    moose.element('/model/chem/dend/C').vec[20].nInit=1
    #moose.element('/model/chem/dend/D').vec[30].nInit=2
    #moose.element('/model/chem/dend/E').vec[30].nInit=2
    #moose.element('/model/chem/dend/F').vec[30].nInit=2
    moose.element('/model/chem/dend/D').vec[60].nInit=1
    moose.element('/model/chem/dend/E').vec[60].nInit=1
    moose.element('/model/chem/dend/F').vec[60].nInit=1
    #moose.element('/model/chem/dend/A').vec[120].nInit=1
    #moose.element('/model/chem/dend/B').vec[120].nInit=1
    #moose.element('/model/chem/dend/C').vec[120].nInit=1
    #moose.element('/model/chem/dend/D').vec[160].nInit=1
    #moose.element('/model/chem/dend/E').vec[160].nInit=1
    #moose.element('/model/chem/dend/F').vec[160].nInit=1
    storeAvec=[]
    storeBvec=[]
    storeCvec=[]
    storeDvec=[]
    storeEvec=[]
    storeFvec=[]
        
    moose.reinit()
    for i in range(1,5000,10):
       moose.start(10)
       avec = moose.vec( '/model/chem/dend/A' ).n
       bvec = moose.vec( '/model/chem/dend/B' ).n
       cvec = moose.vec( '/model/chem/dend/C' ).n
       dvec = moose.vec( '/model/chem/dend/D' ).n
       evec = moose.vec( '/model/chem/dend/E' ).n
       fvec = moose.vec( '/model/chem/dend/F' ).n
       storeAvec.append(avec)
       storeBvec.append(bvec)
       storeCvec.append(cvec)
       storeDvec.append(dvec)
       storeEvec.append(evec)
       storeFvec.append(fvec)
        
    

        

    
    return storeAvec,storeBvec,storeCvec,storeDvec,storeEvec,storeFvec

if __name__ == '__main__':
    storeAvec,storeBvec,storeCvec,storeDvec,storeEvec,storeFvec = main()
    #plt.ion()
    raw_input()
     
 

                   
