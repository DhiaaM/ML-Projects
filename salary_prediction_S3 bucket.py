#!/usr/bin/env python
# coding: utf-8

# In[52]:


# Importing the libraries
import numpy as np


# In[53]:


###SAGEMAKER TRAINING 


# In[54]:


import sagemaker
import boto3
from sagemaker.amazon.amazon_estimator import get_image_uri 
from sagemaker.session import s3_input, Session


# In[55]:


bucket_name = 'mlsalarytest' # <--- CHANGE THIS VARIABLE TO A UNIQUE NAME FOR YOUR BUCKET
my_region = boto3.session.Session().region_name # set the region of the instance
print(my_region)


# In[56]:


s3 = boto3.resource('s3')
try:
    if  my_region == 'us-east-1':
        s3.create_bucket(Bucket=bucket_name)
    print('S3 bucket created successfully')
except Exception as e:
    print('S3 error: ',e)


# In[57]:


# set an output path where the trained model will be saved
prefix = 'trainedModel'
output_path ='s3://{}/{}/output'.format(bucket_name, prefix)
print(output_path)


# In[58]:


##Downloading The Dataset And Storing in S3


# In[80]:


import pandas as pd
import urllib
import urllib.request

try:
    model_data = pd.read_csv('./Salary_Data.csv',sep=',')
    print('Success: Data loaded into dataframe.')
    #print(model_data)
except Exception as e:
    print('Data load error: ',e)


# In[ ]:


boto3.Session().resource('s3').Bucket(bucket_name).Object(os.path.join(prefix, 'data/model_data.csv')).upload_file('model_data.csv')
model_data = sagemaker.s3_input(s3_data='s3://{}/{}/data'.format(bucket_name, prefix), content_type='csv')


# In[82]:


# Importing the dataset
X = model_data.iloc[:, :-1].values
y = model_data.iloc[:, -1].values


# In[83]:


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 42)


# In[85]:


# Fitting Simple Linear regression to the training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_train, y_train)


# In[86]:


###Deploy Machine Learning Model As Endpoints


# In[87]:


deployment = regressor.deploy(initial_instance_count=1,instance_type='ml.m4.xlarge')


# In[ ]:


endpoint=deployment.endpoint
endpoint


# In[ ]:


# Predicting test set results
y_pred = deployment.predict(X_test)
y_pred


# In[ ]:


##Prediction of the Test Data


# In[ ]:


sagemaker.Session().delete_endpoint(deployment.endpoint)
bucket_to_delete = boto3.resource('s3').Bucket(bucket_name)
bucket_to_delete.objects.all().delete()

