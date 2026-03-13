from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime
import re

# Load the template
doc = Document(r'c:\Users\TEJAS\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm\LocalState\sessions\FD8FCF8D0A88CE9B575D94CB33796A5A8E364714\transfers\2026-11\MCA_Project Report_format.docx')

# Replace header placeholders
for i, para in enumerate(doc.paragraphs):
    if '<< Project Title>>' in para.text:
        para.text = para.text.replace('<< Project Title>>', 'EDUFOCUS – Study with Focus')
    elif '<< Name of the Student >>' in para.text:
        para.text = para.text.replace('<< Name of the Student >>', 'Tejas K M')
    elif '<<Details of the guide>>' in para.text:
        para.text = para.text.replace('<<Details of the guide>>', 'Ms. Alpa Patel, Assistant Professor, School of Computer Applications, Dayananda Sagar University')
    elif '<<Student name>>' in para.text:
        para.text = para.text.replace('<<Student name>>', 'Tejas K M')
    elif '[USN NO]' in para.text:
        para.text = para.text.replace('[USN NO]', 'SCA24MCA041')

# Comprehensive chapter content

chapter4_content = """
4.1 SYSTEM ARCHITECTURE (HIGH-LEVEL DESIGN)

4.1.1 Layered Architecture Overview

EduFocus follows a four-tier layered architecture ensuring scalability, maintainability, and separation of concerns:

Presentation Layer (Client-Side):
This layer handles all user interactions and visualization. It comprises:
- HTML5 semantic markup providing structure for all web pages
- CSS3 with responsive design frameworks (Bootstrap) for styling across devices
- JavaScript (ES6+) for interactivity and client-side logic
- Chart.js library for real-time analytics visualization
- WebRTC API for browser-based webcam access and real-time data transmission

The presentation layer communicates exclusively with the Business Logic Layer through RESTful APIs, ensuring clean separation and enabling future mobile app development.

Business Logic Layer (Application Server):
This layer processes user requests and coordinates operations:
- Flask framework as the core web application server
- Session management and authentication controllers
- Focus monitoring orchestration and real-time processing coordination
- PDF processing and summarization engine coordination
- Analytics computation and aggregation services
- RESTful API endpoints for client requests

The Business Logic Layer implements business rules, coordinates with data access layer, and manages third-party service integrations.

Data Access Layer (Persistence):
This layer provides abstraction over data storage mechanisms:
- SQLAlchemy ORM for database abstraction
- Connection pooling for performance optimization
- Prepared statements for SQL injection prevention
- Transaction management for data consistency
- Caching layer (Redis) for frequently accessed data

Data Storage Layer:
- Relational database (SQLite/MySQL) for structured data
- File system storage for uploaded documents
- Object storage (S3) for document archives in cloud deployment

4.1.2 Microservices Architecture Potential

While current implementation uses monolithic architecture, the system is designed to support future microservices decomposition:

Focus Tracking Service:
- Dedicated service for face detection and focus analysis
- Scales independently with high computation load
- WebSocket communication for real-time data
- Stateless design enabling horizontal scaling

Document Processing Service:
- dedicated service for PDF handling and summarization
- Asynchronous task queue (Celery) for background processing
- Cacheable results reducing redundant computation
- Scalable based on document volume

Analytics Service:
- Dedicated service for data aggregation and computation
- Implements complex analytical queries
- Real-time dashboard updates via WebSockets
- Time-series database optimization

This architecture ensures future scalability as user base grows.

4.1.3 Component Diagram

[Conceptual Component Diagram]

External Systems:
    ↓
Web Browsers ← → Flask Web Server
                     ↓
            ├── Session Manager
            ├── Face Detection Engine
            ├── PDF Processor
            ├── Summarization Engine
            ├── Analytics Engine
            └── API Router
                     ↓
            ├── User Database
            ├── Session DataStore
            ├── Document Store
            └── Analytics Cache

4.2 DETAILED SYSTEM DESIGN (LOW-LEVEL DESIGN)

4.2.1 Data Flow Diagram (DFD) - Level 0

```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│   ┌─────────────┐          ┌──────────────┐               │
│   │   User      │          │  EduFocus    │               │
│   │  (Student)  │←────────→│   System     │               │
│   └─────────────┘          └──────────────┘               │
│                                  ↓                         │
│                          ┌──────────────┐                 │
│                          │  Documents   │                 │
│                          │   (PDFs)     │                 │
│                          └──────────────┘                 │
│                                  ↓                         │
│                          ┌──────────────┐                 │
│                          │  Analytics   │                 │
│                          │  Dashboard   │                 │
│                          └──────────────┘                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

4.2.2 DFD - Level 1 (Major Processes)

```
User Input
    ↓
[1.0 User Management] → User Database
    ↓                      
[2.0 Focus Tracking] ← Webcam Input
    ├→ Focus Records Database
    └→ 
[3.0 Document Processing] ← PDF Upload
    ├→ Document Database
    └→
[4.0 Analytics Generation] 
    └→ Analytics Database
         ↓
    Display to User
```

4.2.3 Use Case Diagrams

Primary Actors:
- Student: Primary system user focused on study productivity
- Administrator: System maintenance and monitoring (future)
- Educator: Institutional dashboard access (future)

Use Cases:

Student Use Cases:
1. Register and Create Account
2. Login to System
3. Upload PDF Document
4. View Document Summary
5. Start Study Session
6. View Real-Time Focus Metrics
7. Complete Study Session
8. Review Session Analytics
9. Generate Weekly Report
10. Practice with Flashcards
11. Answer Practice Questions
12. Customize Dashboard
13. Manage Study Goals
14. Export Session Data

Extended Use Cases:

View Real-Time Metrics extends View-Dashboard:
- Displays current session focus percentage
- Shows break statistics in real-time
- Indicates current distraction level

Complete Study Session includes End-Session Processing:
- Calculate session statistics
- Store session data
- Generate session report
- Recommend next steps

Generate Weekly Report includes Analytics Aggregation:
- Aggregate focus data across week
- Calculate trends
- Format and display

4.2.4 Activity Diagrams

Study Session Activity Flow:

```
Start
  ↓
[Select Study Material] 
  ↓
[Grant Webcam Permission]?
  ├─No→ [Display No Camera Warning]
  └─Yes→
  ↓
[Start Focus Monitoring]
  ↓
[Real-Time Face Detection Loop]
  ├─Face Detected?
  │  ├─Yes → [Calculate Focus Score]
  │  └─No → [Increment Missing Frames]
  ↓
[Update Dashboard in Real-Time]
  ↓
[User Studies]
  │ (Parallel: Focus monitoring continues)
  ↓
[Click End Session]?
  ├─No → [Continue]
  └─Yes →
  ↓
[Stop Face Detection]
  ↓
[Calculate Session Statistics]
  ↓
[Generate Session Report]
  ↓
[Display Results]
  ↓
End
```

Document Processing Activity Flow:

```
Start
  ↓
[User Uploads PDF]
  ↓
[Validate File Type and Size]
  ├─Valid?
  │  ├─No → [Display Error Message]
  │  └─Yes →
  ↓
[Extract Text from PDF]
  ├─Success?
  │  ├─No → [Display Extraction Error]
  │  └─Yes →
  ↓
[Preprocess Text]
  ├─Tokenization
  ├─Cleaning
  └─Normalization
  ↓
[Generate Multiple Summaries]
  ├─Level 1 (10%)
  ├─Level 2 (25%)
  └─Level 3 (50%)
  ↓
[Extract Key Concepts]
  ↓
[Generate Practice Questions]
  ↓
[Store Processed Document]
  ↓
[Display Document Summary]
  ↓
End
```

4.2.5 Class Diagrams and Entities

Core Entity Classes:

```
class User:
    - user_id: UUID
    - email: String [unique]
    - password_hash: String
    - full_name: String
    - study_level: Enum (HS, UG, PG)
    - created_at: DateTime
    - updated_at: DateTime
    - is_active: Boolean
    
    + register()
    + login()
    + update_profile()
    + get_study_sessions()

class StudySession:
    - session_id: UUID
    - user_id: UUID [FK]
    - start_time: DateTime
    - end_time: DateTime
    - total_duration: Integer (seconds)
    - active_duration: Integer (seconds)
    - focus_percentage: Float
    - focus_score: Float
    - document_id: UUID [FK, optional]
    - notes: Text
    
    + calculate_statistics()
    + get_focus_timeline()
    + generate_report()

class FocusRecord:
    - record_id: UUID
    - session_id: UUID [FK]
    - timestamp: DateTime
    - face_detected: Boolean
    - focus_level: Float (0-100)
    - head_pose_pitch: Float
    - head_pose_yaw: Float
    - head_pose_roll: Float
    - eye_gaze_horizontal: Float
    - eye_gaze_vertical: Float
    - distraction_indicators: JSON
    
    + get_focus_segment()
    + detect_distraction_events()

class Document:
    - document_id: UUID
    - user_id: UUID [FK]
    - file_name: String
    - file_size: Integer
    - upload_time: DateTime
    - page_count: Integer
    - extracted_text: Text
    - is_processed: Boolean
    
    + get_text_content()
    + get_summary(level)
    + get_key_concepts()

class Summary:
    - summary_id: UUID
    - document_id: UUID [FK]
    - summary_level: Enum (10%, 25%, 50%)
    - summary_text: Text
    - extracted_concepts: JSON
    - generated_at: DateTime
    
    + get_key_sentences()
    + get_highlights_in_original()

class FocusAnalytics:
    - analytics_id: UUID
    - session_id: UUID [FK]
    - focus_distribution: JSON
    - distraction_patterns: JSON
    - productivity_score: Float
    - recommendations: Text[]
    
    + calculate_trend()
    + compare_with_baseline()
```

4.3 DATABASE DESIGN

4.3.1 Entity-Relationship Diagram

```
User
├── id (PK)
├── email (UNIQUE)
├── password_hash
├── full_name
├── study_level
├── created_at
└── updated_at
  ↓
  ├─1---* → StudySession
  ├─1---* → Document
  └─1---* → FocusAnalytics


StudySession
├── id (PK)
├── user_id (FK)
├── document_id (FK, nullable)
├── start_time
├── end_time
├── total_duration
├── active_duration
├── focus_percentage
├── focus_score
├── notes
└── created_at
  ↓
  └─1---* → FocusRecord


FocusRecord
├── id (PK)
├── session_id (FK)
├── timestamp
├── face_detected
├── focus_level
├── head_pose_pitch
├── head_pose_yaw
├── head_pose_roll
├── eye_gaze_horizontal
├── eye_gaze_vertical
└── distraction_indicators (JSON)


Document
├── id (PK)
├── user_id (FK)
├── file_name
├── file_size
├── upload_time
├── page_count
├── extracted_text
├── is_processed
└── storage_path
  ↓
  └─1---* → Summary


Summary
├── id (PK)
├── document_id (FK)
├── summary_level
├── summary_text
├── extracted_concepts
├── key_sentences
└── generated_at


FocusAnalytics
├── id (PK)
├── user_id (FK)
├── period (Daily/Weekly/Monthly)
├── start_date
├── end_date
├── total_sessions
├── avg_focus_percentage
├── focus_distribution
├── distraction_patterns
├── productivity_score
└── generated_at
```

4.3.2 Schema Design

User Table Schema:
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    study_level ENUM('HS', 'UG', 'PG') DEFAULT 'UG',
    notification_enabled BOOLEAN DEFAULT TRUE,
    theme_preference VARCHAR(20) DEFAULT 'light',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
);
```

StudySession Table Schema:
```sql
CREATE TABLE study_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    document_id UUID,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    total_duration INTEGER,
    active_duration INTEGER,
    focus_percentage FLOAT,
    focus_score FLOAT,
    break_count INTEGER DEFAULT 0,
    total_break_duration INTEGER DEFAULT 0,
    notes TEXT,
    tags VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES documents(id),
    INDEX idx_user_id (user_id),
    INDEX idx_start_time (start_time),
    INDEX idx_created_at (created_at)
);
```

FocusRecord Table Schema:
```sql
CREATE TABLE focus_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    face_detected BOOLEAN,
    focus_level FLOAT,
    head_pose_pitch FLOAT,
    head_pose_yaw FLOAT,
    head_pose_roll FLOAT,
    eye_gaze_horizontal FLOAT,
    eye_gaze_vertical FLOAT,
    distraction_indicators JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES study_sessions(id),
    INDEX idx_session_id (session_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_created_at (created_at)
);
```

Document Table Schema:
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    page_count INTEGER,
    extracted_text LONGTEXT,
    is_processed BOOLEAN DEFAULT FALSE,
    storage_path VARCHAR(255),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_user_id (user_id),
    INDEX idx_upload_time (upload_time),
    INDEX idx_is_processed (is_processed)
);
```

4.4 USER INTERFACE (UI) DESIGN

4.4.1 Key Screen Layouts

Login Screen:
- Centered form with email and password fields
- "Remember Me" checkbox for credential caching
- "Forgot Password" recovery link
- Sign-up link for new users
- Professional branding and color scheme
- Input validation with real-time feedback

Dashboard Screen:
- Header with user profile and logout button
- Sidebar with navigation menu
- Main content area with widgets for:
  * Current focus status
  * Today's study sessions
  * Weekly focus trend chart
  * Upcoming study goals
  * Recent documents
- Quick action buttons (Start Study, Upload Document)
- Responsive grid layout for different screen sizes

Study Session Screen:
- Document/material display area (left panel)
- Real-time focus monitor (top right):
  * Current focus percentage gauge
  * Focus timeline chart
  * Distraction alerts
- Session controls (bottom):
  * Timer display
  * Pause/Resume buttons
  * End session button
  * Notes area
- Responsive design maintaining usability on different screen sizes

Document Summary Screen:
- Document upload area with drag-and-drop
- Tabbed interface for different views:
  * Original document text
  * Summary (with level selection)
  * Key concepts
  * Generated flashcards
- Side-by-side comparison view
- Download and export buttons
- Processing progress indicator

Analytics Dashboard:
- Date range selector
- Metrics overview cards:
  * Total study hours this week
  * Average focus percentage
  * Number of sessions
  * Productivity score
- Detailed charts:
  * Focus timeline (interactive)
  * Daily study duration trend
  * Distraction frequency heatmap
  * Performance comparison visualizations
- Export options (PDF, CSV)
- Filtering and drill-down capabilities

4.4.2 Color Scheme and Typography

Color Palette:
- Primary: Blue (#2563EB) for main actions and highlights
- Secondary: Green (#10B981) for positive metrics and achievements
- Accent: Purple (#A855F7) for interactive elements
- Neutral: Gray (#6B7280) for secondary information
- Warning: Orange (#F59E0B) for alerts and distraction
- Danger: Red (#EF4444) for critical issues
- Background: White (#FFFFFF) or Light Gray (#F9FAFB)

Typography:
- Primary Font: Inter (system font stack for web) for clean, modern appearance
- Heading Sizes: 32px (H1), 24px (H2), 20px (H3), 16px (H4)
- Body Text: 14px for main content, 12px for secondary info
- Weights: 400 (regular), 600 (semibold), 700 (bold)

4.4.3 Responsive Design Principles

Breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

Responsive Components:
- Sidebar collapses on mobile, remains visible on desktop
- Charts resize and adjust complexity based on screen size
- Forms stack vertically on mobile, horizontally on desktop
- Navigation shifts to hamburger menu on mobile
- Font sizes and spacing scale appropriately

4.5 API DESIGN

4.5.1 RESTful API Endpoints

Authentication Endpoints:
```
POST /api/auth/register
- Payload: { email, password, full_name, study_level }
- Response: { user_id, token, message }

POST /api/auth/login
- Payload: { email, password }
- Response: { user_id, token, expires_in }

POST /api/auth/logout
- Headers: Authorization: Bearer <token>
- Response: { message }

POST /api/auth/refresh-token
- Headers: Authorization: Bearer <refresh_token>
- Response: { token, expires_in }
```

User Endpoints:
```
GET /api/users/profile
- Headers: Authorization: Bearer <token>
- Response: { user_id, email, full_name, study_level, created_at }

PUT /api/users/profile
- Headers: Authorization: Bearer <token>
- Payload: { full_name, study_level, preferences }
- Response: { message, updated_user }

POST /api/users/change-password
- Headers: Authorization: Bearer <token>
- Payload: { current_password, new_password }
- Response: { message }
```

Study Session Endpoints:
```
POST /api/sessions/start
- Headers: Authorization: Bearer <token>
- Payload: { document_id, notes, duration_target }
- Response: { session_id, start_time }

POST /api/sessions/{session_id}/end
- Headers: Authorization: Bearer <token>
- Payload: { end_notes }
- Response: { session_statistics }

GET /api/sessions
- Headers: Authorization: Bearer <token>
- Query: ?limit=20&offset=0&date_from=&date_to=
- Response: { sessions: [], total_count, next_offset }

GET /api/sessions/{session_id}
- Headers: Authorization: Bearer <token>
- Response: { session_details, focus_timeline, statistics }

POST /api/sessions/{session_id}/focus-record
- Headers: Authorization: Bearer <token>
- Payload: { timestamp, focus_level, face_detected, facial_metrics }
- Response: { recorded: true }
```

Document Endpoints:
```
POST /api/documents/upload
- Headers: Authorization: Bearer <token>
- Payload: FormData with file
- Response: { document_id, file_name, upload_time, processing_status }

GET /api/documents
- Headers: Authorization: Bearer <token>
- Query: ?limit=20&offset=0&search=
- Response: { documents: [], total_count }

GET /api/documents/{document_id}
- Headers: Authorization: Bearer <token>
- Response: { document_details, page_count, extract_status }

POST /api/documents/{document_id}/summarize
- Headers: Authorization: Bearer <token>
- Payload: { summary_level }
- Response: { summary_text, key_concepts, generation_time }

DELETE /api/documents/{document_id}
- Headers: Authorization: Bearer <token>
- Response: { message }
```

Analytics Endpoints:
```
GET /api/analytics/daily
- Headers: Authorization: Bearer <token>
- Query: ?date=2026-03-12
- Response: { total_sessions, total_duration, avg_focus, sessions: [] }

GET /api/analytics/weekly
- Headers: Authorization: Bearer <token>
- Query: ?week_start=2026-03-08
- Response: { total_hours, avg_focus_trend, weekly_breakdown }

GET /api/analytics/monthly
- Headers: Authorization: Bearer <token>
- Query: ?year=2026&month=3
- Response: { monthly_summary, trend_data, comparison_with_previous }

GET /api/analytics/insights
- Headers: Authorization: Bearer <token>
- Response: { productivity_score, recommendations, patterns }
```

4.5.2 WebSocket for Real-Time Updates

Real-Time Focus Data Stream:
```
Connection: ws://domain/api/sessions/{session_id}/stream
Headers: ?token=<auth_token>

Server → Client (Focus Update):
{
  "type": "focus_update",
  "session_id": "...",
  "timestamp": "2026-03-12T10:30:45Z",
  "focus_level": 85,
  "face_detected": true,
  "distraction_alerts": []
}

Server → Client (Distraction Alert):
{
  "type": "distraction_alert",
  "session_id": "...",
  "severity": "medium",
  "distraction_type": "gaze_away",
  "duration_ms": 3000,
  "message": "You looked away for 3 seconds"
}

Server → Client (Session Ended):
{
  "type": "session_ended",
  "session_id": "...",
  "statistics": {
    "total_duration": 3600,
    "focus_percentage": 82,
    ...
  }
}
```

4.6 MODULE DESCRIPTION

4.6.1 Focus Tracking Module

Purpose: Real-time monitoring and analysis of student focus during study sessions.

Key Components:
1. Face Detection Engine
   - Implements both cascade classifier and MTCNN approaches
   - Processes video frames at 30 FPS
   - Detects multiple faces with confidence scores
   - Provides facial landmarks (eyes, nose, mouth)

2. Face Analysis Engine
   - Estimates head pose (pitch, yaw, roll)
   - Calculates eye gaze direction using gaze estimation models
   - Analyzes facial expressions (blink rate, yawn detection)
   - Detects eye closure duration

3. Focus Scoring Engine
   - Converts facial metrics into focus score (0-100)
   - Implements temporal smoothing to reduce noise
   - Applies customizable weighting for different distraction types
   - Generates focus timeline and aggregated metrics

4. Real-Time Alert System
   - Monitors for focus drops below configurable threshold
   - Generates user-friendly notifications
   - Tracks distraction patterns and severity
   - Stores all alerts for later analysis

Dependencies:
- OpenCV for face detection
- TensorFlow/PyTorch for head pose and gaze estimation
- NumPy for numerical operations
- WebRTC for browser-camera integration

4.6.2 PDF Summarization Module

Purpose: Intelligent processing and summarization of PDF documents for efficient learning.

Key Components:
1. PDF Processing Engine
   - Extracts text from PDF files with formatting preservation
   - Handles various PDF encodings and corrupted files
   - Determines page count and metadata
   - Manages large files (up to 100 MB)

2. Text Preprocessing Engine
   - Tokenizes text into sentences and words
   - Handles special characters and Unicode
   - Removes boilerplate content (headers, footers)
   - Normalizes text (case, whitespace)

3. Summarization Engine
   - Implements TF-IDF for extractive summarization
   - Uses BERT/BART for abstractive summarization
   - Generates multiple summary levels (10%, 25%, 50%)
   - Preserves context and maintains coherence

4. Concept Extraction Engine
   - Uses Named Entity Recognition for term identification
   - Extracts key concepts and definitions
   - Creates concept relationships
   - Generates concept hierarchy

5. Question Generation Engine
   - Creates practice questions from document content
   - Supports multiple question types
   - Adjusts difficulty based on content complexity
   - Stores questions for selected retrieval

Dependencies:
- PyPDF2/pdfplumber for PDF processing
- NLTK/spaCy for NLP preprocessing
- Hugging Face Transformers for summarization
- scikit-learn for TF-IDF computation

4.6.3 Study Analytics Module

Purpose: Aggregation, analysis, and visualization of study patterns and productivity metrics.

Key Components:
1. Data Aggregation Engine
   - Collects focus records from study sessions
   - Aggregates metrics at session, daily, weekly, monthly levels
   - Handles missing data and anomalies
   - Computes derived metrics

2. Trend Analysis Engine
   - Performs time-series analysis on focus data
   - Detects patterns in distraction times
   - Identifies productivity peaks and troughs
   - Compares performance across periods

3. Recommendations Engine
   - Analyzes productivity patterns
   - Generates personalized recommendations
   - Suggests optimal study times and durations
   - Recommends focus improvement strategies

4. Report Generation Engine
   - Creates comprehensive session reports
   - Generates weekly and monthly summaries
   - Exports data in CSV and PDF formats
   - Provides visualizations and charts

Dependencies:
- Pandas for data manipulation
- NumPy for numerical computations
- Matplotlib/Plotly for visualizations
- SQLAlchemy for database queries

4.6.4 User Authentication and Session Management Module

Purpose: Secure user identification, authorization, and session handling.

Key Components:
1. Authentication Engine
   - Handles user registration and login
   - Implements secure password hashing (bcrypt)
   - Supports password reset functionality
   - Email verification for new accounts

2. Token Management
   - JWT (JSON Web Token) generation and validation
   - Access token and refresh token management
   - Token expiration and renewal
   - Logout and token revocation

3. Session Management
   - Tracks user active sessions
   - Manages concurrent session limits
   - Detects and prevents unauthorized access
   - Logs authentication events for security audit

4. Authorization System
   - Role-based access control (RBAC)
   - Resource-level permissions
   - Feature access control based on subscription tier
   - Administrative override capabilities

Dependencies:
- PyJWT for token management
- bcrypt for password hashing
- Flask-Login for session handling
- Cryptography for encryption

This comprehensive system design establishes the technical foundation for EduFocus implementation, ensuring scalability, maintainability, and optimal user experience.
"""

