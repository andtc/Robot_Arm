
# coding: utf-8

# # Torque Calculations Ver 2.0

# Author: Andres Tapia

# This code was built since the previous code needed too many changes to update thus this new code will be used for the V4.0 Arm developed

# ## Libraries

# In[26]:


import pandas as pd
import numpy as np
import sympy as sym


# ## Constants

# Define constants such as gravity

# In[27]:


g=9.81 #m/s^2 gravity


# ## Motors

# Define Weights of Motors

# In[28]:


NEMA23=0.8#kg
NEMA34=2.65# kg 
NEMA17=0.39#kg 
NEMA17Geared=0.5#kg


# # Igus Joints

# ## RLD-50

# In[29]:


RLD50W=2.05#kg
N50=48#Gear Ratio


# ## RLD-30

# In[30]:


RLD30W=0.79#kg
N30=50#Gear Ratio


# ## RLD-20

# In[31]:


RLD20W=0.41#kg
N20=38#Gear Ratio


# ## NEMA 17 Geared

# In[32]:


N17=27 #Gear Ratio


# # Arm Calculations

# ## Define Joints

# ## Joint 1

# In[33]:


J1=RLD50W*g


# ## Joint 2

# In[34]:


AS2=0.308#kg Arm Segment mass
J2=(NEMA34+RLD50W)*g# N
A2=2*AS2*g#N
L2=36#cm RLD50 to RLD30
x5=18.98#cm RLD50 to center of mass of arm segment


# ## Joint 3

# In[35]:


AS3=0.518#kg arm segment mass
J3=(NEMA17+RLD30W)*g# N
A3=2*AS3*g#N 2 arm segments
L3=19.8#cm RLD30 to RLD 20
x4=10.8#cm RLD30 to Center of mass of arm segments


# ## Joint 4

# In[36]:


AS4=0.093#kg Arm segment mass
J4=(RLD20W+NEMA17)*g# N
A4=2*AS4*g# N 2 arm segments
L4=14#cm RLD-20 to Joint 5
x3=7.5#cm RLD20 to Center of mass of arm segments


# ## Joint 5

# In[37]:


AS5=0.04#kg Arm segment mass
J5=NEMA17Geared*g# N
A5=AS5*g# N
We=.23*g# N
x1=13.3#cm Motor to End Effector
x2=9.7#cm Motor to Mount
L5=6.5#cm Length from Motor to tip of End Effector


# ## Load

# In[38]:


ml=2#kg
Fl=ml*g#N


# ## Torque Calculations

# In[39]:


T5=(We*x1+A5*x2+Fl*L5)/100
T4=(We*(L4+x1)+(A5*(L4+x2))+(J5*L4)+(A4*x3)+(Fl*(L5+L4)))/100
T3=(We*(L3+L4+x1)+(A5*(L3+L4+x2))+(J5*(L4+L3))+(A4*(L3+x3))+(Fl*(L5+L4+L3)))/100
T2=(We*(L2+L3+L4+x1)+(A5*(L2+L3+L4+x2))+(J5*(L2+L4+L3))+(A4*(L2+L3+x3))+(Fl*(L2+L5+L4+L3)))/100


# In[40]:


T={ 'N-m': [round(T2,2),round(T3,2),round(T4,2),round(T5,2)]}
pd.DataFrame(data=T, index=['DOF2', 'DOF3', 'DOF4', 'DOF5'])


# ## Arm Weights

# In[41]:


W1=J1+J2+J3+J4+J5+A2+A3+A4+A5+We
W2=J2+J3+J4+J5+A2+A3+A4+A5+We
W3=J3+J4+J5+A3+A4+A5+We
W4=J4+J5+A4+A5+We
W5=J5+A5+We


# In[42]:


weight={ 'N': [round(W1,2),round(W2,2),round(W3,2),round(W4,2),round(W5,2)],'kg': [round(W1/g,2),round(W2/g,2),round(W3/g,2),round(W4/g,2),round(W5/g,2)]}
pd.DataFrame(data=weight,columns=['N','kg'], index=['DOF1','DOF2', 'DOF3', 'DOF4', 'DOF5'])


# ## Dynamic Loads

# ### RPM

# In[43]:


RPM1=288
RPM2=240
RPM3=150
RPM4=600
RPM5=1000


# ## Angular Velocity Equation

# In[44]:


RPM=sym.symbols('RPM')
w=(RPM*(2*np.pi))/60


# ## Angular Velocities rad/s

# In[45]:


w1=w.subs({RPM:RPM1})
w2=w.subs({RPM:RPM2})
w3=w.subs({RPM:RPM3})
w4=w.subs({RPM:RPM4})
w5=w.subs({RPM:RPM5})


# ## Angular Accelerations rad/s^2

# In[46]:


a=6*np.pi#rad/s^2
deltat=0.5#sec
a1=a/N50
a2=a/N50
a3=a/N30
a4=a/N20
a5=a/N17


# ## Angular Torque g/cm^2

# In[57]:


#Parrallel Axis Offset
d2=17.75#cm
d3=9.76#cm
d4=6.1#cm
d5=5.72#cm

I1=2065
I2=129740+((A2*1000*100)*d2)
I3=55020+((A3*1000*100)*d3)
I4=4832+((A4*1000*100)*d4)
I5=208.8+((A5*1000*100)*d5)
It1=I1+I2+I3+I4+I5
Lt1=L2+L3+L4+L5
It2=I2+I3+I4+I5
Lt2=L2+L3+L4+L5
It3=I3+I4+I5
Lt3=L3+L4+L5
It4=I4+I5
Lt4=L4+L5
It5=I5
Lt5=L5


# In[64]:


aT1=It1*a1/(1000*100**2)
aT2=It2*a2/(1000*100**2)
aT3=It3*a3/(1000*100**2)
aT4=It4*a4/(1000*100**2)
aT5=It5*a5/(1000*100**2)


# In[65]:


aT={ 'N-m': [round(aT1,3),round(aT2,3),round(aT3,3),round(aT4,3),round(aT5,3)]}
pd.DataFrame(data=aT,columns=['N-m'], index=['DOF1','DOF2', 'DOF3', 'DOF4', 'DOF5'])


# In[60]:


TT1=aT1
TT2=aT2+T2
TT3=aT3+T3
TT4=aT4+T4
TT5=aT5+T5

TT={ 'N-m': [round(TT1,2),round(TT2,2),round(TT3,2),round(TT4,2),round(TT5,2)]}
pd.DataFrame(data=TT,columns=['N-m'], index=['DOF1','DOF2', 'DOF3', 'DOF4', 'DOF5'])

