# 🚀 Astronaut Health Simulation Engine (AHSE)

## Overview

The Astronaut Health Simulation Engine (AHSE) is an AI-powered digital twin system that predicts and visualizes astronaut physiological changes during long-duration space missions. Built for mission planners, health scientists, and astronaut trainers to enable proactive health management.

## Key Features

- **Predictive Health Modeling**: AI models for muscle atrophy, bone density loss, cardiovascular changes
- **Interactive 3D Visualization**: Real-time health status with color-coded organ systems
- **Recommendation Engine**: Personalized interventions for exercise, nutrition, and shielding
- **Mission Planning Tools**: What-if scenarios and risk assessment
- **Data Integration**: NASA Human Research Database compatibility

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd ahse

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run src/dashboard/app.py
```

## Project Structure

```
ahse/
├── src/
│   ├── core/           # Core simulation engine
│   ├── models/             # AI/ML models
│   ├── dashboard/         # Web interface
│   ├── api/              # REST API endpoints
│   └── data/             # Data processing and storage
├── tests/                # Test suite
├── docs/                 # Documentation
└── requirements.txt      # Dependencies
```

## Quick Start

1. **Launch Dashboard**: `streamlit run src/dashboard/app.py`
2. **Configure Mission**: Set duration, gravity, radiation parameters
3. **Run Simulation**: Generate health predictions
4. **View Results**: Interactive 3D avatar and charts
5. **Get Recommendations**: AI-suggested interventions

## Team

- **Product Manager**: Pranay
- **AI/ML Developer**: Kartik  
- **Biomedical Engineer**: Kunal
- **Frontend Developer**: Harshit

## License

MIT License - See LICENSE file for details
