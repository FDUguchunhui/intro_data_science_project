#!/usr/bin/env python
# coding: utf-8

# In[5]:


from Bio import Entrez, Medline
import pandas as pd
import csv
import os


# In[6]:


# extract the PMIDs of the papers
def get_id(db, key, daterange=('2020/01/01', '2020/08/30')):
    Entrez.email = "ruoxing.li@uth.tmc.edu"
    handle = Entrez.esearch(
        db=db,
        mindate=daterange[0],
        maxdate=daterange[1],
        datetype = 'pdat',
        term=key)
    results = Entrez.read(handle)
    # get the count of all papers
    count = results['Count']
    # get the ids of all papers 
    handle = Entrez.esearch(
        db=db,
        mindate=daterange[0],
        maxdate=daterange[1],
        datetype = 'pdat',
        retmax=count,
        term=key)
    results = Entrez.read(handle)
    return results

# extract the details of the papers
def get_paper(id_list):
    ids = ','.join(id_list)
    Entrez.email = "ruoxing.li@uth.tmc.edu"
    handle = Entrez.efetch(db='pubmed',
                           rettype='medline',
                           retmode='text',
                           id=ids)
    results = Medline.parse(handle)
    return results

# input: medline generator
# output: csv file containing 'title, authors and publication time' of the papers
def get_csv(papers, csv_fname):
    df = pd.DataFrame.from_dict(papers)
    df_f = df[['TI', 'FAU', 'DP', 'AB']]
    results = df_f.to_csv(csv_fname)
    return results



def query(keyword, time_window, file):
    '''
    query papers for the given conditions and save the result in the given directory in csv format
    keyword stirng:
    time_window tuple: a tuple of length two, the first is the start data and second is the end date in format YYYY/MM/DD
    file string: directory to save the result csv file
    '''
    ids = get_id(db='pubmed', key=keyword, daterange=time_window)
    papers = get_paper(ids['IdList'])
    get_csv(papers, file)
    
    

# test
# query('HIV', ('2020/01/01', '2020/08/30'), 'HIV.csv')
    
# if __name__ == '__main__':
#     ids = get_id(db='pubmed', key='HIV', daterange=('2020/01/01', '2020/08/30'))
#     papers = get_paper(ids['IdList'])
#     get_csv(papers, 'HIV.csv')


# In[ ]:




