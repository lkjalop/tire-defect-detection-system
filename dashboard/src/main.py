#!/usr/bin/env python3
"""
Laptop Dashboard
===============
"""

import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(
    page_title="Tire Defect Detection - Laptop",
    page_icon="🛞",
    layout="wide"
)

st.title("🛞 Tire Defect Detection - Laptop Edition")
st.markdown("---")

# API connection
api_url = "http://backend:8000"

# Health check
try:
    response = requests.get(f"{api_url}/health", timeout=5)
    if response.status_code == 200:
        st.success("✅ Backend API Connected")
        health_data = response.json()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Status", "Healthy")
        
        with col2:
            st.metric("Device", "Laptop")
        
        with col3:
            st.metric("Uptime", "Running")
        
        # Analytics
        try:
            analytics_response = requests.get(f"{api_url}/api/v1/analytics/summary", timeout=5)
            if analytics_response.status_code == 200:
                data = analytics_response.json()["summary"]
                
                st.markdown("### 📊 Demo Analytics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Processed", data["total_processed"])
                
                with col2:
                    st.metric("Defects", data["defects_found"])
                
                with col3:
                    st.metric("Response Time", f"{data['avg_inference_time_ms']:.0f}ms")
                
                with col4:
                    st.metric("Devices", data["active_devices"])
        
        except:
            st.warning("Analytics temporarily unavailable")
    
except:
    st.error("❌ Cannot connect to backend API")
    st.info("Make sure the backend service is running")

# Auto refresh
if st.checkbox("Auto Refresh (10s)"):
    time.sleep(10)
    st.experimental_rerun()

st.markdown("---")
st.info("🎪 **Laptop Demo Mode**: This is a simplified version optimized for local development")
