#!/usr/bin/env python
# coding: utf-8

# ## Upload CSV Files

# In[73]:


import pandas as pd

filepath = 'C:/Users/CarolineSpears/Desktop/Virginia Papers/Code Solution/'

district_filename = 'Names_Districts_Counties.csv'
asthma_filename = 'Asthma_Data_ALA_6.26.2019.csv'
poll_filename = 'Yale_Polling.csv'


# In[79]:


district = pd.read_csv(filepath + district_filename, encoding = "ISO-8859-1")
asthma = pd.read_csv(filepath + asthma_filename, encoding = "ISO-8859-1")
poll = pd.read_csv(filepath + poll_filename, encoding = "ISO-8859-1")

#print(district.head(5))
#print(asthma.head(5))
#print(poll.head(5))


# ## Clean County Lists
# 

# In[80]:


c_district = district['Counties']
c_asthma = asthma['County']
c_poll = list(poll['GeoName'])

c_asthma = list(c_asthma.drop(labels=133))

#Clean up district values
c_district = pd.Series(c_district.str.split(pat=","))

district_counties = []
for i in range(len(c_district)):
    a = c_district[i]
    for j in range(len(a)):
        district_counties.append(a[j])

district_counties = pd.Series(district_counties).str.replace(pat=' County', repl='')
district_counties = pd.Series(district_counties).str.strip()
district_counties = district_counties.unique()
district_counties = list([i for i in district_counties if i])


# ## Match each district with a dictionary of its respective counties

# # Asthma

# ## Sum childhood, adult, and total asthma for the counties that make up each district

# Text: In the four counties that make up House District 100, 10,000 kids and 20,000 adults live with asthma.

# # Polling

# ## Create a weighted average of polling results for the counties that make up each district

# Text: 
# 
# In the counties that make up this district, [weighted average]% know that global warming is happening, and [weighted average] are somewhat or very worried about it. [weighted average]% support regulating CO2 as a pollutant, and [weighted average] want to provide tax rebates for people who purchase energy-efficient vehicles or solar panels. 
# 
# 
# - Number of people who know that global warming is happening: 
#     - [[x%]] in [[least populous county]], and [[y%]] in [[most populous county]]
# - Percent who are somewhat or very worried about climate change: 
#     - [[x%]] in [[least populous county]], and [[y%]] in [[most populous county]]
# - Support regulating CO2 as a pollutant: 
#     - [[x%]] in [[least populous county]], and [[y%]] in [[most populous county]]
# - Support tax rebates for people who purchase energy-efficient vehicles or solar panels: 
#     - [[x%]] in [[least populous county]], and [[y%]] in [[most populous county]]
# 

# Corresponding column headers in the polling file:
# - Total County Population: TotalPop
# 
# 
# - Know that GW is happening: 'happening'
# - Somewhat/very worried: 'worried'
# - Regulate CO2 as a pollutant: 'regulate'
# - Support tax rebates for vehicles/panels: 'rebates'

# # Opposition Research

# 1. Build out an excel file with the following:
#    - Name of incumbent
#    - Important bills, and a vote (positive/negative)
#    - 2 descriptions for each bill: positive and negative
#    - The correct description to use, based on the vote history
# 
# 2. Match incumbent names into the correct description, then add all descriptions together to create an opposition research paragraph that looks like this:
# 
# When it comes to common sense clean energy reforms, [[incumbent]] has a mixed record. They voted to block Virginia from entering regional collaborative efforts to combat climate change, specifically by voting to prevent Virginia from entering the Regional Greenhouse Gas Initiative. States already in this program have seen lower electricity bills and less pollution – joining it is a no-brainer. [[He/She]] also voted against integrating environmental education into Virginia's classrooms. 
# 
# However, [[incumbent]]’s record is not all bad. [[incumbent last name]] voted to ensure that the State Corporation Commission cannot reject or cut climate-forward legislation without reason. They also voted to establish a Clean Energy Advisory Board, which will run a pilot program to allow low-to-moderate income households to receive rebates for solar panels. Finally, [[Incumbent]] voted to ensure that coal plants dispose of coal ash– one of the largest types of industrial waste generated in the United States– safely and sustainably.
# 
# 

# In[ ]:




