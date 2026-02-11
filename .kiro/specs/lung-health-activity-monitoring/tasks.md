# Implementation Plan: Lung Health Activity Monitoring System

## Overview

This implementation plan breaks down the Lung Health Activity Monitoring System into discrete, incremental coding tasks. The system will be built using React/TypeScript for the frontend, Node.js/Express for the backend Lambda functions, and Python for the ML service. Each task builds on previous work, with property-based tests integrated throughout to validate correctness early.

## Tasks

- [ ] 1. Set up project structure and development environment
  - Initialize React project with Vite and TypeScript
  - Configure TailwindCSS for styling
  - Set up ESLint, Prettier, and TypeScript strict mode
  - Initialize Node.js backend project with Express and TypeScript
  - Set up Python ML service project with virtual environment
  - Configure testing frameworks (Jest, fast-check for frontend/backend; Pytest, Hypothesis for ML service)
  - Create .env files for environment configuration
  - _Requirements: 15.1, 15.2, 15.3_

- [ ] 2. Implement core data models and validation
  - [ ] 2.1 Create TypeScript interfaces for all data models
    - Define UserProfile, ActivitySession, PredictionResult, RegionalStats interfaces
    - Define enums for SessionStatus and HealthCategory
    - Create validation schemas using Zod or similar
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [ ]* 2.2 Write property test for profile data round-trip
    - **Property 1: Profile Data Round-Trip**
    - **Validates: Requirements 1.2, 1.3, 1.4, 1.5, 1.6, 1.12**

  - [ ]* 2.3 Write property test for invalid profile rejection
    - **Property 2: Invalid Profile Rejection**
    - **Validates: Requirements 1.8, 1.9, 1.10, 1.11**

  - [ ] 2.4 Implement age group calculation utility
    - Create getAgeGroup function that calculates 10-year ranges
    - _Requirements: 3.1_

  - [ ]* 2.5 Write property test for age group calculation
    - **Property 4: Age Group Calculation**
    - **Validates: Requirements 3.1**

  - [ ] 2.6 Implement geohash utility for location regions
    - Create getRegion function using geohash library
    - _Requirements: 3.1, 3.2_

- [ ] 3. Build frontend user profile components
  - [ ] 3.1 Create ProfileSetup component
    - Build form with name, age, phone, insurance provider fields
    - Implement client-side validation
    - Add error message display
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 1.9, 1.10, 1.11_

  - [ ]* 3.2 Write unit tests for ProfileSetup component
    - Test form rendering and validation
    - Test error message display
    - _Requirements: 1.8, 1.9, 1.10, 1.11_

  - [ ] 3.3 Create LocationPermission component
    - Implement geolocation permission request with explanation
    - Handle permission states (granted, denied, prompt)
    - Display retry option when denied
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.8, 2.9_

  - [ ]* 3.4 Write property test for location data persistence
    - **Property 3: Location Data Persistence**
    - **Validates: Requirements 2.6, 2.8**

- [ ] 4. Implement voice recording functionality
  - [ ] 4.1 Create VoiceRecorder component
    - Check MediaRecorder API availability
    - Request microphone permission
    - Implement recording with visual feedback
    - Add recording timer (minimum 5 seconds)
    - _Requirements: 5.1, 5.2, 5.3, 14.7, 14.8_

  - [ ] 4.2 Implement audio quality validation
    - Analyze audio for volume and clarity metrics
    - Validate minimum duration
    - Return quality assessment
    - _Requirements: 5.4, 5.5_

  - [ ]* 4.3 Write property test for voice recording quality validation
    - **Property 6: Voice Recording Quality Validation**
    - **Validates: Requirements 5.3, 5.4, 5.5, 7.3, 7.4, 7.5**

  - [ ]* 4.4 Write property test for voice sample session association
    - **Property 7: Voice Sample Session Association**
    - **Validates: Requirements 5.7, 7.7**

- [ ] 5. Build activity monitoring components
  - [ ] 5.1 Create ActivityMonitor component
    - Check for DeviceMotion API availability
    - Implement sensor-based activity detection
    - Implement timer-based fallback
    - Display real-time activity feedback
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ] 5.2 Implement break detection logic
    - Monitor for inactivity periods >30 seconds
    - Record break start time and duration
    - Resume monitoring after breaks
    - _Requirements: 6.6, 6.7, 6.8_

  - [ ] 5.3 Implement activity duration calculation
    - Calculate total duration
    - Calculate active time (excluding breaks)
    - Store break records
    - _Requirements: 6.9_

  - [ ]* 5.4 Write property test for activity detection method selection
    - **Property 8: Activity Detection Method Selection**
    - **Validates: Requirements 6.2, 6.3**

  - [ ]* 5.5 Write property test for activity duration calculation
    - **Property 9: Activity Duration Calculation**
    - **Validates: Requirements 6.7, 6.9**

