
# coding: utf-8

# # Torque Calculations Ver 2.0

# Author: Andres Tapia

# This code was built since the previous code needed too many changes to update thus this new code will be used for the V4.0 Arm developed

# ## Libraries

# In[139]:


import pandas as pd
import numpy as np
import sympy as sym


# ## Constants

# Define constants such as gravity

# In[140]:


g=9.81 #m/s^2 gravity


# ## Motors

# Define Weights of Motors

# In[141]:


NEMA23=0.8#kg
NEMA34=2.65# kg 
NEMA17=0.24#kg 


# # Igus Joints

# ## RLD-50

# In[142]:


RLD50W=2.05#kg


# ## RLD-30

# In[143]:


RLD30W=0.79#kg


# ## RLD-20

# In[144]:


RLD20W=0.41#kg


# # Arm Calculations

# ## Define Joints

# ## Joint 1

# In[145]:


J1=RLD50W*g


# ## Joint 2

# In[146]:


AS2=0.308#kg Arm Segment mass
J2=(NEMA34+RLD50W)*g# N
A2=2*AS2*g#N
L2=36#cm RLD50 to RLD30
x5=18.98#cm RLD50 to center of mass of arm segment


# ## Joint 3

# In[147]:


AS3=0.518#kg arm segment mass
J3=(NEMA23+RLD30W)*g# N
A3=2*AS3*g#N 2 arm segments
L3=19.8#cm RLD30 to RLD 20
x4=10.8#cm RLD30 to Center of mass of arm segments


# ## Joint 4

# In[148]:


AS4=0.093#kg Arm segment mass
J4=(RLD20W+NEMA23)*g# N
A4=2*AS4*g# N 2 arm segments
L4=14#cm RLD-20 to Joint 5
x3=7.5#cm RLD20 to Center of mass of arm segments


# ## Joint 5

# In[149]:


AS5=0.04#kg Arm segment mass
J5=NEMA17*g# N
A5=AS5*g# N
We=.23*g# N
x1=13.3#cm Motor to End Effector
x2=9.7#cm Motor to Mount
L5=6.5#cm Length from Motor to tip of End Effector


# ## Load

# In[150]:


ml=2#kg
Fl=ml*g#N


# ## Torque Calculations

# In[151]:


T5=(We*x1+A5*x2+Fl*L5)/100
T4=(We*(L4+x1)+(A5*(L4+x2))+(J5*L4)+(A4*x3)+(Fl*(L5+L4)))/100
T3=(We*(L3+L4+x1)+(A5*(L3+L4+x2))+(J5*(L4+L3))+(A4*(L3+x3))+(Fl*(L5+L4+L3)))/100
T2=(We*(L2+L3+L4+x1)+(A5*(L2+L3+L4+x2))+(J5*(L2+L4+L3))+(A4*(L2+L3+x3))+(Fl*(L2+L5+L4+L3)))/100


# In[152]:


T={ 'N-m': [round(T2,2),round(T3,2),round(T4,2),round(T5,2)]}
pd.DataFrame(data=T, index=['DOF2', 'DOF3', 'DOF4', 'DOF5'])

