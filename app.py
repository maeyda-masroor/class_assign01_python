import streamlit as st
import pandas as pd
import os
import io 
from io import BytesIO

st.set_page_config(page_title="Data Sweeper",layout="wide")
st.title("Data SWEEPER")
st.write("Transform your files between csv and excel format with built in cleaning and visulaization")
uploaded_files = st.file_uploader("Upload your file (CSV Or Excel)",type=["csv","xlsx"],
accept_multiple_files=True)

if uploaded_files:
	for file in uploaded_files:
		file_ext = os.path.splitext(file.name)[-1].lower()


		if file_ext == '.csv':
			df = pd.read_csv(file)
		elif file_ext == '.xlsx':
			df = pd.read_excel(file)
		else:
			st.error("Unsupported file type: {file_ext}")
			continue

		st.write(f"** File Name:** {file.name}")
		st.write(f"**File Size**{file.size/1024}")
		st.write("Review the head of data frame")

		st.dataframe(df.head())

		st.subheader("Dtaa cleaning Option")
		if st.checkbox(f"clean data for {file.name}"):
			col1 , col2 = st.columns(2)

			with col1:
				if st.button(f"Remove Duplicates from {file.name}"):
					df.drop_duplicates(inplace=True)
					st.write("Duplicates Removed")

			with col2:
				if st.button(f"Fill mising value{file.name}"):
					numeric_cols = df.select_dtypes(include=['numbers']).columns
					df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
					st.write("missing values have been filled")

		st.subheader("select col to convert")
		columns = st.multiselect(f"choose column for {file.name}",df.columns,default=df.columns)
		df = df[columns]

		st.subheader("Data Visulization")
		if st.checkbox(f"show visulaization for {file.name}"):
			st.bar_chart(df.select_dtypes(include='number').iloc[:,2])


		st.subheader("conversion Option")
		conversion_type = st.radio(f"Convert {file.name} to ",["CSV","Excel"],key=file.name)
		if st.button(f"Convert {file.name}"):
			buffer = BytesIO()
			if conversion_type == "CSV":
				df.to_csv(buffer,index=False)
				file_name = file.name.replace(file_ext,".csv")
				mime_type = "text/csv"

			elif conversion_type == "Excel":
				df.to_excel(buffer,index=False)
				file_name = file.name.replace(file_ext,".xlsx")
				mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
			buffer.seek(0)

			st.download_button(
				label=f"Fownload {file.name} as {conversion_type}",
				data=buffer,
				file_name=file_name,
				mime=mime_type
				)
st.success("All files processed")