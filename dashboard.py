import ollama
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Student Analytics",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Student Performance & Career Analytics")
st.caption("Student performance, skills and career insights in one dashboard")
st.write("Student analytics dashboard")

data = pd.read_csv("data/students.csv")


st.subheader("📂 Upload Student Data")

uploaded_file = st.file_uploader(
    "📂 Upload Student Data",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel file containing Name, Subject, Marks and Attendance."
)

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    # Remove extra index column
    if "Unnamed: 0" in data.columns:
        data = data.drop(columns=["Unnamed: 0"])

    # Check required columns
    required_columns = [
        "Name",
        "Subject",
        "Marks",
        "Attendance"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        st.error(
            f"❌ Missing columns: {', '.join(missing_columns)}"
        )
        st.write("Columns found:", data.columns.tolist())

    else:
        st.success("✅ Student data uploaded successfully!")
        st.dataframe(data)
    required_columns = [
    "Name",
    "Subject",
    "Marks",
    "Attendance"
]

required_columns = [
    "Name",
    "Subject",
    "Marks",
    "Attendance"
]
required_columns = [
    "Name",
    "Subject",
    "Marks",
    "Attendance"
]
missing_columns = [
    col for col in required_columns
    if col not in data.columns
]

if missing_columns:
    st.error(
        "❌ Missing columns: "
        + ", ".join(missing_columns)
    )
    st.stop()
def performance_category(score):
    if score >= 85:
        return "Excellent"
    elif score >= 75:
        return "Good"
    else:
        return "Needs Improvement"

st.subheader("📊 Student Data")
st.dataframe(data)

st.subheader("📊 Key Statistics")
st.subheader("📊 Dashboard Overview")
col1, col2, col3 = st.columns(3)

col1, col2, col3 = st.columns(3)

col1.metric(
    "👥 Total Students",
    data["Name"].nunique()
)

col2.metric(
    "📈 Average Marks",
    round(data["Marks"].mean(), 2)
)

col3.metric(
    "📝 Average Attendance",
    f"{round(data['Attendance'].mean(), 2)}%"
)
st.subheader("📈 Student-wise Performance")
student_average = data.groupby("Name")["Marks"].mean()
st.bar_chart(student_average)

st.subheader("📅 Student-wise Attendance")
student_attendance = data.groupby("Name")["Attendance"].mean()
st.bar_chart(student_attendance)

st.subheader("📚 Subject-wise Average Marks")
subject_average = data.groupby("Subject")["Marks"].mean()
st.bar_chart(subject_average)

st.subheader("🎯 Student Performance Score")
student_marks = data.groupby("Name")["Marks"].mean()
student_attendance = data.groupby("Name")["Attendance"].mean()

performance = student_marks * 0.7 + student_attendance * 0.3
st.subheader("📈 Overall Performance")

avg_performance = performance.mean()

st.metric(
    "⭐ Average Performance Score",
    f"{avg_performance:.2f}"
)
st.progress(
    int(avg_performance)
)
performance_report = pd.DataFrame(
    {
        "Average Marks": student_marks.round(2),
        "Average Attendance": student_attendance.round(2),
        "Performance Score": performance.round(2),
    },
    index=student_marks.index,
)
st.subheader("📈 Marks vs Attendance")

marks_attendance = data.groupby("Name").agg(
    Average_Marks=("Marks", "mean"),
    Average_Attendance=("Attendance", "mean")
).round(2)

st.dataframe(marks_attendance)

st.bar_chart(marks_attendance)
performance_report.index.name = "Name"
performance_report["Category"] = performance_report["Performance Score"].apply(
    performance_category
)
st.subheader("🎯 Performance Category Summary")

st.subheader("📋 Student Performance Report")

st.dataframe(
    performance_report,
    use_container_width=True
)

st.write("Performance distribution of all students:")

category_summary = performance_report["Category"].value_counts()

st.bar_chart(category_summary)

st.download_button(
    label="📥 Download Performance Report",
    data=performance_report.to_csv(index=True).encode("utf-8"),
    file_name="student_performance_report.csv",
    mime="text/csv",
    key="download_performance_report"
)
st.subheader("👤 Student Analysis")

selected_student = st.selectbox(
    "Select a Student",
    performance_report.index
)
student_data = performance_report.loc[selected_student]

category = performance_category(
    student_data["Performance Score"]
)

st.write("### 📋 Selected Student Performance")

st.write(f"Category: {category}")

st.metric(
    "Performance Score",
    student_data["Performance Score"]
)

st.metric(
    "Average Marks",
    student_data["Average Marks"]
)

st.metric(
    "Average Attendance",
    f"{student_data['Average Attendance']}%"
)

st.subheader("🎯 Career Skill Gap Analyzer")

# Career roles based on PCMB subject strengths
career_roles = {
    "Engineering / Technical": {
        "subjects": ["Math", "Physics"],
        "skills": [
            "Math",
            "Physics",
            "Problem Solving",
            "Programming"
        ]
    },

    "Medical / Health Science": {
        "subjects": ["Biology", "Chemistry"],
        "skills": [
            "Biology",
            "Chemistry"
        ]
    },

    "Biotechnology / Life Science": {
        "subjects": ["Biology", "Chemistry"],
        "skills": [
            "Biology",
            "Chemistry"
        ]
    },

    "Data / Analytics": {
        "subjects": ["Math"],
        "skills": [
            "Math",
            "Statistics",
            "Python",
            "SQL"
        ]
    }
}
# Student's subject marks
# Select student for career analysis
career_student = st.selectbox(
    "👨‍🎓 Select Student",
    data["Name"].dropna().unique().tolist(),
    key="dynamic_career_student"
)
student_subjects = data[
    data["Name"] == career_student
].groupby("Subject")["Marks"].mean()

# Calculate subject strengths
math = student_subjects.get("Math", 0)
physics = student_subjects.get("Physics", 0)
chemistry = student_subjects.get("Chemistry", 0)
biology = student_subjects.get("Biology", 0)

# Calculate career scores
career_scores = {
    "Engineering / Technical": (math + physics) / 2,
    "Medical / Health Science": (biology + chemistry) / 2,
    "Biotechnology / Life Science": (biology + chemistry) / 2,
    "Data / Analytics": math
}

# Highest score becomes suggested career role
suggested_role = max(
    career_scores,
    key=career_scores.get
)

st.write("### 🎯 Suggested Career Role")

st.success(
    f"🎓 {suggested_role}"
)

st.write("### 📊 Subject Performance")

subject_display = pd.DataFrame({
    "Subject": ["Math", "Physics", "Chemistry", "Biology"],
    "Marks": [math, physics, chemistry, biology]
})

st.bar_chart(
    subject_display.set_index("Subject")
)

# Required skills for suggested role
required_skills = career_roles[suggested_role]["skills"]

st.write("### 📚 Required Skills")

for skill in required_skills:
    st.write("•", skill)

# Get student's current skills
# 👨‍💻 Automatically suggest skills from subject performance

student_skills = []

if math >= 70:
    student_skills.append("Mathematics")

if physics >= 70:
    student_skills.append("Physics")

if chemistry >= 70:
    student_skills.append("Chemistry")

if biology >= 70:
    student_skills.append("Biology")

# Problem solving suggested when Math + Physics are strong
if math >= 70 and physics >= 70:
    student_skills.append("Problem Solving")

# Programming suggested when Math performance is good
if math >= 70:
    student_skills.append("Programming")

student_skills = list(dict.fromkeys(student_skills))
st.write("### 👨‍💻 Current Skills")

if student_skills:
    for skill in student_skills:
        st.write("•", skill)
else:
    st.info("No skills added for this student yet.")

# Match skills
matched_skills = [
    skill for skill in required_skills
    if skill.lower() in [s.lower() for s in student_skills]
]

missing_skills = [
    skill for skill in required_skills
    if skill.lower() not in [s.lower() for s in student_skills]
]

st.write("### ✅ Matched Skills")

if matched_skills:
    for skill in matched_skills:
        st.success(f"✓ {skill}")
else:
    st.info("No required skills matched yet.")

st.write("### ❌ Missing Skills")

if missing_skills:
    for skill in missing_skills:
        st.warning(f"📌 {skill}")
else:
    st.success("🎉 No missing skills!")

# Skill match percentage
skill_match = (
    len(matched_skills) / len(required_skills)
) * 100

st.write("### 📈 Skill Match")

st.progress(int(skill_match))

st.metric(
    "Skill Match Percentage",
    f"{skill_match:.0f}%"
)
# 🎨 AI Assistant Color Design
st.markdown("""
<style>

/* AI chat area */
[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 12px 16px;
    margin-bottom: 10px;
    border: 1px solid rgba(120, 100, 255, 0.18);
}

/* User message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(135deg, #e8f1ff, #f3eaff);
}

/* AI message */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(135deg, #f5f3ff, #eaf9ff);
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 14px;
}

/* Chat input box */
[data-testid="stChatInput"] textarea {
    border-radius: 14px;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# 🤖 OLLAMA AI CAREER ASSISTANT
# ============================================================

st.divider()

st.header("🤖 AI Career Assistant")
st.caption(
    "Ask questions about student performance, skills and career guidance."
)

# ------------------------------------------------------------
# Chat memory
# ------------------------------------------------------------

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []


# ------------------------------------------------------------
# Student context for AI
# ------------------------------------------------------------

student_context = f"""
Student Name: {career_student}

Average Marks: {student_data['Average Marks']}
Average Attendance: {student_data['Average Attendance']}%
Performance Score: {student_data['Performance Score']}
Performance Category: {category}

Subject Performance:
Math: {math}
Physics: {physics}
Chemistry: {chemistry}
Biology: {biology}

Suggested Career Role: {suggested_role}

Required Skills:
{", ".join(required_skills)}

Current Skills:
{", ".join(student_skills) if student_skills else "No current skills"}

Matched Skills:
{", ".join(matched_skills) if matched_skills else "None"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "None"}

Skill Match Percentage:
{skill_match:.0f}%
"""


# ------------------------------------------------------------
# Display previous AI messages
# ------------------------------------------------------------

for message in st.session_state.ai_messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown("""
<style>

/* AI Chat / Search Box */
[data-testid="stChatInput"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    border: 2px solid #a78bfa;
    border-radius: 18px;
    padding: 5px;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
}

/* User typed text */
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: white !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    letter-spacing: 0.2px;
}

/* Placeholder text */
[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(255, 255, 255, 0.75) !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
    font-size: 15px !important;
}

/* Focus effect */
[data-testid="stChatInput"]:focus-within {
    border: 2px solid #c4b5fd;
    box-shadow: 0 0 16px rgba(124, 58, 237, 0.45);
}

</style>
""", unsafe_allow_html=True)
# ------------------------------------------------------------
# Chat input
# ------------------------------------------------------------

user_question = st.chat_input(
    "Ask AI about this student's career..."
)


# ------------------------------------------------------------
# Generate AI answer
# ------------------------------------------------------------

if user_question:

    # Display user question
    with st.chat_message("user"):
        st.markdown(user_question)

    # Save user message
    st.session_state.ai_messages.append({
        "role": "user",
        "content": user_question
    })

    # System instruction
    system_message = f"""
You are an AI Student Career Assistant and General Student Assistant.

You can answer BOTH:
1. General questions
2. Questions about the student's performance, subjects, skills and career

For general questions:
- Answer normally and helpfully.
- You do not need to use student data.
- Explain concepts clearly in simple language.

For student-related questions:
- Use the student information provided below.
- Do not invent marks, attendance, skills or achievements.
- Use the actual student data when relevant.
- Give practical and useful guidance.

For study and exam questions:
- Explain difficult topics in simple language.
- Give clear definitions, main points and examples.
- For 5-mark answers, give a medium-length structured answer.
- For 8-mark answers, give a detailed but easy answer with headings and points.
- Keep answers beginner-friendly and exam-oriented when the question is academic.

For career questions:
- Consider the student's subjects, marks, current skills, missing skills and suggested career role.
- Give realistic next steps and learning guidance.

For unrelated questions:
- Answer the question normally.
- Do not force the student's information into unrelated answers.

Student information:
{student_context}
"""
    # Combine system + conversation
    messages_for_ai = [
        {
            "role": "system",
            "content": system_message
        }
    ]

    messages_for_ai.extend(
        st.session_state.ai_messages
    )

    # AI response
    with st.chat_message("assistant"):

        response_placeholder = st.empty()
        full_response = ""

        try:

            response = ollama.chat(
                model="llama3.2:latest",
                messages=messages_for_ai,
                stream=True
            )

            for chunk in response:

                text = chunk["message"]["content"]

                full_response += text

                response_placeholder.markdown(
                    full_response + "▌"
                )

            response_placeholder.markdown(
                full_response
            )

            # Save AI response
            st.session_state.ai_messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:

            error_message = f"""
### ❌ AI connection error

Please check that Ollama is running.

Try this command in PowerShell:

`ollama list`

If `qwen3:8b` is not installed, run:

`ollama pull qwen3:8b`

Technical error:

`{e}`
"""

            response_placeholder.error(
                error_message
            )
