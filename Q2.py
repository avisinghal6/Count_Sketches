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
import heapq

random.seed(2315); 
# print(os.path.abspath(os.getcwd())) 
path=os.path.abspath(os.getcwd())+"/user-ct-test-collection-01.txt";
data = pd.read_csv(path, sep="\t");
querylist = data.Query.dropna();
# print(querylist.shape);

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
        self.heap=[];
        heapq.heapify(self.heap);
        self.heap_dict={};
        # self.dictionary={};
        for i in range(d):
            self.hash.append(self.hashfunc(r));
            self.sketch.append([0] * r );

    def insert(self,x,type):
        for i in range(self.d):
            self.sketch[i][self.hash[i](x)]+=1;
        
        c=self.query(x,type);
        if self.heap_dict.__contains__(x):
            self.heap_dict[x][0]+=1;
            heapq.heapify(self.heap);
        else:
            dp=[c,x];
            if len(self.heap)==0:
                self.heap_dict[x]=dp;
                heapq.heappush(self.heap,dp);
            else:
                min=self.heap[0];
                
                if c>min[0] and len(self.heap)<500:
                    self.heap_dict[x]=dp;
                    heapq.heappush(self.heap,dp);
                elif c>min[0] and len(self.heap)==500:
                    rem=heapq.heappop(self.heap);
                    del self.heap_dict[rem[1]];
                    heapq.heapify(self.heap);
                    heapq.heappush(self.heap,dp);
                    self.heap_dict[x]=dp;
        # print(x,self.heap);

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
        self.heap=[];
        self.sketch=[];
        self.heap_dict={};
        heapq.heapify(self.heap);
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
        
        c=self.query(x);
        if self.heap_dict.__contains__(x):
            self.heap_dict[x][0]+=1;
            heapq.heapify(self.heap);
        else:
            dp=[c,x];
            if len(self.heap)==0:
                self.heap_dict[x]=dp;
                heapq.heappush(self.heap,dp);
            else:
                min=self.heap[0];
                
                if c>min[0] and len(self.heap)<500:
                    self.heap_dict[x]=dp;
                    heapq.heappush(self.heap,dp);
                elif c>min[0] and len(self.heap)==500:
                    rem=heapq.heappop(self.heap);
                    del self.heap_dict[rem[1]];
                    heapq.heapify(self.heap);
                    heapq.heappush(self.heap,dp);
                    self.heap_dict[x]=dp;

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
# print(querylist[:3])
for s in querylist:
    # print(s);
    li=s.split(" ");
    for l in li:
        dict_obj.insert(l);

FREQ=dict_obj.freq100();
INFREQ=dict_obj.infreq100();
RAND=dict_obj.rand100();
X=[];
Y=[];
# print(FREQ)

#,2**14,2**18
for i in [2**10,2**14,2**18]:
    MinSketch=MINSketches(5,i);
    MedianSketch=MINSketches(5,i);
    CountSketch=CountSketches(5,i);
    for s in querylist:
        li=s.split(" ");
        for l in li:
            MinSketch.insert(l,'min');
            MedianSketch.insert(l,'median');
            CountSketch.insert(l);

    x=[]
    y=[]    
    sorted_list=MinSketch.heap;
    sorted_list3=MedianSketch.heap;
    sorted_list2=CountSketch.heap;
    # print(sorted_list)
    ans=0;
    ans2=0;
    ans3=0;
    for j in FREQ:
        s,c=j;
        for k in sorted_list:
            if s==k[1]:
                ans+=1;
        for k in sorted_list2:
            if s==k[1]:
                ans2+=1;
        for k in sorted_list3:
            if s==k[1]:
                ans3+=1;
    
    x.append(i)
    x.append(i)
    x.append(i)
    
    y.append(ans)
    y.append(ans2)
    y.append(ans3)
    X.append(x);
    Y.append(y);
    # print(x)
    
# print(X)    
plt.figure();
color=["r","g","b"]
label=["minSketch","countSketch","medianSketch"]
plt.scatter(X[0][0], Y[0][0],c=color[0],label=label[0]);
plt.scatter(X[0][1], Y[0][1],c=color[1],label=label[1]);
plt.scatter(X[0][2], Y[0][2],c=color[2],label=label[2]);
for i in [1,2]:
    plt.scatter(X[i][0], Y[i][0],c=color[0]);
    plt.scatter(X[i][1], Y[i][1],c=color[1]);
    plt.scatter(X[i][2], Y[i][2],c=color[2]);
    
# plt.scatter(X[1], Y[1],c=["r","g","b"]);
# plt.scatter(X[2], Y[2],c=["r","g","b"]);
# plt.plot(X[1], Y[1]);
# plt.plot(X[2], Y[2]);
# plt.plot(x, y2,'g',label='mediansketch');
plt.legend(loc="upper left")
# plt.title("Max 100 Frequency :%s"%i);
plt.xlabel('Memory');
plt.ylabel('Intersection');

plt.show()

