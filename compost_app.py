import streamlit as st
import pandas as pd
import os
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ---------- Style Section (CSS + backgrounds) ----------
st.set_page_config(page_title="Community Composting Network", layout="centered", page_icon="🌱")

st.markdown("""
    <style>
    /* Background image & color overlay */
    body {
        background: linear-gradient(135deg,#F0FFF0 60%,#E3F1DF 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg,#eaf8df 0%,#c6eca9 100%);
    }
    /* Widget styles */
    .stButton>button, .stForm>form>button {
        background: linear-gradient(90deg,#A5D6A7,#FFD54F);
        color:#212121;
        border-radius:12px;
        padding:0.75em 2em;
        font-size:1.1em;
        border:0;
        margin-top: 0.3em;
        font-weight:bold;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background:linear-gradient(90deg,#81c784,#ffe082);
        color:#1b5e20;
    }
    h1, h2, h3 { 
    color:#207720!important; font-family: 'Segoe UI', sans-serif;}
    .metric { font-size:1.1em; color:#207720;}
    /* Custom card backgrounds */
    .css-1v0mbdj, .css-1offfwp, .stDataFrame { 
        background: #fffde7!important; 
        border-radius:18px!important;
        border: 1px solid #f0efeb;
    }
    /* Extra spacing */
    .block-container { padding-top: 0.5rem;}
    .leaflet-control-attribution,
        .leaflet-control-container .leaflet-control {
            display: none !important;
    </style>
    """, unsafe_allow_html=True
)

# ---------- CSV Setup ----------
DATA_FILE = "compost_data.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Name", "Weight_lb", "Method", "Location", "Date"])
    df.to_csv(DATA_FILE, index=False)
df = pd.read_csv(DATA_FILE)

# ---------- Sidebar Navigation ----------
#st.sidebar.image("https://static.vecteezy.com/system/resources/thumbnails/008/418/190/small/green-composting-icon-vector.jpg", width=80)
pages = [
    "Home",
    "Add Compost",
    "Dashboard",
    "Leaderboard",
    "Community Map",
    "Garbage Input",
    "About"
]

# Initialize current page in session state
if "page" not in st.session_state:
    st.session_state["page"] = pages[0]

st.sidebar.markdown("## 🌿 Navigation")
for p in pages:
    if st.sidebar.button(p):
        st.session_state["page"] = p

# Current page variable
page = st.session_state["page"]


