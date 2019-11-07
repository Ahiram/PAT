# -*- coding: utf-8 -*-
#!/home/noselab/anaconda3/envs/Canon2/bin python3.6
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import copy
import time
import datetime
from PIL import Image, ImageOps
import sys

def testtest(a):
    print(a)
    
def gofl(pots):
    #read tiff file and create folder for output data
    """pot = input("input path of tiff >> ")"""
    '''pot = "/home/noselab/Desktop/Twopointpython/181114_MhcGFPUAS-Kir_A18gSplit1_03_8bit_color_adjusted.tif"'''
    pot=pots
    pdop=os.path.split(pot)[0]
    finame=pot.split("/")[-1].split(".")[0]
    t=time.time()
    ts = datetime.datetime.now().strftime('%Y%m%d-%H%M')
    #image_xxx.png-->csv_image_YYMMDD-HHMM
    setname=pot.split("/")[-1].split(".")[0]+"_"+ts
    outputfolname='output_%s'%(finame)
    outputfname='output_%s'%(ts)
    os.chdir(pdop)
    try:
        os.mkdir(outputfolname)
        rd=os.path.join(pdop,outputfolname)
    except:
        rd=os.path.join(pdop,outputfolname)
    os.chdir(rd)
    try:
        os.mkdir(outputfname)
        rd0=os.path.join(rd,outputfname)
    except:
        rd0=os.path.join(rd,outputfname)
    os.chdir(rd0)
    
    return setname,finame,ts,pot,rd0

def gofl2(setname,ts,pot,rd0,numpo,ininum,fininum):
    #create output data for each duration of tiff file
    os.chdir(rd0)
    """number_point=int(input("number of point you want to annotate(input 2N) >> "))
    initiation=int(input("initiation flame of annotation >> "))
    duration=int(input("last flame of annotation >> "))-initiation
    """
    number_point=int(numpo)
    initiation=int(ininum)
    duration=int(fininum)-initiation
    setname2=ts+"_"+"%04d-%04d"%(initiation,int(initiation+duration-1))
    setname3=setname+"_"+"%04d-%04d"%(initiation,int(initiation+duration-1))
    outputdurfname="%04d-%04d"%(initiation,int(initiation+duration-1))
    lwname='dep'
    csvfname='csv'
    figfname='fig'
    try:
        os.mkdir(outputdurfname)
        rd00=os.path.join(rd0,outputdurfname)
    except:
        rd00=os.path.join(rd0,outputdurfname)    
    os.chdir(rd00)
    
    try:
        os.mkdir(csvfname)
        rd01=os.path.join(rd00,csvfname)
    except:
        rd01=os.path.join(rd00,csvfname)
    try:
        os.mkdir(lwname)
        rd02=os.path.join(rd00,lwname)
    except:
        rd02=os.path.join(rd00,lwname)
    try:
        os.mkdir(figfname)
        rd03=os.path.join(rd00,figfname)
    except:
        rd03=os.path.join(rd00,figfname)
    os.chdir(rd00)
    file = open('info_%s.txt'%(setname2), 'w')
    file.writelines(str("tiff name:%s"%(os.path.split(pot)[1]))+"\n")
    file.writelines(str("date of analysis:%s"%(ts))+"\n")
    file.writelines(str("number of anotasion point:%d"%(number_point))+"\n")
    file.writelines(str("duration flames of anotation:%04d-%04d"%(initiation,int(initiation+duration-1)))+"\n")
    file.close()
   
    return number_point,initiation,duration,rd01,rd02,rd03,outputdurfname

