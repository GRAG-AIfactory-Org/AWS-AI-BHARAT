# Lung Health Activity Monitoring System - AWS Architecture

## Architecture Diagram (Text-Based)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER (Client)                               │
│  - MediaRecorder API (Voice Recording)                                      │
│  - Geolocation API (Location Services)                                      │
│  - DeviceMotion API (Activity Detection)                                    │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ HTTPS
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel/Netlify)                                │
│  - React 18+ with Vite                                                      │
│  - TailwindCSS                                                              │
│  - React Router                                                             │
│  - Axios HTTP Client                                                        │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │ HTTPS/REST API
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AWS CLOUD                                          │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      API GATEWAY                                      │  │
│  │  - REST API Endpoints                                                │  │
│  │  - CORS Configuration                                                │  │
│  │  - Request Validation                                                │  │
│  │  - Rate Limiting                                                     │  │
│  └────────────────────────────┬─────────────────────────────────────────┘  │
│                                │                                             │
│                                ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    LAMBDA FUNCTIONS (Node.js)                        │  │
│  │                                                                       │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐                │  │
│  │  │  Profile    │  │  Session    │  │ Voice Upload │                │  │
│  │  │  Handler    │  │  Handler    │  │   Handler    │                │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘                │  │
│  │         │                 │                 │                        │  │
│  │  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴───────┐                │  │
│  │  │ Prediction  │  │Recommendation│  │    Stats     │                │  │
│  │  │  Handler    │  │   Handler    │  │   Handler    │                │  │
│  │  └──────┬──────┘  └──────────────┘  └──────────────┘                │  │
│  └─────────┼──────────────────────────────────────────────────────────┘  │
│            │                                                                │
│            ▼                                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    ML SERVICE (Python)                               │  │
│  │  - EC2 Instance / Lambda                                            │  │
│  │  - XGBoost Classifier                                               │  │
│  │  - librosa (Audio Feature Extraction)                               │  │
│  │  - Flask/FastAPI                                                    │  │
│  └────────────────────────────┬─────────────────────────────────────────┘  │
│                                │                                             │
│  ┌─────────────────────────────┴──────────────────────────────────────┐    │
│  │                                                                      │    │
│  ▼                              ▼                        ▼             ▼    │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐ │
│  │   S3 STORAGE     │  │    DYNAMODB      │  │     CLOUDWATCH           │ │
│  │                  │  │                  │  │                          │ │
│  │ ┌──────────────┐ │  │ ┌──────────────┐│  │ ┌──────────────────────┐ │ │
│  │ │Voice Samples │ │  │ │ Users Table  ││  │ │ Logs                 │ │ │
│  │ │(30-day TTL)  │ │  │ └──────────────┘│  │ └──────────────────────┘ │ │
│  │ └──────────────┘ │  │                  │  │                          │ │
│  │                  │  │ ┌──────────────┐ │  │ ┌──────────────────────┐ │ │
│  │ ┌──────────────┐ │  │ │Sessions Table│ │  │ │ Metrics              │ │ │
│  │ │  ML Models   │ │  │ └──────────────┘ │  │ └──────────────────────┘ │ │
│  │ └──────────────┘ │  │                  │  │                          │ │
│  │                  │  │ ┌──────────────┐ │  │ ┌──────────────────────┐ │ │
│  │ ┌──────────────┐ │  │ │Predictions   │ │  │ │ Alarms               │ │ │
│  │ │  Datasets    │ │  │ │    Table     │ │  │ └──────────────────────┘ │ │
│  │ └──────────────┘ │  │ └──────────────┘ │  │                          │ │
│  │                  │  │                  │  │ ┌──────────────────────┐ │ │
│  │ - Encryption at  │  │ ┌──────────────┐ │  │ │ Dashboards           │ │ │
│  │   Rest (AES-256) │  │ │Regional Stats│ │  │ └──────────────────────┘ │ │
│  │ - Lifecycle      │  │ │    Table     │ │  │                          │ │
│  │   Policies       │  │ └──────────────┘ │  │                          │ │
│  │                  │  │                  │  │                          │ │
│  │                  │  │ - Encryption at  │  │                          │ │
│  │                  │  │   Rest           │  │                          │ │
│  │                  │  │ - On-Demand      │  │                          │ │
│  │                  │  │   Capacity       │  │                          │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Profile Creation
```
Browser → API Gateway → ProfileHandler Lambda → DynamoDB (Users Table)
```

