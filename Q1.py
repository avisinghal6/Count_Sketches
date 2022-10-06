import csv
from tokenize import String
from typing import List
import pandas as pd
import random;
import os;
from sklearn.utils import murmurhash3_32;
# import mmh3;
import numpy as np;
from bitarray import bitarray
import math;
import string;
import matplotlib.pyplot as plt;
import sys
import statistics
from sympy import Min;

random.seed(2315); 
path=os.path.abspath(os.getcwd())+"/user-ct-test-collection-01.txt";
data = pd.read_csv(path, sep="\t");
querylist = data.Query.dropna();


class dict_func:
    def __init__(self):
        self.dictionary={};

    def insert(self,x):
        self.dictionary[x]=self.dictionary.get(x,0)+1;

    def freq100(self):
        dict=list(sorted(self.dictionary.items(), key=lambda item: item[1],reverse=True));
        sorted_dict=[];
        for i in range(100):
            sorted_dict.append(dict[i]);
        return sorted_dict;

    def infreq100(self):
        dict=list(sorted(self.dictionary.items(), key=lambda item: item[1]));
        sorted_dict=[];
        for i in range(100):
            sorted_dict.append(dict[i]);
        return sorted_dict;

    def rand100(self):
        dictionary_keys = list(self.dictionary.keys());
        unsorted_dict=[];
        for i in range(100):
            s=dictionary_keys[random.randrange(1,len(dictionary_keys))];
            unsorted_dict.append((s,self.dictionary.get(s)));
        return unsorted_dict;
    

class MINSketches:

    def __init__(self,d,r):
        self.d=d;
        self.r=r;
        self.count=0;
        self.hashseed=random.randint(1,500);
        self.hash=[];
        self.sketch=[];
        # self.dictionary={};
        for i in range(d):
            self.hash.append(self.hashfunc(r));
            self.sketch.append([0] * r );

    def insert(self,x):
        for i in range(self.d):
            self.sketch[i][self.hash[i](x)]+=1;
        # print(x,self.dictionary[x])
    def query(self,x,type):
        if(type=='min'):
            m=sys.maxsize;
            for i in range(self.d):
                m=min(m,self.sketch[i][self.hash[i](x)]);
            return m;
        else:
            medlist=[];
            for i in range(self.d):
                medlist.append(self.sketch[i][self.hash[i](x)]);
            return statistics.median(medlist);
 
    def hashfunc(self,m):
        a=self.hashseed+self.count;
        self.count=self.count+1;
        def murmur(x):
            #print(a);
            return murmurhash3_32(x,a,True) % m ;
        return murmur;

class CountSketches:

    def __init__(self,d,r):
        self.d=d;
        self.r=r;
        self.count=0;
        self.hashseed=random.randint(1,500);
        self.hashseed2=random.randint(1,500);
        self.hash=[];
        self.hash2=[];
        self.sketch=[];
        # self.dictionary={};
        for i in range(d):
            self.hash.append(self.hashfunc(r));
            self.hash2.append(self.hashfunc(2));
            self.sketch.append([0] * r );

    def insert(self,x):
        for i in range(self.d):
            sign=self.hash2[i](x);
            if sign==1:
                self.sketch[i][self.hash[i](x)]+=1;
            else:
                self.sketch[i][self.hash[i](x)]-=1;

        # print(x,self.dictionary[x])
    def query(self,x):
        medlist=[];
        for i in range(self.d):
            sign=self.hash2[i](x);
            if sign==1:
                medlist.append(self.sketch[i][self.hash[i](x)]);
            else:
                medlist.append(-1*self.sketch[i][self.hash[i](x)]);
            
        return statistics.median(medlist);
 
    def hashfunc(self,m):
        a=self.hashseed+self.count;
        self.count=self.count+1;
        def murmur(x):
            return murmurhash3_32(x,a,True) % m ;
        return murmur;
    def hashfunc2(self,m):
        a=self.hashseed2+self.count;
        self.count=self.count+1;
        def murmur(x):
            #print(a);
            return murmurhash3_32(x,a,True) % m ;
        return murmur;


dict_obj=dict_func();
for s in querylist:
    li=s.split(" ");
    for l in li:
        dict_obj.insert(l);

# print(len(dict_obj.dictionary));
FREQ=dict_obj.freq100();
INFREQ=dict_obj.infreq100();
RAND=dict_obj.rand100();
X=[];
Y=[];
for i in [2**10,2**14,2**18]:
    MinSketch=MINSketches(5,i);
    MedianSketch=MINSketches(5,i);
    CountSketch=CountSketches(5,i);
    for s in querylist:
        li=s.split(" ");
        for l in li:
            MinSketch.insert(l);
            CountSketch.insert(l);
            MedianSketch.insert(l);
            
    x=[]
    y1=np.zeros(100);
    y2=np.zeros(100);
    y3=np.zeros(100);
    for j in range(100):
        s,c=FREQ[j];
        sc1=MinSketch.query(s,'min')
        sc2=CountSketch.query(s)
        sc3=MedianSketch.query(s,'median');
        y1[j]=abs(sc1-c)/c;
        y2[j]=abs(sc2-c)/c;
        y3[j]=abs(sc3-c)/c;
        x.append(s);
    plt.figure();
    plt.plot(x, y1,'r',label='minsketch');
    plt.plot(x, y2,'g',label='countsketch');
    plt.plot(x, y3,'b',label='mediansketch');
    plt.legend(loc="upper left")
    plt.title("Max 100 Frequency :%s"%i);
    plt.xlabel('Words');
    plt.ylabel('Error');

    x=[]
    y1=np.zeros(100);
    y2=np.zeros(100);
    for j in range(100):
        s,c=INFREQ[j];
        sc1=MinSketch.query(s,'min')
        sc2=CountSketch.query(s)
        sc3=MedianSketch.query(s,'median');
        y1[j]=abs(sc1-c)/c;
        y2[j]=abs(sc2-c)/c;
        y3[j]=abs(sc3-c)/c;
        x.append(s);
    plt.figure();
    plt.plot(x, y1,'r',label='minsketch');
    plt.plot(x, y2,'g',label='countsketch');
    plt.plot(x, y3,'b',label='mediansketch');
    plt.legend(loc="upper left")
    plt.title("Lowest 100 Frequency :%s"%i);
    plt.xlabel('Words');
    plt.ylabel('Error');

    x=[]
    y1=np.zeros(100);
    y2=np.zeros(100);
    for j in range(100):
        s,c=RAND[j];
        sc1=MinSketch.query(s,'min')
        sc2=CountSketch.query(s)
        sc3=MedianSketch.query(s,'median');
        y1[j]=abs(sc1-c)/c;
        y2[j]=abs(sc2-c)/c;
        y3[j]=abs(sc3-c)/c;
        x.append(s);
    plt.figure();
    plt.plot(x, y1,'r',label='minsketch');
    plt.plot(x, y2,'g',label='countsketch');
    plt.plot(x, y3,'b',label='mediansketch');
    plt.legend(loc="upper left")
    plt.title("Random 100 Frequency :%s"%i);
    plt.xlabel('Words');
    plt.ylabel('Error');

plt.show()

