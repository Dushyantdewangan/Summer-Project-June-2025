import streamlit as st
from skyfield.api import EarthSatellite, load
from datetime import datetime
import pandas as pd
import time

# TLE data for ISS (update regularly for accuracy)
line1 = '1 25544U 98067A   25204.16864096  .00010724  00000+0  19544-3 0  9992'
line2 = '2 25544  51.6344 128.7280 0002115 106.2807 253.8414 15.50025731520740'
satellite = EarthSatellite(line1, line2, 'ISS (ZARYA)')
ts = load.timescale()

st.set_page_config(layout="wide", page_title="Live ISS Tracker")

st.sidebar.title("Refresh rate (seconds)")
refresh_rate = st.sidebar.slider("", min_value=5, max_value=60, value=10, step=1)

st.title("Live ISS Tracker")

placeholder = st.empty()

while True:
    now = ts.now()
    subpoint = satellite.at(now).subpoint()
    lat = subpoint.latitude.degrees
    lon = subpoint.longitude.degrees
    alt = subpoint.elevation.km

    with placeholder.container():
        st.markdown(f"**Local Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Latitude:** <span style='color:#00FFAA'>{lat:.2f}°</span>", unsafe_allow_html=True)
        st.markdown(f"**Longitude:** <span style='color:#00FFAA'>{lon:.2f}°</span>", unsafe_allow_html=True)
        st.markdown(f"**Altitude:** <span style='color:#00FFAA'>{alt:.2f} km</span>", unsafe_allow_html=True)
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

    time.sleep(refresh_rate)