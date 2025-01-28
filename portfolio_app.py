import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="My Portfolio",
    page_icon="👨‍💻",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
:root {
    --primary-color: #2D3250;
    --secondary-color: #424769;
    --accent-color: #7077A1;
    --text-color: #333;
    --light-bg: #F6F4EB;
}

.main {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.stApp {
    background-color: var(--light-bg);
    color: var(--text-color);
}

.css-1d391kg {
    padding-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    page = st.radio(
        "Go to",
        ["About", "Experience", "Skills", "Projects", "Contact"]
    )

# Header Section
if page == "About":
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/200", width=200)
    
    with col2:
        st.title("John Doe")
        st.subheader("Full Stack Developer")
        st.write("""
        Passionate software developer with expertise in building scalable web applications 
        and solving complex problems. Experienced in modern web technologies and best practices.
        """)
        
        # Social Links
        st.write("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)")
        st.write("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com)")

# Experience Section
elif page == "Experience":
    st.title("Professional Experience")
    
    with st.container():
        st.subheader("Senior Software Developer | Tech Corp")
        st.write("2020 - Present")
        st.write("""
        - Led development of microservices architecture
        - Implemented CI/CD pipelines
        - Mentored junior developers
        """)
    
    with st.container():
        st.subheader("Software Developer | StartUp Inc")
        st.write("2018 - 2020")
        st.write("""
        - Developed full-stack web applications
        - Optimized database performance
        - Collaborated with cross-functional teams
        """)

# Skills Section
elif page == "Skills":
    st.title("Skills & Expertise")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Technical Skills")
        skills_data = {
            'Skill': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
            'Level': [90, 85, 80, 85, 90]
        }
        df = pd.DataFrame(skills_data)
        st.bar_chart(df.set_index('Skill'))
    
    with col2:
        st.subheader("Tools & Technologies")
        st.write("""
        - **Version Control:** Git, GitHub
        - **Databases:** PostgreSQL, MongoDB
        - **Cloud:** AWS, Google Cloud
        - **Other:** Docker, Kubernetes
        """)

# Projects Section
elif page == "Projects":
    st.title("Featured Projects")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("E-commerce Platform")
        st.image("https://via.placeholder.com/300x200")
        st.write("""
        Built a full-stack e-commerce platform using React and Node.js.
        Features include user authentication, product management, and payment integration.
        """)
        st.button("View Project", key="proj1")
    
    with col2:
        st.subheader("AI Image Recognition")
        st.image("https://via.placeholder.com/300x200")
        st.write("""
        Developed an AI-powered image recognition system using TensorFlow.
        Achieved 95% accuracy in object detection.
        """)
        st.button("View Project", key="proj2")

# Contact Section
elif page == "Contact":
    st.title("Get in Touch")
    
    contact_form = """
    <form action="https://formsubmit.co/your@email.com" method="POST">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    
    st.markdown(contact_form, unsafe_allow_html=True)
    
    # Custom CSS for form styling
    st.markdown("""
    <style>
    input[type=text], input[type=email], textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        box-sizing: border-box;
        margin-top: 6px;
        margin-bottom: 16px;
        resize: vertical
    }
    button[type=submit] {
        background-color: #04AA6D;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    button[type=submit]:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)