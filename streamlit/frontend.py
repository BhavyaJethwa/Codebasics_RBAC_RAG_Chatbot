import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from typing import List
import uuid


API_URL = "http://localhost:8000"  # Adjust as needed

def admin_sidebar():
    with st.sidebar:
        st.title("FinSolve Technologies")
        st.title(f"Hello {st.session_state.name} !")
        st.markdown("Your Role")
        st.info(st.session_state.role.capitalize())

        # Styled logout button
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                padding: 12px 24px !important;
                font-size: 18px !important;
                width: 100% !important;
                background-color: #e63946 !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                cursor: pointer;
            }
            div.stButton > button:first-child:hover {
                background-color: #d62828 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def fetch_roles():
    try:
        response = requests.get(f"{API_URL}/get_roles") 
        if response.status_code == 200:
            return [role["role"] for role in response.json()]
        else:
            return []
    except:
        return []

def home_ui():
    # Custom page title
    st.set_page_config(page_title="FinSolve Technologies Assistant", layout="centered")

    # Centered content
    st.markdown("<h1 style='text-align: center; color: #F1F0E8;'>FinSolve Technologies</h1>", unsafe_allow_html=True)

    # Description box
    st.markdown("""
    <div style="text-align: center; padding: 1.2rem; background-color: #004080; border-radius: 10px; border-left: 5px solid #004080; margin-bottom: 2rem;">
        <p style="font-size: 18px; color: #F1F0E8; line-height: 1.75rem;">
            <strong>FinSolve Technologies</strong> is a leading FinTech company providing 
            innovative financial solutions and services to individuals, businesses, and enterprises.
            <br>
            Let our intelligent assistant help you navigate and find answers to your questions faster and smarter.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Username and password input
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Centered Login Button
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.warning("Please enter both username and password.")
        else:
            with st.spinner("Logging in..."):
                try:
                    response = requests.get(f"{API_URL}/login", auth=HTTPBasicAuth(username, password))
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.password = password
                        st.session_state.role = data["role"]
                        st.session_state.name = data["name"]
                        st.session_state.is_admin = data.get("is_admin", False)
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                except requests.exceptions.RequestException:
                    st.error("⚠️ Server unreachable. Please try again later.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Optional footer
    st.markdown("""
    <div style="text-align: center; color: grey; margin-top: 3rem;">
        © 2025 FinSolve Technologies | Secure. Smart. Scalable.
    </div>
    """, unsafe_allow_html=True)


# --- Auth Pages ---

def register_ui():
    admin_sidebar()
    st.title("📝 Register")
    
    name = st.text_input("Name of the User")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    re_password = st.text_input("Re-Enter Password")
    roles = list(set(fetch_roles() + ["executive"]))
    role = st.selectbox("Role", roles)

    if st.button("Register"):
        if not all([name, username, password, role]):
            st.warning("Please fill all fields.")
        elif password != re_password:
            st.warning("Passwords don't match.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/register",
                    json={"name": name, "username": username, "password": password, "role": role}
                )
                if response.status_code == 201:
                    st.session_state.just_registered = True
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error("Registration failed. Try a different username.")
            except requests.exceptions.RequestException:
                st.error("⚠️ Server unreachable. Please try again later.")

def reset_password_ui():
    admin_sidebar()
    st.title("🔒 Reset User Password")

    username = st.text_input("Enter Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    # Style the button
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: #ffb703;
            color: black;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 6px;
            border: none;
            margin-top: 10px;
        }
        div.stButton > button:hover {
            background-color: #faa307;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("Reset Password"):
        if not username or not new_password or not confirm_password:
            st.warning("Please fill all fields.")
        elif new_password != confirm_password:
            st.warning("Passwords do not match.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/reset_password",
                    json={
                        "username": username,
                        "new_password": new_password
                    },
                    auth=HTTPBasicAuth(st.session_state.username, st.session_state.password)
                )
                if response.status_code == 200:
                    st.success("✅ Password reset successfully.")
                elif response.status_code == 404:
                    st.error("❌ User not found.")
                else:
                    st.error("⚠️ Failed to reset password.")
            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Server unreachable. {e}")


def add_role_ui():
    admin_sidebar()
    st.title("👤➕ Add New Role")

    with st.form("add_role_form"):
        role_name = st.text_input("Type the Role you want to add:")
        role_name = role_name.lower()
        confirm_role = st.text_input("Confirm the Role:")
        confirm_role = confirm_role.lower()
        folder_name = st.text_input("Folder name: ")
        folder_name = folder_name.lower()
        # Custom styled submit button
        st.markdown("""
            <style>
            div.stButton > button {
                background-color: #1f77b4;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 6px;
                border: none;
                margin-top: 10px;
            }
            div.stButton > button:hover {
                background-color: #16659c;
            }
            </style>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button("Add Role")

    if submitted:
        if not role_name or not confirm_role or not folder_name:
            st.error("Please fill in fields.")
            return
        if role_name.strip() != confirm_role.strip():
            st.error("Role names do not match. Please try again.")
            return

        payload = {"role": role_name.strip(), "folder_name":folder_name.strip()}
        try:
            # If using auth:
            # auth=HTTPBasicAuth(st.session_state.username, st.session_state.password)
            response = requests.post(f"{API_URL}/add_role", json=payload)
            if response.status_code == 201:
                st.success(f"✅ Role '{role_name}' added successfully!")
            elif response.status_code == 400:
                st.warning("⚠️ This role already exists.")
            else:
                st.error(f"Unexpected error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Server connection failed: {e}")

def add_docs_role_ui():
    admin_sidebar()
    st.title("📂 Upload Documents for Role")

    # --- Get roles from API ---
    roles = fetch_roles()
    if not roles:
        st.warning("No roles available. Please add roles first.")
        return

    # --- Tabs layout ---
    tab1, = st.tabs(["📁 Upload Files"])

    with tab1:
        selected_role = st.selectbox("Select Role", roles)
        uploaded_files = st.file_uploader(
            "Choose documents",
            type=["csv", "txt", "md", "pdf", "docx"],
            accept_multiple_files=True
        )

    # --- Upload Button ---
    if st.button("➕ Add Documents", type="primary"):
        if not uploaded_files:
            st.error("Please upload at least one document.")
            return

        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
        data = {"role": selected_role}
        with st.spinner("Uploading and ingesting documents..."):
            response = requests.post(
                f"{API_URL}/add_docs_role",
                data=data,
                files=files
            )

            if response.status_code == 200:
                res = response.json()
                st.success("✅ Upload and Ingestion Successful!")

                # ✅ Show file list
                with st.expander("📄 Uploaded Files"):
                    for file in res["saved_files"]:
                        st.markdown(f"- `{file}`")


                # ✅ Success badge-style message
                st.markdown("""
                <div style="padding: 1rem; border-radius: 10px; background-color: #d4edda; color: #155724; margin-top: 1rem;">
                ✅ Your documents are now live in ChromaDB and ready for search!
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(f"❌ Failed: {response.status_code} - {response.text}")
            
        

# --- Chat UI ---

def chat_ui():
    # ----- Session Initialization -----
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'sources' not in st.session_state:
        st.session_state.sources = []

    # ---- Sidebar ----
    with st.sidebar:
        st.title("FinSolve Technologies")
        st.title(f"Hello {st.session_state.name} !")
        

        st.markdown("Your Role")
        st.info(st.session_state.role.capitalize())

        st.markdown("## 📄 Source Document(s)")
        if st.session_state.sources:
            for src in st.session_state.sources:
                st.markdown(f"- {src}")
        else:
            st.markdown("*No sources yet.*")

        # Styled logout button
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                padding: 12px 24px !important;
                font-size: 18px !important;
                width: 100% !important;
                background-color: #e63946 !important;
                color: white !important;
                border: none !important;
                border-radius: 6px !important;
                cursor: pointer;
            }
            div.stButton > button:first-child:hover {
                background-color: #d62828 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

#----------------------Main Chat-------------------------------------

    # --- Session Initialization ---
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())


    # Title
    st.title(f"💬 {st.session_state.role.capitalize()} Chat Assistant")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Get user input
    prompt = st.chat_input("Ask a question...")

    if prompt:

        st.session_state.sources = []
        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                placeholder = st.empty()  # Create an empty container for typing animation
                placeholder.markdown("*Assistant is typing...*")  # Initial typing indicator

                with st.spinner("Generating response..."):
                    # Prepare the payload
                    payload = {
                        "query": prompt,
                        "role": st.session_state.role,
                        "session_id": st.session_state.session_id
                    }

                    # Send request to backend
                    response = requests.post(f"{API_URL}/chat", json=payload, auth=HTTPBasicAuth(st.session_state.username, st.session_state.password))
                    if response.status_code == 200:
                        data = response.json()
                        assistant_reply = data.get("response", "⚠️ No response from model.")
                        new_sources = data.get("sources", [])
                        if new_sources:
                            st.session_state.sources = new_sources
                        
                    else:
                        assistant_reply = f"⚠️ Error from backend. Status code: {response.status_code}"
                        st.session_state.sources = []

        except requests.exceptions.RequestException as e:
            assistant_reply = f"⚠️ Server unreachable. Error: {e}"
            st.session_state.sources = []
                    
        # Store and display assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
        st.rerun()



def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
    if "show_login" not in st.session_state:
        st.session_state.show_login = False

    if st.session_state.get("just_registered"):
        st.success("🎉 Registration successful!.")
        del st.session_state["just_registered"]

    if st.session_state.logged_in:
        with st.sidebar:
            if st.session_state.is_admin:
                selected_page = st.radio(
                                "Go to",
                                ["💬 Chat", "📝 Register", "👤➕ Add Role", "📂 Upload Docs", "🔒 Reset Password"],
                                key="selected_page"
                            )

            else:
                selected_page = "💬 Chat"  # force chat only


        # Route pages
        if selected_page == "💬 Chat":
            chat_ui()
        elif selected_page == "📝 Register" and st.session_state.is_admin:
            register_ui()
        elif selected_page == "👤➕ Add Role" and st.session_state.is_admin:
            add_role_ui()
        elif selected_page == "📂 Upload Docs" and st.session_state.is_admin:
            add_docs_role_ui()
        elif selected_page == "🔒 Reset Password" and st.session_state.is_admin:
            reset_password_ui()
        else:
            st.error("Access denied.")

    elif st.session_state.show_register:
        if st.session_state.get("is_admin"):
            register_ui()
        else:
            st.error("❌ Access denied. Only admins can register users.")
    else:
        home_ui()


if __name__ == "__main__":
    main()
