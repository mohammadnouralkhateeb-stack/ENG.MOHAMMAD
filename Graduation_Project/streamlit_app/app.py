import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Jordanian Smart Recruitment System", layout="wide")

# Initialize session state.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "has_history" not in st.session_state:
    st.session_state.has_history = False
if "history_data" not in st.session_state:
    st.session_state.history_data = []

# ----------------- 1. Sign in / account creation -----------------
if not st.session_state.logged_in:
    st.title("🔐 Sign in to the Smart Recruitment System")
    st.markdown("Enter your username and password. If your account does not exist, it will be created automatically.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign in / Create account")

        if submit_button:
            if username and password:
                # Send a POST request to the Django user endpoint.
                try:
                    res = requests.post(
                        "http://127.0.0.1:8000/user/", 
                        data={"username": username, "password": password}
                    )
                    
                    if res.status_code == 200:
                        res_data = res.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = res_data.get("user_id")
                        st.session_state.auth_token = res_data.get("token")
                        
                        # Check for previous search history.
                        if res_data.get("status") == "history_found":
                            st.session_state.history_data = res_data.get("results") or []
                            st.session_state.has_history = bool(st.session_state.history_data)
                        else:
                            st.session_state.has_history = False
                            st.session_state.history_data = []
                            
                        st.rerun()
                    else:
                        st.error(f"Invalid credentials: {res.json().get('error', res.text)}")
                except Exception as e:
                    st.error(f"Could not connect to the server: {str(e)}")
            else:
                st.warning("Please enter your username and password.")

# ----------------- 2. Interface after sign-in -----------------
else:
    st.sidebar.success(f"Welcome! (User ID: {st.session_state.user_id})")
    if st.sidebar.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.auth_token = None
        st.session_state.has_history = False
        st.session_state.history_data = []
        st.rerun()

    # Case A: Previous search history exists.
    if st.session_state.has_history and len(st.session_state.history_data) > 0:
        st.title("📋 Your Previous Job Search Results")
        st.info("Previous search results were found for your account:")
        
        df_history = pd.DataFrame(st.session_state.history_data).rename(
            columns={
                "job_title": "Job title",
                "location": "Location",
                "description": "Description",
                "score": "Match score",
                "link": "Job listing",
            }
        )
        df_history = df_history.reindex(
            columns=["Job title", "Location", "Description", "Match score", "Job listing"]
        )
        st.dataframe(
            df_history,
            column_config={
                "Job listing": st.column_config.LinkColumn("Job listing"),
                "Match score": st.column_config.ProgressColumn(
                    "Match score", format="%d%%", min_value=0, max_value=100
                ),
            },
            hide_index=True,
            use_container_width=True
        )
        
        if st.button("🔍 Start a new job search"):
            st.session_state.has_history = False
            st.rerun()

    # Case B: No previous search history, or the user chose to start a new search.
    else:
        st.title("📄 Find Jobs That Match Your Resume")
        
        with st.form("job_search_form"):
            job_title = st.text_input("Desired Job Title")
            location = st.text_input("Location", "Irbid")
            description = st.text_area("Job Description")
            salary = st.number_input("Expected Salary", min_value=0, value=500)
            uploaded_file = st.file_uploader(
                "Upload Your Resume (PDF)",
                type=["pdf"],
                help="PDF files only, with a maximum of 20 pages.",
            )
            
            search_submitted = st.form_submit_button("Analyze Resume and Search")

            if search_submitted:
                if job_title and description and uploaded_file:
                    files = {
                        "resume_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                    }
                    data = {
                        "job_title": job_title,
                        "location": location,
                        "description": description,
                        "salary": salary
                    }
                    
                    with st.spinner("Analyzing your resume and matching jobs with AI..."):
                        try:
                            response = requests.post(
                                "http://127.0.0.1:8000/details/",
                                data=data,
                                files=files,
                                headers={
                                    "Authorization": f"Token {st.session_state.auth_token}"
                                },
                            )
                            
                            if response.status_code in [200, 201]:
                                st.success("Your information was saved and the analysis completed successfully!")
                                data_result = response.json()
                                
                                if isinstance(data_result, list) and len(data_result) > 0:
                                    df = pd.DataFrame(data_result)
                                    st.subheader("📋 Recommended Job Matches")
                                    st.dataframe(
                                        df,
                                        column_config={
                                            "link": st.column_config.LinkColumn("Job Listing"),
                                            "score": st.column_config.ProgressColumn("Match Score", format="%d%%", min_value=0, max_value=100),
                                        },
                                        hide_index=True,
                                        use_container_width=True
                                    )
                                else:
                                    st.info("The request completed, but no matching jobs were returned.")
                            else:
                                st.error(f"The server returned an error: {response.text}")
                        except Exception as e:
                            st.error(f"Could not connect to the server: {str(e)}")
                else:
                    st.warning("Please complete all required fields and upload your resume.")