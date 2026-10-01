import pandas as pd
import sqlite3

# CSV file read karna
data = pd.read_csv("data/students.csv")

# Data screen par dikhana
print(data)
print("\nTotal Students:", data["Name"].nunique())
print("\nAverage Marks:", data["Marks"].mean())
print("\nAverage Attendance:", data["Attendance"].mean())
student_average = data.groupby("Name")["Marks"].mean()

print("\nStudent-wise Average Marks:")
print(student_average)
subject_average = data.groupby("Subject")["Marks"].mean()

print("\nSubject-wise Average Marks:")
print(subject_average)

import matplotlib.pyplot as plt

student_average.plot(kind="bar")

plt.title("Student-wise Average Marks")
plt.xlabel("Student")
student_attendance = data.groupby("Name")["Attendance"].mean()

print("\nStudent-wise Average Attendance:")
print(student_attendance)
performance = (
    student_average * 0.7
    + student_attendance * 0.3
)

print("\nStudent Performance Score:")
print(performance.round(2))
performance.plot(kind="bar")

plt.title("Student Performance Score")
plt.xlabel("Student")
plt.ylabel("Performance Score")
plt.tight_layout()
plt.show()
def performance_category(score):
    if score >= 85:
        return "Excellent"
    elif score >= 75:
        return "Good"
    else:
        return "Needs Improvement"

category = performance.apply(performance_category)

print("\nPerformance Category:")
print(category)
report = pd.DataFrame({
    "Average Marks": student_average.round(2),
    "Average Attendance": student_attendance.round(2),
    "Performance Score": performance.round(2),
    "Category": category
})

print("\nStudent Performance Report:")
print(report)
report.to_csv("data/student_performance_report.csv")

print("\nReport successfully saved!")
connection = sqlite3.connect("data/students.db")

data.to_sql("students", connection, if_exists="replace", index=False)

print("Student data added to database!")
cursor = connection.cursor()

cursor.execute("""
SELECT * FROM students
""")

rows = cursor.fetchall()

print("\nData from SQL Database:")
for row in rows:
    print(row)


cursor.execute("""
SELECT Name, AVG(Marks)
FROM students
GROUP BY Name
""")

average_rows = cursor.fetchall()

print("\nAverage Marks from SQL:")
for row in average_rows:
    print(row)


cursor.execute("""
SELECT Subject, AVG(Marks)
FROM students
GROUP BY Subject
""")

subject_rows = cursor.fetchall()

print("\nSubject-wise Average Marks from SQL:")
for row in subject_rows:
    print(row)



cursor.execute("""
SELECT Name, AVG(Attendance)
FROM students
GROUP BY Name
""")

attendance_rows = cursor.fetchall()

print("\nAverage Attendance from SQL:")
for row in attendance_rows:
    print(row)
    cursor.execute("""
SELECT Name,
       AVG(Marks) AS Average_Marks,
       AVG(Attendance) AS Average_Attendance,
       (AVG(Marks) * 0.7 + AVG(Attendance) * 0.3) AS Performance_Score
FROM students
GROUP BY Name
""")

performance_rows = cursor.fetchall()

print("\nStudent Performance from SQL:")
for row in performance_rows:
    print(row)
    cursor.execute("""
SELECT Name,
       AVG(Marks) AS Average_Marks,
       AVG(Attendance) AS Average_Attendance,
       (AVG(Marks) * 0.7 + AVG(Attendance) * 0.3) AS Performance_Score,
       CASE
           WHEN (AVG(Marks) * 0.7 + AVG(Attendance) * 0.3) >= 85
               THEN 'Excellent'
           WHEN (AVG(Marks) * 0.7 + AVG(Attendance) * 0.3) >= 75
               THEN 'Good'
           ELSE 'Needs Improvement'
       END AS Category
FROM students
GROUP BY Name
""")

category_rows = cursor.fetchall()

print("\nStudent Performance Category from SQL:")
for row in category_rows:
    print(row)
    sql_report = pd.DataFrame(
    category_rows,
    columns=[
        "Name",
        "Average Marks",
        "Average Attendance",
        "Performance Score",
        "Category"
    ]
)

print("\nFinal SQL Analytics Report:")
print(sql_report)
connection.close()
    # Performance Score Chart

sql_report.plot(
    x="Name",
    y="Performance Score",
    kind="bar",
    legend=False
)

plt.title("Student Performance Score")
plt.xlabel("Student")
plt.ylabel("Performance Score")
plt.tight_layout()
plt.show()
# Attendance Chart

student_attendance.plot(
    kind="bar",
    legend=False
)

plt.title("Student-wise Average Attendance")
plt.xlabel("Student")
plt.ylabel("Attendance (%)")
plt.tight_layout()
plt.show()
# Subject Performance Chart

subject_average.plot(
    kind="bar",
    legend=False
)

plt.title("Subject-wise Average Marks")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.tight_layout()
plt.show()
import streamlit as st

st.title("🎓 AI Student Performance & Career Analytics")
st.write("Student analytics dashboard")