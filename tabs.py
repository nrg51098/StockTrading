import streamlit as st

# Create three tabs
tab1, tab2, tab3 = st.tabs(["Dashboard", "Data View", "Settings"])

# Add content to each tab
with tab1:
    st.header("Sales Dashboard")
    st.write("Displaying key performance indicators and charts.")
    # You can add charts, metrics, etc. here

with tab2:
    st.header("Raw Data Table")
    st.write("Presenting the underlying data in a tabular format.")
    # You can add a dataframe here
    import pandas as pd
    data = {'Product': ['A', 'B', 'C'], 'Sales': [100, 150, 200]}
    df = pd.DataFrame(data)
    st.dataframe(df)

with tab3:
    st.header("Application Settings")
    st.write("Configure various parameters for the application.")
    st.checkbox("Enable dark mode")
    st.slider("Adjust refresh rate", 1, 10, 5)