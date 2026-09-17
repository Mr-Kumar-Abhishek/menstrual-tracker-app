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
    - **Linux Build:** Use PyInstaller to generate Linux executables, `.deb`, `.rpm`, and `.AppImage` packages.
    - **Android Build:** Use Buildozer to generate `.aab` release bundles.
  - Perform end-to-end testing on Android emulator/physical device.
  - Final release preparation.

#### Sprint 5: Security, Resilience & Play Store Compliance Upgrade
- **Goal:** Upgrade target Android API level, establish Play Store versioning standards, enhance encryption, and harden local storage resilience.
- **Tasks:**
  - **Android Target API Upgrade:** Updated target SDK to **API Level 36** (`android.api = 36`) in `buildozer.spec` to ensure compatibility with modern Android runtime requirements.
  - **16 KB Memory Page Size Support:** Configured linker flags (`-Wl,-z,max-page-size=16384`) in `buildozer.spec` (`p4a.extra_args`) and CI/CD (`LDFLAGS`) to ensure native `.so` binaries align with Android 15/16 16 KB page size standards.
  - **Play Store Version Code Management:** Configured baseline numeric version code to **401** in `buildozer.spec` and automated CI/CD version code incrementing as `400 + ${{ github.run_number }}` in `build-and-release.yml`.
  - **Data Security:** Implemented transparent field-level AES-128 Fernet encryption (`crypto_manager.py`) for sensitive logs stored locally in SQLite.
  - **Storage Resilience:** Added a shared in-memory database fallback (`file:memdb1?mode=memory&cache=shared`) to handle read-only filesystems without app freezes.
  - **CI/CD Pipeline Refinement:** Consolidated release workflows into `build-and-release.yml` with automated semver tag creation, release notes, and multi-platform binary signing.

### 3. Continuous Integration / Continuous Deployment (CI/CD) Strategy
GitHub Actions is utilized to automate test and release pipelines:
1. **`test.yml`**: Triggers on push and pull requests. Runs Python `pytest` suite and `flake8` linting.
2. **`build-and-release.yml`**: Triggers on pushes to `main`/`master`. Packages and releases binaries for Windows (`.exe`), Linux (`.deb`, `.rpm`, `.AppImage`), Android (`.aab` signed), and iOS (`.xcarchive`). Increments version tag and sets `android.numeric_version` > 400 dynamically.

### 4. Testing Strategy
- **Unit Tests (`pytest`):** Core logic (predictions, math), Database queries, and ViewModel state management.
- **Integration Tests:** Verifying interaction between ViewModels and the SQLite database.
- **UI Tests / Manual QA:** Ensure Kivy widgets render correctly and handle touch/click events as expected on desktop and Android.
