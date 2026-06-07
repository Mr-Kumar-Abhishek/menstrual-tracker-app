# Software Requirements Specification (SRS)
## Menstrual Tracker App

### 1. Introduction
**1.1 Purpose**
The purpose of this document is to specify the software requirements for the Menstrual Tracker App. It provides a comprehensive overview of the application's functionality, target audience, and system constraints.

**1.2 Scope**
The Menstrual Tracker App is a cross-platform application designed to help users log and predict their menstrual cycles, track daily symptoms, and monitor their overall reproductive health. The application will be built using Python and the Kivy framework, supporting Windows, Linux, and Android operating systems.

### 2. Overall Description
**2.1 User Needs**
Users need a reliable, privacy-focused, and easy-to-use tool to track their menstrual cycles, anticipate future periods, and record health symptoms to share with medical professionals if necessary.

**2.2 Operating Environment**
- **Desktop:** Windows 10/11, Linux (Ubuntu/Debian-based).
- **Mobile:** Android 8.0 and above.
- **Framework:** Python 3.10+, Kivy.

### 3. Functional Requirements
- **FR1: Cycle Logging:** Users must be able to log the start and end dates of their periods.
- **FR2: Symptom Tracking:** Users must be able to log daily symptoms (e.g., flow intensity, cramps, headache, mood) and add personal notes.
- **FR3: Cycle Prediction:** The system must predict the next period start date, estimated end date, and ovulation window based on historical data.
- **FR4: Calendar View:** The system must provide a calendar interface highlighting past periods, predicted future periods, and logged symptoms.
- **FR5: Data Export/Backup:** Users must be able to export their data to a standard format (e.g., CSV or JSON) for backup or medical consultation.
- **FR6: Notifications:** The system should optionally provide local notifications (reminders) for upcoming periods.

### 4. Non-Functional Requirements
- **NFR1: Privacy & Security:** All user data must be stored locally on the device. No cloud synchronization without explicit user opt-in (if implemented in future versions).
- **NFR2: Performance:** The app must launch within 3 seconds and provide smooth scrolling and immediate UI responsiveness.
- **NFR3: Portability:** The app must utilize the same core Python/Kivy codebase for Windows, Linux, and Android.
- **NFR4: Usability:** The user interface must be intuitive, modern, and accessible, requiring no tutorials for basic operations.
