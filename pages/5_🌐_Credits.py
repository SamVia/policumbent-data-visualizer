import streamlit as st

st.set_page_config(
  page_title="Policumbent",
  page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLBnwH3bm6RwJvsl1-w4PDKxydP6wUIJNDs9pMaI1lpw&s",
  layout="centered" 
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
st.sidebar.markdown("""<style>
.reportview-container .main .block-container {
    max-width: 120px;
    padding-top: 2rem;
    padding-right: 2rem;
    padding-left: 2rem;
    padding-bottom: 10rem;
}
.footer {
    position: absolute;
    bottom: -87vh;
    width: 100%;
    text-align: center;
    color:rgba(128,128,128,0.6);
    font-weight: bold;  
    font-size: 2.5vh; 
}
</style>
<p class="footer">Version 1.0.0</p>
""", unsafe_allow_html=True)

def display_image(img_link):
    """function to generate markdown for displaying image
    """
    return f"""
                <div class="image-container">
    <img src="{img_link}" alt="Description of the image" 
    style="
    background-color: rgba(0,0,0,0.3);
    height: auto; 
    width: 230px;
    border-radius: 10px;
    padding:0px;
    position:relative;
    left:-160px;
    /*box-shadow: 0 0 10px rgba(100, 100, 100, 0.1);*/">
</div>"""

def display_text(text):
    """generates markdown for a text field in similar fashion to others, need printable text as input
    """
    return f"""<head>
    <style>
    .custom-text {{
      /* Dimension Properties */
      width: 230px;
      height: auto;

      /* Padding and Margin Properties */
      padding: 20px;
      margin: 0px;

      /* Border Properties */
      border-width: 2px;
      border-style: solid;
      border-color: black;
      border-radius: 10px;

      /* Background Properties */
      background-color: #000000;

      /* Text Properties */
      color: white;
      text-align: center;
      font-size: 16px;

      /* Display Properties */
      display: block;

      /* Positioning Properties */
      position: relative;
      left:-160px;
      top:15px;

      /* Transition Properties */
      transition: all 0.5s ease;
    }}
  </style>
  </head>
  <body>
    <div class="custom-text">
    {text}
</div>
</body>
"""

def button_logo(site, logo, circle):
    """generates markdown for a button to a site
    accepts site link, logo link better if png, and circle is true if the logo is circular else false
    """
    if circle: circle = "border-radius:50%;"
    else: circle = ""
    return f"""
<style>
    .myButton {{
        background-color: transparent;
        color: white;
        padding: 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 0px;
        cursor: pointer;
        border: none;
        border-radius: 50%;
        transition: transform .2s;
        outline: none;
        position:relative;
        left:{-100}px;
    }}

    .myButton:hover {{
        transform: scale(1.1);
    }}
</style>

<a href="{site}" class="myButton" target="_blank">
    <button class="myButton">
        <img src="{logo}" alt="Image description" style="width:50px;height:50px;{circle}">
    </button>
</a>
"""

st.title("Credits")
#markdown for all tools used in this project
st.markdown("""<!DOCTYPE html>
<html>
<head>
    <style>
        .myDiv {
            width: 800px; /* Width of the div */
            height: auto; /* Height of the div */
            padding: 20px; /* Inner space of the div */
            margin: 10px; /* Outer space of the div */
            background-color: transparent; /* Background color of the div */
            border: transparent; /* Border around the div */
            font-size: 50px; /* Text size in the div */
            color: #f0f0f0; /* Text color in the div */
            text-align: justify; /* Text alignment in the div */
            position:relative;
            left:-170px;
        }
        .myDiv img {
            display: inline-block;
            width: auto;
            height: 80px;
            position: relative;
            top:5px;
        }
    </style>
</head>
<body>
<div class="myDiv">
    Tools used:
    <br>
    <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" alt="">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/935px-Python-logo-notext.svg.png" alt="" style="position:relative; top:7px; left: 7px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/CSS3_and_HTML5_logos_and_wordmarks.svg/1280px-CSS3_and_HTML5_logos_and_wordmarks.svg.png" alt="" style="position:relative; right:-15px;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Firebase_icon.svg/2048px-Firebase_icon.svg.png" alt="" style="position:relative; right:-20px;">
</div>
</body>
</html>
       """, unsafe_allow_html=True)

st.divider()
col1, col2,col3 = st.columns(3)
with col1:
    col1.markdown(display_image("https://www.datocms-assets.com/39999/1686210442-samuele-vianello-it.png?fm=webp&q=70&w=270"), unsafe_allow_html=True)
    col1.markdown(display_text("TEST"), unsafe_allow_html=True)
    columns = col1.columns(4)
    # text1 =button_logo("","https://miro.medium.com/v2/resize:fit:400/1*MgGIm08OdUTUvgNyaUl0hw.jpeg",True)
    # text2 = button_logo("","https://miro.medium.com/v2/resize:fit:400/1*MgGIm08OdUTUvgNyaUl0hw.jpeg",True)
    # st.markdown(text1+text2, unsafe_allow_html=True)
    with columns[0]:
        st.markdown(button_logo("https://github.com/SamVia","https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",True), unsafe_allow_html=True)
    with columns[1]:
       st.markdown(button_logo("https://www.linkedin.com/in/samuele-vianello/","https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/640px-LinkedIn_logo_initials.png",False), unsafe_allow_html=True)
    




template = """
    HOW-TO:
    0. copy the template, to leave for future usage the empty one
    1. chose position in page: col1, col2, col3. if already present it will be added under it.
    2. input personal image link 
    3. input personal links, possibly even icons to those links in the columns part. 0 is the left-most, there can be max 4 links
    """
# with col2:
#     col2.markdown(display_image("insert personal image link"), unsafe_allow_html=True)
#     col2.markdown(display_text("insert description"), unsafe_allow_html=True)
#     columns = col2.columns(4)
#     with columns[0]:
#         st.markdown(button_logo("github link","https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",True), unsafe_allow_html=True)

#     with columns[1]:
#         st.markdown(button_logo("link to something round","round.png",True), unsafe_allow_html=True)
#     with columns[2]:
#        st.markdown(button_logo("link to something squared","https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/LinkedIn_logo_initials.png/640px-LinkedIn_logo_initials.png",False), unsafe_allow_html=True)
#     with columns[3]:
#         st.markdown(button_logo("possible fourth link","delete if not needed",True), unsafe_allow_html=True)
    