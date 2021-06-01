import math
import streamlit as st
import numpy as np
import json
#import rdflib
import altair as alt
from urllib.request import urlopen
#from xml.etree.ElementTree import parse
import urllib
import urllib.parse as urlparse
import requests
import pandas as pd
import pandas_profiling
#@st.cache


import codecs
from pandas_profiling import ProfileReport 

# Components Pkgs
import streamlit.components.v1 as components
from streamlit_pandas_profiling import st_profile_report

# Custome Component Fxn
import sweetviz as sv 



#fulltext_list
#'''hello amelia!  it is very nice to see you today'''

@st.cache(suppress_st_warning=True)
def bigask ():
    dct = {}
    for col in ['oa','author','year','title','doi','id','cited','aff']:
        dct[col] = []

    cr_mrk= '' #current cursor mark
    nxt_mrk = '*' #next cursor mark
    while cr_mrk != nxt_mrk:              
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'
        query = '(AFF:"University of Virginia") AND (FIRST_PDATE:[2017-01-01 TO 2020-12-31])'
        params = {'query':query, 'resultType':'core', 'synonym':'TRUE','cursorMark':nxt_mrk,'pageSize':'1000','format':'json'}
        response = requests.get(url,params)
        rjson = response.json()
        cr_mrk = urlparse.unquote(rjson['request']['cursorMark'])
        nxt_mrk = urlparse.unquote(rjson['nextCursorMark'])
        for rslt in rjson['resultList']['result']:
            dct['author'].append(rslt['authorString']) if 'authorString' in rslt.keys() else dct['author'].append(0)
            dct['year'].append(rslt['pubYear']) if 'pubYear' in rslt.keys() else dct['year'].append(0)
            dct['title'].append(rslt['title']) if 'title' in rslt.keys() else dct['title'].append(0)
            dct['doi'].append(rslt['doi']) if 'doi' in rslt.keys() else dct['doi'].append(0)
            dct['id'].append(rslt['id']) if 'id' in rslt.keys() else dct['id'].append(0)
            dct['oa'].append(rslt['isOpenAccess']) if 'isOpenAccess' in rslt.keys() else dct['oa'].append(0)
            dct['cited'].append(rslt['citedByCount']) if 'citedByCount' in rslt.keys() else dct['cited'].append(0) 
            dct['aff'].append(rslt['affiliation']) if 'affiliation' in rslt.keys() else dct['aff'].append(0)
            #dct['journal'].append(rslt['journalInfo']['journal']['title']) if ['journalInfo']['journal']['title'] in rslt.keys() else dct['journal'].append(0)  
    df=pd.DataFrame.from_dict(dct, orient='columns')
        #print(dct)
    return df

def bigask2 ():
    dct = {}
    for col in ['oa','author','year','title','doi','id','cited','aff']:
        dct[col] = []

    cr_mrk= '' #current cursor mark
    nxt_mrk = '*' #next cursor mark
    while cr_mrk != nxt_mrk:              
        url = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'
        query = '(AFF:"Virginia Tech") AND (FIRST_PDATE:[2017-01-01 TO 2020-12-31])'
        params = {'query':query, 'resultType':'core', 'synonym':'TRUE','cursorMark':nxt_mrk,'pageSize':'1000','format':'json'}
        response = requests.get(url,params)
        rjson = response.json()
        cr_mrk = urlparse.unquote(rjson['request']['cursorMark'])
        nxt_mrk = urlparse.unquote(rjson['nextCursorMark'])
        for rslt in rjson['resultList']['result']:
            dct['author'].append(rslt['authorString']) if 'authorString' in rslt.keys() else dct['author'].append(0)
            dct['year'].append(rslt['pubYear']) if 'pubYear' in rslt.keys() else dct['year'].append(0)
            dct['title'].append(rslt['title']) if 'title' in rslt.keys() else dct['title'].append(0)
            dct['doi'].append(rslt['doi']) if 'doi' in rslt.keys() else dct['doi'].append(0)
            dct['id'].append(rslt['id']) if 'id' in rslt.keys() else dct['id'].append(0)
            dct['oa'].append(rslt['isOpenAccess']) if 'isOpenAccess' in rslt.keys() else dct['oa'].append(0)
            dct['cited'].append(rslt['citedByCount']) if 'citedByCount' in rslt.keys() else dct['cited'].append(0) 
            dct['aff'].append(rslt['affiliation']) if 'affiliation' in rslt.keys() else dct['aff'].append(0)
            #dct['journal'].append(rslt['journalInfo']['journal']['title']) if ['journalInfo']['journal']['title'] in rslt.keys() else dct['journal'].append(0)  
    df2=pd.DataFrame.from_dict(dct, orient='columns')
        #print(dct)
    return df2

#menu = ["Y", "N"]
#st.sidebar.subheader("Select Option")
#choice = st.sidebar.selectbox("Full Text", menu)

dfdata=bigask()
dfdata2=bigask2()

#dfdata= dfdata[dfdata['oa'] == choice] 
#df=pd.DataFrame.from_dict(rslt)        

citations = st.sidebar.slider('Number of citations', 0, 100, 1)
#citations = 0
dfdata = dfdata[dfdata['cited'] >= citations] 
dfdata['doi'] = dfdata['doi'].astype(str)  #pandas was calling this a mixed type column and it borked sweetviz
dfdata['aff'] = dfdata['aff'].astype(str)  #pandas was calling this a mixed type column and it borked sweetviz
#dfdata
dfdata.to_csv('opendata.csv', index=False)
st.write(dfdata)
        


#openFilter = sorted(df['openAccess'].drop_duplicates()) # select the open access values 
#open_Filter = st.sidebar.selectbox('Open Access?', openFilter) # render the streamlit widget on the sidebar of the page using the list we created above for the menu
#df2=df[df['openAccess'].str.contains(open_Filter)] # create a dataframe filtered below
#st.write(df2.sort_values(by='date'))




valLayer = alt.Chart(dfdata).mark_bar().encode(x='year',y='count(oa)',color='oa')#

st.altair_chart(valLayer, use_container_width=True)



def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)


def main():
	"""A Simple EDA"""

	menu = ["Home","Pandas Profile","Sweetviz","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Pandas Profile":
		st.subheader("Automated EDA with Pandas Profile")
		profile = ProfileReport(dfdata)
		st_profile_report(profile)

	elif choice == "Sweetviz":
		st.subheader("Automated EDA with Sweetviz")
		if st.button("Generate Sweetviz Report"):
			# Normal Workflow
			report = sv.analyze(dfdata)
			report.show_html()
			st_display_sweetviz("SWEETVIZ_REPORT.html")

if __name__ == '__main__':
	main()
    


st.markdown('Download a copy of the data [opendata.csv](https://tljh.codeforcville.org/user/alibama/doc/tree/opendata.csv)')