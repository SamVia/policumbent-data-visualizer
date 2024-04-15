import streamlit as st
import git
import os
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
@st.cache_resource(ttl=10000)
def cloneDB():
  username= "SamVia"
  password = "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"
  remote = f"https://{username}:{password}@github.com/SamVia/test_python"
  git.Repo.clone_from(remote, r"/mount/src/policumbent-data-visualizer/database")
  return 0
result = cloneDB()

def check_file_permissions(file_path):
   if os.access(file_path, os.R_OK):
      st.write(f"Read permission is granted for file: {file_path}")
   else:
      st.write(f"Read permission is not granted for file: {file_path}")
    
   if os.access(file_path, os.W_OK):
      st.write(f"Write permission is granted for file: {file_path}")

   else:
      print(f"Write permission is not granted for file: {file_path}")
    
   if os.access(file_path, os.X_OK):
      st.write(f"Execute permission is granted for file: {file_path}")
   else:

      st.write(f"Execute permission is not granted for file: {file_path}")

st.write(os.path.realpath("test_python/test.tb"))
check_file_permissions(os.path.realpath("test_python/test.tb"))

