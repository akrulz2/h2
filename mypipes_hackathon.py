
import pandas as pd
import numpy as np
from datetime import date

from sklearn.pipeline import Pipeline,FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin


class VarSelector(BaseEstimator, TransformerMixin):

    def __init__(self,feature_names):

        self.feature_names=feature_names


    def fit(self,x,y=None):

        return self

    def transform(self,X):

        return X[self.feature_names]

    def get_feature_names(self):

        return self.feature_names

class get_age(BaseEstimator, TransformerMixin):
    def __init__(self):

        self.feature_names=[]
        self.age=0
        self.year=date.today().year

    def fit(self,x,y=None):
        self.feature_names=x.columns
        for  col in x.columns:
            self.median_age=(pd.to_datetime(x[col],errors='coerce').dt.year).median()
        return self

    def transform(self,X):
        dummy_data=x.copy()
        for col in X.columns:
            dummy_data[age]= self.year-(dummy_data[col]).dt.year
            dummy_data[(dummy_data[age]<0 or dummy_data[age]>100) ]=self.median_age
            del dummy_data[col]
        
        return dummy_data
    def get_feature_names(self):
        return self.feature_names

class convert_to_string(BaseEstimator, TransformerMixin):

    def __init__(self):

        self.feature_names=[]

    def fit(self,x,y=None):
        self.feature_names=x.columns
        return self

    def transform(self,X):
        for col in X.columns:
            X[col]= X[col].astype(str)
        return X
    def get_feature_names(self):
        return self.feature_names



class string_clean(BaseEstimator, TransformerMixin):

    def __init__(self,replace_it='',replace_with=''):

        self.replace_it=replace_it
        self.replace_with=replace_with
        self.feature_names=[]

    def fit(self,x,y=None):

        self.feature_names=x.columns
        return self

    def transform(self,X):

        for col in X.columns:
            X[col]=X[col].str.replace(self.replace_it,self.replace_with)
        return X
    def get_feature_names(self):

        return self.feature_names
    


class get_dummies_Pipe(BaseEstimator, TransformerMixin):

    def __init__(self,freq_cutoff=0):

        self.freq_cutoff=freq_cutoff
        self.var_cat_dict={}
        self.feature_names=[]

    def fit(self,x,y=None):

        data_cols=x.columns

        for col in data_cols:

            k=x[col].value_counts()

            if (k<=self.freq_cutoff).sum()==0:
                cats=k.index[:-1]

            else:
                cats=k.index[k>self.freq_cutoff]

            self.var_cat_dict[col]=cats

        for col in self.var_cat_dict.keys():
            for cat in self.var_cat_dict[col]:
                self.feature_names.append(col+'_'+cat)
        return self

    def transform(self,x,y=None):
        dummy_data=x.copy()

        for col in self.var_cat_dict.keys():
            for cat in self.var_cat_dict[col]:
                name=col+'_'+cat
                dummy_data[name]=(dummy_data[col]==cat).astype(int)

            del dummy_data[col]
        return dummy_data

    def get_feature_names(self):

        return self.feature_names
    
class convert_to_datetime(BaseEstimator,TransformerMixin):
    
    def __init__(self):
        
        self.feature_names=[]
        
    
    def fit(self,x,y=None):

        self.feature_names=x.columns

        return self 
    
    def transform(self,x) :

        for col in x.columns:

            x[col]=pd.to_datetime(x[col],errors='coerce')

        return x
    
    def get_feature_names(self) :
                
        return self.feature_names

class cyclic_features(BaseEstimator,TransformerMixin):

    def __init__(self):

        self.feature_names=[]
        self.week_freq=7
        self.month_freq=12
        self.month_day_freq=31

    def fit(self,x,y=None):

        for col in x.columns:

            for kind in ['week','month','month_day']:

                self.feature_names.extend([col + '_'+kind+temp for temp in ['_sin','_cos']])

        return self 

    def transform(self,x):

        for col in x.columns:
            
            wdays=x[col].dt.dayofweek
            month=x[col].dt.month
            day=x[col].dt.day

            x[col+'_'+'week_sin']=np.sin(2*np.pi*wdays/self.week_freq)
            x[col+'_'+'week_cos']=np.cos(2*np.pi*wdays/self.week_freq)

            x[col+'_'+'month_sin']=np.sin(2*np.pi*month/self.month_freq)
            x[col+'_'+'month_cos']=np.cos(2*np.pi*month/self.month_freq)

            x[col+'_'+'month_day_sin']=np.sin(2*np.pi*day/self.month_day_freq)
            x[col+'_'+'month_day_cos']=np.cos(2*np.pi*day/self.month_day_freq)

            del x[col]

        return x

    def get_feature_names(self):

        self.feature_names



class DataFrameImputer(BaseEstimator,TransformerMixin):

    def __init__(self):

        self.impute_dict={}
        self.feature_names=[]

    def fit(self, X, y=None):

        self.feature_names=X.columns

        for col in X.columns:
            if X[col].dtype=='O':
                self.impute_dict[col]='missing'
            else:
                # initialising non object variables as 0 (assuming numeric fields)
                self.impute_dict[col]=0
        return self

    def transform(self, X, y=None):
        return X.fillna(self.impute_dict)

    def get_feature_names(self):

        return self.feature_names

class pdPipeline(Pipeline):

    def get_feature_names(self):

        last_step = self.steps[-1][-1]

        return last_step.get_feature_names()

