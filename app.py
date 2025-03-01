import time
import board
import adafruit_dht
import streamlit as st

# Streamlit app title
st.title("Realtime Env Monitoring")

# Custom CSS for visible semi-circular gauge
st.markdown(
    """
    <style>
    .gauge-container {
        text-align: center;
        margin: 20px;
        position: relative;
    }
    .gauge {
        width: 200px;
        height: 100px;
        position: relative;
        overflow: hidden;
        margin: 0 auto;
    }
    .gauge-background {
        width: 200px;
        height: 200px;
        border: 8px solid #00F3FF;  /* Neon blue border */
        border-radius: 50%;
        position: absolute;
        top: 0;
        left: 0;
        box-sizing: border-box;
        clip-path: polygon(0 0, 100% 0, 100% 50%, 0 50%);
    }
    .needle {
        width: 2px;
        height: 80px;
        background: #FF1A1A;  /* Bright red needle */
        position: absolute;
        bottom: 10px;
        left: 50%;
        transform-origin: 50% 100%;
        transform: rotate(-90deg);
        transition: transform 0.5s ease-in-out;
        z-index: 2;
    }
    .gauge-value {
        font-size: 24px;
        font-weight: bold;
        color: #00F3FF;
        margin-top: 15px;
    }
    .gauge-title {
        font-size: 18px;
        font-weight: bold;
        color: #00F3FF;
        margin-top: 5px;
    }
    .dashboard {
        display: flex;
        justify-content: space-around;
        background: #000000;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create two columns for gauges
col1, col2 = st.columns(2)
temp_ph = col1.empty()
hum_ph = col2.empty()

# Initialize sensor
try:
    sensor = adafruit_dht.DHT22(board.D4)
except Exception:
    st.stop()

# Main loop
while True:
    try:
        # Read sensor data
        retries = 5
        temp, hum = None, None
        for _ in range(retries):
            try:
                temp = sensor.temperature
                hum = sensor.humidity
                if temp is not None and hum is not None: break
            except RuntimeError:
                time.sleep(1)
        
        if temp is None or hum is None:
            time.sleep(2)
            continue

        # Calculate angles (-90° to 90°)
        temp_angle = (temp / 50) * 180 - 90  # 0-50°C range
        hum_angle = (hum / 100) * 180 - 90   # 0-100% range

        # Update displays
        temp_ph.markdown(
            f"""
            <div class="dashboard">
                <div class="gauge-container">
                    <div class="gauge">
                        <div class="gauge-background"></div>
                        <div class="needle" style="transform: rotate({temp_angle}deg);"></div>
                    </div>
                    <div class="gauge-value">{temp:.1f} °C</div>
                    <div class="gauge-title">TEMPERATURE</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        hum_ph.markdown(
            f"""
            <div class="dashboard">
                <div class="gauge-container">
                    <div class="gauge">
                        <div class="gauge-background"></div>
                        <div class="needle" style="transform: rotate({hum_angle}deg);"></div>
                    </div>
                    <div class="gauge-value">{hum:.1f} %</div>
                    <div class="gauge-title">HUMIDITY</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        time.sleep(3)

    except Exception:
        time.sleep(2)