# ---------- Home Page ----------
if page == "Home":
    st.markdown(
        """
        <div style="background: linear-gradient(115deg,#a5d6a7 50%,#fffde7 100%);border-radius:28px;padding:2.4em 2.2em 2.8em;">
            <h1 style="text-align:center;font-size:3em;text-shadow:1px 1px #c6eca9;">
                🌱 Community Composting Network
            </h1>
            <h2 style="text-align:center;color:#FFD54F;font-weight:900;text-shadow:1px 1px #fff;">Turn Waste Into Growth!</h2>
            <p style="text-align:center;font-size:1.35em;">
                <span style="color:#338a31;font-weight:bold;">
                    Track, share, and grow your local composting impact with every household and neighbor!
                </span>
            </p>
            <div style="display:flex;justify-content:center;gap:32px;margin:22px 0 16px 0;">
                <img src="https://cdn-icons-png.flaticon.com/512/2972/2972885.png" width="70">
                <img src="https://cdn-icons-png.flaticon.com/512/3944/3944343.png" width="70">
                <img src="https://cdn-icons-png.flaticon.com/512/3172/3172641.png" width="70">
            </div>
            <p style="background:#b4f2b5;padding:0.7em 1.5em;border-radius:12px;text-align:center;margin:auto;width:90%">
                <b>Join a movement where every banana peel, coffee ground, and lawn clippings make a difference.
                <br>Together, we grow green communities!</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2, c3 = st.columns([1.5,1,1.5])
   # with c2:
    #    st.button("Get Started! 🚀")
    st.markdown("---")
    st.info("Tip: Use the navigation menu (left) to add compost, record garbage, or view your community's progress.", icon="🌍")

# ---------- Add Compost Page ----------
elif page == "Add Compost":
    st.write("")
    st.header("Add Compost Contribution")
    with st.form("compost_form", clear_on_submit=True):
        name = st.text_input("Name")
        weight = st.number_input("Weight (lb)", min_value=0.1, step=0.1)
        method = st.selectbox("Method", ["Drop-off", "Pickup"])
        location = st.text_input("Location (city/community)")
        submitted = st.form_submit_button("Add Entry")
    if submitted:
        new_entry = pd.DataFrame(
            [[name.strip(), weight, method, location.strip(), datetime.now().strftime("%Y-%m-%d")]],
            columns=["Name", "Weight_lb", "Method", "Location", "Date"],
        )
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Compost entry added! Thank you for making the planet greener.")

# ---------- Dashboard ----------
elif page == "Dashboard":
    st.write("")
    st.header("Composting Dashboard")
    total_lb = df["Weight_lb"].sum()
    unique_users = df["Name"].nunique()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Compost (lb)", round(total_lb, 1))
    col2.metric("Participants", unique_users)
    col3.metric("Drop-off:Pickup", f"{(df['Method']=='Drop-off').sum()}:{(df['Method']=='Pickup').sum()}")
    st.subheader("Recent Contributions")
    st.dataframe(df.tail(7).reset_index(drop=True))

# ---------- Leaderboard ----------
elif page == "Leaderboard":
    st.write("")
    st.header("Top Composters 🌾")
    leaderboard = df.groupby("Name")["Weight_lb"].sum().sort_values(ascending=False)
    st.bar_chart(leaderboard)
    st.success("🏆 Celebrate your composting champions and encourage your friends & neighbors to rise in the ranks!")

# ---------- Map -----------

elif page == "Community Map":
    st.write("")
    st.markdown("""
        <style>
            .leaflet-control-attribution,
            .leaflet-control-container .leaflet-control {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)
    st.header("Community Composting Map")

    m = folium.Map(location=[30.2672, -97.7431], zoom_start=11, tiles="OpenStreetMap",attr='' )
    # Provide a slightly random location for the demo, no geolocation
    # add markers ...
    for tile_layer in m._children:
        try:
            m._children[tile_layer].options['attribution'] = ''
        except Exception:
            pass
    m.save('map.html')
    for _, row in df.iterrows():
        folium.Marker(
            [30.26 + (hash(row["Name"]) % 10) * 0.01,
             -97.74 + (hash(row["Location"]) % 10) * 0.01],
            popup=f"{row['Name']}: {row['Weight_lb']}lb"
        ).add_to(m)

    st_folium(m, width=700, height=400)

# ---------- Garbage Input (Homeowners) ----------
elif page == "Garbage Input":
    st.write("")
    st.header("Homeowner Garbage Contribution")
    with st.form("garbage_form", clear_on_submit=True):
        homeowner = st.text_input("Homeowner Name")
        garbage_lb = st.number_input("Garbage Amount (lb)", min_value=0.1, step=0.1)
        location = st.text_input("Location (address or community)")
        compostable = st.radio("Is this garbage compostable?", ["Yes", "No"])
        give = st.form_submit_button("Give Garbage")
    if give:
        entry_type = "Compost-Garbage" if compostable == "Yes" else "Non-Compost Garbage"
        new_entry = pd.DataFrame(
            [[homeowner.strip(), garbage_lb, entry_type, location.strip(), datetime.now().strftime("%Y-%m-%d")]],
            columns=["Name", "Weight_lb", "Method", "Location", "Date"],
        )
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"{'♻️ Compostable garbage recorded!' if compostable == 'Yes' else '🗑️ Non-compost garbage recorded!'} Thanks for participating.")

    st.info(
        "Help sort and record your household's waste. "
        "Only compostable waste adds to community compost! "
        "Try entering both types for educational impact.",
        icon="🌱"
    )

# ---------- About Page (with more detail and color) -----------
elif page == "About":
    st.markdown(
        """
        <div style="background: linear-gradient(90deg,#fffde7 50%, #e0f2f1 100%);border-radius:22px;padding:2em 2em 2.6em;margin-bottom:2em;">
            <h1 style="color:#338a31;font-size:2.2em;">About Community Composting Network</h1>
            <h3 style="color:#ffb300;font-size:1.1em;margin-top:0em;">🌍 Greener Together: Our Vision</h3>
            <p style="font-size:1.15em;">
                <b>Community Composting Network</b> started with the belief that small, local compost efforts can create huge, positive change for the planet. <br>
                We empower homeowners, students, neighborhood gardens, and eco-leaders to collaborate for <span style="color:#2e7d32;">a cleaner, more fertile world</span>.
            </p>
            <hr>
            <h3 style="color:#388e3c;">Our Mission</h3>
            <ul style="font-size:1.05em;">
                <li>🌱 Make composting easy and accessible for everyone</li>
                <li>🏡 Give every household a role in reducing landfill waste</li>
                <li>🤝 Connect people to local gardens, drop-off centers, and each other</li>
                <li>✨ Grow environmental leadership and sustainable habits</li>
            </ul>
            <blockquote style="background:#b2dfdb;color:#205943;padding:0.9em 2em;margin:1em 0;border-left:6px solid #00abb5;">
                <em>"The greatest threat to our planet is the belief that someone else will save it."</em> — Robert Swan
            </blockquote>
            <h3 style="color:#ffb300;">Contact & Feedback</h3>
            <p>
                <b>Email:</b> <a href="mailto:team@compostingnetwork.org">team@compostingnetwork.org</a> <br>
                Or drop your suggestions below!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_input("💬 Your feedback, ideas, or just say hello:")

# ---- End of App ----
