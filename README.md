# 📘 Student Attention Prediction System

A machine learning system that models and predicts student attention levels
using behavioral simulation and regression modeling.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-WebApp-green)
![ML](https://img.shields.io/badge/Machine%20Learning-RandomForest-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

---

## 📌 Overview

This project builds a **student attention modeling and prediction system** using:

- Behavioral simulation
- Synthetic dataset generation
- Machine Learning regression
- Visualization
- Flask-based web interface

The system models how a student’s attention varies during the day based on practical real-world factors such as sleep schedule, activity type, fatigue, environmental distractions, and biological focus cycles.

The goal is to:

- Simulate realistic student attention data
- Train a machine learning model
- Predict attention levels
- Recommend optimal study hours

---

## 🎯 Objectives

- Model individual student attention using hidden behavioral variables
- Generate realistic datasets using practical assumptions
- Train a machine learning model to predict attention
- Identify best study times for students
- Provide visualization through graphs and a web interface

---

## 🧠 Core Idea

Student attention is influenced by multiple factors:

### Personal Capacity
Hidden individual ability to focus.

### Sleep Schedule
Sleep duration and timing affect next-day attention.

### Activity Type
- Textbook study → low distraction
- Mobile study → high distraction
- Coding / revision → moderate distraction

### Fatigue
Long continuous study reduces attention while breaks help recovery.

### Environment
Certain hours naturally have higher distractions.

### Circadian Rhythm
Biological focus peaks during late morning hours.

## ⚙️ Dataset Generation

The dataset is generated using practical behavioral rules.

### Parameters Included

- day
- student id
- hour
- activity type
- continuous study hours
- capacity (hidden variable)
- sleep start & end
- sleep duration
- sleep factor
- environmental factor
- biological factor
- fatigue factor
- final attention %

### Behavioral Rules

- Attention drops after long study sessions
- Mobile usage causes distraction spikes
- Breaks reduce fatigue
- Late sleep reduces morning attention
- Attention peaks naturally around late morning

---

## 🤖 Machine Learning Model

### Model Used
Random Forest Regressor

### Input Features

- hour
- activity
- continuous study duration
- sleep factor
- environment factor
- biological factor
- fatigue factor

### Output
Predicted attention percentage.

---

## 📊 Features Implemented

- ✅ Synthetic realistic dataset generation
- ✅ Hidden-variable attention modeling
- ✅ Regression model training
- ✅ Attention prediction
- ✅ Best study hour recommendation
- ✅ Daily attention graph visualization
- ✅ Flask-based web interface

---

## 🚀 How to Run

### 1️⃣ Generate Dataset

```bash
python generate_attention_dataset.py
```
Creates:
```bash
attention_dataset.csv
```
### 2️⃣ Train Model
```bash
python train_model.py
```
Creates:
```bash
attention_model.pkl
```
### 3️⃣ Run Flask App
```bash
python app.py
```
Open in browser:
```bash
http://127.0.0.1:5000
```
## 📈 Output Examples

- Daily attention graphs
- Predicted attention values
- Recommended best study hour

## 🔬 Future Improvements

- Real student data integration
- Deep learning models
- Personalized study recommendations
- Mobile app interface
- Real-time attention tracking

## 👨‍💻 Authors

- Siddharth
- Raghav
- Kishor Kumar
- Shri Vishwa D
