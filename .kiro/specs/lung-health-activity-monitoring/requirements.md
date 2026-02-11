# Requirements Document

## Introduction

The Lung Health Activity Monitoring System is a web-based preventive health application that collects user demographic, environmental, and activity data, performs voice-based analysis before and after physical activity, and uses AI prediction to assess lung health and provide personalized recommendations.

The goal is to enable preventive respiratory health screening using accessible web technology, improving efficiency and support within healthcare ecosystems by:

- Enabling early risk detection
- Providing AI-driven patient decision support
- Reducing burden on clinicians via automated analysis
- Supporting preventive healthcare workflows

This solution aligns with patient education systems, decision-support tools, and healthcare automation initiatives.

## Problem Statement

Unlike standard symptom checkers, this system combines multimodal data (voice biomarkers, activity metrics, demographics, and environmental factors) using pre/post activity comparison to provide personalized, insurance-aware recommendations. The focus is on prevention rather than diagnosis, enabling continuous monitoring without requiring medical hardware.

## Glossary

- **System**: The Lung Health Activity Monitoring System (web-based application)
- **User**: A person using the application to monitor their lung health
- **AI_Predictor**: The artificial intelligence service (XGBoost classifier) that analyzes collected data and predicts lung health categories
- **Location_Service**: The browser-based geolocation service that manages location permissions and retrieves user location data
- **Activity_Detector**: The service that detects and monitors physical activity using browser motion sensors or timer-based fallback
- **Recommendation_Engine**: The service that generates health recommendations based on prediction results
- **Voice_Sample**: An audio recording of the user's voice captured using MediaRecorder API
- **Activity_Session**: A period during which the system monitors user activity
- **Health_Category**: A classification of lung health risk (Severe, Average, or Good)
- **Regional_Statistics**: Aggregated lung health data for a specific age group and geographic location
- **Frontend**: The React.js web application using Vite and TailwindCSS
- **Backend**: The Node.js/Express serverless backend deployed on AWS Lambda
- **ML_Service**: The Python inference service hosting the XGBoost model on AWS
- **Storage_Service**: AWS S3 for audio and datasets, DynamoDB for sessions and results

## Requirements

### Requirement 1: User Profile Management

**User Story:** As a user, I want to create my profile with demographic information, so that the system can provide personalized health assessments and recommendations.

#### Acceptance Criteria

1. THE System SHALL provide a text input field for user name
2. THE System SHALL store the user name when provided
3. THE System SHALL provide a numeric input field for user age
4. THE System SHALL store the user age when provided
5. THE System SHALL provide a text input field for user phone number
6. THE System SHALL store the user phone number when provided
7. WHERE insurance provider information is provided, THE System SHALL store the insurance provider name
8. WHEN the user submits the profile, THE System SHALL validate that the name field is not empty
9. WHEN the user submits the profile, THE System SHALL validate that the age is between 1 and 120 years
10. WHEN the user submits the profile, THE System SHALL validate that the phone number matches a valid format
11. IF validation fails, THEN THE System SHALL display an error message indicating which field is invalid
12. IF validation succeeds, THEN THE System SHALL save the user profile

### Requirement 2: Location Permission Management

**User Story:** As a user, I want the system to request location permission with clear explanations, so that I understand why location access is needed for regional health statistics.

#### Acceptance Criteria

1. WHEN the System first loads, THE System SHALL display a location permission request with an explanation message
2. THE explanation message SHALL describe why location access is needed for regional health statistics
3. IF the user denies location permission, THEN THE System SHALL display a detailed explanation message
4. IF the user denies location permission, THEN THE System SHALL display a button to request permission again
5. WHEN the user grants location permission, THE Location_Service SHALL retrieve the current location coordinates
6. WHEN the user grants location permission, THE System SHALL store the location coordinates
7. WHILE location permission is granted, THE Location_Service SHALL monitor for significant location changes
8. WHEN a significant location change is detected, THE System SHALL update the stored location coordinates
9. IF location permission is permanently denied, THEN THE System SHALL continue operating with regional statistics features disabled

### Requirement 3: Regional Health Statistics Display

**User Story:** As a user, I want to see average lung health statistics for my age group and location, so that I can understand how my health compares to regional averages.

#### Acceptance Criteria