class Pointlist():
    def __init__(self,npo,nfl,inif):
        self.npo = npo
        self.nfl = nfl
        self.curfl = inif
        self.pos = 0
        self.ptarray = np.empty((npo,2),dtype=int)
        self.ptlist=[]
        self.count=0
    def addp(self,x,y):
        if self.pos < self.npo:
            self.ptarray[self.pos,:]=[x,y]
            self.pos+=1
            return True
        else:
            return False
    def delp(self):
        self.pos = 0
        self.ptarray = np.empty((self.npo,2),dtype=int)
    def adda(self):
        if self.pos == self.npo:
            self.ptlist.append(copy.deepcopy(self.ptarray))
            self.pos=0
            self.ptarray = np.empty((self.npo,2),dtype=int)
            self.curfl+=1
            self.count+=1
            return True
        else:
            return False
    def dela(self):
        del self.ptlist[-1]
        self.pos=0
        self.ptarray = np.empty((self.npo,2),dtype=int)
        self.curfl-=1
        self.count-=1
        
    def copya(self):
        self.ptarray=self.ptlist[-1]
        self.pos=self.npo
        
def ghostlayer(orimg,polist,colorset,alpha):
    layer = np.full((int(orimg.shape[1]), int(orimg.shape[0]), 3), 0, dtype=np.uint8)
    for ncolors in range(int(len(polist)/2)):
        bgrcolor=int(colorset[ncolors][2]),int(colorset[ncolors][1]),int(colorset[ncolors][0])
        cv2.line(layer, (polist[ncolors*2][0], polist[ncolors*2][1]),
                     (polist[ncolors*2+1][0], polist[ncolors*2+1][1]), bgrcolor, 2)
    ghost = cv2.addWeighted(orimg, 1, layer, alpha, 0)
    return ghost

