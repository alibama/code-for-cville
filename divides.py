import streamlit as st
import pandas as pd
import pandas_profiling
import sweetviz as sv
from streamlit_pandas_profiling import st_profile_report
import codecs
import streamlit.components.v1 as components
from pandas_profiling import ProfileReport 

def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)
   
def main():
	"""A Simple EDA App with Streamlit Components"""

	menu = ["Home","Pandas Profile","Sweetviz","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Pandas Profile":
		st.subheader("Automated EDA with Pandas Profile")
		data_file = st.file_uploader("Upload CSV",type=['csv'])
		if data_file is not None:
			df = pd.read_csv(data_file)
			st.dataframe(df.head())
			profile = ProfileReport(df)
			st_profile_report(profile)

	elif choice == "Sweetviz":
		st.subheader("Automated EDA with Sweetviz")
		data_file = st.file_uploader("Upload CSV",type=['csv'])
		if data_file is not None:
			df = pd.read_csv(data_file)
			st.dataframe(df.head())
			if st.button("Generate Sweetviz Report"):

				# Normal Workflow
				report = sv.analyze(df)
				report.show_html()
				st_display_sweetviz("SWEETVIZ_REPORT.html")    


if __name__ == '__main__':
	main()