- [ ] 6. Implement survey and regional statistics features
  - [ ] 6.1 Create SurveyFlow component
    - Display survey prompt with accept/decline options
    - Render survey questions when accepted
    - Store survey responses
    - Navigate to activity monitoring after completion or declination
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [ ]* 6.2 Write property test for survey flow state transitions
    - **Property 5: Survey Flow State Transitions**
    - **Validates: Requirements 4.2, 4.6**

  - [ ] 6.3 Create RegionalStats component
    - Display regional health statistics
    - Show age group and region information
    - Handle insufficient data case
    - _Requirements: 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [ ] 7. Checkpoint - Ensure frontend components work independently
  - Test each component in isolation
  - Verify browser API mocking works in tests
  - Ensure all tests pass
  - Ask the user if questions arise

- [ ] 8. Set up AWS infrastructure with Terraform
  - [ ] 8.1 Create Terraform configuration for AWS resources
    - Define VPC and networking (if needed)
    - Configure S3 buckets with encryption and lifecycle policies
    - Configure DynamoDB tables (Users, Sessions, Predictions, RegionalStats)
    - Set up IAM roles and policies for Lambda functions
    - _Requirements: 15.7, 15.8, 15.9, 15.10_

  - [ ] 8.2 Create API Gateway configuration
    - Define REST API endpoints
    - Configure CORS for frontend domain
    - Set up request validation
    - Add rate limiting
    - _Requirements: 15.4_

  - [ ] 8.3 Deploy infrastructure to AWS
    - Run terraform apply
    - Verify all resources created successfully
    - Note endpoint URLs and resource ARNs
    - _Requirements: 15.4, 15.7, 15.8, 15.9_

- [ ] 9. Implement backend Lambda functions
  - [ ] 9.1 Create ProfileHandler Lambda function
    - Implement POST /api/profile endpoint
    - Validate profile data
    - Store profile in DynamoDB Users table
    - Return userId and profile data
    - _Requirements: 1.8, 1.9, 1.10, 1.11, 1.12_

  - [ ] 9.2 Create SessionHandler Lambda function
    - Implement POST /api/session/start endpoint
    - Initialize activity session in DynamoDB
    - Return sessionId
    - _Requirements: 6.1_

  - [ ] 9.3 Create VoiceUploadHandler Lambda function
    - Implement POST /api/voice/upload endpoint
    - Validate audio file
    - Upload to S3 with encryption
    - Update session record with voice URL
    - _Requirements: 5.6, 5.7, 7.6, 7.7, 11.1, 11.9_

  - [ ]* 9.4 Write property test for data encryption at rest
    - **Property 16: Data Encryption at Rest**
    - **Validates: Requirements 11.1, 11.2, 11.9, 11.10**

  - [ ] 9.5 Create SessionCompleteHandler Lambda function
    - Implement POST /api/session/complete endpoint
    - Validate session has both voice samples
    - Invoke ML service asynchronously
    - Return processing status
    - _Requirements: 8.1, 8.2_

  - [ ]* 9.6 Write property test for prediction data package completeness
    - **Property 10: Prediction Data Package Completeness**
    - **Validates: Requirements 8.1**

  - [ ] 9.7 Create PredictionHandler Lambda function
    - Implement GET /api/prediction/:sessionId endpoint
    - Retrieve prediction from DynamoDB
    - Return health category and recommendations
    - _Requirements: 8.5, 8.6_

  - [ ]* 9.8 Write property test for prediction result persistence
    - **Property 11: Prediction Result Persistence**
    - **Validates: Requirements 8.6**

  - [ ] 9.9 Create StatsHandler Lambda function
    - Implement GET /api/stats/regional endpoint
    - Query RegionalStats table by region and age group
    - Return statistics or insufficient data message
    - _Requirements: 3.2, 3.5_

