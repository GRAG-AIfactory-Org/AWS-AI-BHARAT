# Lung Health Activity Monitoring System

A serverless web prototype for preventive lung health screening. The app collects demographics, location, activity, and pre/post-activity voice samples, then uses an AI model to estimate lung health risk and provide personalized recommendations.

## Key Features

- Voice-based assessment before and after walking activity
- Location-aware insights (AQI/region + age group)
- Activity monitoring (motion sensors or timer fallback)
- AI/ML lung health risk prediction (XGBoost)
- Insurance-aware hospital recommendations
- Runs fully in the browser + serverless backend (no custom hardware)

## High-Level Architecture

`React Browser` → `API Gateway` → `AWS Lambda (Node.js)` →  
`ML Inference (Python + XGBoost)` → `DynamoDB (sessions/results)` + `S3 (audio/datasets)`

- Frontend: React + Vite + TailwindCSS, MediaRecorder API, Geolocation API  
- Backend: Node.js/Express on AWS Lambda + API Gateway  
- ML Layer: Python inference service with XGBoost classifier (AWS)  
- Storage: S3 (audio, datasets), DynamoDB (sessions, predictions)

## Tech Stack

- **Frontend:** React, Vite, TailwindCSS, MediaRecorder API, Geolocation API  
- **Backend:** Node.js, Express, AWS Lambda, API Gateway  
- **ML:** Python, XGBoost, AWS (Lambda/SageMaker-style inference)  
- **Data:** S3, DynamoDB  
- **Infra (prototype):** Serverless, deployable to AWS, frontend on Vercel/Netlify or S3+CloudFront

