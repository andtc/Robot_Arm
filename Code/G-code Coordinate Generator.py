
# coding: utf-8

# # This code is to generate G-Code for the arm designed

# In[176]:


import sympy as sym
import numpy as np
import pandas as pd
pi=np.pi


# ## Lengths

# In[177]:


L1=3.68#cm Base Height
L2=36#cm
L3=19.8#cm
L4=14#cm
L5=13.3#cm


# ## Joint Movement Freedom

# ## Joint 1

# In[178]:


D1min=0
D1max=360


# ## Joint 2

# In[179]:


D2min=-115
D2max=115


# ## Joint 3

# In[180]:


D3min=-105
D3max=105


# ## Joint 4

# In[181]:


D4min=-65
D4max=115


# ## Joint 5

# In[182]:


D5min=0
D5max=360


# ## Define Angles

# In[183]:


DOF1D=np.linspace(D1min,D1max,200)
DOF2D=np.linspace(D2min,D2max,200)
DOF3D=np.linspace(D3min,D3max,200)
DOF4D=np.linspace(D4min,D4max,200)
DOF5D=np.linspace(D5min,D5max,200)


# In[184]:


q1=0
q2=0
q3=0
q4=0
q5=0
q6=0


# In[185]:


# Create Modified DH parameters
alpha0=0
alpha1=-pi/2
alpha2=0
alpha3=0
alpha4=-pi/2
alpha5=0

a0=0
a1=0
a2=L2
a3=0
a4=0
a5=0

d1=L1
d2=0
d3=0
d4=L3
d5=0
d6=L4+L5


# ## Transfer Matrix

# In[186]:


# Define Modified DH Transformation matrix
def TF_Matrix(alpha,a,d,q):
    TF=([[np.cos(q),-np.sin(q),0,a],
    [np.sin(q)*np.cos(alpha),np.cos(q)*np.cos(alpha),-np.sin(alpha),-np.sin(alpha)*d],
    [np.sin(q)*np.sin(alpha),np.cos(q)*np.sin(alpha),np.cos(alpha),np.cos(alpha)*d],
    [0,0,0,1]])
    return TF


# In[187]:


# Create individual transformation matrices
T0_1=np.array(TF_Matrix(alpha0,a0,d1,q1))
T1_2=np.array(TF_Matrix(alpha1,a1,d2,q2))
T2_3=np.array(TF_Matrix(alpha2,a2,d3,q3))
T3_4=np.array(TF_Matrix(alpha3,a3,d4,q4))
T4_5=np.array(TF_Matrix(alpha4,a4,d5,q5))
T5_EE=np.array(TF_Matrix(alpha5,a5,d6,q6))


# In[188]:


# Extract rotation matrices from the transformation matrices
T0_EE=T0_1*T1_2*T2_3*T3_4*T4_5*T5_EE


# In[189]:


print(T0_EE)