1. WHEN location permission is granted and user age is provided, THE System SHALL calculate the user's age group in 10-year ranges
2. WHEN location permission is granted and user age is provided, THE System SHALL request regional statistics from the backend for the user's age group and location
3. WHEN regional statistics are available, THE System SHALL display average lung health metrics for the user's demographic
4. THE System SHALL display the age range and geographic region associated with the statistics
5. IF regional statistics are unavailable for the user's demographic, THEN THE System SHALL display a message indicating insufficient data
6. WHEN the user's location changes to a different region, THE System SHALL request updated regional statistics
7. WHEN updated regional statistics are received, THE System SHALL refresh the displayed statistics

### Requirement 4: Survey Management

**User Story:** As a user, I want the option to complete a health survey, so that I can provide additional context that may improve the accuracy of my lung health assessment.

#### Acceptance Criteria

1. WHEN the user completes profile setup, THE System SHALL display a prompt asking whether the user wants to take a health survey
2. WHEN the user clicks decline on the survey prompt, THE System SHALL proceed directly to the activity monitoring flow
3. WHEN the user clicks accept on the survey prompt, THE System SHALL display the first survey question
4. WHEN the user completes all survey questions, THE System SHALL store all survey responses with the user's profile identifier
5. WHEN the user completes all survey questions, THE System SHALL associate the survey responses with the current timestamp
6. WHEN survey responses are stored or survey is declined, THE System SHALL proceed to activity monitoring

### Requirement 5: Pre-Activity Voice Analysis

**User Story:** As a user, I want to record a voice sample before starting my activity, so that the system can establish a baseline for comparison with post-activity analysis.

#### Acceptance Criteria

1. WHEN the user initiates an activity session, THE System SHALL display a prompt to record a pre-activity voice sample
2. WHEN the user starts voice recording, THE System SHALL use MediaRecorder API to capture audio
3. THE System SHALL record audio for a minimum duration of 5 seconds
4. WHEN recording completes, THE System SHALL analyze the audio to verify it meets minimum quality thresholds for volume and clarity
5. IF audio quality is below the minimum threshold, THEN THE System SHALL display an error message and prompt the user to record again
6. WHEN a voice sample meets quality thresholds, THE System SHALL store the audio data in the Storage_Service
7. WHEN a voice sample is stored, THE System SHALL associate it with the current activity session identifier and timestamp
8. WHEN a valid pre-activity voice sample is stored, THE System SHALL enable the start activity button

### Requirement 6: Activity Session Monitoring

**User Story:** As a user, I want the system to automatically detect and monitor my activity, so that I can focus on exercising without manual tracking.

#### Acceptance Criteria

1. WHEN a pre-activity voice sample is recorded, THE System SHALL start an activity session
2. WHERE browser motion sensors are available, THE Activity_Detector SHALL use motion sensors to monitor activity
3. WHERE browser motion sensors are unavailable, THE Activity_Detector SHALL use timer-based activity tracking as a fallback
4. WHILE an activity session is active, THE Activity_Detector SHALL continuously monitor for activity
5. WHEN activity is detected, THE System SHALL record the start time of the activity
6. WHILE activity continues, THE System SHALL monitor for activity breaks exceeding 30 seconds
7. WHEN an activity break exceeding 30 seconds is detected, THE System SHALL record the break duration
8. WHEN activity resumes after a break, THE System SHALL continue monitoring
9. THE System SHALL record the total duration of activity excluding breaks
10. WHEN the user manually ends the activity session, THE System SHALL stop monitoring

### Requirement 7: Post-Activity Voice Analysis

**User Story:** As a user, I want to record a voice sample after completing my activity, so that the system can analyze changes in my voice that may indicate lung health status.

#### Acceptance Criteria

1. WHEN the user clicks the end activity button, THE System SHALL display a prompt to record a post-activity voice sample
2. WHEN the user starts post-activity voice recording, THE System SHALL use MediaRecorder API to capture audio
3. THE System SHALL record audio for a minimum duration of 5 seconds
4. WHEN recording completes, THE System SHALL analyze the audio to verify it meets minimum quality thresholds for volume and clarity
5. IF audio quality is below the minimum threshold, THEN THE System SHALL display an error message and prompt the user to record again
6. WHEN a post-activity voice sample meets quality thresholds, THE System SHALL store the audio data in the Storage_Service
7. WHEN a post-activity voice sample is stored, THE System SHALL associate it with the completed activity session identifier and timestamp
8. WHEN a valid post-activity voice sample is stored, THE System SHALL mark the activity session as complete

### Requirement 8: AI-Powered Lung Health Prediction

**User Story:** As a user, I want the system to analyze my activity and voice data using AI, so that I receive an accurate assessment of my lung health.

#### Acceptance Criteria

