import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import warnings
import time
warnings.filterwarnings("ignore")
import firebase_admin
from firebase_admin import db,credentials
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred,{"databaseURL":"https://netman-559dc-default-rtdb.firebaseio.com/Device"})
def main():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            width: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    selected_option = st.sidebar.radio("",["Network Statistics", "Device Statistics"])
    st.title(" :bar_chart: "+selected_option)

    network_stats()
def network_stats():
    st.markdown("---")
    st.header("Traffic Usage")
    ref = db.reference('/41_70_47_67/Traffic_Out/FastEthernet0_0')

    num_points = 3600
    start_time = pd.Timestamp("2023-06-29 00:00:00")
    time_index = pd.date_range(start=start_time, periods=num_points, freq="T")
    traffic_data = np.zeros(num_points)  # Initialize an array to store traffic data

    # Create the DataFrame
    data = pd.DataFrame({"time": time_index, "traffic": traffic_data})

    # Create initial plot
    fig = go.Figure(data=go.Scatter(x=data["time"], y=data["traffic"], mode='lines'))
    fig.update_layout(
        title="Up Link Traffic",
        xaxis_title="Time",
        yaxis_title="Traffic"
    )

    # Display the initial plot using Plotly
    chart = st.plotly_chart(fig)

    old_value = None
    # Update the graph every second
    for i in range(num_points):
        # Retrieve traffic data from Firebase
        value = ref.get()

        if value is not None:
            if old_value is not None:
                traffic_value = (value - old_value)/ 1024
            else:
                traffic_value = 0
            old_value = value
        else:
            traffic_value = 0

        # Update the traffic data in the DataFrame
        traffic_data[i] = traffic_value

        # Update the y-values of the plot
        fig.data[0].y = traffic_data[:i + 1]

        # Update the chart in Streamlit
        chart.plotly_chart(fig, use_container_width=True)

        # Wait for 1 second before updating again
        time.sleep(1)
if __name__ == "__main__":
    main()
