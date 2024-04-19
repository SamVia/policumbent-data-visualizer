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
st.write("home page")
# @st.cache_resource(ttl=10000)
# def cloneDB():
#   username= "SamVia"
#   password = "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"
#   remote = f"https://{username}:{password}@github.com/SamVia/test_python"
#   git.Repo.clone_from(remote, r"/mount/src/policumbent-data-visualizer/database")
#   return 0
# result = cloneDB()

# def check_file_permissions(file_path):
#    if os.access(file_path, os.R_OK):
#       st.write(f"Read permission is granted for file: {file_path}")
#    else:
#       st.write(f"Read permission is not granted for file: {file_path}")
    
#    if os.access(file_path, os.W_OK):
#       st.write(f"Write permission is granted for file: {file_path}")

#    else:
#       print(f"Write permission is not granted for file: {file_path}")
    
#    if os.access(file_path, os.X_OK):
#       st.write(f"Execute permission is granted for file: {file_path}")
#    else:

#       st.write(f"Execute permission is not granted for file: {file_path}")

# # st.write(os.path.realpath("test_python/test.tb"))
# # check_file_permissions(os.path.realpath("test_python/test.tb"))
# # os.chmod("test_python/test.tb", 0o777)
# # check_file_permissions(os.path.realpath("test_python/test.tb"))

# # Assuming you are currently in the 'START' directory
# start_directory = os.getcwd()

# # Navigate to the 'REPO' directory within the 'START' directory
# repo_directory = os.path.join(start_directory, "database/test_python")
# full_file_path = ""
# # Check if the 'REPO' directory exists
# if os.path.exists(repo_directory):
#     # Change the current working directory to the 'REPO' directory
#     os.chdir(repo_directory)

#     # Open and read the file 'FILE' within the 'REPO' directory
#     file_path = "test.tb"
#     full_file_path = os.path.join(repo_directory, "test.tb")

#     # Check if the file exists
#     if os.path.exists(full_file_path):
#         # Open and read the file
#       check_file_permissions(full_file_path)
#     else:
#         print("File not found.")
# else:
#     print("Repository directory not found.")
# os.chmod(full_file_path, 0o777)
# check_file_permissions(full_file_path)