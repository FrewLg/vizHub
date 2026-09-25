# Health Data Visualization
# Vizhub
# NDMC
# UnivW
# National Data Amangement For Health -NDMC
# Ethiopian Public Health Institute Visualization Hub (VizHub)

> A professional-grade, interactive health data visualization and analytics platform developed for the National Data Management Center (NDMC) at the Ethiopian Public Health Institute (EPHI) .

---

## Overview

**VizHub** is an advanced health data dashboard designed to centralize and visualize public health metrics across Ethiopia . Inspired by global health data platforms, it enables policymakers, researchers, and public health professionals to explore epidemiological trends, disease burdens, and health indicators dynamically .

---

## Key Features

* **Advanced Faceted Search Sidebar**: Multi-parameter filtering options located conveniently on the left panel, supporting:
  * Year 
  * Disease Type 
  * Region / Location 
  * Facility 
  * Other critical public health parameters 
* **Geographic Map Visualization**: Dynamic, interactive maps displaying regional and localized health data distribution .
* **Multi-Format Analytics Charts**: Integrated visual representations including bar charts, pie charts, and additional analytical data views .

---

## Technology Stack

* **Backend**: Python, Django
* **Database**: PostgreSQL
* **Frontend Visualization**: D3.js, Chart.js
* **Styling**: Tailwind CSS

---

## Getting Started

### 1. Clone the Repository 
```bash
git clone [https://github.com/your-org/ephi-vizhub.git](https://github.com/your-org/ephi-vizhub.git)
cd VizHub

### 2. Set Up Virtual Environment and Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

### 3. Configure Environment Variables
####Create a .env file in the root directory:

```bash
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=ephi_vizhub_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
###4. Run Migrations and Start Server
```bash 
python manage.py migrate
python manage.py runserver

####Access the application locally at http://127.0.0.1:8000/.

##Institutional Context
Developed to strengthen evidence-based decision-making and data dissemination under the umbrella of the National Data Management Center (NDMC) at the Ethiopian Public Health Institute (EPHI)