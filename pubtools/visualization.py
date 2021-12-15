#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
from plotnine import *

# convert the date to date
# format shoube be %Y %b (%d)
def to_date(pulication_date):
    dates = []
    for x in pulication_date:
        try:
            d = datetime.strptime(x, '%Y %b %d')
        except ValueError:
            try: 
                d = datetime.strptime(x,'%Y %b')
            except ValueError:
                d = None
        dates.append(d)    
    return dates

# read the csv file and print the number of papers by month
def paper_by_month(csv_f):
    hiv_df = pd.read_csv(csv_f, index_col=0)
    hiv_df['date'] = to_date(hiv_df['DP'])
    hiv_df['month'] = hiv_df['date'].dt.to_period('M')
    per_month = hiv_df.groupby(['month'])['month'].count()
    return per_month


# calculate summary statistics 
def summary(csv_f):
    x = paper_by_month(csv_f)
    return{
        'mean': np.mean(x),
        'std': np.std(x),
        'range': (np.min(x), np.max(x)),
        'quantiles': np.quantile(x, [0.25, 0.50, 0.75])
    }


# input should be the output from function paper_by_month
def plot_poisson(csv_f):
    df_month = paper_by_month(csv_f)
    hiv_df_month = df_month.to_frame()
    hiv_df_month = hiv_df_month.rename(columns={'month': 'count'})
    hiv_df_month['month'] = hiv_df_month.index
    hiv_df_month['count_lci'] = stats.poisson.ppf(0.05, df_month.values)
    hiv_df_month['count_rci'] = stats.poisson.ppf(0.95, df_month.values)
    return (
    ggplot(hiv_df_month, aes(x='month', y='count')) +
        theme_classic() +
        geom_col(fill='#990099') +
        geom_errorbar(
            aes(ymin='count_lci', ymax='count_rci'),
            width = 0.3
        ) +
        theme(axis_text_x = element_text(angle=45, hjust=1))
    )

