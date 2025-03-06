import streamlit as st
import smtplib
from email.mime.text import MIMEText
import plotly.express as px
import json
import os
from io import BytesIO

# Set page title and icon
st.set_page_config(page_title="Student Portfolio", page_icon="🎓")

# Custom CSS for animations, hover effects, and timeline
st.markdown("""
<style>
    /* Timeline styling */
    .timeline {
        position: relative;
        max-width: 800px;
        margin: 0 auto;
    }
    .timeline::after {
        content: '';
        position: absolute;
        width: 6px;
        background-color: #4CAF50;
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -3px;
    }
    .timeline-item {
        padding: 10px 40px;
        position: relative;
        background-color: inherit;
        width: 50%;
    }
    .timeline-item::after {
        content: '';
        position: absolute;
        width: 25px;
        height: 25px;
        right: -12px;
        background-color: white;
        border: 4px solid #4CAF50;
        top: 15px;
        border-radius: 50%;
        z-index: 1;
    }
    .left {
        left: 0;
    }
    .right {
        left: 50%;
    }
    .left::before {
        content: " ";
        height: 0;
        position: absolute;
        top: 22px;
        width: 0;
        z-index: 1;
        right: 30px;
        border: medium solid white;
        border-width: 10px 0 10px 10px;
        border-color: transparent transparent transparent white;
    }
    .right::before {
        content: " ";
        height: 0;
        position: absolute;
        top: 22px;
        width: 0;
        z-index: 1;
        left: 30px;
        border: medium solid white;
        border-width: 10px 10px 10px 0;
        border-color: transparent white transparent transparent;
    }
    .right::after {
        left: -12px;
    }
    .timeline-content {
        padding: 20px 30px;
        background-color: white;
        color:black;
        position: relative;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .timeline-content::hover {
        padding: 20px 30px;
        background-color: black;
        color:yellow;
    }
</style>
""", unsafe_allow_html=True)

# File to store user data
DATA_FILE = "user_data.json"
TESTIMONIALS_FILE = "testimonials.json"
DEFAULT_IMAGE = "default.jpeg"

# Load user data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {
        "name": "Clement M.",
        "location": "Musanze, Rwanda",
        "profile_pic": DEFAULT_IMAGE,
        "about_me": "I am a passionate AI look forward engineer!"
    }

# Save user data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Load testimonials from file
def load_testimonials():
    if os.path.exists(TESTIMONIALS_FILE):
        with open(TESTIMONIALS_FILE, "r") as file:
            return json.load(file)
    return []

# Save testimonials to file
def save_testimonials(testimonials):
    with open(TESTIMONIALS_FILE, "w") as file:
        json.dump(testimonials, file)

# Load user data and testimonials
user_data = load_data()
testimonials = load_testimonials()

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go To:", ["Home", "Projects", "Skills", "Testimonials", "Timeline", "Settings", "Contact"])

# Home section
if page == "Home":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🎓 Student Portfolio")

    # Profile image
    uploaded_image = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
    if uploaded_image is not None:
        # Save the uploaded image to a temporary file
        user_data['profile_pic'] = uploaded_image.name
        with open(uploaded_image.name, "wb") as f:
            f.write(uploaded_image.getbuffer())
        save_data(user_data)

    # Display the profile picture
    if os.path.exists(user_data['profile_pic']):
        st.image(user_data['profile_pic'], width=150, caption="Profile Picture")
    else:
        st.image(DEFAULT_IMAGE, width=150, caption="Default Profile Picture")

    # Student details (Editable!)
    name = st.text_input("Name: ", user_data['name'])
    location = st.text_input("Location: ", user_data['location'])
    field_of_study = st.text_input("Field of Study: ", "Computer Science, SWE")
    university = st.text_input("University: ", "INES - Ruhengeri")

    st.write(f"📍{location}")
    st.write(f"📚{field_of_study}")
    st.write(f"🎓{university}")

    # Resume download button
    with open("resume.pdf", "rb") as file:
        resume_bytes = file.read()
    st.download_button(label="📄Download Resume",
                       data=resume_bytes, file_name="resume.pdf",
                       mime="application/pdf")

    st.markdown("---")
    st.subheader("About Me")
    about_me = st.text_area("Short introduction about myself:", user_data['about_me'])
    user_data['about_me'] = about_me
    save_data(user_data)
    st.write(about_me)
    st.markdown('</div>', unsafe_allow_html=True)

# Projects section
elif page == "Projects":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("💻 My Projects")

    with st.expander("🏃‍ Smart Queue Management (SQM) Project"):
        st.write("To design and implement an intelligent queue management system that improves efficiency, reduces wait times, and enhances user satisfaction by leveraging advanced technologies like AI, IoT, and data analytics.")
        st.markdown("[GitHub Repository](https://github.com/your-repo)")
        st.image("project1.png", caption="GDP Analysis Visualization")

    with st.expander("Attendene Recording System"):
        st.write("Simplify The way Attendence is done from traditional paper to Digital system")
        st.markdown("[Live Demo](https://your-demo-link.com)")
    st.markdown('</div>', unsafe_allow_html=True)

