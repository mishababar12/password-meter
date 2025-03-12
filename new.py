import streamlit as st
import re
import matplotlib.pyplot as plt
import pandas as pd
import random
import string

# Custom CSS for styling
st.markdown("""
<style>
/* Main background color */
.stApp {
    background-color: #001F3F; /* Dark blue */
    font-family: 'Arial', sans-serif;
    color: white; /* White text for better visibility */
}
/* Header styling */
header {
    background-color:  #001F3F !important; /* Dark blue */
}
/* Overlay to improve text visibility */
.overlay {
    background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black overlay */
    padding: 20px;
    border-radius: 10px;
}
@keyframes progress {
    0% { width: 0%; }
    100% { width: 100%; }
}
.progress-bar {
    height: 20px;
    background-color: #4CAF50;
    width: 0%;
    animation: progress 2s ease-in-out;
}
.password-feedback {
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
.password-feedback.weak {
    background-color: #FFCCCB;
}
.password-feedback.medium {
    background-color: #FFD700;
}
.password-feedback.strong {
    background-color: #90EE90;
}
/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(173, 216, 230, 0.8) !important; /* Light blue with transparency */
    padding: 20px;
    border-radius: 10px;
}
/* Main title styling */
.main-title {
    font-size: 36px;
    font-weight: bold;
    color: #FF5733; /* Orange */
    text-align: center;
    margin-bottom: 20px;
}
/* Feedback styling */
.feedback-heading {
    font-size: 20px;
    font-weight: bold;
    color: white; /* White color */
    background-color: rgba(255, 87, 51, 0.8); /* Orange background with transparency */
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    margin-bottom: 10px;
}
/* Visual Insights Heading */
.visual-insights-heading {
    font-size: 24px;
    font-weight: bold;
    color: #FF5733; /* Orange */
    text-align: center;
    margin-bottom: 20px;
}
/* Password input styling */
.password-input {
    font-size: 18px;
    padding: 10px;
    border-radius: 5px;
    border: 2px solid #FF5733; /* Orange */
}
/* Sidebar text styling */
.sidebar-text {
    font-size: 18px;
    color: #333; /* Dark gray */
}
</style>
""", unsafe_allow_html=True)

# Password blacklist (common weak passwords)
PASSWORD_BLACKLIST = [
    "password", "123456", "qwerty", "admin", "letmein", "welcome", "123abc"
]

# Function to check password strength
def check_password_strength(password):
    strength = 0
    feedback = []

    # Check length
    if len(password) >= 12:
        strength += 1
    else:
        feedback.append("Password should be at least 12 characters long.")

    # Check for uppercase letters
    uppercase_count = len(re.findall(r'[A-Z]', password))
    if uppercase_count >= 1:
        strength += 1
    else:
        feedback.append("Include at least one uppercase letter.")

    # Check for lowercase letters
    lowercase_count = len(re.findall(r'[a-z]', password))
    if lowercase_count >= 1:
        strength += 1
    else:
        feedback.append("Include at least one lowercase letter.")

    # Check for numbers
    numbers_count = len(re.findall(r'[0-9]', password))
    if numbers_count >= 1:
        strength += 1
    else:
        feedback.append("Include at least one number.")

    # Check for special characters
    special_chars_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', password))
    if special_chars_count >= 1:
        strength += 1
    else:
        feedback.append("Include at least one special character.")

    # Check against blacklist
    if password.lower() in PASSWORD_BLACKLIST:
        strength = 0
        feedback.append("This password is too common and weak. Please choose a stronger one.")

    return strength, feedback, uppercase_count, lowercase_count, numbers_count, special_chars_count

# Function to generate a strong password
def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# Streamlit App
st.markdown("<div class='overlay'><div class='main-title'>✨ Advanced Password Strength Meter</div></div>", unsafe_allow_html=True)

# Sidebar content
st.sidebar.markdown("<div class='sidebar-text'>🔐 <strong>Generate a Strong Password</strong></div>", unsafe_allow_html=True)
if st.sidebar.button("Generate Password 🛠️"):
    strong_password = generate_strong_password()
    st.sidebar.write(f"Generated Password: `{strong_password}`")

st.sidebar.markdown("<div class='sidebar-text'>📜 <strong>Password History</strong></div>", unsafe_allow_html=True)

# Password input
password = st.text_input("Enter your password to check its strength:", type="password", key="password_input")

# Password history
if "password_history" not in st.session_state:
    st.session_state.password_history = []

if password:
    strength, feedback, uppercase_count, lowercase_count, numbers_count, special_chars_count = check_password_strength(password)
    st.session_state.password_history.append((password, strength))

    # Progress bar with animation
    progress_width = (strength / 5) * 100
    st.markdown(f"""
    <div style="background-color: #f3f3f3; border-radius: 5px; width: 100%;">
        <div class="progress-bar" style="width: {progress_width}%;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Strength feedback
    if strength == 5:
        st.markdown("<div class='password-feedback strong'>✅ Your password is strong!</div>", unsafe_allow_html=True)
    elif strength >= 3:
        st.markdown("<div class='password-feedback medium'>⚠️ Your password is medium. Consider improving it.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='password-feedback weak'>❌ Your password is weak. Please improve it.</div>", unsafe_allow_html=True)

    # Display feedback
    if feedback:
        st.markdown("<div class='feedback-heading'>📝 Feedback to Improve</div>", unsafe_allow_html=True)
        for tip in feedback:
            st.write(f"- {tip}")

    # Visual insights using Matplotlib (Line Chart)
    st.markdown("<div class='visual-insights-heading'>📊 Visual Insights</div>", unsafe_allow_html=True)
    categories = ['Uppercase', 'Lowercase', 'Numbers', 'Special Chars']
    counts = [uppercase_count, lowercase_count, numbers_count, special_chars_count]

    fig, ax = plt.subplots()
    ax.plot(categories, counts, marker='o', linestyle='-', color='b', label='Counts')
    ax.set_ylim(0, max(counts) + 1)
    ax.set_ylabel("Count")
    ax.set_title("Password Composition")
    ax.legend()
    st.pyplot(fig)

# Password History
if st.session_state.password_history:
    history_df = pd.DataFrame(st.session_state.password_history, columns=["Password", "Strength"])
    st.sidebar.write(history_df)
else:
    st.sidebar.write("No password history yet.")