import streamlit as st
import google.generativeai as genai
import os

# Authentication
def authenticate():
        # Authentication
    st.sidebar.title("🔒 Authentication")

    if not st.session_state.get("authenticated"):
        username = st.sidebar.text_input("Username", placeholder="Enter your username")
        password = st.sidebar.text_input("Password", type="password", placeholder="••••••••")
        
        if st.sidebar.button("Login", use_container_width=True):
            if username == "admin" and password == "password":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
    else:
        if st.sidebar.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    if not st.session_state.get("authenticated"):
        st.warning("Please login from the sidebar to continue")
        st.stop()

authenticate()

# App Title
st.title("📧 AI-Powered Customer Care Assistant")
st.caption("Streamline your customer support with AI-generated responses")

# Session State Initialization
if "company_details" not in st.session_state:
    st.session_state.company_details = {
        "TechCorp": "Leading technology solutions provider",
        "MediCare": "Healthcare services organization",
        "EduLearn": "Online education platform"
    }

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Navigation
page = st.sidebar.radio("Navigate to", ["🏠 Dashboard", "✉️ Generate Response", "⚙️ Configuration"])

# Dashboard Page
if page == "🏠 Dashboard":
    st.header("Welcome to Your Customer Care Hub")
    st.write("""
    **Key Features:**
    - Instant AI-generated email responses
    - Multi-company profile support
    - Customizable response tones
    - Secure API integration
    """)
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your Companies")
        for company in st.session_state.company_details:
            st.markdown(f"- **{company}**: {st.session_state.company_details[company]}")
    
    with col2:
        st.subheader("Quick Actions")
        st.button("View API Documentation", disabled=True)
        st.button("View Usage Analytics", disabled=True)

# Generate Response Page
elif page == "✉️ Generate Response":
    st.header("Create AI-Generated Response")
    
    with st.form("response_form"):
        col1, col2 = st.columns(2)
        with col1:
            company = st.selectbox(
                "Select Company",
                options=list(st.session_state.company_details.keys()),
                help="Select the company profile to use"
            )
        with col2:
            tone = st.selectbox(
                "Response Tone",
                options=["Professional", "Friendly", "Compassionate", "Formal"],
                index=0,
                help="Select the desired communication tone"
            )
        
        query = st.text_area(
            "Customer Query",
            height=150,
            placeholder="Paste the customer's message here...",
            help="Enter the customer's original query"
        )
        
        if st.form_submit_button("Generate Response", use_container_width=True):
            if st.session_state.api_key and query:
                try:
                    genai.configure(api_key=st.session_state.api_key)
                    model = genai.GenerativeModel("gemini-pro")
                    prompt = f"""
                    Generate a {tone.lower()} email response for {company} ({st.session_state.company_details[company]}).
                    Customer query: {query}
                    """
                    with st.spinner("Crafting professional response..."):
                        response = model.generate_content(prompt)
                        st.divider()
                        st.markdown("**AI-Generated Response**")
                        st.markdown(response.text)
                except Exception as e:
                    st.error(f"Generation error: {str(e)}")
            else:
                st.error("Please configure API key and enter query")

# Configuration Page
elif page == "⚙️ Configuration":
    st.header("Configuration Settings")
    
    with st.expander("🔑 API Key Management", expanded=True):
        st.session_state.api_key = st.text_input(
            "Google API Key",
            type="password",
            value=st.session_state.api_key,
            help="Enter your Google Generative AI API key"
        )
        if st.button("Save API Key", help="Secure storage in session"):
            st.success("API key saved for current session")
    
    with st.expander("🏢 Company Profiles"):
        # Section 1: Existing Companies
        st.subheader("📋 Existing Company Profiles")
        st.write("Manage your current company configurations")
        
        if not st.session_state.company_details:
            st.info("No companies added yet. Use the section below to add new ones.")
        else:
            for company in list(st.session_state.company_details.keys()):
                with st.container(border=True):
                    cols = st.columns([0.7, 0.3])
                    with cols[0]:
                        new_desc = st.text_input(
                            f"{company} Description",
                            value=st.session_state.company_details[company],
                            key=f"desc_{company}"
                        )
                    with cols[1]:
                        if st.button(f"🔄 Update {company}", key=f"update_{company}"):
                            st.session_state.company_details[company] = new_desc
                            st.rerun()
                        if st.button(f"❌ Delete {company}", key=f"delete_{company}"):
                            del st.session_state.company_details[company]
                            st.rerun()
        
        st.divider()
        
        # Section 2: Add New Company
        st.subheader("✨ Add New Company")
        st.write("Create new company profiles for email generation")
        
        with st.form("new_company_form"):
            new_name = st.text_input("Company Name", placeholder="Enter new company name")
            new_desc = st.text_input("Company Description", placeholder="Enter company description")
            
            if st.form_submit_button("➕ Add Company", use_container_width=True):
                if new_name and new_desc:
                    if new_name in st.session_state.company_details:
                        st.error("Company already exists!")
                    else:
                        st.session_state.company_details[new_name] = new_desc
                        st.rerun()
                else:
                    st.error("Both fields are required!")

# Footer
st.divider()
st.caption("© 2024 Customer Care AI - Developed by Ansh, Praneet & Himangi")