### 2. Voice Sample Upload
```
Browser → API Gateway → VoiceUploadHandler Lambda → S3 (Voice Samples Bucket)
                                                   → DynamoDB (Sessions Table)
```

### 3. Activity Session
```
Browser → API Gateway → SessionHandler Lambda → DynamoDB (Sessions Table)
```

### 4. AI Prediction
```
Browser → API Gateway → PredictionHandler Lambda → ML Service (EC2/Lambda)
                                                  ↓
                                    ML Service → S3 (Voice Samples + Models)
                                                  ↓
                                    ML Service → Feature Extraction (librosa)
                                                  ↓
                                    ML Service → XGBoost Inference
                                                  ↓
                                    ML Service → PredictionHandler Lambda
                                                  ↓
                                    PredictionHandler → DynamoDB (Predictions Table)
```

### 5. Recommendations
```
Browser → API Gateway → RecommendationHandler Lambda → DynamoDB (Predictions Table)
                                                     → External Hospital DB
                                                     → Response to Browser
```

### 6. Regional Statistics
```
Browser → API Gateway → StatsHandler Lambda → DynamoDB (Regional Stats Table)
```

## Key Components

### Frontend (React + Vite)
- **ProfileSetup**: User demographic data collection
- **LocationPermission**: Geolocation permission management
- **VoiceRecorder**: Pre/post activity voice recording
- **ActivityMonitor**: Activity session tracking
- **ResultsDisplay**: Prediction results and recommendations

### Backend (AWS Lambda + Node.js)
- **ProfileHandler**: User profile CRUD operations
- **SessionHandler**: Activity session management
- **VoiceUploadHandler**: Voice sample upload to S3
- **PredictionHandler**: ML prediction orchestration
- **RecommendationHandler**: Health recommendations generation
- **StatsHandler**: Regional statistics retrieval

### ML Service (Python + XGBoost)
- **Feature Extraction**: MFCC, pitch, speech rate, pause patterns
- **Model Inference**: XGBoost classifier (Severe/Average/Good)
- **Voice Analysis**: Pre/post activity comparison

### Storage
- **S3 Buckets**:
  - Voice samples (encrypted, 30-day retention)
  - ML models
  - Training datasets
  
- **DynamoDB Tables**:
  - Users (userId, demographics, location)
  - Sessions (sessionId, voice URLs, activity data)
  - Predictions (sessionId, health category, confidence)
  - Regional Stats (region, age group, statistics)

### Monitoring
- **CloudWatch Logs**: Lambda function logs, ML service logs
- **CloudWatch Metrics**: API response times, error rates
- **CloudWatch Alarms**: Error rate thresholds, timeout alerts
- **CloudWatch Dashboards**: Real-time system health

## Security Features

1. **Encryption**:
   - TLS 1.3 for all connections
   - S3 server-side encryption (AES-256)
   - DynamoDB encryption at rest

2. **Authentication**:
   - API Gateway with API keys
   - JWT tokens for user sessions
   - IAM roles for Lambda functions

3. **Privacy**:
   - No PHI storage
   - Temporary session data only
   - 30-day retention for voice samples
   - PII redaction in logs

4. **Compliance**:
   - HIPAA considerations (advisory only)
   - GDPR compliance
   - Right to deletion

## Scalability

- **Auto-scaling**: Lambda functions scale automatically
- **Serverless**: Pay-per-use pricing model
- **Cost-effective**: ~$25.50/month for 1000 users
- **Global**: CloudFront CDN for frontend assets
- **Regional**: DynamoDB global tables for multi-region

## Cost Breakdown (per 1000 users/month)

| Service | Estimated Cost |
|---------|---------------|
| Lambda Functions | ~$5 |
| API Gateway | ~$3.50 |
| S3 Storage | ~$2 |
| DynamoDB | ~$5 |
| ML Service (EC2) | ~$10 |
| **Total** | **~$25.50** |
