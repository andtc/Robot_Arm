
# coding: utf-8

# # Static Load Calculation

# This code is used to calculate the static loads of the arm to find the holding torque required in each joint. The code outputs the Torque of DOF 2-5 in kg-cm, N-m and oz-in
# 
# Inputs: The Material Specification allows user to type in the Cross sectional area of the arm material to be used and the sproperties of said arm Material
# 
# The next section consists of the inputs for each arm segment where Degree of Freedom(DOF) 1 is located at the base and DOF 5 is the end effector
# 
# DOF 1 is not included in this code since it is not part of the arm so it plays no role on the holding torque of the arm.
# DOF 2-4 have the same inputs of Arm,Motor,Igus Joint Mass and Length whereas DOF 5 has an additional input for the load to be carried

# ## Libraries

# In[1]:


import pandas as pd
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


# ## Constants

# In[2]:


g=9.81#gravity m/s^2
I=1 #Second Moment of Inertia
E=1 #Elastic Modulus


# ## Material Specifications

# In[3]:


Area=19.19 #cm^2
rho=2.7 #material Density in g/cm^3
wg=(rho*Area)/1000 #Weight per unit length kg/cm


# # Degree of Freedom Parameters

# The first degree (base) is not included since it is rotary and does not contribute to torque calculations
# 
# Glossary:
# 
# L= Length of Arm in cm
# 
# IJ= Igus Joint Mass in kg
# 
# AW= Arm Mass in kg
# 
# MW= Motor Mass kg
# 
# CW= Combined Mass of Igus and Motor kg
# 
# WJ= Weight of joint N
# 
# AW= Arm Weight N

# ## 2nd Degree

# In[4]:


IJ2=2.05
MW2=1.2
CW2=IJ2+MW2
WJ2=CW2*g


# ## 3rd Degree

# In[5]:


L12=6#cm
L820=14.2#cm
L11=16.2#cm
IJ3=0.79
W12=.09#kg mass of section connecting 820 to RLD 30
Wv=.66#kg mass of Vacuum
W820=.2#kg mass of 820 section
W11=.39#kg mass of connection piece
MW3=1.3 #kg mass of motor and mount
CW3=IJ3+MW3
WJ3=CW3*g
AW12=W12*g
WV=Wv*g
AW820=W820*g
AW11=W11*g


# ## 4th Degree

# In[6]:


L4=18.8
IJ4=0.41
AM4=0.2763
MW4=1.2
CW4=IJ4+MW4
WJ4=CW4*g
AW4=AM4*g


# ## 5th Degree

# In[7]:


L5=18#cm
IJ5=0#no Joint
AM5=0.082#Arm Mass kg
MW5=1.2#Motor Weight
CW5=IJ5+MW5
WJ5=CW5*g#Weight N
AW5=AM5*g#Weight N
CM5=12.38#cm Center of Mass


# ## End Effector

# In[8]:


Me=0.6#kg
Load=1#kg
We=Me*g#N
F=Load*g#N
mmt=0.040#mass of end effector mount
Wmt=mmt*g#N


# ## Weight

# In[9]:


WT=F+Wmt+We+AW5+WJ5+WJ4+AW4+WJ3+AW11+WV+AW820+AW12+WJ2


# In[10]:


print('Weight of Arm=',"%.2f" % WT,'N' )
MA=WT/g
print('Mass of Arm=',"%.2f" % MA,'kg' )


# ## Center of Mass Distance

# In[11]:


x1=10.66#cm
x2=7.69#cm
x3=22.01#cm
x4=19.04#cm
x5=11.35#cm
x6=11.33#cm
x7=25.91#cm
x8=6.91#cm
x9=33.22#cm
x10=25.18#cm
x11=20.87#cm
x12=18.09#cm
x13=4.33#cm
Lmax=L12+L11+L820+L4+L5+x1
print('Lmax=','%.2f'% Lmax,'cm')


# ## Torque Calculations

# In[12]:


T5=((We+F)*x1+Wmt*x2)/g
T4=((We+F)*x3+Wmt*x4+WJ5*x5+AW5*x6)/g
T3=((We+F)*(x7+x3)+Wmt*(x7+x4)+WJ5*(x7+x5)+AW5*(x7+x6)+WJ4*x7+AW4*x8)/g
T2=((We+F)*(x9+x7+x3)+Wmt*(x9+x7+x4)+WJ5*(x9+x7+x5)+AW5*(x9+x7+x6)+WJ4*(x9+x7)+AW4*(x9+x8)+(WJ3*x9)+AW12*x10+WV*x11+AW820*x12+AW11*x13)/g


# ## Print Results

# In[13]:


T={ 'kg-cm': [round(T2,2),round(T3,2),round(T4,2),round(T5,2)],'N-m': [round(T2*.0981,2),round(T3*.0981,2),round(T4*.0981,2),round(T5*.0981,2)],'oz-in': [round(T2*13.89,2),round(T3*13.89,2),round(T4*13.89,2),round(T5*13.89,2)]}
pd.DataFrame(data=T,columns=['kg-cm','N-m','oz-in'], index=['DOF2', 'DOF3', 'DOF4', 'DOF5'])


# ## Igus Calculations

