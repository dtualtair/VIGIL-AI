# VIGIL-AI (Her SafeSphere)
## Safeguarding Women with Technology and AI

**VIGIL-AI** is an AI-driven predictive analytics system designed to forecast crime hotspots, optimize law enforcement resources, and proactively prevent crimes against women. The project aims to create safer urban spaces through intelligent data analysis and real-time safety alerts.

---

## 🎯 Project Overview

Crime against women in India has reached alarming levels, with 31,878 rape cases reported in 2021 alone. Globally, 1 in 3 women have experienced violence, leading to chronic stress, PTSD, and anxiety disorders. Traditional law enforcement approaches are primarily reactive, lacking proactive, data-driven crime prevention strategies.

**VIGIL-AI** addresses these challenges by:
- Analyzing historical crime data to identify patterns and predict future crime hotspots
- Providing real-time alerts to law enforcement and citizens
- Suggesting safer travel routes based on crime data and environmental factors
- Optimizing police resource deployment through predictive insights

---

## ✨ Key Features

### 1. **Predictive Crime Mapping**
Uses machine learning to analyze historical crime data and predict future crime hotspots, with a special focus on crimes against women.

### 2. **Real-Time Alerts**
Provides law enforcement with instant notifications about emerging risks and high-crime periods, enabling rapid response.

### 3. **Safe Route Recommendations**
Suggests safer travel routes for women based on:
- Real-time crime data
- Sociological factors
- Environmental conditions (e.g., poorly lit areas, isolated zones)

### 4. **Proactive Resource Deployment**
Helps police departments position personnel strategically where and when they are needed most by predicting crime peaks.

### 5. **Safety Score Prediction**
Users can check safety scores for specific locations by:
- Selecting districts
- Entering addresses
- Choosing locations on a map
- Specifying date and time

### 6. **SOS Emergency System**
Integrated emergency calling feature for immediate assistance in dangerous situations.

---

## 🏗️ Technical Architecture

### **Data Sources**
- Historical crime data
- Real-time surveillance feeds
- Socioeconomic data
- Environmental data (lighting, infrastructure)
- Geospatial data

### **Data Storage**
- Centralized data warehouse
- Privacy-compliant anonymization
- Secure cloud-based infrastructure (AWS)

### **AI/ML Integration**

#### **Predictive Models:**
- Time-series forecasting
- Clustering algorithms
- Anomaly detection
- Pathfinding algorithms

#### **Tools & Technologies:**
- **PyTorch** - Deep learning framework
- **Scikit-learn** - Machine learning library
- **Bintrees** - Data structure optimization
- **Python** - Primary programming language (97.5%)
- **JavaScript** - Frontend integration (2.5%)

#### **Capabilities:**
- Crime hotspot prediction
- Real-time alert generation
- Safe route suggestions
- Resource optimization for law enforcement

---

## 📱 Application Ecosystem

### **Law Enforcement Dashboard**
Interactive interface featuring:
- Crime heatmaps
- Real-time alerts
- Resource tracking and allocation
- Patrol optimization tools

### **Mobile Application**
User-facing features:
- Safe route navigation
- Citizen reporting
- Real-time safety alerts
- Location-based safety scores
- SOS emergency calling
- Community engagement

### **API Integration**
Seamless communication with:
- Existing surveillance systems
- Navigation platforms
- Ride-hailing services
- Emergency response systems

---

## 🔒 Security & Scalability

### **Security Measures:**
- End-to-end encryption
- Role-Based Access Control (RBAC)
- GDPR compliance
- Privacy-compliant data anonymization

### **Scalability:**
- Cloud-based deployment on AWS
- Modular design for easy feature updates
- City-wide expansion capabilities
- High-availability architecture

---

## 🔄 Flow of Operations

```
Data Collection
    ↓
Data Preprocessing
    ↓
AI Model Training
    ↓
Prediction Engine
    ├── Crime Hotspot Detection
    ├── Risk Period Prediction
    └── Safe Route Prediction
    ↓
Real-time Integrations
    ├── Mobile App Alerts
    ├── Surveillance System
    └── Live Data Feedback
    ↓
Outputs
    ├── Law Enforcement Dashboard
    │   ├── Resource Allocation
    │   └── Patrol Optimization
    └── Public Safety Interface
        ├── Alerts & SOS Calls
        └── Community Engagement
```


## 🚀 Getting Started

### **Prerequisites**
```bash
Python 3.7+
PyTorch
Scikit-learn
Bintrees
```

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/dtualtair/VIGIL-AI.git
cd VIGIL-AI
```

2. **Set up virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the application**
Edit configuration files according to your deployment needs.

5. **Run the application**
```bash
python app.py
```

---

## 📱 User Interface Features

### **Select District Mode**
- Choose specific districts
- Select date and time
- Get predicted safety scores with actionable advice

### **Search Address Mode**
- Enter any address
- Get location details (pincode, district)
- Receive safety predictions with personalized recommendations

### **Choose on Map Mode**
- Interactive map selection
- Latitude/longitude coordinates
- Real-time safety score calculation

### **SOS Emergency**
- One-tap emergency calling
- Automatic location sharing
- Instant alert to emergency contacts
