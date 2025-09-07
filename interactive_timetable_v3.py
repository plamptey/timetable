#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys

# Load timetable
timetable = pd.read_excel("C:/Users/HP/Documents/AAMUSTED/2025/timetable/input_data/exam_timetable_split.xlsx")

def run_jupyter_mode():
    """Preview timetable in Jupyter with filters applied manually."""
    from IPython.display import display

    print("⚠️ Running in Jupyter preview mode (not Streamlit).")

    faculties = ["All"] + sorted(timetable["FACULTY"].dropna().unique().tolist())
    departments = ["All"] + sorted(timetable["DEPARTMENT"].dropna().unique().tolist())
    levels = ["All"] + sorted(timetable["CLASS"].dropna().unique().tolist())
    days = ["All"] + sorted(timetable["DAY & DATE"].dropna().unique().tolist())

    # simple manual filter values (can edit here in Jupyter)
    faculty_filter = "All"
    dept_filter = "All"
    level_filter = "All"
    day_filter = "All"

    filtered = timetable.copy()
    if faculty_filter != "All":
        filtered = filtered[filtered["FACULTY"] == faculty_filter]
    if dept_filter != "All":
        filtered = filtered[filtered["DEPARTMENT"] == dept_filter]
    if level_filter != "All":
        filtered = filtered[filtered["CLASS"] == level_filter]
    if day_filter != "All":
        filtered = filtered[filtered["DAY & DATE"] == day_filter]

    styled = filtered.style.set_table_styles(
        [{
            'selector': 'thead th',
            'props': [('background-color', '#4CAF50'),
                      ('color', 'white'),
                      ('font-weight', 'bold'),
                      ('text-align', 'center')]
        }]
    )
    display(styled)


def run_streamlit_mode():
    """Run full interactive app with Streamlit."""
    import streamlit as st
    from io import BytesIO

    st.set_page_config(page_title="University Exam Timetable", layout="wide")
    st.title("📘 University Semester Examination Timetable")

    # Sidebar filters
    st.sidebar.header("🔎 Filter Timetable")
    faculties = ["All"] + sorted(timetable["FACULTY"].dropna().unique().tolist())
    departments = ["All"] + sorted(timetable["DEPARTMENT"].dropna().unique().tolist())
    levels = ["All"] + sorted(timetable["CLASS"].dropna().unique().tolist())
    days = ["All"] + sorted(timetable["DAY & DATE"].dropna().unique().tolist())

    faculty_filter = st.sidebar.selectbox("Select Faculty", faculties)
    dept_filter = st.sidebar.selectbox("Select Department", departments)
    level_filter = st.sidebar.selectbox("Select Level", levels)
    day_filter = st.sidebar.selectbox("Select Day", days)

    filtered = timetable.copy()
    if faculty_filter != "All":
        filtered = filtered[filtered["FACULTY"] == faculty_filter]
    if dept_filter != "All":
        filtered = filtered[filtered["DEPARTMENT"] == dept_filter]
    if level_filter != "All":
        filtered = filtered[filtered["CLASS"] == level_filter]
    if day_filter != "All":
        filtered = filtered[filtered["DAY & DATE"] == day_filter]

    st.subheader("📅 Filtered Timetable")
    st.dataframe(filtered)

    # Export to Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        filtered.to_excel(writer, index=False, sheet_name="Timetable")
    output.seek(0)

    st.download_button(
        label="⬇️ Download Filtered Timetable as Excel",
        data=output,
        file_name="filtered_timetable.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --- Auto-detect environment ---
if "streamlit" in sys.modules:
    run_streamlit_mode()
else:
    run_jupyter_mode()


# In[ ]:




