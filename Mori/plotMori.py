import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import numpy as np

def plotXML(tree,totTime,trialNum,timeStep):
   plt.ion()
   fig=plt.figure(figsize=(6,6))
   plt.xlabel('time')
   plt.ylabel('conc of a')
   cCount = 0
   cList = ['blue','green','red', 'black','yellow','cyan']
   for i in totTime:
     yValues = []
     yaxis = tree.find('avec'+str(i)+str(trialNum))
     yValues = [float(j) for j in yaxis.text.split()]
     plt.plot(yValues,color=cList[cCount])
     cCount = cCount + 1


def main():

    xmlfilename = 'Mori.xml'
    tree = ET.parse(xmlfilename)
    trialNum = 1
    timeStep = 0
    totTime = [0,199]
    plotXML(tree,totTime,trialNum,timeStep)

if __name__=='__main__':
    main()
    raw_input()
