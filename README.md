# MenstrualTracker

A privacy-focused, cross-platform menstrual cycle tracking application built with Python, Kivy, and KivyMD.

MenstrualTracker prioritizes your data privacy by keeping all your personal health data locally on your device using SQLite. No cloud sync, no tracking, no data selling.

## 🌟 Features

- **Privacy First**: All data is stored locally via a SQLite database. 
- **Cross-Platform**: Seamlessly runs on Android, Windows, and Linux.
- **Dashboard**: Quick overview of your current cycle status and predictions.
- **Calendar View**: Visual timeline of past periods and predicted future dates.
- **Logging**: Easy-to-use interface for logging flow intensity, symptoms, and moods.
- **Reminders**: Local push notifications for upcoming period predictions.

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

- **Models**: SQLite-backed models (`Cycle`, `LogEntry`) utilizing `sqlite3`.
- **ViewModels**: Handles business logic, cycle predictions, and state management.
- **Views**: KivyMD-based UI components (`DashboardView`, `CalendarView`, `LogEntryView`).
- **Notifications**: Cross-platform system notifications via `plyer`.
- **Project Estimation**: See the [COCOMO Calculation Report](COCOMO_Report.md) for effort and cost estimations.

## 📜 License

This project is dual-licensed:
- The **source code** is licensed under the **MIT License**. Please see the `LICENSE` file for more details.
- The **documentation and assets** are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Please see the `LICENSE-DOCS` file for more details.