# ### RLD-50-S-48-ST

# In[14]:


GR50S=48#Gear Ratio
MT50S=50#N m
Eff50S=0.35 #Efficiency


# ### RLD-30-S-50-ST

# In[15]:


GR30S=50#Gear Ratio
MT30S=20#N m
Eff30S=0.35 #Efficiency


# ### RLD-20-S-38-ST

# In[16]:


GR20S=38#Gear Ratio
MT20S=20#N m
Eff20S=0.40 #Efficiency


# ## Stepper Motors Torque Equations

# ### NEMA 23: 23HS22-2804D-E1000

# In[17]:


x=sym.symbols ('x')#x in RPM
Motor23=0.0007*x+0.8765#N-m


# ### NEMA 34: 34HS31-5504D-E1000

# In[18]:


y=sym.symbols('y')#y in  RPM
Motor34=3E-14*y**5 - 9E-11*y**4 + 9E-8*y**3 - 4E-5*y**2 - 0.0004*y + 3.0134 #N-m


# ## DOF 1 Rotary Base Joint: RLD-50-A-48-ST

# In[19]:


#Input
ARPM1=6#RPM of Arm
TN1=6.06# N-m Torque needed at Base
#Output
MRPM1=ARPM1*GR50S
TM1=Motor23.subs({x:MRPM1})
TT1=Eff50S*TM1*GR50S


# ## DOF 2 1st Arm Degree:RLD-50-S-48-ST

# In[20]:


#Input
ARPM2=3#RPM of Arm
TN2=30.7# N-m Torque needed 1st Joint
#Output
MRPM2=ARPM2*GR50S
TM2=Motor34.subs({y:MRPM2})
TT2=Eff50S*TM2*GR50S


# ## DOF 3 2nd Arm Degree: RLD-30-S-50-ST

# In[21]:


#Input
ARPM3=3#RPM of Arm
TN3=10# N-m Torque needed at 2nd Joint
#Output
MRPM3=ARPM3*GR30S
TM3=Motor23.subs({x:MRPM3})
TT3=Eff30S*TM3*GR30S


# ## DOF 4 Arm 3rd Degree: RLD-20-S-ST

# In[22]:


#Input
ARPM4=12#RPM of Arm
TN4=1.5# N-m Torque needed at 2nd Joint
#Output
MRPM4=ARPM4*GR20S
TM4=Motor23.subs({x:MRPM4})
TT4=Eff20S*TM4*GR20S


# ## DOF 5 4rd Arm Degree: NEMA 23

# In[23]:


#Input
MRPM5=400#RPM
TN5=.08#N-m
#Output
TM5=Motor23.subs({x:MRPM5})


# In[24]:


IG={ 'Joint RPM': [round(ARPM1,2),round(ARPM2,2),round(ARPM3,2),round(ARPM4,2),0],'Motor RPM': [round(MRPM1,2),round(MRPM2,2),round(MRPM3,2),round(MRPM4,2),round(MRPM5,2)],'Torque Transfered(N-m)': [round(TT1,2),round(TT2,2),round(TT3,2),round(TT4,2),round(TM5,2)],'Torque Needed(N-m)': [round(TN1,2),round(T2*.0981,2),round(T3*.0981,2),round(T4*.0981,2),round(T5*.0981,2)]}
pd.DataFrame(data=IG,columns=['Joint RPM','Motor RPM','Torque Transfered(N-m)','Torque Needed(N-m)'], index=['DOF1','DOF2', 'DOF3', 'DOF4', 'DOF5'])


# # Inertia Calculations

# Inertia Ratio=Inertia Load/Inertia Motor
# 
# Inertia Motor=Inertia Load/(Gear Ratio^2)
# 
# Inertia Ratio must be less than 10 for it to be safe

# ## Equations

# In[25]:


Jl,R,Jm,JM=sym.symbols('Jl,R,Jm,JM')

IR=Jl/JM
Jm=Jl/R**2


# ## Constants

# In[26]:


JNEMA23=300#g*cm^2
JNEMA34=1400#g*cm^2


# In[27]:


# All Inertias are in g*cm^2
IDOF1=29700
IDOF2=27200
IDOF3=27200
IDOF4=4345
IDOF5=653.2


# In[28]:


Jm1=Jm.subs({Jl:IDOF1,R:GR50S})
Jm2=Jm.subs({Jl:IDOF2,R:GR50S})
Jm3=Jm.subs({Jl:IDOF3,R:GR30S})
Jm4=Jm.subs({Jl:IDOF4,R:GR20S})


# In[29]:


IR1=IR.subs({Jl:Jm1,JM:JNEMA23})
IR2=IR.subs({Jl:Jm2,JM:JNEMA34})
IR3=IR.subs({Jl:Jm3,JM:JNEMA23})
IR4=IR.subs({Jl:Jm4,JM:JNEMA23})  
IR5=IR.subs({Jl:IDOF5,JM:JNEMA23})


# In[30]:


IC={ 'Inertia Ratio': [round(IR1,3),round(IR2,3),round(IR3,3),round(IR4,3),round(IR5,3)]}
pd.DataFrame(data=IC, index=['DOF1','DOF2', 'DOF3', 'DOF4', 'DOF5'])

