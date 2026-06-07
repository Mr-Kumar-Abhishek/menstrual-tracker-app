# Software Design Document (SDD)
## Menstrual Tracker App

### 1. Architectural Design
The application will follow a **Model-View-ViewModel (MVVM)** architecture to ensure a clean separation of concerns, making the UI decoupled from the business logic and facilitating cross-platform development and testing.

- **Model:** Represents the data layer and business logic (Database, Prediction Engine).
- **View:** The Kivy `.kv` files and Python UI classes responsible for rendering the interface.
- **ViewModel:** Acts as an intermediary, handling user input from the View, interacting with the Model, and exposing data for the View to display.

### 2. Technology Stack
- **Language:** Python 3.10+
- **UI Framework:** Kivy & KivyMD (for Material Design components).
- **Local Storage:** SQLite3 (via built-in Python module or SQLAlchemy/Peewee ORM).
- **Platform Features (Notifications):** Plyer (Python library for accessing hardware features/APIs across platforms).
- **Build Tools:** PyInstaller (Windows/Linux), Buildozer (Android).

### 3. Database Schema
A local SQLite database will be used with the following core tables:

**Table: `cycles`**
- `cycle_id` (Integer, Primary Key)
- `start_date` (Date)
- `end_date` (Date, Nullable)
- `cycle_length` (Integer, Calculated)

**Table: `daily_logs`**
- `log_id` (Integer, Primary Key)
- `date` (Date)
- `flow_intensity` (String/Enum: Light, Medium, Heavy)
- `symptoms` (String/JSON: Array of symptom tags)
- `mood` (String)
- `notes` (Text)

### 4. Core Components
#### 4.1 Storage Manager
Handles all CRUD (Create, Read, Update, Delete) operations with the SQLite database. Ensures data integrity and provides backup/restore functionality.

#### 4.2 Prediction Engine
An algorithmic module that calculates the user's average cycle length and luteal phase from historical data (e.g., a rolling average of the last 6 cycles) to forecast future period dates and ovulation windows.

#### 4.3 Notification Service
A background or scheduled task manager using `plyer` to schedule local reminders for upcoming periods (e.g., "Your period is predicted to start in 2 days").

### 5. User Interface (View) Structure
- **Dashboard Screen:** Shows current cycle day, prediction for the next period, and a quick "Log Today" button.
- **Calendar Screen:** A full-month calendar view with color-coded days (e.g., red for period, blue for ovulation, dots for logged symptoms).
- **Log Entry Screen:** A form for users to input flow, symptoms, and notes for a specific date.
- **Settings & Data Screen:** Options for notifications, exporting data, and modifying average cycle baselines.
