# MenstrualTracker

A privacy-focused, cross-platform menstrual cycle tracking application built with Python, Kivy, and KivyMD.

MenstrualTracker prioritizes privacy by keeping app entries locally on your device using SQLite, with no app-side cloud sync or marketing collection. Google Play, Android, and other platform providers have separate privacy practices; see the [privacy policy](index.html#privacy).

## 🌟 Features

- **Privacy First**: Data is stored locally via SQLite. Daily-log fields (symptoms, mood, flow intensity, and notes) are encrypted at rest using AES-256-GCM; cycle dates and settings are not encrypted by the app. Includes a fallback to an in-memory database on read-only filesystems.
- **Cross-Platform**: Seamlessly runs on Android, Windows, and Linux.
- **Dashboard**: Quick overview of your current cycle status and predictions.
- **Calendar View**: Visual timeline of past periods and predicted future dates.
- **Logging**: Easy-to-use interface for logging flow intensity, symptoms, and moods.
- **Reminders**: Local push notifications for upcoming period predictions.

## 🔒 Privacy Policy

Read the [MenstrualTracker privacy policy](index.html#privacy) for details about
on-device data, encryption, platform-provider data, GDPR and California
privacy and child-protection considerations. The app does not collect health
entries for marketing or integrate an in-app advertising or analytics service.
Google Play, Android, and other platform providers may process information
independently under their own policies.

## 🚀 Downloads

You can download the compiled binaries for Windows, Linux, and Android from the [GitHub Releases](../../releases).
- `MenstrualTracker.exe` for Windows
- `MenstrualTracker` (executable) for Linux
- `MenstrualTracker.apk` for Android

## 🛠️ Development & Building from Source

This project uses [Poetry](https://python-poetry.org/) for dependency management and GitHub Actions for CI/CD automation.

### Prerequisites
- Python 3.10+
- Poetry

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Mr-Kumar-Abhishek/menstrual-tracker-app.git
   cd menstrual-tracker-app
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the app:
   ```bash
   poetry run python main.py
   ```

### Building Binaries Locally

**Windows / Linux (PyInstaller)**:
```bash
poetry run pip install pyinstaller
poetry run pyinstaller --name "MenstrualTracker" --windowed --onefile main.py
```

**Android (Buildozer)**:
```bash
pip install --user --upgrade buildozer cython virtualenv
buildozer android debug
```
*(Note: Android builds require NDK 25b and specific Linux dependencies like `libtool-bin`, `automake`, etc. Check `.github/workflows/build-android.yml` for the full dependency list).*

## 🏗️ Architecture

- **Models**: SQLite-backed models (`Cycle`, `LogEntry`) utilizing `sqlite3` with dynamic path resolution (Kivy `user_data_dir`) and resilient in-memory fallbacks.
- **ViewModels**: Handles business logic, cycle predictions, and state management.
- **Views**: KivyMD-based UI components (`DashboardView`, `CalendarView`, `LogEntryView`).
- **Notifications**: Cross-platform system notifications via `plyer`.
- **Project Estimation**: See the [COCOMO Cost Estimation Report](COCOMO_Report.md) for detailed effort and USA-adjusted cost estimations.

## 📊 Project Estimation (COCOMO)

Based on the actual size of the codebase (~1.91 KLOC), the MenstrualTracker App most closely aligns with the **Organic** COCOMO model.

- **Estimated Effort:** 4.77 Person-Months
- **Development Time:** 4.53 Months
- **Required Staffing:** 1 Developer
- **Estimated Cost:** $47,700 USD (~₹39.8 Lakhs)

See the full [COCOMO Cost Estimation Report](COCOMO_Report.md) for detailed calculations across different development models.

## 📜 License

This project is dual-licensed:
- The **source code** is licensed under the **MIT License**. Please see the `LICENSE` file for more details.
- The **documentation and assets** are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Please see the `LICENSE-DOCS` file for more details.