- [ ] 10. Implement ML inference service
  - [ ] 10.1 Create Python ML service with Flask/FastAPI
    - Set up Flask or FastAPI application
    - Define POST /ml/predict endpoint
    - _Requirements: 15.5, 15.6_

  - [ ] 10.2 Implement voice feature extraction
    - Use librosa to extract MFCCs, pitch, speech rate
    - Calculate pause patterns and voice intensity
    - _Requirements: 8.3, 8.4_

  - [ ] 10.3 Load and configure XGBoost model
    - Load pre-trained XGBoost model from S3
    - Configure model parameters
    - _Requirements: 15.6, 15.7_

  - [ ] 10.4 Implement prediction pipeline
    - Download voice samples from S3
    - Extract features from both samples
    - Combine with activity and demographic features
    - Normalize feature vector
    - Run XGBoost inference
    - Return health category and confidence score
    - _Requirements: 8.3, 8.4, 8.5_

  - [ ]* 10.5 Write unit tests for feature extraction
    - Test MFCC extraction with sample audio
    - Test feature vector normalization
    - _Requirements: 8.3, 8.4_

  - [ ] 10.6 Implement error handling and timeout management
    - Handle S3 download failures
    - Handle invalid audio formats
    - Implement 30-second timeout
    - Return appropriate error responses
    - _Requirements: 8.7, 8.8, 8.9_

  - [ ]* 10.7 Write property test for prediction error handling
    - **Property 12: Prediction Error Handling**
    - **Validates: Requirements 8.7, 8.8, 8.9**

- [ ] 11. Implement recommendation engine
  - [ ] 11.1 Create RecommendationHandler Lambda function
    - Implement recommendation generation logic
    - _Requirements: 9.1, 10.1_

  - [ ] 11.2 Implement hospital recommendation logic for severe cases
    - Query hospital database within 50 miles
    - Filter by insurance provider if specified
    - Sort by distance ascending
    - Include hospital details (name, address, phone, distance)
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ]* 11.3 Write property test for hospital recommendation sorting
    - **Property 13: Hospital Recommendation Sorting**
    - **Validates: Requirements 9.1, 9.3**

  - [ ]* 11.4 Write property test for insurance-based hospital filtering
    - **Property 14: Insurance-Based Hospital Filtering**
    - **Validates: Requirements 9.2**

  - [ ] 11.5 Implement health improvement recommendations for average/good cases
    - Generate at least 3 personalized recommendations
    - Include title, description, and educational content
    - Base recommendations on activity data and demographics
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ]* 11.6 Write property test for health improvement recommendations completeness
    - **Property 15: Health Improvement Recommendations Completeness**
    - **Validates: Requirements 10.1, 10.3, 10.4, 10.5**

- [ ] 12. Implement offline support and network resilience
  - [ ] 12.1 Add local storage for offline activity recording
    - Store activity data in browser localStorage when offline
    - Detect network connectivity changes
    - _Requirements: 12.1_

  - [ ] 12.2 Implement data synchronization on reconnection
    - Upload locally stored data when network restored
    - Handle sync conflicts
    - _Requirements: 12.2_

  - [ ]* 12.3 Write property test for offline activity recording
    - **Property 17: Offline Activity Recording**
    - **Validates: Requirements 12.1, 12.2**

  - [ ] 12.4 Implement retry logic with exponential backoff
    - Retry failed ML prediction requests up to 3 times
    - Use exponential backoff (1s, 2s, 4s)
    - Display error after all retries fail
    - _Requirements: 12.3, 12.4, 12.5_

  - [ ]* 12.5 Write property test for request retry with exponential backoff
    - **Property 18: Request Retry with Exponential Backoff**
    - **Validates: Requirements 12.4**

- [ ] 13. Implement session persistence and recovery
  - [ ] 13.1 Add session state persistence to localStorage
    - Save session state on exit
    - Include all recorded data and current status
    - _Requirements: 13.1_

  - [ ] 13.2 Implement session recovery on app restart
    - Check for saved session on app load
    - Display resume/discard prompt
    - Restore session state when user chooses resume
    - _Requirements: 13.2, 13.3, 13.4_

  - [ ]* 13.3 Write property test for session state round-trip
    - **Property 19: Session State Round-Trip**
    - **Validates: Requirements 13.1, 13.2, 13.4**

  - [ ] 13.4 Implement error recovery for voice recording and activity detection
    - Display error messages for microphone failures
    - Provide retry buttons
    - Offer manual activity logging when detection fails
    - Log errors without PII
    - _Requirements: 13.5, 13.6, 13.8, 13.9, 13.10, 13.11, 13.12_

