"""
Generate AWS Architecture Diagram for Lung Health Monitoring System
Run: python generate_diagram.py
"""

import os

# Add Graphviz to PATH for Windows
graphviz_path = r"C:\Program Files\Graphviz\bin"
if os.path.exists(graphviz_path):
    os.environ["PATH"] += os.pathsep + graphviz_path

from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User
from diagrams.programming.framework import React

with Diagram("Lung Health Monitoring System - AWS Architecture", show=False, direction="LR", filename="lung-health-architecture"):
    # User
    user = User("User Browser")
    
    # Frontend
    with Cluster("Frontend (Vercel/Netlify)"):
        frontend = React("React App\nVite + TailwindCSS")
    
    # AWS Cloud
    with Cluster("AWS Cloud"):
        # API Gateway
        api_gateway = APIGateway("API Gateway\nREST API")
        
        # Lambda Functions
        with Cluster("Lambda Functions (Node.js)"):
            profile_lambda = Lambda("ProfileHandler")
            session_lambda = Lambda("SessionHandler")
            voice_lambda = Lambda("VoiceUploadHandler")
            prediction_lambda = Lambda("PredictionHandler")
            recommendation_lambda = Lambda("RecommendationHandler")
            stats_lambda = Lambda("StatsHandler")
        
        # ML Service
        with Cluster("ML Inference"):
            ml_service = EC2("Python ML Service\nXGBoost + librosa")
        
        # Storage
        with Cluster("Storage Layer"):
            s3_voice = S3("Voice Samples\n(30-day TTL)")
            s3_models = S3("ML Models")
            s3_datasets = S3("Datasets")
        
        # Database
        with Cluster("Database Layer"):
            db_users = Dynamodb("Users Table")
            db_sessions = Dynamodb("Sessions Table")
            db_predictions = Dynamodb("Predictions Table")
            db_stats = Dynamodb("Regional Stats Table")
        
        # Monitoring
        monitoring = Cloudwatch("CloudWatch\nLogs + Metrics + Alarms")
    
    # Main flow connections
    user >> Edge(label="HTTPS") >> frontend
    frontend >> Edge(label="REST API") >> api_gateway
    
    # API Gateway to Lambda functions
    api_gateway >> profile_lambda
    api_gateway >> session_lambda
    api_gateway >> voice_lambda
    api_gateway >> prediction_lambda
    api_gateway >> recommendation_lambda
    api_gateway >> stats_lambda
    
    # Lambda to DynamoDB
    profile_lambda >> db_users
    session_lambda >> db_sessions
    prediction_lambda >> db_predictions
    stats_lambda >> db_stats
    
    # Lambda to S3
    voice_lambda >> s3_voice
    voice_lambda >> db_sessions
    
    # Prediction flow
    prediction_lambda >> Edge(label="Invoke") >> ml_service
    ml_service >> Edge(label="Download") >> s3_voice
    ml_service >> Edge(label="Load Model") >> s3_models
    ml_service >> Edge(label="Training Data") >> s3_datasets
    
    # Monitoring connections
    profile_lambda >> monitoring
    session_lambda >> monitoring
    voice_lambda >> monitoring
    prediction_lambda >> monitoring
    recommendation_lambda >> monitoring
    stats_lambda >> monitoring
    ml_service >> monitoring

print("Diagram generated successfully: lung-health-architecture.png")
