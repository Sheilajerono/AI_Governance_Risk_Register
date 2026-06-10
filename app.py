import streamlit as st
import plotly.express as px
from database import create_table, insert_tool, get_tools

st.set_page_config(
    page_title="AI Governance & Risk Register",
    layout="wide"
)

create_table()

st.title("AI Governance & Risk Register")
st.caption("Supporting responsible AI adoption, cyber security oversight, privacy protection, and governance compliance.")

st.markdown("""
### About This Platform

This platform supports the development of an organisational AI Register by capturing how AI tools and AI-enabled systems are being used across business areas.

As AI capabilities become embedded in everyday systems, organisations need visibility over AI usage not only from an innovation perspective, but also from a cyber security, privacy, information protection, and governance perspective.
""")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Register AI Tool",
        "AI Register",
        "Governance Framework"
    ]
)

def calculate_risk(data_classification, ai_usage_type, approval_status):
    score = 0

    if data_classification == "Public":
        score += 1
    elif data_classification == "Internal":
        score += 2
    elif data_classification == "Confidential":
        score += 3

    if ai_usage_type == "Customer-facing":
        score += 2
    elif ai_usage_type == "Decision support":
        score += 2
    elif ai_usage_type == "Automation":
        score += 1

    if approval_status == "Not Approved":
        score += 3
    elif approval_status == "Under Review":
        score += 2
    elif approval_status == "Approved":
        score += 0

    if score >= 6:
        return "High"
    elif score >= 3:
        return "Medium"
    else:
        return "Low"

if menu == "Dashboard":
    st.header("Governance Dashboard")

    df = get_tools()

    if df.empty:
        st.info("No AI tools registered yet. Use the registration form to add the first AI tool.")
    else:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total AI Tools", len(df))
        col2.metric("High Risk", len(df[df["risk_level"] == "High"]))
        col3.metric("Medium Risk", len(df[df["risk_level"] == "Medium"]))
        col4.metric("Low Risk", len(df[df["risk_level"] == "Low"]))

        st.markdown("---")

        left, right = st.columns(2)

        with left:
            st.subheader("AI Tools by Risk Level")
            fig = px.pie(
                df,
                names="risk_level",
                title="Risk Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        with right:
            st.subheader("AI Usage by Department")
            fig2 = px.bar(
                df,
                x="department",
                color="risk_level",
                title="Department AI Usage"
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("Governance Insights")

        high_risk_count = len(df[df["risk_level"] == "High"])

        if high_risk_count > 0:
            st.warning(f"{high_risk_count} high-risk AI tool(s) require governance review.")
        else:
            st.success("No high-risk AI tools currently recorded.")

elif menu == "Register AI Tool":
    st.header("Register AI Tool or AI-Enabled System")

    st.markdown("""
    Use this form to capture AI tools, AI features embedded in existing systems, or informal AI use cases.
    """)

    with st.form("ai_tool_form"):
        tool_name = st.text_input("AI Tool or Feature Name")
        vendor = st.text_input("Vendor / System Provider")
        department = st.selectbox(
            "Department / Business Area",
            ["IT", "Records", "Finance", "HR", "Customer Service", "Planning", "Community Services", "Other"]
        )

        business_owner = st.text_input("Business Owner / Responsible Team")

        ai_usage_type = st.selectbox(
            "AI Usage Type",
            ["Generative AI", "Automation", "Decision support", "Customer-facing", "Embedded AI feature", "Other"]
        )

        purpose = st.text_area("Purpose of Use")

        data_classification = st.selectbox(
            "Data Classification",
            ["Public", "Internal", "Confidential"]
        )

        approval_status = st.selectbox(
            "Approval Status",
            ["Approved", "Under Review", "Not Approved"]
        )

        cyber_privacy_risk = st.text_area(
            "Cyber Security / Privacy Risk Notes",
            placeholder="Example: May process internal documents, personal information, or confidential data."
        )

        submitted = st.form_submit_button("Submit to AI Register")

        if submitted:
            risk_level = calculate_risk(data_classification, ai_usage_type, approval_status)

            insert_tool(
                tool_name,
                vendor,
                department,
                purpose,
                data_classification,
                risk_level
            )

            st.success(f"{tool_name} has been added to the AI Register.")
            st.info(f"Automated Risk Rating: {risk_level}")

elif menu == "AI Register":
    st.header("AI Register")

    df = get_tools()

    if df.empty:
        st.info("No AI tools registered yet.")
    else:
        search = st.text_input("Search AI Register")

        if search:
            df = df[
                df["tool_name"].str.contains(search, case=False, na=False) |
                df["vendor"].str.contains(search, case=False, na=False) |
                df["department"].str.contains(search, case=False, na=False)
            ]

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)

        st.download_button(
            "Download AI Register as CSV",
            csv,
            "ai_register.csv",
            "text/csv"
        )

elif menu == "Governance Framework":
    st.header("AI Governance Framework")

    st.markdown("""
    ## Project Objectives

    This AI Register supports the following governance objectives:

    - Identify where AI is currently being used across the organisation.
    - Understand how staff are using AI tools in day-to-day work.
    - Capture emerging opportunities, risks, and support needs.
    - Strengthen protection of organisational systems and data.
    - Manage cyber security and privacy risks associated with AI use.
    - Support informed decision-making on new AI tools and investments.
    - Meet audit, compliance, and reporting requirements.

    ---

    ## What the AI Register Captures

    The register records:

    - AI tools or features in use.
    - Business purpose and use case.
    - Vendor or system provider.
    - Department or business area.
    - Data classification.
    - Approval status.
    - Cyber security and privacy risk considerations.
    - Automated risk rating.

    ---

    ## Key AI Risk Categories

    ### Cyber Security Risk
    AI tools may introduce risks such as data leakage, unauthorised access, prompt injection, and third-party vendor vulnerabilities.

    ### Privacy Risk
    AI systems may process personal, confidential, or sensitive information without appropriate visibility or controls.

    ### Governance Risk
    Without a central register, organisations may lack transparency over where AI is used and who is accountable.

    ### Compliance Risk
    Poor documentation of AI systems may create audit, reporting, and regulatory compliance challenges.

    ### Ethical Risk
    AI systems may produce biased, inaccurate, or difficult-to-explain outputs if not reviewed appropriately.

    ---

    ## Disclaimer

    This application is a demonstration project developed for learning and portfolio purposes. It does not represent an official City of Hobart system or publication.
    """)