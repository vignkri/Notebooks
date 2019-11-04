#!/usr/bin/env python
# coding: utf-8

# In[23]:


import pandas as pd
from bs4 import BeautifulSoup as bs


# In[9]:


sample_text = '<TABLE><TR><TD><B>Close cause</B></TD> <TD>Normal Release (0)</TD></TR><TR><TD><B>IMSI</B></TD> <TD>272023118178778</TD></TR><TR> <TD><B>Device IP</B></TD> <TD> 10.2.82.222</TD></TR><TR><TD><B>SGSN/SGW</B></TD> <TD> <SPAN TITLE= "80.251.193.210 ">Hi3G Denmark</SPAN></TD></TR><TR><TD><B>APN</B></TD> <TD> <SPAN TITLE= "Low Bandwidth APN. ">3iot.com</SPAN></TD></TR><TR><TD><B>Bytes</B></TD><TD>1214 Up ,270 Down</TD></TR><TR><TD><B>Duration</B></TD> <TD> 00:00:10</TD></TR><TR><TD><B>GGSN/PGW</B></TD> <TD> <SPAN TITLE= "185.60.124.148 ">HUE_3IE_SAE02</SPAN></TD></TR></TABLE>'


# In[34]:


# -- Test set 1k
test_1k = pd.DataFrame(index=range(0, 1000))
test_1k['desc'] = sample_text
# -- Test set 10k
test_10k = pd.DataFrame(index=range(0, 10000))
test_10k['desc'] = sample_text
# -- Test set 30k
test_30k = pd.DataFrame(index=range(0, 30000))
test_30k['desc'] = sample_text


# In[35]:


get_ipython().run_line_magic('timeit', '-n1 -r3 test_1k.applymap(func=lambda x: bs(x).findAll("td")[11].text)')


# In[37]:


get_ipython().run_line_magic('timeit', '-n1 -r3 test_10k.applymap(func=lambda x: bs(x).findAll("td")[11].text)')


# In[40]:


get_ipython().run_line_magic('timeit', "-n1 -r3 test_1k.desc.str.extract(r'(\\d*) (Up) ,(\\d*) (Down)', expand=True)")


# In[41]:


get_ipython().run_line_magic('timeit', "-n1 -r3 test_10k.desc.str.extract(r'(\\d*) (Up) ,(\\d*) (Down)', expand=True)")


# In[48]:


get_ipython().run_line_magic('timeit', "-n1 -r3 test_30k.desc.str.extract(r'(\\d*) Up ,(\\d*) Down', expand=True)")


# In[ ]:




