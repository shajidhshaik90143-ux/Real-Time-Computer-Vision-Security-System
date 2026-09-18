import streamlit as st

from config.settings import (
    CAMERA_INDEX,
    YOLO_MODEL,
    CONFIDENCE_THRESHOLD,
    DATABASE_PATH,
    EVIDENCE_DIR,
    KNOWN_FACES_DIR,
    LOG_DIR
)

from database.database import SecurityDatabase

from dashboard.live_monitor import (
    run_live_monitor
)

from dashboard.events import (
    show_events
)

from dashboard.analytics import (
    show_analytics
)

from utils.logger import (
    create_logger
)


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Real-Time CV Security",
    page_icon="👁️",
    layout="wide"
)


# -------------------------------
# INITIALIZATION
# -------------------------------

@st.cache_resource
def get_database():

    return SecurityDatabase(
        DATABASE_PATH
    )


@st.cache_resource
def get_logger():

    return create_logger(
        LOG_DIR
    )


database = get_database()
logger = get_logger()


# -------------------------------
# HEADER
# -------------------------------

st.title(
    "👁️ Real-Time Computer Vision Security System"
)

st.caption(
    "AI-powered real-time camera monitoring and security event detection"
)


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title(
    "⚙️ Control Panel"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📹 Live Monitoring",
        "📋 Event History",
        "📊 Analytics",
        "👥 Registered Faces",
        "ℹ️ About"
    ]
)


# -------------------------------
# DASHBOARD
# -------------------------------

if page == "🏠 Dashboard":

    st.subheader(
        "🏠 Security Dashboard"
    )

    events = database.get_events(1000)

    total_events = len(events)

    motion_events = sum(
        1 for event in events
        if event[1] == "Motion Detected"
    )

    person_events = sum(
        1 for event in events
        if event[1] == "Person Detected"
    )

    unknown_events = sum(
        1 for event in events
        if event[1] == "Unknown Face"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📋 Total Events",
        total_events
    )

    col2.metric(
        "🏃 Person Events",
        person_events
    )

    col3.metric(
        "🚶 Motion Events",
        motion_events
    )

    col4.metric(
        "⚠️ Unknown Faces",
        unknown_events
    )

    st.divider()

    st.markdown(
        """
        ### 🔐 System Status

        | Component | Status |
        |---|---|
        | Camera System | 🟢 Ready |
        | YOLO Detection | 🟢 Ready |
        | Face Detection | 🟢 Ready |
        | SQLite Database | 🟢 Ready |
        | Evidence Storage | 🟢 Ready |
        """
    )

    st.info(
        "Go to **📹 Live Monitoring** to start the camera."
    )


# -------------------------------
# LIVE MONITORING
# -------------------------------

elif page == "📹 Live Monitoring":

    st.header(
        "📹 Live Security Monitoring"
    )

    camera_index = st.sidebar.number_input(
        "Camera Index",
        min_value=0,
        max_value=10,
        value=CAMERA_INDEX,
        step=1
    )

    confidence = st.sidebar.slider(
        "YOLO Confidence",
        min_value=0.10,
        max_value=0.95,
        value=CONFIDENCE_THRESHOLD,
        step=0.05
    )

    st.warning(
        "Press Start Monitoring to activate the camera."
    )

    start = st.button(
        "▶️ Start Monitoring",
        type="primary"
    )

    if start:

        logger.info(
            "Live monitoring started."
        )

        run_live_monitor(
            camera_index=int(camera_index),
            model_name=YOLO_MODEL,
            confidence=confidence,
            database=database,
            evidence_dir=EVIDENCE_DIR,
            known_faces_dir=KNOWN_FACES_DIR
        )


# -------------------------------
# EVENT HISTORY
# -------------------------------

elif page == "📋 Event History":

    show_events(
        database
    )


# -------------------------------
# ANALYTICS
# -------------------------------

elif page == "📊 Analytics":

    show_analytics(
        database
    )


# -------------------------------
# REGISTERED FACES
# -------------------------------

elif page == "👥 Registered Faces":

    st.header(
        "👥 Registered Faces"
    )

    st.write(
        "Place JPG or PNG face images inside:"
    )

    st.code(
        str(KNOWN_FACES_DIR)
    )

    st.markdown(
        """
        ### Example

        ```text
        known_faces/
        │
        ├── shajidh.jpg
        ├── admin.jpg
        └── student1.jpg
        ```

        The filename becomes the person's name.
        """

    )

    image_files = list(
        KNOWN_FACES_DIR.glob("*.jpg")
    ) + list(
        KNOWN_FACES_DIR.glob("*.png")
    ) + list(
        KNOWN_FACES_DIR.glob("*.jpeg")
    )

    if image_files:

        for image in image_files:

            st.image(
                str(image),
                caption=image.stem,
                width=180
            )

    else:

        st.info(
            "No registered face images found."
        )


# -------------------------------
# ABOUT
# -------------------------------

elif page == "ℹ️ About":

    st.header(
        "ℹ️ About the Project"
    )

    st.markdown(
        """
        ## 👁️ Real-Time Computer Vision Security System

        This application combines computer vision and AI
        techniques to monitor a live camera feed.

        ### Technologies

        - Python
        - OpenCV
        - YOLO
        - Streamlit
        - SQLite
        - NumPy
        - Plotly

        ### Detection

        - Person detection
        - Motion detection
        - Face detection
        - Basic registered-face matching
        - Security event logging
        - Evidence image capture

        ### Important

        This project is intended as an educational/prototype
        security-monitoring system. It should not be treated as
        a substitute for professionally validated surveillance,
        biometric identification, or emergency-security systems.
        """
    )