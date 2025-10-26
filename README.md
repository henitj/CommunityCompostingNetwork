# Community Composting Network

**Turning Waste into Growth — An easy, fun platform for tracking, sharing, and growing composting impact in households, schools, and communities.**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Demo Data](#demo-data)
- [Contributing](#contributing)
- [License & Credits](#license--credits)

---

## Overview

Community Composting Network is a web app prototype built for hackathons, education, and local engagement.  
Using Python and Streamlit, it helps anyone **log compost, view dashboards & maps, compete on leaderboards, and build green habits.**  
Perfect for households, schools, gardens, and sustainability clubs!

---

## Features

- 🌱 Modern, colorful UI (mobile/desktop)
- 📝 Log compost and garbage contributions
- 📈 Real-time analytics dashboard
- 🏆 Leaderboard for friendly competition
- 🗺️ Map of community compost activity (Austin, TX base)
- 🏠 Homeowner garbage input and sorting education
- 👩‍🏫 About & feedback pages, hackathon-ready navigation
- 🔒 No backend required—uses CSV for demo data

---

## How to Run

1. **Clone this repo**

    ```
    git clone [https://github.com/your-username](https://github.com/henitj/community-composting-network.git
    cd community-composting-network
    ```

2. **Install dependencies**

    ```
    pip install -r requirements.txt
    ```

3. **Run Streamlit demo**

    ```
    streamlit run compost_app.py
    ```

4. **Open app in your browser**

    - Default: http://localhost:8501

*No Python backend needed. All data stored in `compost_data.csv`.*

---

## Tech Stack

- Python 3.7+
- Streamlit
- Pandas
- Folium + streamlit-folium (mapping)
- CSV for lightweight demo/database

---

## Demo Data

- `compost_data.csv`: Community entries for compost, garbage, drop-off/pickup, leaderboard, etc.
- Map markers are randomized around Austin, TX (privacy-safe for demo).

---

## Contributing

We welcome ideas and contributions!
- Open issues for bugs or features
- Fork this repo, create a pull request
- Suggestions for UI/UX, map data, or deployment welcome

---

## License & Credits

- **MIT License**
- Map tiles: OpenStreetMap contributors
- Icons: [flaticon.com](https://flaticon.com), [undraw.co](https://undraw.co)
- Inspired by Austin’s local sustainability efforts

---

### Contact

Questions or feedback: team@compostingdemo.org

---

**Let’s make waste matter—for the planet and for the people!**
