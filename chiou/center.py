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
   begA=[]
   endA=[]
   for k in tree:
     print 'k is', k
     cCount = 0
     for i in totTime:
       yValues = []
       yaxis = k.find('avec'+str(i)+str(trialNum))
       yValues = [float(j) for j in yaxis.text.split()]
       indArEnd=[]
       indArBeg=[]
       ysize=len(yValues)
       print ysize
       for ci in yValues[0:ysize-1]:
            ind=yValues.index(ci) 
            #print ci, yValues[ind+1]
            if yValues[ind+1]-ci>0.01:
               print 'begin', ind
               indArBeg.append(ind) 
               #break
            if ci-yValues[ind+1]>0.001:
               print 'end',ind
               indArEnd.append(ind)
       end = indArEnd[-1]
       beg = indArBeg[0]
       print beg,end
     begA.append[beg]
     endA.append[end]
     print begA,endA
       #plt.plot(yValues,color=cList[cCount],label=str(i*40))
       if l==1 and m==1:
          axarr[l,m].plot(yValues,color=cList[cCount])
       else:
          axarr[l,m].plot(yValues,color=cList[cCount])

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

    xmlfilename1 = 'chioPos500timeDur_4000_4001_dist2.xml'
    xmlfilename2 = 'chioPos530timeDur_4000_4001_dist2.xml'
    xmlfilename3 = 'chioPos550timeDur_4000_4001_dist2.xml'
    xmlfilename4 = 'chioPos600timeDur_4000_4001_dist2.xml'
    tree1 = ET.parse(xmlfilename1)
    tree2 = ET.parse(xmlfilename2)
    tree3 = ET.parse(xmlfilename3)
    tree4 = ET.parse(xmlfilename4)
    trialNum = 1
    timeStep = 0
    totTime = [249]
    tree = [tree1,tree2,tree3,tree4]
    G=[0.001,0.01,0.1,0.1]
    plotXML(tree,totTime,trialNum,timeStep,G)

if __name__=='__main__':
    main()
    raw_input()