1. WHEN both pre-activity and post-activity voice samples are stored, THE System SHALL create a data package containing user demographics, activity metrics, voice sample references, and survey responses
2. WHEN the data package is created, THE System SHALL send the data package to the AI_Predictor via HTTPS
3. WHEN the AI_Predictor receives the data package, THE AI_Predictor SHALL extract features from the voice samples
4. WHEN features are extracted, THE AI_Predictor SHALL apply the XGBoost model to predict a Health_Category
5. WHEN prediction is complete, THE AI_Predictor SHALL return the Health_Category to the System
6. WHEN the System receives the Health_Category, THE System SHALL store the prediction result in DynamoDB with the session identifier
7. IF the AI_Predictor does not respond within 30 seconds, THEN THE System SHALL display a timeout error message to the user
8. IF the AI_Predictor returns an error response, THEN THE System SHALL display an appropriate error message to the user
9. IF the AI_Predictor returns an error response, THEN THE System SHALL log the error details for diagnostic purposes

### Requirement 9: Health Recommendations for Severe Cases

**User Story:** As a user with severe lung health concerns, I want to receive hospital recommendations that accept my insurance, so that I can quickly access appropriate medical care.

#### Acceptance Criteria

1. WHEN the Health_Category prediction is Severe, THE Recommendation_Engine SHALL query a database of hospitals within 50 miles of the user's location
2. WHERE the user has specified an insurance provider, THE Recommendation_Engine SHALL filter hospitals to prioritize those accepting the user's insurance
3. WHEN hospitals are identified, THE Recommendation_Engine SHALL sort the list by distance from the user's current location in ascending order
4. THE Recommendation_Engine SHALL include hospital name, address, phone number, and distance in each recommendation
5. WHERE insurance information is available, THE Recommendation_Engine SHALL indicate whether each hospital accepts the user's insurance
6. WHEN recommendations are generated, THE System SHALL display the hospital list to the user
7. THE System SHALL provide a clickable phone number for each hospital to initiate a call
8. THE System SHALL provide a navigation button for each hospital to open maps with directions

### Requirement 10: Health Recommendations for Average or Good Cases

**User Story:** As a user with average or good lung health, I want to receive actionable steps to improve my lung health, so that I can maintain or enhance my respiratory wellness.

#### Acceptance Criteria

1. WHEN the Health_Category prediction is Average or Good, THE Recommendation_Engine SHALL generate personalized health improvement recommendations based on the user's activity data
2. THE Recommendation_Engine SHALL generate personalized health improvement recommendations based on the user's demographic information
3. THE Recommendation_Engine SHALL include at least 3 specific, actionable steps in the recommendations
4. WHEN recommendations are generated, THE System SHALL display each recommendation with a title and detailed description
5. THE System SHALL provide educational content explaining the health benefits of each recommendation
6. THE System SHALL provide a save button allowing the user to bookmark recommendations for future reference
7. WHEN the user clicks save, THE System SHALL store the recommendations in the user's profile

### Requirement 11: Data Privacy and Security

**User Story:** As a user, I want my health data to be stored securely and privately, so that my sensitive information is protected.

#### Acceptance Criteria

1. THE System SHALL encrypt all voice samples before storage
2. THE System SHALL encrypt all user demographic data before storage
3. THE System SHALL transmit all data to the AI_Predictor using HTTPS protocol
4. THE System SHALL comply with health data privacy regulations
5. THE System SHALL allow users to delete their data upon request
6. THE System SHALL not share user data with third parties without explicit consent
7. THE System SHALL not store Protected Health Information (PHI)
8. THE System SHALL store only temporary session data
9. THE System SHALL use AWS S3 for audio and dataset storage with encryption at rest
10. THE System SHALL use DynamoDB for session and result storage with encryption at rest

### Requirement 12: Session Recovery and Error Handling

**User Story:** As a user, I want the system to handle unexpected interruptions gracefully, so that I don't lose my progress if the app crashes or I exit mid-session.

#### Acceptance Criteria

1. WHEN the user exits the application during an active session, THE System SHALL save the current session state to browser local storage
2. WHEN the user reopens the application, THE System SHALL check for a saved session in local storage
3. IF a saved session exists, THEN THE System SHALL display a prompt asking whether to resume or discard the session
4. WHEN the user chooses to resume, THE System SHALL restore the session state and continue from the last saved point
5. WHEN the user chooses to discard, THE System SHALL delete the saved session data
6. IF the application crashes during an active session, THEN THE System SHALL save the session state before termination when possible
7. WHEN the application restarts after a crash, THE System SHALL attempt to recover the session state from local storage
8. IF voice recording fails due to microphone error, THEN THE System SHALL display an error message explaining the microphone issue
9. IF voice recording fails, THEN THE System SHALL provide a retry button
10. IF activity detection fails due to sensor unavailability, THEN THE System SHALL notify the user and offer manual activity logging
11. WHEN an error occurs, THE System SHALL log error details to the backend for diagnostic purposes
12. WHEN logging errors, THE System SHALL exclude personally identifiable information from error logs