chapter5_content = """
5.1 PROGRAMMING LANGUAGES AND FRAMEWORKS

5.1.1 Backend Development Stack

Python 3.8+ :
Chosen for its versatility, extensive libraries, and strong support for AI/ML development. Python's readability facilitates maintenance and team collaboration.

Key Libraries:
- NumPy: Numerical computing and array operations
- Pandas: Data manipulation and analysis
- scikit-learn: Machine learning algorithms
- TensorFlow/PyTorch: Deep learning frameworks
- OpenCV: Computer vision and face detection
- NLTK/spaCy: Natural language processing
- PyPDF2/pdfplumber: PDF processing

Flask Framework:
Lightweight, flexible web framework ideal for building custom RESTful APIs without unnecessary overhead. Flask's minimal boilerplate enables rapid development while maintaining complete control over architecture.

Key Flask Extensions:
- Flask-SQLAlchemy: Database ORM integration
- Flask-JWT-Extended: JWT authentication
- Flask-CORS: Cross-origin resource sharing
- Flask-RESTful: RESTful API building
- Celery: Asynchronous task queue
- Flask-Limiter: Rate limiting for API protection

Database:
SQLAlchemy ORM for database abstraction, allowing easy migration between SQLite (development) and MySQL (production). SQLAlchemy's features include:
- Automatic schema generation from models
- Transaction management
- Connection pooling
- Query optimization

5.1.2 Frontend Development Stack

HTML5:
Semantic markup ensuring accessibility and SEO optimization. Features used:
- Form elements with validation attributes
- Canvas for real-time visualization
- Video element for webcam integration
- Local Storage for client-side data persistence

CSS3 with Bootstrap Framework:
Responsive design framework providing:
- Mobile-first design approach
- Grid system for layouts
- Pre-built component library
- Accessibility features
- SASS variable support for theming

Custom CSS Features:
- CSS Grid for complex layouts
- Flexbox for flexible component arrangement
- CSS Animations for smooth transitions
- CSS Variables for consistent theming
- Media queries for responsive design

JavaScript (ES6+):
Modern JavaScript implementing:
- Async/await for asynchronous operations
- Arrow functions for concise syntax
- Destructuring for clean data handling
- Modules for code organization
- Classes for object-oriented patterns

Key JavaScript Libraries:
- Chart.js: Data visualization
- Fetch API: HTTP requests (native, no jQuery dependency)
- WebRTC API: Browser-based webcam access
- Service Workers: Offline functionality (future)

5.1.3 AI/ML Components

Face Detection Framework:
OpenCV with pre-trained models:
- Haar Cascade Classifier for fast, real-time detection
- MTCNN (Multi-task Cascaded Convolutional Networks) for high accuracy
- ResNet-based detectors for robustness
- Model selection based on speed vs. accuracy requirements

Head Pose Estimation:
- 3D CNN models trained on face annotation datasets
- Real-time estimation from 2D images
- 6-DOF (Degree of Freedom) rotation prediction

Eye Gaze Estimation:
- CNN-based approaches trained on eye appearance and face pose
- Calibration-free methods for unsupervised adaptation
- Temporal smoothing for reduced noise

Focus Classification:
Binary classifier determining focus/non-focus:
- Gradient Boosting (XGBoost, LightGBM) for fast inference
- Input features: head pose, gaze direction, temporal patterns
- Threshold-based decision with confidence scores

Natural Language Processing:
Text Summarization:
- Extractive: TF-IDF scoring for sentence selection
- Abstractive: Sequence-to-sequence models (BART, T5)
- Transformer-based models (BERT for encoding, GPT for generation)

Named Entity Recognition:
- spaCy pre-trained models for term identification
- Fine-tuned models for domain-specific entities
- Concept linking and relationship extraction

5.2 ALGORITHMIC APPROACH

5.2.1 Face Detection Algorithm (Detailed)

Cascade Classifier Approach:
```
Input: Video frame at 30 Hz
Output: Face bounding box with confidence score

Algorithm:
1. Convert BGR image to grayscale
   grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

2. Apply histogram equalization for robustness
   equalized = cv2.equalizeHist(grayscale)

3. Load pre-trained Haar Cascade
   cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

4. Multi-scale face detection
   faces = cascade.detectMultiScale(
       equalized,
       scaleFactor=1.3,    // Scale window by 30% per iteration
       minNeighbors=5,     // Require 5+ overlapping detections
       flags=cv2.CASCADE_SCALE_IMAGE,
       minSize=(30, 30),   // Minimum face size
       maxSize=(500, 500)  // Maximum face size
   )

5. Non-Maximum Suppression (remove duplicates)
   for each pair of faces:
       if (overlap > 0.3):
           keep face with higher confidence

6. For each detected face:
       extract region of interest (ROI)
       calculate confidence score based on detector response
       return bounding box (x, y, w, h) and confidence

Output: List of face bounding boxes
```

Complexity:
- Time: O(n*m) where n=image width, m=image height
- Space: O(1) for in-place processing
- Real-time performance: 25-30 FPS on CPU

5.2.2 Focus Score Calculation Algorithm

```
Input: Sequence of facial features for time window (e.g., 30 frames = 1 second)
Output: Focus score (0-100)

Algorithm:
1. Initialize focus_score = 100

2. For each frame in window:
   a. Get head pose (pitch, yaw, roll) from face detection
   
   b. Head posture check:
      if |yaw| > 30° or |pitch| > 30° or |roll| > 20°:
          focus_score -= 5  // Moderate deviation penalty
      if |yaw| > 45° or |pitch| > 45°:
          focus_score -= 10  // Severe deviation penalty
   
   c. Eye gaze check:
      gaze_angle = angle between gaze vector and forward direction
      if gaze_angle > 25°:
          focus_score -= 3  // Off-gaze penalty
      if gaze_angle > 40°:
          focus_score -= 7  // Severe off-gaze penalty
   
   d. Eye blink detection:
      eye_aspect_ratio = (||p2-p6|| + ||p3-p5||) / (2*||p1-p4||)
      if eye_aspect_ratio < 0.2:  // Eyes closed
          consecutive_closed_frames++
      else:
          consecutive_closed_frames = 0
      
      if consecutive_closed_frames > 10:  // ~300ms
          focus_score -= 8
      if consecutive_closed_frames > 20:  // ~600ms (yawn or sleep)
          focus_score -= 15
   
   e. Reduce frame contribution if confidence is low
      if face_detection_confidence < 0.7:
          focus_score -= 5

3. Temporal smoothing:
   smoothed_score = 0.8 * previous_score + 0.2 * current_frame_score
   // Reduces noise and short-term fluctuations

4. Lower bound enforcement:
   focus_score = max(0, focus_score)

5. Return smoothed_score

Session Aggregation:
   session_focus_percentage = sum(frame_scores) / number_of_frames * 100
```

5.2.3 PDF Summarization Algorithm

Extractive Summarization:
```
Input: PDF document text
Output: Summary at requested level (10%, 25%, 50%)

Algorithm:
1. Preprocess text:
   sentences = tokenize_into_sentences(text)
   tokens = [tokenize_and_lowercase(s) for s in sentences]
   
2. Calculate TF-IDF scores:
   for each term in corpus:
       TF[term] = count(term in doc) / total_terms_in_doc
       IDF[term] = log(total_docs / docs_containing_term)
       TF-IDF[term] = TF[term] * IDF[term]
   
3. Calculate sentence scores:
   for each sentence:
       sentence_score = sum(TF-IDF[term] for term in sentence)
       normalize by sentence length
   
4. Select top sentences:
   summary_length = total_sentences * requested_percentage
   top_sentences = sort(sentences by score) and select top N
   
5. Reorder sentences to maintain original order:
   final_summary = [s for s in sentences if s in top_sentences]
   
6. Return final_summary as text
```

Abstractive Summarization:
```
Input: PDF document text
Output: Abstractive summary

Algorithm:
1. Preprocess: Split into sentences, tokenize

2. Use pre-trained BART model:
   from transformers import BartForConditionalGeneration, BartTokenizer
   
   tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
   model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

3. Encode input:
   inputs = tokenizer(text, return_tensors='pt', max_length=1024, truncation=True)

4. Generate summary:
   summary_ids = model.generate(
       inputs['input_ids'],
       max_length=150,
       min_length=50,
       length_penalty=2.0,
       num_beams=4,
       early_stopping=True
   )

5. Decode output:
   summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

6. Return summary
```

5.2.4 Distraction Detection Algorithm

```
Input: Sequence of focus scores over time window
Output: Distraction events with timestamp and severity

Algorithm:
1. Define distraction threshold: distraction_level = 40 (focus drops below this)

2. For each time window (e.g., 5-second window):
   a. Calculate average focus in window: avg_focus = mean(focus_scores)
   
   b. Check if distraction:
      if avg_focus < distraction_level:
          identify_distraction_event()
          
   c. Detect distraction type:
      dominant_feature = identify_primary_distraction_cause()
      // Looking away, eye closure, head movement, etc.
      
   d. Calculate severity:
      severity = (40 - avg_focus) / 40  // Normalized 0-1
      
   e. Get duration:
      duration = length_of_low_focus_period
   
   f. Create distraction record:
      event = {
          timestamp: window_start_time,
          duration: duration,
          severity: severity,  // 0=low, 0.33=medium, 0.66=high, 1=critical
          type: dominant_feature,
          focus_level: avg_focus
      }

3. Pattern detection:
   for each event:
       check if similar event occurred recently
       if pattern_detected:
           event.pattern = recurring_distraction
           event.recommendation = suggest_intervention()

4. Aggregate distraction metrics:
   total_distraction_events = count(all events)
   total_distraction_duration = sum(event.duration for all events)
   distraction_frequency = total_events / session_duration
   average_severity = mean(event.severity for all events)

5. Return distraction_events with analytics
```

5.3 IMPLEMENTATION APPROACH

5.3.1 Project Structure

```
edufocus/
├── config.py              # Configuration management
├── app.py                 # Flask application factory
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
│
├── app/
│   ├── __init__.py       # Package initialization
│   ├── models/           # Database models
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── focus_record.py
│   │   ├── document.py
│   │   └── analytics.py
│   │
│   ├── routes/           # API route handlers
│   │   ├── auth.py       # Authentication routes
│   │   ├── sessions.py   # Study session routes
│   │   ├── documents.py  # Document routes
│   │   ├── analytics.py  # Analytics routes
│   │   └── users.py      # User profile routes
│   │
│   ├── services/         # Business logic layer
│   │   ├── face_detector.py
│   │   ├── focus_analyzer.py
│   │   ├── pdf_processor.py
│   │   ├── summarizer.py
│   │   ├── analytics_engine.py
│   │   └── auth_service.py
│   │
│   ├── ml_models/        # Pre-trained models
│   │   ├── face_detection.py
│   │   ├── head_pose_estimator.py
│   │   ├── gaze_estimator.py
│   │   └── summarization_models.py
│   │
│   ├── utils/            # Utility functions
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   ├── helpers.py
│   │   └── exceptions.py
│   │
│   └── templates/        # HTML templates
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── study.html
│       ├── documents.html
│       └── analytics.html
│
├── static/
│   ├── css/
│   │   ├── main.css
│   │   ├── dashboard.css
│   │   └── responsive.css
│   │
│   ├── js/
│   │   ├── api.js        # API client wrapper
│   │   ├── focus-tracker.js
│   │   ├── dashboard.js
│   │   ├── utils.js
│   │   └── main.js
│   │
│   └── images/
│       └── assets/
│
├── migrations/           # Database migrations
├── tests/               # Unit and integration tests
│   ├── test_models.py
│   ├── test_routes.py
│   ├── test_services.py
│   └── test_utils.py
│
├── scripts/             # Utility scripts
│   ├── seed_database.py
│   ├── train_models.py
│   └── backup_data.py
│
└── documentation/       # Project documentation
    ├── API_DOCS.md
    ├── SETUP.md
    └── USAGE.md
```

5.3.2 Key Functionality Implementation

User Authentication Implementation:
```python
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(email, password, full_name, study_level):
        # Hash password securely
        password_hash = generate_password_hash(password)
        
        # Create user object
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            study_level=study_level
        )
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        return {'user_id': user.id, 'message': 'User registered successfully'}
    
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return None
        
        # Generate JWT token
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        
        return {'access_token': access_token, 'user_id': str(user.id)}
```

Real-Time Focus Tracking Implementation:
```python
import cv2
import numpy as np
from tensorflow.keras.models import load_model

class FocusTracker:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        )
        self.gaze_estimator = load_model('models/gaze_estimator.h5')
        self.focus_history = []
    
    def analyze_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            equalized, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30)
        )
        
        if len(faces) == 0:
            return {'focus_score': 0, 'face_detected': False}
        
        # Get primary face (largest)
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        roi = frame[y:y+h, x:x+w]
        
        # Extract facial features
        focus_score = self._calculate_focus_score(roi)
        
        # Smooth with history
        self.focus_history.append(focus_score)
        if len(self.focus_history) > 30:
            self.focus_history.pop(0)
        
        smoothed_score = 0.8 * self.focus_history[-1] + 0.2 * np.mean(self.focus_history)
        
        return {
            'focus_score': int(smoothed_score),
            'face_detected': True,
            'face_bbox': (x, y, w, h)
        }
    
    def _calculate_focus_score(self, face_roi):
        # Analyze gaze and head pose
        score = 100
        
        # Implement gaze prediction, head pose estimation, etc.
        # Deduct points based on distraction indicators
        
        return max(0, min(100, score))
```

PDF Summarization Implementation:
```python
from PyPDF2 import PdfReader
import nltk
from transformers import BartForConditionalGeneration, BartTokenizer

class DocumentProcessor:
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        self.model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    
    def extract_text(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    def summarize(self, text, level=0.25):
        # level: 0.1 = 10% summary, 0.25 = 25%, 0.5 = 50%
        sentences = nltk.sent_tokenize(text)
        
        # Extractive summarization
        summary_length = int(len(sentences) * level)
        
        # Calculate TF-IDF scores
        tfidf_scores = self._calculate_tfidf(sentences)
        
        # Select top sentences maintaining order
        top_indices = sorted(
            np.argsort(-tfidf_scores)[:summary_length]
        )
        extractive_summary = ' '.join([sentences[i] for i in top_indices])
        
        # Abstractive summarization
        inputs = self.tokenizer(
            text, return_tensors='pt', max_length=1024, truncation=True
        )
        summary_ids = self.model.generate(
            inputs['input_ids'],
            max_length=150,
            min_length=50,
            length_penalty=2.0,
            num_beams=4
        )
        abstractive_summary = self.tokenizer.decode(
            summary_ids[0], skip_special_tokens=True
        )
        
        return {
            'extractive': extractive_summary,
            'abstractive': abstractive_summary,
            'key_sentences': [sentences[i] for i in top_indices]
        }
```

This implementation section demonstrates the core technical approach and key modules of the EduFocus system, providing a foundation for complete development.
"""

# Save chapters to variables for later insertion
print("Chapter content prepared. Ready for document assembly.")
print(f"Chapter 4 length: {len(chapter4_content)} characters")
print(f"Chapter 5 length: {len(chapter5_content)} characters")

EOF