# Skills section
elif page == "Skills":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("⚡ Skills and Achievements")

    st.subheader("Programming Skills")
    skill_python = st.slider("Python", 0, 100, 90)
    skill_js = st.slider("JavaScript", 0, 100, 75)
    skill_AI = st.slider("Artificial Intelligence", 0, 100, 65)

    # Bar chart for skills
    skills = {
        "Python": skill_python,
        "JavaScript": skill_js,
        "AI": skill_AI
    }
    fig = px.bar(x=list(skills.keys()), y=list(skills.values()), labels={"x": "Skill", "y": "Proficiency"})
    st.plotly_chart(fig)

    st.subheader("Certifications & Achievements")
    st.write("✔️ Completed AI&ML in Business Certification")
    st.write("✔️ Certified AI in Research and Course Preparation for Education")
    st.markdown('</div>', unsafe_allow_html=True)

# Testimonials section
elif page == "Testimonials":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🗣️ Student Testimonials")

    # Display existing testimonials
    st.subheader("What People Say About Me")
    for testimonial in testimonials:
        st.markdown(f"**{testimonial['name']}** says:")
        st.write(f"\"{testimonial['message']}\"")
        st.write(f"– {testimonial['role']}")
        st.markdown("---")

    # Form to submit a new testimonial
    st.subheader("Leave a Testimonial")
    with st.form("testimonial_form"):
        name = st.text_input("Your Name")
        role = st.text_input("Your Role (e.g., Classmate, Mentor)")
        message = st.text_area("Your Testimonial")

        submitted = st.form_submit_button("Submit Testimonial")
        if submitted:
            if name and role and message:
                new_testimonial = {
                    "name": name,
                    "role": role,
                    "message": message
                }
                testimonials.append(new_testimonial)
                save_testimonials(testimonials)
                st.success("✅ Thank you for your testimonial!")
            else:
                st.error("❌ Please fill out all fields.")
    st.markdown('</div>', unsafe_allow_html=True)

# Timeline section
elif page == "Timeline":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("⏳ Timeline of Academic & Project Milestones")

    # Timeline HTML
    st.markdown("""
    <div class="timeline">
        <div class="timeline-item left">
            <div class="timeline-content">
                <h3>Year 1</h3>
                <p>First project completed ✅</p>
            </div>
        </div>
        <div class="timeline-item right">
            <div class="timeline-content">
                <h3>Year 2</h3>
                <p>Hackathon participation 🏆</p>
            </div>
        </div>
        <div class="timeline-item left">
            <div class="timeline-content">
                <h3>Year 3</h3>
                <p>Internship experience 💼</p>
            </div>
        </div>
        <div class="timeline-item right">
            <div class="timeline-content">
                <h3>Year 4</h3>
                <p>Dissertation submission 📚</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
# Settings section
elif page == "Settings":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🎨 Customize your profile")

    st.subheader("Upload a Profile Picture")
    uploaded_image = st.file_uploader("Choose a file", type=["jpg", "png"])
    if uploaded_image:
        user_data['profile_pic'] = uploaded_image.name
        with open(uploaded_image.name, "wb") as f:
            f.write(uploaded_image.getbuffer())
        save_data(user_data)
        st.image(user_data['profile_pic'], width=150)

    st.subheader("✍️ Edit Personal Info")
    name = st.text_input("Name: ", user_data['name'])
    location = st.text_input("Location: ", user_data['location'])
    about_me = st.text_area("About Me: ", user_data['about_me'])

    if st.button("Save Changes"):
        user_data['name'] = name
        user_data['location'] = location
        user_data['about_me'] = about_me
        save_data(user_data)
        st.success("✅ Changes saved successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# Contact section
elif page == "Contact":
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("📬 Contact Me")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")

        submitted = st.form_submit_button("Send Message")
        if submitted:
            try:
                # Configure email settings
                msg = MIMEText(f"Name: {name}\nEmail: {email}\nMessage: {message}")
                msg['Subject'] = "New Contact Form Submission"
                msg['From'] = "your-email@example.com"
                msg['To'] = "recipient@example.com"

                # Send email
                with smtplib.SMTP("smtp.example.com") as server:
                    server.sendmail("your-email@example.com", "recipient@example.com", msg.as_string())
                st.success("✅ Message sent successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    st.write("📧 rogermuhire8@gmail")
    st.write("[🔗LinkedIn](https://www.linkedin.com/in/muhire-roger-9a304b268/)")
    st.write("[📂GitHub](https://www.linkedin.com/in/muhire-roger-9a304b268/w)")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.sidebar.write("---")
st.sidebar.write("🔹 Made with Roger Muhire")