- [ ] 14. Implement security features
  - [ ] 14.1 Add HTTPS redirect logic
    - Redirect HTTP requests to HTTPS
    - Display error if HTTPS unavailable
    - _Requirements: 14.13, 14.14_

  - [ ]* 14.2 Write property test for HTTP to HTTPS redirect
    - **Property 20: HTTP to HTTPS Redirect**
    - **Validates: Requirements 14.13**

  - [ ] 14.3 Implement data encryption for transmission
    - Ensure all API calls use HTTPS
    - Validate SSL certificates
    - _Requirements: 11.3_

  - [ ] 14.4 Add API authentication
    - Implement JWT tokens for user sessions
    - Add API key authentication for ML service
    - Configure rate limiting
    - _Requirements: 11.3_

- [ ] 15. Build results display and recommendations UI
  - [ ] 15.1 Create ResultsDisplay component
    - Display health category prediction
    - Show confidence score
    - Display disclaimer for advisory predictions
    - _Requirements: 8.5, 16.5_

  - [ ] 15.2 Create HospitalRecommendations component
    - Display list of recommended hospitals
    - Show hospital details (name, address, phone, distance)
    - Add clickable phone numbers and navigation buttons
    - Indicate insurance acceptance
    - _Requirements: 9.5, 9.6, 9.7, 9.8_

  - [ ] 15.3 Create HealthImprovementRecommendations component
    - Display actionable health improvement steps
    - Show educational content
    - Add save functionality
    - _Requirements: 10.4, 10.5, 10.6, 10.7_

- [ ] 16. Implement browser compatibility checks
  - [ ] 16.1 Add capability detection on app load
    - Check for MediaRecorder API
    - Check for Geolocation API
    - Display appropriate error messages if unavailable
    - _Requirements: 14.7, 14.8, 14.9, 14.10_

  - [ ] 16.2 Implement responsive design
    - Use TailwindCSS responsive utilities
    - Test on screen widths 320px-2560px
    - Support portrait and landscape orientations
    - _Requirements: 14.11, 14.12_

- [ ] 17. Wire all components together and implement routing
  - [ ] 17.1 Set up React Router
    - Define routes for all pages
    - Implement navigation flow
    - _Requirements: All workflow requirements_

  - [ ] 17.2 Create App component with global state
    - Set up React Context for user profile and session
    - Implement state management for workflow
    - _Requirements: All workflow requirements_

  - [ ] 17.3 Connect frontend to backend APIs
    - Implement API client with Axios
    - Add request/response interceptors
    - Handle authentication tokens
    - _Requirements: All API requirements_

  - [ ] 17.4 Implement complete user workflow
    - Profile setup → Location permission → Regional stats → Survey → Voice recording → Activity monitoring → Post-activity voice → Results → Recommendations
    - _Requirements: All workflow requirements_

- [ ] 18. Checkpoint - End-to-end testing
  - Test complete user journey from profile to recommendations
  - Verify all API integrations work
  - Test error scenarios and recovery
  - Ensure all property tests pass
  - Ask the user if questions arise

- [ ] 19. Add monitoring and logging
  - [ ] 19.1 Implement CloudWatch logging for Lambda functions
    - Add structured JSON logging
    - Include correlation IDs
    - Redact sensitive data
    - _Requirements: 13.11, 13.12_

  - [ ] 19.2 Set up CloudWatch alarms
    - API error rate > 5%
    - ML service timeout rate > 10%
    - Lambda cold start > 3 seconds
    - _Requirements: Monitoring requirements_

  - [ ] 19.3 Create CloudWatch dashboards
    - Real-time user activity
    - System health overview
    - ML model performance
    - Cost tracking
    - _Requirements: Monitoring requirements_

- [ ] 20. Deploy to production
  - [ ] 20.1 Deploy frontend to Vercel/Netlify
    - Configure custom domain
    - Set up environment variables
    - Enable HTTPS
    - _Requirements: 15.10_

  - [ ] 20.2 Deploy backend Lambda functions to production
    - Update API Gateway endpoints
    - Configure production environment variables
    - _Requirements: 15.4, 15.11_

  - [ ] 20.3 Deploy ML service to AWS
    - Set up EC2 or Lambda for ML inference
    - Configure auto-scaling
    - _Requirements: 15.6, 15.11, 15.12, 15.13_

  - [ ]* 20.4 Run smoke tests in production
    - Test basic health checks
    - Verify API endpoints respond
    - Test one complete user flow
    - _Requirements: All requirements_

- [ ] 21. Final checkpoint - Production validation
  - Verify all features work in production
  - Check monitoring dashboards
  - Confirm all tests pass
  - Review security configuration
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties (minimum 100 iterations each)
- Unit tests validate specific examples and edge cases
- Checkpoints ensure incremental validation at key milestones
- The implementation follows a bottom-up approach: data models → components → integration → deployment
