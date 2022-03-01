# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 23:45:10 2022

@author: ASUS
"""

import numpy as np
import matplotlib.pyplot as plt
import random

X=Y=100 #ابعاد نقشه
nc=10 #number of cities

np.random.seed(2022)
x=np.random.uniform (0,X,nc) #x of cities
y=np.random.uniform (0,Y,nc) #y of cities
np.random.seed() 
p=100 #population

def func (mem):
    mem=np.append(mem,mem[0])
    distance=0
    for i in range (1,len(mem)):
        distance+=((x[mem[i]]-x[mem[i-1]])**2+(y[mem[i]]-y[mem[i-1]])**2)**.5
    return (distance)

def new_mem (nc):
    allc=set(np.arange(nc,dtype=int))
    nm=list(random.sample(allc,nc))
    return (np.array(nm))

def new_society (p):
    soc=new_mem(nc)
    for i in range (1,p):
        soc=np.vstack([soc,new_mem(nc)])
    return (soc)

def mutate (mem):
    allc=set(np.arange(nc,dtype=int))
    nm=list(random.sample(allc,2))
    mem2=[]
    for i in range (0,len(mem)):
        if i == nm[0]:
            mem2.append(mem[nm[1]])
        elif i == nm[1]:
            mem2.append(mem[nm[0]])
        else:
            mem2.append(mem[i])
        
    return (mem2)

def takeout (nums, mem):
    mem2=[]
    for c in mem:
        if c not in nums:
            mem2.append(c)
    return (mem2)

def child (mom, dad):
    
    line= np.random.randint(1,nc-1)
    sp2=takeout(mom [0:line],dad)
    eg2=takeout(dad [0:line],mom)
    sp1=dad [0:line]
    eg1=mom [0:line]
    
    child1= np.append (eg1,sp2)
    child2= np.append (sp1,eg2)
    
    if random.uniform(0, 1)<1/p:
        child1=mutate(child1)
    if random.uniform(0, 1)<1/p:
        child2=mutate(child2)
    
    return (child1,child2)

def measure (soc):
    val=[]
    for mem in soc:
        val.append(func(mem))
    return (np.array(val))

def sort (vals,soc):
    idx = vals.argsort()[::-1]   
    vals = vals[idx]
    soc=np.transpose(soc)
    soc = soc[:,idx]
    soc=np.transpose(soc)
    return (vals[::-1],soc[::-1])

def picker (p): 
    chance= np.random.uniform(0,p*(p+1)/2)
    nn=0
    for n in range (1,p+1):
        if chance> n*(n+1)/2 and chance <(n+1)*(n+2)/2:
            nn=(p-(n))         
    return (nn)

def new_gen(soc,vals):
    newsoc=soc[0:2]
    for i in range (1,int(p/2)):
        mom=soc[picker(p)]
        dad=soc[picker(p)]
        ch1,ch2=child (mom, dad)
        newsoc=np.vstack([newsoc,ch1,ch2])
    vals= measure(newsoc)
    return (sort(vals, newsoc))



soc=new_society(p)
vals=measure(soc)
vals,soc=sort(vals,soc)

avg_val_time=[]
min_val_time=[]
max_val_time=[]
T=[]
for t in range (0,70): #70 generations
    avg_val_time.append(np.average(vals))
    max_val_time.append(np.max(vals))
    min_val_time.append(np.min(vals))
    T.append(t)
    vals,soc=new_gen(soc, vals)

plt.figure()
plt.plot(T,avg_val_time,label='average value')
plt.plot(T,max_val_time,label='maximum value')
plt.plot(T,min_val_time,label='minimum value')
plt.xlabel('generations')
plt.ylabel('values')
plt.legend()
plt.show()