### Requirement 13: Device Compatibility

**User Story:** As a user, I want the system to work in my web browser, so that I can monitor my lung health without installing native apps.

#### Acceptance Criteria

1. THE System SHALL function in Chrome browser version 90 or later
2. THE System SHALL function in Firefox browser version 88 or later
3. THE System SHALL function in Safari browser version 14 or later
4. THE System SHALL function in Edge browser version 90 or later
5. THE System SHALL function on desktop operating systems including Windows, macOS, and Linux
6. THE System SHALL function on mobile operating systems including iOS and Android
7. WHEN the application loads, THE System SHALL check for MediaRecorder API availability
8. IF MediaRecorder API is unavailable, THEN THE System SHALL display an error message indicating microphone recording is not supported
9. WHEN the application loads, THE System SHALL check for Geolocation API availability
10. IF Geolocation API is unavailable, THEN THE System SHALL display a warning that location features will be disabled
11. THE System SHALL use responsive CSS to adapt the layout to screen widths from 320px to 2560px
12. THE System SHALL support both portrait and landscape orientations on mobile devices
13. WHEN the user accesses the application via HTTP, THE System SHALL redirect to HTTPS
14. IF HTTPS is unavailable, THEN THE System SHALL display an error message indicating secure connection is required

### Requirement 14: Technology Stack and Architecture

**User Story:** As a system administrator, I want the system to use scalable, cost-effective cloud infrastructure, so that the service can grow with demand while minimizing operational costs.

#### Acceptance Criteria

1. THE Frontend SHALL be implemented using React.js framework with Vite build tool
2. THE Frontend SHALL use TailwindCSS for user interface styling
3. THE Backend SHALL be implemented using Node.js runtime with Express framework
4. THE Backend SHALL be deployed as serverless functions on AWS Lambda
5. THE System SHALL route API requests through AWS API Gateway
6. THE ML_Service SHALL be implemented in Python programming language
7. THE ML_Service SHALL use XGBoost classifier for prediction
8. THE ML_Service SHALL be deployed on AWS infrastructure
9. THE Storage_Service SHALL store audio files and datasets in AWS S3
10. THE Storage_Service SHALL store session data and prediction results in AWS DynamoDB
11. THE Frontend SHALL be deployed on Vercel or Netlify platform
12. WHEN demand increases, THE System SHALL automatically scale AWS Lambda functions
13. WHEN demand decreases, THE System SHALL automatically scale down AWS Lambda functions to minimize costs

### Requirement 15: Prototype Constraints and Limitations

**User Story:** As a stakeholder, I want to understand the prototype limitations, so that I have realistic expectations about the system's capabilities.

#### Acceptance Criteria

1. THE System SHALL use only synthetic datasets or public datasets for training the ML model
2. THE System SHALL use only synthetic datasets or public datasets for testing the ML model
3. THE System SHALL not process real patient data during the prototype phase
4. THE System SHALL generate advisory predictions only, not clinical diagnoses
5. WHEN displaying prediction results, THE System SHALL display a disclaimer stating predictions are for informational purposes only
6. THE System SHALL require active user participation for data collection
7. WHERE browser motion sensors are unavailable, THE System SHALL display a message explaining simplified activity detection is in use
8. THE System SHALL inform users that activity detection accuracy may vary across different browsers

### Requirement 16: Impact and Beneficiaries

**User Story:** As a healthcare stakeholder, I want to understand who benefits from this system, so that I can evaluate its value proposition.

#### Acceptance Criteria

1. THE System SHALL provide lung health monitoring features suitable for individuals in polluted regions
2. THE System SHALL provide lung health monitoring features suitable for respiratory-risk patients
3. THE System SHALL provide lung health monitoring features suitable for preventive healthcare users
4. THE System SHALL generate data that clinics can use to reduce patient screening burden
5. THE System SHALL generate early detection data that insurance providers can use for risk assessment
6. THE System SHALL generate population health data that public health agencies can use for regional analysis
7. THE System SHALL track early detection rates as an impact metric
8. THE System SHALL track user engagement as an impact metric
9. THE System SHALL provide reporting capabilities for measuring healthcare burden reduction
