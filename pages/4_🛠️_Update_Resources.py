import streamlit as st
import os
from github import Github
import base64
import json
from google.cloud import firestore
from google.oauth2 import service_account
import hashlib
from time import sleep

st.set_page_config(
  page_title="Policumbent",
  page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLBnwH3bm6RwJvsl1-w4PDKxydP6wUIJNDs9pMaI1lpw&s",
  layout="centered" 
)
#code to hide streamlit normal view
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </stile>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
footer="""<style>
.footer {
-webkit-user-select: none; 
-moz-user-select: none; 
-ms-user-select: none; 
user-select: none; 
position: fixed;
right: -7vh;
bottom: 0;
width: 100%;
background-color: transparent;
color: rgba(128,128,128,0.6);
text-align: left;
}
</style>
<div class="footer">
<p>Version 1.0.0<a style='display: block; text-align: right;</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
# with st.sidebar:
#     st.sidebar.markdown("""<style>
# .reportview-container .main .block-container {
#     max-width: 120px;
#     padding-top: 2rem;
#     padding-right: 2rem;
#     padding-left: 2rem;
#     padding-bottom: 10rem;
# }
# .footer {
#     position: absolute;
#     bottom: -87vh;
#     width: 100%;
#     text-align: center;
#     color:rgba(128,128,128,0.6);
#     font-weight: bold;  
#     font-size: 2.5vh; 
# }
# </style>
# <p class="footer">Version 1.0.0</p>
# """, unsafe_allow_html=True)
#connection to firebase and fetch all current data
@st.cache_resource
def connect_to_db():
  key_dict = json.loads(st.secrets["textkey"])
  creds = service_account.Credentials.from_service_account_info(key_dict,)
  return firestore.Client(credentials=creds)

if "auth" not in st.session_state:
    #check on credentials
    st.session_state.auth = False

def verify_password(username, plain_password, stored_hash, salt):
    """function to check credentials, combines username and password with a salt

    Args:
        username (String): username field
        plain_password (String): password field
        
    Returns:
        bool: True if hash is the same
    """
    # Hash the input password with the stored salt
    combined = f"{username}{plain_password}{salt}"
    hashed_password = hashlib.sha256(combined.encode()).hexdigest()
    # Compare with the stored hash
    return hashed_password == stored_hash

if not st.session_state.auth:
    #while not authorized
    username = str(st.text_input("username",type="password"))
    password = str(st.text_input("password",type="password"))
    if st.button("log in"):
        with st.spinner("checking credentials"):
            sleep(1.5)
        #check password
        if verify_password(username = username, plain_password = password, stored_hash= st.secrets["hash"], salt = st.secrets["salt"]):
            st.success("authorized, logging in")
            st.session_state.auth = True
            st.empty()
            sleep(0.5)
            st.rerun()
        else:st.error("unauthorized user, check credentials")
else:
    #creation of github object
    g = Github(st.secrets["pat"])
    # Then get the specific repo
    repo = g.get_user().get_repo("Policumbent-Database")
    # Get the ref for the file
    contents = repo.get_contents("test.db")

    os.chdir("/mount/src/policumbent-data-visualizer/database/") 
    if st.button("commit"):
        try:
            #encoding database content in base64 format
            with open("/mount/src/policumbent-data-visualizer/database/new_db.db", "rb") as file:
                content = file.read()
                content_encoded = base64.b64encode(content)
        except Exception as e:
            st.write(e)
        try:
            #pushing database to repo
            repo.update_file(path=contents.path, message="updated database", content=content_encoded.decode(), sha=contents.sha)
            #print("File updated successfully.")
        except Exception as e:
            st.write(e)
        st.success("commit done!")

    os.chdir("/mount/src/policumbent-data-visualizer/")

    g.close()