def onMouse(event, x, y, flags, params):
    wname, img_pil, ptset,setname,ccet = params
    img_pil.seek(ptset.curfl)
    img = np.asarray(img_pil)
    '''
    img = (img/255).astype('uint8')
    img = cv2.equalizeHist(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    '''
    
    if ptset.count >0:
        img=ghostlayer(img,ptset.ptlist[int(ptset.count-1)],ccet,0.1)
        cv2.putText(img, '%04d'%(ptset.curfl), (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
    if event == cv2.EVENT_LBUTTONDOWN:
        
        if ptset.addp(x,y) == True:
            cv2.circle(img, (x, y), 1, (0, 0, 255), -1)
            cv2.putText(img, '%04d'%(ptset.curfl), (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            cv2.imshow(wname, img)
        else:
            pass
        if ptset.pos == ptset.npo:
            
            for ncolor in range(int(ptset.npo/2)):
                bgrcolorp=int(ccet[ncolor][2]),int(ccet[ncolor][1]),int(ccet[ncolor][0])
                cv2.line(img, (ptset.ptarray[ncolor*2][0], ptset.ptarray[ncolor*2][1]),
                     (ptset.ptarray[ncolor*2+1][0], ptset.ptarray[ncolor*2+1][1]), bgrcolorp, 2)
            

            cv2.imshow(wname, img)
    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_SHIFTKEY:
        ptset.delp()

        cv2.destroyAllWindows()
    if event == cv2.EVENT_RBUTTONDOWN:
        if ptset.pos == ptset.npo:
            img_pil.seek(ptset.curfl)
            img = np.asarray(img_pil)
            for ncolor in range(int(ptset.npo/2)):
                bgrcolorp = int(ccet[ncolor][2]),int(ccet[ncolor][1]),int(ccet[ncolor][0])
                cv2.line(img, (ptset.ptarray[ncolor*2][0], ptset.ptarray[ncolor*2][1]),
                     (ptset.ptarray[ncolor*2+1][0], ptset.ptarray[ncolor*2+1][1]), bgrcolorp, 2)
            cv2.imshow(wname, img)
            cv2.imwrite("depicted_%s_%04d.jpg"%(setname,ptset.curfl),img)
        
        
        if ptset.adda() == True:

            cv2.destroyAllWindows()

    if event == cv2.EVENT_LBUTTONDOWN and flags & cv2.EVENT_FLAG_CTRLKEY:
        ptset.dela()

        cv2.destroyAllWindows()
    
    
    
    if event == cv2.EVENT_MBUTTONDOWN:
        
        if ptset.count >0:
            ptset.copya()
            img_pil.seek(ptset.curfl)
            img = np.asarray(img_pil)
            for ncolor in range(int(ptset.npo/2)):
                bgrcolorp = int(ccet[ncolor][2]),int(ccet[ncolor][1]),int(ccet[ncolor][0])
                cv2.line(img, (ptset.ptarray[ncolor*2][0], ptset.ptarray[ncolor*2][1]),
                                             (ptset.ptarray[ncolor*2+1][0], ptset.ptarray[ncolor*2+1][1]), bgrcolorp, 2)
                cv2.imshow(wname, img)

            cv2.destroyAllWindows()


def twopoints(pots,numpo,ininum,fininum):
    
    rgbcolorlist=[]
    cRed=np.array([255,0,0],dtype=int)
    cGre=np.array([0,255,0],dtype=int)
    cBlu=np.array([0,0,255],dtype=int)
    cCya=np.array([0,255,255],dtype=int)
    cYel=np.array([255,255,0],dtype=int)
    cMag=np.array([255,0,255],dtype=int)

    rgbcolorlist.append(cCya)
    rgbcolorlist.append(cYel)
    rgbcolorlist.append(cMag)
    rgbcolorlist.append(cRed)
    rgbcolorlist.append(cGre)
    rgbcolorlist.append(cBlu)

    setname,filename,timest,pot,rd0=gofl(pots)

    npoint,ini,dur,rd1,rd2,rd3,setname2=gofl2(setname,timest,pot,rd0,numpo,ininum,fininum)
    img_pil = Image.open(pot)

    segd=np.zeros((dur,npoint*3))
    pset=Pointlist(npoint,dur,ini)
    os.chdir(rd2)
    while pset.curfl != ini+dur:
        if pset.count ==0:
            img_pil.seek(pset.curfl)
            img = np.asarray(img_pil)
            '''
            img = (img/255).astype('uint8')
            img = cv2.equalizeHist(img)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            '''
            cv2.putText(img, '%04d'%(pset.curfl), (20, 25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            wname = "Movie"
            cv2.namedWindow(wname)
            cv2.setMouseCallback(wname, onMouse, [wname, img_pil, pset,filename,rgbcolorlist])
            cv2.imshow(wname, img)
            if cv2.waitKey(0) & 0xFF == ord("q"):
                break

        else:
            img_pil.seek(pset.curfl)
            img = np.asarray(img_pil)
            '''
            img = (img/255).astype('uint8')
            img = cv2.equalizeHist(img)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            '''
            img=ghostlayer(img,pset.ptlist[int(pset.count-1)],rgbcolorlist,0.1)
            cv2.putText(img, '%04d'%(pset.curfl), (20,25), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=2)
            wname = "Movie"
            cv2.namedWindow(wname)
            cv2.setMouseCallback(wname, onMouse, [wname, img_pil, pset,filename,rgbcolorlist])
            cv2.imshow(wname, img)
            if cv2.waitKey(0) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
    os.chdir(rd1)
    for i in range(dur):
        for j in range(npoint):
            segd[i,j*2] = pset.ptlist[i][j][0]
            segd[i,j*2+1] = pset.ptlist[i][j][1]
        for leng in range(int(npoint/2)):
            vec=np.array([segd[i,leng*4],segd[i,leng*4+1]])-np.array([segd[i,leng*4+2],segd[i,leng*4+3]])
            segd[i,npoint*2+leng]=np.linalg.norm(vec)
    for j in range(int(npoint/2)):
        mxleng=segd[:,npoint*2+j].max()
        for i in range(dur):
            segd[i,npoint*2+int(npoint/2)+j]=segd[i,npoint*2+j]/mxleng
    with open ('csv_%s.csv'%(pot.split("/")[-1].split(".")[0]+'_'+setname2), 'w') as f:

        writer=csv.writer(f)
        writer.writerows(segd)
    os.chdir(rd3)
