import os
import re
import pandas as pd
import subprocess
import sys
from datetime import datetime
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install',package])
import_or_install("recordlinkage")
import_or_install("pickle")
import pickle
import recordlinkage
from recordlinkage import Compare

my_dict= {'name': 'First Name', 'givenname': 'First Name', 'fname': 'First Name', 'firstname': 'First Name',
          'surname': 'Last Name', 'familyname': 'Last Name', 'lname': 'Last Name', 'lastname': 'Last Name',
          'streetno': 'Street Number', 'stno': 'Street Number', 'streetnumber': 'Street Number',
          'streetaddress': 'Address', 'addr': 'Address', 'addressline1': 'Address1', 'address':'Address', 'address1':'Address1',
          'unitnumber': 'Address2', 'apartmentnumber': 'Address', 'addr2': 'Address2', 'addressline2': 'Address2', 'address2': 'Address2',
          'county': 'Suburb', 'city': 'Suburb', 'area': 'Suburb', 'region': 'Suburb', 'suburb':'Suburb',
          'zipcode':'Postcode', 'areacode':'Postcode','zip':'Postcode', 'postalcode':'Postcode', 'postcode':'Postcode',
          'state': 'State',
          'dob':'Date of Birth', 'birthdate':'Date of Birth', 'dateofbirthddmmyy':'Date of Birth', 'dateofbirthmmddyy':'Date of Birth', 'dateofbirthddmmyyyy':'Date of Birth', 'dateofbirthmmddyyyy':'Date of Birth', 'dobddmmyy':'Date of Birth', 'dobmmddyy':'Date of Birth', 'dobddmmyyyy':'Date of Birth', 'dobmmddyyyy':'Date of Birth', 'dateofbirth':'Date of Birth',
          'ssn':'Social Security Number', 'socsecid': 'Social Security Number', 'socialsecuritynumber':'Social Security Number', 'ssa':'Social Security Number', 'socialsecuritycard':'Social Security Number', 'ssid':'Social Security Number', 'socialsecuritynumer':'Social Security Number',
          'contactnumber':'Phone Number', 'number':'Phone Number', 'phone':'Phone Number', 'phno':'Phone Number', 'phoneo':'Phone Number', 'phnumber':'Phone Number', 'mobile':'Phone Number', 'mobileno':'Phone Number', 'mobilenumber':'Phone Number', 'cellphone':'Phone Number', 'cellphoneno':'Phone Number', 'cellphonenumber':'Phone Number', 'phonenumber':'Phone Number',
          'email':'Email Address', 'emailid':'Email Address', 'emailaddress':'Email Address'}
def candidate_links_func(dfA,dfB,blocker): 
      indexer = recordlinkage.Index()
      if blocker!="":
        indexer.block(blocker)
        candidate_links = indexer.index(dfA, dfB)
      else:
        a=list(dfA.index)
        b=list(dfB.index)
        candidate_links=pd.MultiIndex.from_product([a,b]) 
      return candidate_links  

def data1(dfA,dfB,blocker=""):
      candidate_links=candidate_links_func(dfA,dfB,blocker)
      compare = Compare()
      compare.string('First Name', 'First Name', method='cosine', label="First Name")
      compare.string('Last Name', 'Last Name', method='cosine', label="Last Name")
      compare.string('Suburb', 'Suburb', method='cosine', label="Suburb")
      compare.string('State', 'State', method='cosine', label="State")
      compare.string('Address', 'Address', method='cosine', label="Address")
      compare.string("Date of Birth","Date of Birth",method='cosine', label="Date of Birth")
      features = compare.compute(candidate_links, dfA, dfB)
      return features

def column_matching(column_names):
    canonical_lst=[]
    new_column_names=[]
    def standard_name(col_name):
        col_name= ''.join(col_name.split()).lower()
        col_name= re.sub("[^A-Za-z0-9]", '', col_name)
        if col_name in my_dict:
            col_name= my_dict[col_name]
        else:
            canonical_lst.append(col_name)
        new_column_names.append(col_name)
    for col in  column_names:
        standard_name(col)
    return new_column_names,canonical_lst

def check_columns(col_names):
    columns_model=["First Name","Last Name","Suburb","State","Address","Date of Birth"]
    str1=""
    for col in columns_model:
        if col not in col_names:
            str1+=col+"; "
    return str1        

def record_linkage_func(list_df):
    dfA,dfB=list_df[0],list_df[1]
    new_column_names,canonical_lst=column_matching(list(dfA.columns))
    dfA.columns=new_column_names
 
    new_column_names,canonical_lst=column_matching(list(dfB.columns))
    dfB.columns=new_column_names

    ans1=check_columns(list(dfA.columns))
    ans2=check_columns(list(dfB.columns))

    if ans1!="" or ans2!="":
        return 0,(ans1,ans2)
    dfA["initials"] = (dfA["First Name"].str[0]  + dfA["Last Name"].str[0])
    dfB["initials"] = (dfB["First Name"].str[0]  + dfB["Last Name"].str[0])
    dfA["Date of Birth"] = dfA["Date of Birth"].astype(str).str.replace('-', "")
    dfB["Date of Birth"] = dfB["Date of Birth"].astype(str).str.replace('-', "")
    dfA["soc_sec_id"] = dfA["Social Security Number"].str.replace('-', "")
    dfB["soc_sec_id"] = dfB["Social Security Number"].str.replace('-', "")
    features1=data1(dfA,dfB,"initials")
    input1=features1.copy()
    model = pickle.load(open('model_pkl.pkl', 'rb'))
    features1['Match']=model.predict_proba(input1)[:,1]
    features1.reset_index(inplace=True)
    show=features1[features1['Match']>=0]
    show.sort_values(['Match'],ascending=False,inplace=True)
    show=show.reset_index(drop=True)
    show=show[['level_0','level_1','Match']]
    show.columns=['First_File_Index','Second_File_Index','Probabilty_Match_Rate']
    show['Probabilty_Match_Rate']=round(show['Probabilty_Match_Rate']*100,2)
    new_filename = f'output_{str(datetime.now())}.csv'
    save_loction=os.path.join('output', new_filename)
    show.to_csv(save_loction,index=False) 
    return 1,save_loction
