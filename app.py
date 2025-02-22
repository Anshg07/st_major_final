import streamlit as st
import google.generativeai as genai
import os
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_image});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Arial', sans-serif;
        }}
        .glassmorphism-block {{
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }}
        .title {{
            font-size: 2rem;
            font-weight: bold;
            text-align: center;
            padding: 10px;
        }}
        .footer {{
            text-align: center;
            padding: 10px;
            font-size: 0.9rem;
            color: #ccc;
        }}
        .auth-container {{
            display: flex;
            justify-content: center;
            gap: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# add_bg_from_local('green_trees.jpg')

# Authentication
st.sidebar.title("Authentication")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    if st.sidebar.button("Login"):
        if username == "admin" and password == "password":  # Replace with proper authentication
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.sidebar.error("Invalid credentials")
else:
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

if not st.session_state["authenticated"]:
    st.warning("Please login to continue.")
    st.stop()

st.markdown("<h1 class='title'>AI-Powered Customer Care Email Generator</h1>", unsafe_allow_html=True)

# Pagination setup
page = st.sidebar.radio("Navigation", ["Home", "Generate Response", "Settings"])

if "company_details" not in st.session_state:
    st.session_state["company_details"] = {
        "TechCorp": "A leading technology company providing AI solutions.",
        "MediCare": "A healthcare organization focused on patient well-being.",
        "EduLearn": "An ed-tech company delivering quality online education."
    }

if "api_key" not in st.session_state:
    st.session_state["api_key"] = ""


if page == "Home":
    st.write("## Welcome to the AI-Powered Customer Care Email Generator!")
    st.write("This project aims to automate professional email responses using AI.")
    st.write("### Strengths of this project:")
    st.write("- Automated customer support responses.")
    st.write("- Customizable for different companies.")
    st.write("- Secure and user-friendly.")
    st.write("- AI-powered insights for improved engagement.")

elif page == "Generate Response":
    selected_company = st.selectbox("Select your Company", list(st.session_state["company_details"].keys()))
    company_name = selected_company
    company_description = st.session_state["company_details"][selected_company]
    company_tone = st.selectbox("Select the tone of your emails", ["Professional", "Friendly", "Casual", "Formal"])
    customer_query = st.text_area("Enter customer query")

    if st.button("Generate Response"):
        if st.session_state["api_key"] and customer_query:
            os.environ["API_KEY"] = st.session_state["api_key"]
            genai.configure(api_key=os.environ["API_KEY"])
            model = genai.GenerativeModel("gemini-1.5-flash")
            combined_query = f"""
            You are generating customer care emails for {company_name}, a company that {company_description}. 
            Your task is to respond to customer queries in a {company_tone.lower()} manner while maintaining clarity and helpfulness.
            
            Please follow these guidelines:
            - If the customer query is related to {company_name}'s services, provide a detailed and informative response.
            - If the query falls outside the scope of {company_name}, politely inform the customer and redirect them if necessary.
            - Keep responses well-structured, concise, and relevant.
            - Maintain a {company_tone.lower()} tone throughout the response.
            
            Here is a new customer query:

            {customer_query}

            Please generate an appropriate customer care email response following the style and structure of professional customer support communication.
            Include proper markdown formatting in the response.
            """
            
            try:
                response = model.generate_content(combined_query)
                generated_text = response.candidates[0].content.parts[0].text
                st.markdown(f"<div class='glassmorphism-block'>{generated_text}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a valid customer query. Ensure API Key is set in the settings.")


elif page == "Settings":
    st.write("## Manage API Key")
    with st.expander("API Key Management"):
        st.session_state["api_key"] = st.text_input("Enter your Google API Key", type="password", value=st.session_state["api_key"])
        if st.button("Save API Key"):
            st.success("API Key saved successfully!")
            st.rerun()
    
    st.write("### Manage Companies")
    for company, desc in list(st.session_state["company_details"].items()):
        with st.expander(f"{company}"):
            new_desc = st.text_area(f"Update description for {company}", value=desc)
            col1, col2 = st.columns(2)
            if col1.button(f"Update {company}"):
                st.session_state["company_details"][company] = new_desc
                st.success(f"{company} updated successfully!")
                st.rerun()
            if col2.button(f"Delete {company}"):
                del st.session_state["company_details"][company]
                st.success(f"{company} deleted successfully!")
                st.rerun()
    
    new_company_name = st.text_input("New Company Name")
    new_company_desc = st.text_area("New Company Description")
    if st.button("Add Company"):
        if new_company_name and new_company_desc:
            st.session_state["company_details"][new_company_name] = new_company_desc
            st.success(f"Company {new_company_name} added successfully!")
            st.rerun()
        else:
            st.error("Please enter both company name and description.")



st.markdown(f"<div class='footer' style='text-align: center;'>Powered by AI CRM | {st.session_state.get('company_name', 'MAJOR PROJECT - ANSH,PRANEET,HIMANGI')}</div>", unsafe_allow_html=True)
