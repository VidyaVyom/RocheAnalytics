import streamlit as st
import os
from os import environ

import openai
import pandas as pd
# PandasAI
from pandasai import SmartDataframe
from pandasai.llm.azure_openai import AzureOpenAI

# Setting up the API key
openai.api_type = "azure"
openai.api_key= "ee7792ec6fec4fa49e44fe82bda7434d"
openai.api_base="https://diamarketinggenaiapp2.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
environ['CURL_CA_BUNDLE'] = ''

environ["OPENAI_API_KEY"] = "ee7792ec6fec4fa49e44fe82bda7434d"
os.environ["deployment_id"] = "gpt-35-turbo-1106"
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] = "ee7792ec6fec4fa49e44fe82bda7434d"
os.environ["OPENAI_API_BASE"] = "https://diamarketinggenaiapp2.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
os.environ["deployment_id"] = "gpt-4-32k"

# Function to load data from file
def load_data(file):
    data = pd.read_excel(file, sheet_name='Test')
    return data

# Function to initialize the LLM model
def initialize_llm():
    return AzureOpenAI(
        openai_api_key="ee7792ec6fec4fa49e44fe82bda7434d",
        openai_api_type="azure",
        model_name="gpt-4",
        deployment_name="gpt-4-32k",
        api_base="https://diamarketinggenaiapp2.openai.azure.com/"
    )

# Streamlit app
def main():
    st.title("PandasAI Chat Interface")

    uploaded_file = st.file_uploader("Upload a file", type=["xlsx"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        list_of_columns_names = ["Indication","Disease Staging","Treatment  Eligible and Treated population","Treatment type and Biomarker subgroups","Year","Abs. Number","Rate"]
        data1 = data[list_of_columns_names].copy()

        llm = initialize_llm()
        df = SmartDataframe(data, config={"llm": llm})

        option = st.selectbox(
            'Select a question:',
            ("What percentage of colorectal cancer patients are in the Early Stage I and are eligible for treatment?",
             "Can you provide the absolute number of colorectal cancer cases diagnosed in France in 2019?",
             "How has the total number of colorectal cancer cases in France evolved annually from 2023 to 2027, including both the yearly figures and the cumulative total over this period?",
             "How does the treatment eligibility for colorectal cancer patients vary by Disease Staging in France?",
             "What is the projected rate and estimated cases of colorectal cancer in France for year 2029?",
             "What is the distribution of metastatic colorectal cancer cases by biomarker subgroup BRAF+ in France for 2026",
             "How many colorectal cancer patients in early Stage II are undergoing surgery as their treatment method in 2024?",
             "Can you provide a breakdown of colorectal cancer cases by disease staging in France for 2030?",
             "Is there a difference in the rate of Colorectal Cancer between early and late stages in the data?",
             "How does the incidence of metastatic treatment eligible colorectal cancer in the PDL1+ biomarker subgroup compare to the overall incidence rate?",
             "How has the number of cases with MSI positive biomarkers changed annually?")
        )

        if st.button("Get Answer"):
            st.write(df.chat(option))

if __name__ == "__main__":
    main()
