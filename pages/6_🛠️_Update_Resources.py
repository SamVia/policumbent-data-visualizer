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
)
#code to hide streamlit normal view
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </stile>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

#check password and user?


#connection to firebase and fetch all current data
@st.cache_resource
def connect_to_db():
  key_dict = json.loads(st.secrets["textkey"])
  creds = service_account.Credentials.from_service_account_info(key_dict,)
  return firestore.Client(credentials=creds)

if "auth" not in st.session_state:
    st.session_state.auth = False

def verify_password(username, plain_password, stored_hash, salt):
    # Hash the input password with the stored salt
    combined = f"{username}{plain_password}{salt}"
    hashed_password = hashlib.sha256(combined.encode()).hexdigest()
    # Compare with the stored hash
    return hashed_password == stored_hash

#establish github object


if not st.session_state.auth:
    username = str(st.text_input("username",type="password"))
    password = str(st.text_input("password",type="password"))
    if st.button("log in"):
        with st.spinner("checking credentials"):
            sleep(0.7)
            if verify_password(username = username, plain_password = password, stored_hash= st.secrets["hash"], salt = st.secrets["salt"]):
                st.success("authorized, logging in")
                st.session_state.auth = True
                st.empty()
                sleep(0.5)
                st.rerun()
else:
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
            print("File updated successfully.")
        except Exception as e:
            st.write(e)

    os.chdir("/mount/src/policumbent-data-visualizer/")

    g.close()