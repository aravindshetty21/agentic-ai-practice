from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st

llm = ChatOpenAI(model="gpt-5-nano")

financial_analysis_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are an experienced financial advisor in India
         who specializes in personal finance management. Analyze the
         customer's financial situation and provide detailed insigths.
         Present the output in a clean format with clear sections."""),

        ("user", """Perform initial financial analysis for the client in india:
        - Monthly Income: {monthly_income} INR
        - Monthly Expenses: {monthly_expenses} INR
        - Savings: {savings} INR
        Create a comporehensive assesment of their financial health,
         
         Following is the expected output 
         A detailed financial analysis report including:
         - current financial health assessment
         - cash flow analysis
         - savings potential
         - Risk capacity evaluation"""),
    ]
)

fa_chain = financial_analysis_prompt | llm | StrOutputParser()

investment_recommendation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """You are a seasoned investment advisor in India
         who specializes in personal finance management. Based on the
         client's financial analysis, provide tailored investment recommendations.
         Present the output in a clean format with clear sections."""),

        ("user", """Based on the following financial analysis:
        {financial_analysis}
        Provide personalized investment recommendations considering:
        - Risk Tolerance Level: {risk_tolerance}
        - Investment Duration: {investment_years} years
         
        Following is the expected output format:
        Create a detailed investment plan including:
        - Recommended investment vehicles (mutual funds, stocks, bonds, etc.)
        - Asset allocation strategy
        - Expected returns and risk assessment"""),
    ]
) 

ir_chain = investment_recommendation_prompt | llm | StrOutputParser()

# chain = {
#     "financial_analysis": fa_chain,
#     "risk_tolerance": lambda x: x["risk_tolerance"],
#     "invesment_years": lambda x: x["invesment_years"]
# } | ir_chain

from langchain_core.runnables import RunnablePassthrough, RunnablePick

chain = {
    "financial_analysis": fa_chain, 
    "risk_tolerance": lambda x: x["risk_tolerance"], 
    "investment_years": lambda x: x["investment_years"]
} | RunnablePassthrough.assign(
    investment_recommendations=ir_chain
) | RunnablePick(["financial_analysis", "investment_recommendations"])


st.set_page_config(page_title="Financial Analysis Chain", layout="wide", page_icon="💰")
st.title("💰 Financial Analysis Chain")

with st.sidebar:
    st.header("Input Financial Details")
    monthly_income = st.number_input("Monthly Income (INR)", min_value=0, value=50000, step=1000)
    monthly_expenses = st.number_input("Monthly Expenses (INR)", min_value=0, value=30000, step=1000)
    savings = st.number_input("Savings (INR)", min_value=0, value=200000, step=1000)
    risk_tolerance = st.selectbox("Risk Tolerance Level", options=["Low", "Medium", "High"], index=1)
    investment_years = st.slider("Investment Duration (Years)", min_value=1, max_value=30, value=10)

    analyze_button = st.button("Analyze Financials")

if analyze_button:
    with st.spinner("Generating financial analysis..."):
        analysis_report = chain.invoke({
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
            "savings": savings,
            "risk_tolerance": risk_tolerance,
            "investment_years": investment_years
        })
        # print(analysis_report)
        # st.markdown(analysis_report)
        tab1, tab2 = st.tabs(["Financial Analysis", "Investment Recommendations"])
        with tab1:
            st.header("Financial Analysis Report")
            st.markdown(analysis_report["financial_analysis"])
        with tab2:
            st.header("Investment Recommendations")
            st.markdown(analysis_report["investment_recommendations"])