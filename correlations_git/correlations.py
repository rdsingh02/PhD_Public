#%% importing the libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as pa
from scipy.stats import pearsonr, spearmanr
import os

#%%setting the context
sns.set(style="white", font_scale=1.25)

# reading the data
path = r".xlsx"
da = pd.read_excel(path, sheet_name='') # insert the sheet name here 

#%% cleaning the data
da = da.dropna() # or
# you can apply fillna()
# da = da.fillna(da.mean()) # you may use da.median() OR da.quantile(0.10) OR da.min() 

## Ideally, columns having categorical data should be removed
COLS_list = [] # column names should be in strings # add the names of the columns you want to remove 
da = da.drop(COLS_list, axis = 1) 

#%% defining the functions that will calculate the coefficients
# in this code, we will be calculating the pearson and spearman coefficients

def pearsonr_pval(x,y):
    return pearsonr(x,y)[1]

def spearman_pval(x,y):
    return spearmanr(x,y)[1]

def pearson_r(x,y):
    return pearsonr(x,y)[0]

def spearman_r(x,y):
    return spearmanr(x,y)[0]

#%%create an empty dataframe
# uncomment if you need the r and p values

df=pd.DataFrame()

#create the output excel file 
# we will name a file here and create a path 
opath1 = r".xlsx"

df.to_excel(opath1, sheet_name='dummy')

def corr_plot(data, type, image, excel):
    # type denotes 'spearman'/'pearson'
    # image = 0 if image is to be saved else 1 if image is not to be saved
    # excel = 0 if excel file is to be created or else 1 if we dont need it

    #getting the pvalues and rvalues 
    if type == 'spearman':
        p=data.corr(method=spearman_pval, min_periods=1)
        r=data.corr(method=spearman_r, min_periods=1)
    elif type == 'pearson':
        p=data.corr(method=pearsonr_pval, min_periods=1)
        r=data.corr(method=pearson_r, min_periods=1)

    #
    r_da=pd.DataFrame(r)
    p_da = pd.DataFrame(p)

    #exporting the data to the excel file
    if excel == 0:
        with pd.ExcelWriter(opath1, mode='a') as writer:
            p.to_excel(writer, sheet_name='pvalue')
            r.to_excel(writer, sheet_name='rvalues')

    #creating the mask
    mask = np.triu(np.ones_like(p, dtype=np.bool))
    ## if you are using higher version of python, use dtype=bool

    #initialising the matplotlib functions

    fig, ax= plt.subplots(figsize=(18, 16))

    cut_off= 0.05
    extreme=0.01

    annot=[[('\n')+('' if abs(val) > cut_off else '*') + 
        ('' if abs(val) > extreme else '*') 
        for val in row] 
        for row in  p.to_numpy()]

    #'BrBG'
    # change the colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.heatmap(r, mask=mask, cmap=cmap, 
                vmin=-1, vmax=1, center=0,
                square=True, annot=annot, 
                annot_kws={'size':30, 'color':'k'}, 
                fmt='', linewidths=.75, 
                cbar_kws={"shrink": .5})

    plt.xticks(rotation=90)
    plt.yticks(rotation=0)

    if image == 0:
        savepath = r".png" #change the path for your own computer!
        plt.tight_layout()
        plt.savefig(savepath, dpi=300)

    plt.tight_layout()
    plt.show()

    print('corr matrix has been plotted')

#%% running the function
corr_plot(data = da, type='spearman', image = 0 , excel = 0)
