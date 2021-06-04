import matplotlib.pyplot as plt
import os, fnmatch
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np
from scipy.signal import butter,filtfilt
##############################################
# Caratteristiche del segnale
#  # Filter requirements.
T = 5.0         # Sample Period
fs = 16000       # sample rate, Hz
cutoff = 1000      # desired cutoff frequency of the filter, Hz ,      slightly higher than actual 1.2 Hznyq = 0.5 * fs  # Nyquist Frequencyorder = 2       # sin wave can be approx represented as quadratic
n = int(T * fs) # total number of samples
nyq = 0.5 * fs  # Nyquist Frequencyorder = 2       # sin wave can be approx represented as quadratic
def GetXposForTrigger(Data,Tensione,Slop=True,Soglia=0.05):
    i=0
    #cerco la posizione del trigger
    Res=[]
    k=0
    while(i<len(Data)):
        if(k==0):
            if(((Data[i])>Tensione-Soglia) and((Dat[i]<Tensione+Soglia))):
                if(Slop):
                    if((Data[i+5]-Data[i])>0):
                        k=i
                        return i
                else:
                    if((Data[i+5]-Data[i])<0):
                        k=i
                        return i
        i=i+1
        
def GetReTriggeredTrace(Data,Tensione,Slop=True,Soglia=0.05):
    i=GetXposForTrigger(Data,Tensione,Slop,Soglia)
    Res=[]
    while(i<len(Data)):
        Res.append(Data[i])
        i=i+1
    return Res

def butter_lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / nyq
    print("normal_catoff is ",normal_cutoff)
    # Get the filter coefficients 
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y




def findfile(pattern ,mypath):
    Res=[]
    print(" pattern",pattern)
    print("mypath",mypath)
    for f in listdir(mypath):
        if f.endswith('.txt'):
            #print(f)
            if fnmatch.fnmatch(f, pattern):
                Res.append(f)
    print(Res)
    return Res

def findjsonfile(pattern ,mypath):
    Res=[]
    print(" pattern",pattern)
    print("mypath",mypath)
    for f in listdir(mypath):
        if f.endswith('.json'):
            #print(f)
            if fnmatch.fnmatch(f, pattern):
                Res.append(f)
    print(Res)
    return Res
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path,topdown=False):
        for name in files:
            if name.endswith('.txt'):
                #print(name)
                #print(pattern)
                if fnmatch.fnmatch(name, pattern):
                    print(name)
                    ##print(pattern)
                    result.append(os.path.join(root, name))
                    print(result)
    print(result)
    return result

#find('demofile*.txt', '/home/novello')


def readfile(filename):
    Res=[]
    with open(filename) as f:
        content = f.readlines()
        # Show the file contents line by line.
        # We added the comma to print single newlines and not double newlines.
        # This is because the lines contain the newline character '\n'.
    for line in content:
        #print(line)
        line1=line.strip()
        line2=line1.split(" ")
        #print(line2)
        Res.append(float(line2[0]))
    return Res

class SnaptoCursor(object):
    def __init__(self, ax, x, y):
        self.ax = ax
        self.ly = ax.axvline(color='k', alpha=0.2)  # the vert line
        self.marker, = ax.plot([0],[0], marker="o", color="crimson", zorder=3) 
        self.x = x
        self.y = y
        self.txt = ax.text(0.7, 0.9, '')

    def mouse_move(self, event):
        if not event.inaxes: return
        x, y = event.xdata, event.ydata
        indx = np.searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        self.ly.set_xdata(x)
        self.marker.set_data([x],[y])
        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        self.txt.set_position((x,y))
        self.ax.figure.canvas.draw_idle()



 

def main():  
    # Provide the location of datafile 
    #data = 'demofile5001.txt'
    data=findfile('demo*.txt','/home/novello')
    #data=find('demofile*.txt', '/home/novello')
    print(data)
    i=0
    Errore=[]
    Name=[]
    F=[]
    print(data)
    while(i<len(data)):
        A=readfile(data[i])
        if (len(A)<(20000*5)):
            #print(len(A))
            F.append(butter_lowpass_filter(A, 1000, 16000, 8))
            plt.plot(A)
        else:
            print("errore %d",i)
            Errore.append(A)
            Name.append(data[i])
            print(data[i])
        i=i+1
    plt.show()
    k=0
    while(k<len(Errore)):
        t=[]
        i=0
        while(i<len(Errore[k])):
          t.append(i/16000.0)
          i=i+1
        fig, ax = plt.subplots()
        #cursor = Cursor(ax)
        cursor = SnaptoCursor(ax, t, Errore[k])
        cid =  plt.connect('motion_notify_event', cursor.mouse_move)
        ax.plot(t, Errore[k],)
        #plt.axis([0, 1, -1, 1])
        plt.title(Name[k])
        plt.grid(True)
        plt.xlabel('time')
        plt.ylabel('Volts')
        plt.show()
        k=k+1
    i=0      
    while(i<len(Errore)):
        plt.plot(Errore[i])
        i=i+1
    plt.show()

    i=0      
    while(i<len(F)):
        plt.plot(F[i])
        i=i+1
    plt.show()


if __name__ == "__main__":
    main()
