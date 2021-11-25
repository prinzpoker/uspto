#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import csv


# In[3]:


pd.set_option("display.max_rows", 10, "display.max_columns", None)


# # Melero approach

# ## PatEx - USPTO
# PatEx data are generally representative of the population of patent applications filed in the United States after November 2000 across observable characteristics.
# 
# Different Data sets (we concentrate on three: application_data; all_inventors; status_codes)

# ### application_data

# In[3]:


df_application = pd.DataFrame()
df_application = pd.read_csv("application_data.csv", delimiter = ",")


# In[5]:


df_application.head()


# In[6]:


df_application.shape


# In[ ]:


df_application["application_number"]=df_application["application_number"].astype("string")


# Which columns are useless? -> "invention_title"; "small_entity_indicator" ; "wipo_pub_date"; "wipo_pub_number" => Rest mit Lars besprechen

# In[8]:


df_application.drop(columns = {"invention_title", "small_entity_indicator", "wipo_pub_date", "wipo_pub_number"}, inplace = True)


# ### all_inventors

# In[9]:


df_inventors = pd.DataFrame()
df_inventors = pd.read_csv("all_inventors.csv", delimiter = ",")


# In[26]:


df_inventors.head()


# In[147]:


df_inventors["application_number"]= df_inventors["application_number"].astype("string")


# ### status_codes
# Not included for this version

# In[28]:


df_status = pd.DataFrame()
df_status = pd.read_csv("status_codes.csv", delimiter = ",")


# In[29]:


df_status.head()


# ### merge PatEx

# In[11]:


df_patex = pd.DataFrame()
df_patex = pd.merge(df_inventors, df_application, left_on = "application_number", right_on = "application_number")


# In[35]:


df_patex.shape


# In[153]:


df_patex.head()


# ## Patentsview
# 

# ### application 
# preGrant-Application

# In[17]:


df3_application = pd.DataFrame()
df3_application = pd.read_csv("application_PreGrant.tsv", delimiter = "\t")


# In[20]:


df3_application.head()


# In[21]:


df3_application["application_number"] = df3_application["application_number"].astype("string")


# ### application 
# Grants (not included here)
# 
# id = application_number (delete "/")

# In[8]:


df4_application = pd.DataFrame()
df4_application = pd.read_csv("application.tsv", delimiter = "\t")


# In[9]:


df4_application.head()


# ### assignee & publication_assignee

# In[23]:


df_assignee = pd.DataFrame()
df_assignee = pd.read_csv("assignee.tsv", delimiter="\t") 


# In[24]:


df_assignee.head()


# In[24]:


df_publication_assignee = pd.DataFrame()
df_publication_assignee = pd.read_csv("publication_assignee.tsv", delimiter="\t")


# In[69]:


df_publication_assignee.head()


# ### Merge Patentsview
# without grants

# In[26]:


df_patentsview = pd.DataFrame()
df_patentsview = pd.merge(df3_application, df_publication_assignee, left_on ="document_number",right_on = "document_number")


# In[30]:


df_patentsview = pd.merge(df_patentsview,df_assignee, left_on = "assignee_id", right_on = "id")


# In[33]:


df_patentsview.head()


# In[118]:


df_patentsview["application_number"] = df_patentsview["application_number"].astype("string")


# In[32]:


df_patentsview.shape


# ## Patent Assignment

# ### documentid_admin

# In[39]:


df_document = pd.DataFrame()
df_document = pd.read_csv("documentid_admin.csv")


# In[85]:


df_document.head()


# In[40]:


### Clean dataframe -> preperation for merge with Patentsview-data

df_document =df_document.loc[df_document.appno_doc_num.isna()==False, :]
df_document = df_document.loc[df_document.error != "incorrect appno_doc_num",:]
df_document.appno_doc_num = df_document.appno_doc_num.astype("string")
df_document.appno_doc_num= df_document.appno_doc_num.str.replace(".","")


# In[42]:


df_document.shape


# ### assignee

# In[43]:


###Assignee -> University
df3_assignee = pd.DataFrame()
df3_assignee = pd.read_csv("assignee.csv")


# In[90]:


df3_assignee.head()


# ### assignor

# In[44]:


###Assignor -> Researcher (?)
df_assignor = pd.DataFrame()
df_assignor = pd.read_csv("assignor.csv")


# In[92]:


df_assignor.head()


# ### Merge Patent Assignment

# In[45]:


df_assignment = pd.DataFrame()
df_assignment = pd.merge(df3_assignee, df_assignor, left_on = "rf_id", right_on ="rf_id")


# In[46]:


df_assignment.head()


# In[61]:


df_assignment = pd.merge(df_assignment, df_document, left_on = "rf_id", right_on = "rf_id")


# In[99]:


df_assignment.shape


# In[50]:


df_assignment.head()


# In[49]:


df_assignment["rf_id"]= df_assignment["rf_id"].astype("string")


# # Merge of all data sets

# In[36]:


df_patent = pd.DataFrame()
df_patent = pd.merge(df_patex, df_patentsview, left_on = "application_number", right_on="application_number" )


# In[38]:


df_patent.shape


# In[51]:


df_patent = pd.merge(df_patent, df_assignment, left_on="application_number", right_on="appno_doc_num")


# In[ ]:


df_patent.head()


# In[ ]:


df_patent.shape

