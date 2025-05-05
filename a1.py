import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load the processed data
df = pd.read_csv("C:\\Users\\AISHWARYA\\Desktop\\processed_data.csv") 

# CSS
st.markdown("""
    <style>
        /* ... (Your existing CSS) ... */
    </style>
""", unsafe_allow_html=True)

# Sidebar for Filters 
with st.sidebar:
    st.title("Project Filters")
    with st.expander("Filter by Status and Manager"):
        all_options = ["Status: " + s for s in df['Status'].unique()] + ["Manager: " + m for m in df['Project Manager'].unique()]
        combined_filter = st.multiselect("Select Status or Manager", all_options)

    with st.expander("Choose Specific Project Managers"): 
        manager_filter = st.multiselect("Select Project Manager", df['Project Manager'].unique())

# Apply Filters
filtered_data = df.copy()
status_filter = []
manager_filter_combined = []

if combined_filter:
    for item in combined_filter:
        if item.startswith("Status: "):
            status_filter.append(item[len("Status: "):])
        elif item.startswith("Manager: "):
            manager_filter_combined.append(item[len("Manager: "):])

if status_filter:
    filtered_data = filtered_data[filtered_data['Status'].isin(status_filter)]

if manager_filter_combined:
    filtered_data = filtered_data[filtered_data['Project Manager'].isin(manager_filter_combined)]

if manager_filter: # Separate manager filter
    filtered_data = filtered_data[filtered_data['Project Manager'].isin(manager_filter)]

#  KPIs 
st.subheader("Key Metrics")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown(f'<div style="background-color: #fff; border-radius: 8px; padding: 1.2rem; box-shadow: 0 0.1rem 0.2rem rgba(0, 0, 0, 0.08); display: flex; flex-direction: column; align-items: center; justify-content: center; border-left: 5px solid #007bff;"><div style="color: #777; font-size: 0.9em; margin-bottom: 0.3rem;">Total Projects</div><div style="color: #333; font-size: 1.6em; font-weight: bold;">{len(filtered_data)}</div></div>', unsafe_allow_html=True)
with kpi2:
    avg_roi = f"{filtered_data['ROI'].mean():.2%}" if not filtered_data.empty else "N/A"
    st.markdown(f'<div style="background-color: #fff; border-radius: 8px; padding: 1.2rem; box-shadow: 0 0.1rem 0.2rem rgba(0, 0, 0, 0.08); display: flex; flex-direction: column; align-items: center; justify-content: center; border-left: 5px solid #007bff;"><div style="color: #777; font-size: 0.9em; margin-bottom: 0.3rem;">Average ROI</div><div style="color: #333; font-size: 1.6em; font-weight: bold;">{avg_roi}</div></div>', unsafe_allow_html=True)
with kpi3:
    avg_completion = f"{filtered_data['Completion%'].mean():.2f}%" if not filtered_data.empty else "N/A"
    st.markdown(f'<div style="background-color: #fff; border-radius: 8px; padding: 1.2rem; box-shadow: 0 0.1rem 0.2rem rgba(0, 0, 0, 0.08); display: flex; flex-direction: column; align-items: center; justify-content: center; border-left: 5px solid #007bff;"><div style="color: #777; font-size: 0.9em; margin-bottom: 0.3rem;">Average Completion %</div><div style="color: #333; font-size: 1.6em; font-weight: bold;">{avg_completion}</div></div>', unsafe_allow_html=True)

# Tabbed Sections for Visualizations
tab1, tab2, tab3 = st.tabs(["Overview", "Performance", "Status & Details"])

with tab1:
    st.markdown('<div class="tab-card"><div class="tab-card-title">Project Timelines (Gantt Chart)</div>', unsafe_allow_html=True)
    fig_gantt = px.timeline(filtered_data, x_start="Start Date", x_end="End Date", y="Project Name", color="Status", title="", hover_data=["Project Manager", "Duration (days)", "Completion%"])
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Project Analysis")

    st.markdown('<div class="tab-card"><div class="tab-card-title">Project Cost vs Benefit Over Time</div>', unsafe_allow_html=True)
    fig_cost_benefit = px.line(
        filtered_data,
        x='Start Date',
        y=['Project Cost', 'Project Benefit'],
        title=''
    )
    st.plotly_chart(fig_cost_benefit, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tab-card"><div class="tab-card-title">Average Completion % by Complexity and Status</div>', unsafe_allow_html=True)
    heatmap_data = filtered_data.pivot_table(
        index='Complexity',
        columns='Status',
        values='Completion%',
        aggfunc='mean'
    )
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(8, 5))
    sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt=".2f", ax=ax_heatmap)
    plt.title('')
    plt.ylabel('Complexity')
    plt.xlabel('Status')
    st.pyplot(fig_heatmap)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Project Status & Details")

    st.markdown('<div class="tab-card"><div class="tab-card-title">Number of Projects by Status</div>', unsafe_allow_html=True)
    fig_status, ax_status = plt.subplots(figsize=(8, 5))
    sns.countplot(data=filtered_data, x='Status', palette='viridis', ax=ax_status)
    plt.title('')
    plt.xlabel('Project Status')
    plt.ylabel('Number of Projects')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig_status)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tab-card"><div class="tab-card-title">Filtered Project Data</div>', unsafe_allow_html=True)
    st.dataframe(filtered_data) # Displaying the filtered data as a DataFrame
    st.markdown('</div>', unsafe_allow_html=True)


#Footer 
st.markdown("""
    <hr style="margin-top: 2em; border-top: 1px solid #e0e0e0;"/>
    <div style="text-align: center; font-size: 0.9em; color: #777; padding-top: 1rem;">
        © 2025 Project Dashboard by Aishwarya. All rights reserved.
    </div>
""", unsafe_allow_html=True)