# 🚌 Late or !Late A Python-Powered Transit Assistant (🚏)

**Halifax Transit Assistant** is a console-based Python tool designed to help users make sense of GTFS (General Transit Feed Specification) data. I built this as a personal project to apply and extend the concepts I learned in my **first-year Applied Computer Science courses at Dalhousie University**.

With this assistant, you can explore live bus updates, check arrivals, manage tracked routes, and understand how real-world transit data systems work—all from your terminal.

Although it’s set up for Halifax Transit by default, you can switch it to any other city or system by updating the feed links and data files.

---

## 🧠 What I Applied from First-Year Applied Computer Science

This project connects to several concepts I learned across first-year courses:

- **CSCI 1105 / 1110 (Intro to Computer Programming / Science)**  
    → Object-Oriented Programming, modular design, functions, and file handling  
- **CSCI 1120 (Intro to Computer Systems)**  
    → Understanding how data (like GTFS) is structured and transmitted  
- **CSCI 1170 (Intro to Web Design and Development)**  
    → Consuming web APIs and live data feeds, making HTTP requests, and handling real-time updates

This project helped solidify my understanding of how computer systems interact, how to process structured data, and how to build practical software tools that connect to live external systems.

---

## 🚀 Features

- 🔔 View live service alerts for Halifax Transit routes  
- 🚌 Track real-time bus positions on specific routes  
- ⏱ Check upcoming arrivals at a stop by stop ID and route  
- 🗺 Find the nearest stops to a given location  
- 🏢 View agency details directly from static GTFS data  
- 🛠 Manage your personal list of tracked routes interactively

---

## 🛠️ Requirements

- Python 3.8+  
- [Requests](https://pypi.org/project/requests/) (`pip install requests`)  
- [geopy](https://pypi.org/project/geopy/)  (`pip install geopy`) 
- [protobuf](https://pypi.org/project/protobuf/) (`pip install protobuf`)

Check the `requirements.txt` for the full list.

---

## 🚀 Getting Started

1. **Clone this repository**
    ```bash
    git clone https://github.com/d3n-ze1/halifax-transit-assistant.git
    cd halifax-transit-assistant
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Add GTFS static data**
    - Download the official Halifax Transit GTFS static feed (or another city’s feed).
    - Place it in the `data/` folder as:
    ```
    Static_data.zip
    ```

4. **Run the assistant**
    ```bash
    python main.py
    ```

*Note: To change the transit system, update the feed URLs in `config.py` and replace the GTFS static zip file.*

---

## 📝 Credits

This project uses publicly available GTFS data for educational and personal learning purposes.

- Halifax Transit data: [Halifax Open Data Portal](https://www.halifax.ca/home/open-data)  
- GTFS-realtime Protocol Buffers: [GTFS Realtime Spec](https://developers.google.com/transit/gtfs-realtime)

---

## 🙌 Acknowledgments

Thank you to my professors, classmates, and the online open-source community that supported my learning journey in first-year Applied Computer Science.

---

Built with Python by [Nwadilioramma](https://github.com/d3n-ze1)



