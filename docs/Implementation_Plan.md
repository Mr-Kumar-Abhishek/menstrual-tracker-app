# Implementation Plan
## Menstrual Tracker App

### 1. Methodology
This project will be developed using **Agile methodologies** combined with a **Test-Driven Development (TDD)** approach. 
- **Agile:** Development will be broken down into iterative, 1-2 week Sprints. Each sprint will deliver a working, incremented version of the application.
- **TDD:** Before writing functional code, unit tests will be authored for models, business logic, and view models. Code will be written to pass these tests, followed by refactoring.

### 2. Development Sprints

#### Sprint 1: Project Initialization & Core Models (Data Layer)
- **Goal:** Set up the project environment, CI/CD foundation, and local database management.
- **Tasks:**
  - Initialize Git repository and Python virtual environment (e.g., using `poetry`).
  - Write unit tests for `StorageManager` (DB creation, inserting cycles, fetching logs).
  - Implement SQLite database schema and `StorageManager`.
  - Write unit tests for `PredictionEngine` using mock historical data.
  - Implement `PredictionEngine` logic.

#### Sprint 2: ViewModels and Basic UI Integration
- **Goal:** Connect business logic to intermediary ViewModels and create basic, unstyled UI screens.
- **Tasks:**
  - Write unit tests for ViewModels (DashboardViewModel, CalendarViewModel).
  - Implement ViewModels to interface with `StorageManager` and `PredictionEngine`.
  - Scaffold Kivy app structure (ScreenManager, basic navigation).
  - Integrate Dashboard Screen with real data (no advanced styling yet).

#### Sprint 3: UI/UX Refinement & Calendar Component
- **Goal:** Deliver a polished user experience using KivyMD.
- **Tasks:**
  - Implement Material Design themes and colors.
  - Build custom Calendar UI component for Kivy.
  - Create the detailed Log Entry screen (symptoms, flow, notes).
  - Integrate navigation drawer or bottom navigation.
  - Manual UI testing across different window sizes.

#### Sprint 4: Notifications & Cross-Platform Build Automation
- **Goal:** Implement device-specific features and configure automated CI/CD builds.
- **Tasks:**
  - Integrate `plyer` for local notifications.
  - Set up **GitHub Actions** workflows:
    - **Linting & Testing:** Run `pytest` and `flake8/black` on every push.
    - **Windows Build:** Use PyInstaller to generate `.exe` files.
    - **Linux Build:** Use PyInstaller to generate Linux executables.
    - **Android Build:** Use Buildozer to generate `.apk`/`.aab` files.
  - Perform end-to-end testing on Android emulator/physical device.
  - Final release preparation.

### 3. Continuous Integration / Continuous Deployment (CI/CD) Strategy
GitHub Actions will be utilized to automate the test and build pipelines:
1. **`test.yml`**: Triggers on push and pull request. Runs Python `pytest` suite to ensure no regressions occur.
2. **`build-desktop.yml`**: Triggers on tags or specific branches. Packages the Kivy app for Windows and Linux.
3. **`build-android.yml`**: Triggers on tags. Uses a Linux runner with `buildozer` to compile the Android APK.

### 4. Testing Strategy
- **Unit Tests (`pytest`):** Core logic (predictions, math), Database queries, and ViewModel state management.
- **Integration Tests:** Verifying interaction between ViewModels and the SQLite database.
- **UI Tests / Manual QA:** Ensure Kivy widgets render correctly and handle touch/click events as expected on desktop and Android.
