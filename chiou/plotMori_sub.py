import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np

def plotXML(tree,totTime,trialNum,timeStep,G):
   plt.ion()
   txt="For all plots K=10, two perturbations are added at 500 and 650"
   #fig=plt.figure(figsize=(6,6))
   #plt.xlabel('length of dendrite')
   #plt.ylabel('Number of GTPases')
   #plt.title('Random perturbations all throughout length (ranging from 1 to 5 number of molecules), chiou wave pin model, a.diff=1e-13,b.diff=1e-11')
   cCount = 0
   cList = ['blue','green','red', 'black','yellow','cyan']
   f, axarr = plt.subplots(2,2)
   l=0
   m=0
   gv=0
   f.text(.5, .05, txt, ha='center')
   for k in tree:
     print 'k is', k
     cCount = 0
     for i in totTime:
       yValues = []
       yaxis = k.find('avec'+str(i)+str(trialNum))
       yValues = [float(j) for j in yaxis.text.split()]
       #plt.plot(yValues,color=cList[cCount],label=str(i*40))
       if l==1 and m==1:
          axarr[l,m].plot(yValues,color=cList[cCount],label='gamma= '+str(G[gv])+' amplitude 500')
       else:
          axarr[l,m].plot(yValues,color=cList[cCount],label='gamma= '+str(G[gv])+' amplitude 300')

       cCount = cCount + 1
       axarr[l,m].legend()
     m=m+1
     print 'm is', l,m
     if m>1:
         print 'm is', l, m
         l=l+1
         m=0
     if l>1:
         break
     gv=gv+1

   #f, axarr = plt.subplots(2, 2)
   #axarr[0, 0].plot(x, y)
   #axarr[0, 0].set_title('Axis [0,0]')
   #axarr[0, 1].scatter(x, y)
   #axarr[0, 1].set_title('Axis [0,1]')
   #axarr[1, 0].plot(x, y ** 2)
   #axarr[1, 0].set_title('Axis [1,0]')
   #axarr[1, 1].scatter(x, y ** 2)
   #axarr[1, 1].set_title('Axis [1,1]')
# Fine-tune figure; hide x ticks for top plots and y ticks for right plots
   #plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
   #plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

def main():

    xmlfilename1 = 'chio_amp300_K10_g001.xml'
    xmlfilename2 = 'chio_amp300_K10_g0_01.xml'
    xmlfilename3 = 'chio_amp300_K10_g0_1.xml'
    xmlfilename4 = 'chio_amp500_K10_g0_1.xml'
    tree1 = ET.parse(xmlfilename1)
    tree2 = ET.parse(xmlfilename2)
    tree3 = ET.parse(xmlfilename3)
    tree4 = ET.parse(xmlfilename4)
    trialNum = 1
    timeStep = 0
    totTime = [224]
    tree = [tree1,tree2,tree3,tree4]
    G=[0.001,0.01,0.1,0.1]
    plotXML(tree,totTime,trialNum,timeStep,G)

if __name__=='__main__':
    main()
    raw_input()
