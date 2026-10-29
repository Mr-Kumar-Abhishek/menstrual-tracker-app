# Software Requirements Specification (SRS)
## Anonymous Menstrual Tracker App

### 1. Product Vision & Overview
**Anonymous Menstrual Tracker** is a private, offline, and secure menstrual cycle and period tracking application designed to give you complete ownership of your personal health data.

No account registration, no cloud uploads, no third-party analytics, and no intrusive ads. Everything stays strictly on your device.

---

### 2. Core Architectural Principles

- **True Privacy by Design**: Zero network egress. The application does not require internet access, possesses no telemetry or third-party trackers, and requires no account or authentication credentials.
- **On-Device Cryptographic Security**: Sensitive user health observations (flow intensity, symptoms, mood, notes) are stored encrypted at rest using authenticated AES-256-GCM.
- **Data Sovereignty**: The user maintains total custody of their data with export and deletion capabilities in standard JSON format.
- **Deterministic & Safe Predictions**: Menstrual cycle modeling relies on historical cycle lengths with defensive bounding to avoid pathological calculation overflows or infinite loops.

---

### 3. Key Features & Functional Requirements

#### 3.1 🔒 True Privacy by Design
- **FR-PRIV-1 (100% Offline Operation)**: The system shall function entirely without internet connectivity. No remote server requests, APIs, or cloud synchronization mechanisms shall be present in the application.
- **FR-PRIV-2 (Zero Telemetry & Ad-Free)**: The system shall contain no analytics libraries, crash reporting beacons, tracking SDKs, or advertising networks.
- **FR-PRIV-3 (No Account Required)**: The system shall immediately launch to the main functional dashboard without requiring user registration, email, phone number, login, or social authentication.
- **FR-PRIV-4 (Military-Grade Encryption at Rest)**: Sensitive daily observations (flow intensity, symptoms, mood, personal notes) must be transparently encrypted before persistence to the SQLite database using authenticated AES-256-GCM with PBKDF2/cryptographic key storage.

#### 3.2 🌸 Intelligent Cycle & Period Predictions
- **FR-PRED-1 (Historical Cycle Tracking)**: The system shall compute cycle lengths from recorded cycle start dates and order historical cycles chronologically.
- **FR-PRED-2 (Period Start Prediction)**: The system shall predict future period start dates based on weighted historical averages, clamped between 21 and 45 days for biological plausibility.
- **FR-PRED-3 (Period Duration & End Date Prediction)**: The system shall calculate estimated period duration (clamped between 1 and 10 days) and projected end dates.
- **FR-PRED-4 (Fertility & Ovulation Window Calculation)**: The system shall compute the estimated ovulation date (14 days prior to predicted cycle start) and project a 5-day fertile window (ovulation date - 4 days through ovulation date).
- **FR-PRED-5 (Dashboard Overview)**: The system shall display a Dashboard showing the current cycle day (e.g., "Day 14"), days remaining until the next cycle, and clear milestone summaries.

#### 3.3 📝 Comprehensive Daily Health Logging
- **FR-LOG-1 (Flow Intensity Tracking)**: Users shall be able to record flow intensity using standardized categories (`Light`, `Medium`, `Heavy`, `None`).
- **FR-LOG-2 (Mood & Energy Tracking)**: Users shall be able to log daily emotional states and moods (`Happy`, `Neutral`, `Sad`, `Irritable`, `Anxious`).
- **FR-LOG-3 (Physical Symptom Recording)**: Users shall be able to log physical symptoms (`Cramps`, `Headache`, `Bloating`, `Fatigue`, `Backache`, `Nausea`, `None`).
- **FR-LOG-4 (Private Encrypted Notes)**: Users shall be able to record free-form personal notes for any date, stored strictly encrypted under AES-256-GCM.
- **FR-LOG-5 (Cycle Boundary Controls)**: Users shall be able to record the direct start and end of a cycle directly from the logging screen.

#### 3.4 📅 Interactive Visual Calendar
- **FR-CAL-1 (Monthly Calendar View)**: The system shall render a monthly grid calendar with month/year navigation controls (`<` and `>`).
- **FR-CAL-2 (Visual Status Highlighting)**: The calendar grid shall visually distinguish:
  - Past confirmed periods (Red / Coral badge).
  - Predicted future periods (Pink badge).
  - Estimated fertile & ovulation window (Purple / Blue badge).
  - Days with logged symptoms or notes (Green badge / indicator).
- **FR-CAL-3 (Date Selection & Detail View)**: Users shall be able to select any calendar date to view or edit logged symptoms for that day.

#### 3.5 🔔 Local Smart Notifications
- **FR-NOTIF-1 (On-Device Reminder Triggering)**: The system shall generate local system notifications for upcoming periods (2 days before predicted start and day of period start).
- **FR-NOTIF-2 (Zero Background Battery Drain)**: Notification evaluations shall execute strictly via lightweight local checks without background battery-draining polling daemons.
- **FR-NOTIF-3 (Notification Configuration)**: Users shall be able to toggle reminders on or off at any time in the Settings view.

#### 3.6 💾 Data Ownership & Backup
- **FR-DATA-1 (Standard JSON Export)**: The system shall export complete cycle histories, decrypted daily logs, and configuration preferences into an unencrypted, human-readable JSON file.
- **FR-DATA-2 (Data Deletion & Reset)**: Users shall have full authority to reset or clear application records.

---

### 4. Non-Functional Requirements (NFR)

- **NFR-SEC-1 (Cryptographic Rigor)**: Storage encryption must use authenticated AES-256 in Galois/Counter Mode (GCM). Any tampering with stored ciphertexts must fail gracefully without unhandled exceptions or data corruption.
- **NFR-REL-1 (Filesystem & Storage Resilience)**: If the SQLite database file cannot be accessed or is corrupted, the application must automatically fall back to an in-memory SQLite instance to prevent startup crashes.
- **NFR-PERF-1 (Responsiveness & Launch Time)**: App startup shall occur within 3 seconds on modern mobile and desktop environments. Prediction and calendar rendering calculations shall take less than 200 ms.
- **NFR-UI-1 (Material Design & Touch Ergonomics)**: The user interface must adhere to Material Design principles with flat elevation (0 elevation / 0 shadow) to prevent GPU GLSL overscroll artifacts and respect mobile navigation insets.
- **NFR-PORT-1 (Multi-Platform Parity)**: The core application logic and UI shall execute uniformly across Android (API Level 24 through 36, arm64-v8a), Windows (x64), and Linux (x86_64).
