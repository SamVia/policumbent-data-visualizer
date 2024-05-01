import streamlit as st
import git
import os
import base64
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

pat = st.secrets["pat"]

repo_dir = "/mount/src/policumbent-data-visualizer/database"
username = "SamVia"
repo_name = "Policumbent-Database"
remote = f"https://{username}:{pat}@github.com/{username}/{repo_name}.git"

def decode_base64_file(database_path):
    # Read the base64-encoded content from the input file
    try:
        with open(database_path, "rb") as file:
            encoded_content = file.read()

        # Decode the base64-encoded content
        decoded_content = base64.b64decode(encoded_content)

        # Write the decoded content to the output file
        with open(database_path, "wb") as file:
            file.write(decoded_content)
    except:
        st.write("there has been an error reading the file")


try:
    if os.path.isdir(repo_dir):
        # If the directory already exists, just pull the changes
        st.write("pulling")
        repo = git.Repo(repo_dir)
        repo.remotes.origin.pull()
        
    else:
        #If the directory doesn't exist, clone the repository
        st.write("cloning")
        git.Repo.clone_from(remote, repo_dir, depth=1)
        repo = git.Repo(repo_dir)
except Exception as e: st.write(e)

decode_base64_file(database_path=r'/mount/src/policumbent-data-visualizer/database/test.db')


#change current working directory to where the database is:

#change permissions to database file and folder#
os.chmod("/mount/src/policumbent-data-visualizer/database/test.db", 0o777)
os.chmod("/mount/src/policumbent-data-visualizer/database", 0o777)