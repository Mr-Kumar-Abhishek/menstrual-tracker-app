# Menstrual Tracker App: SRS Compliance Report

This report evaluates the current codebase against the Software Requirements Specification (SRS) defined in `docs/SRS.md`. 

Overall, the project is highly compliant with the specified requirements. Below is a detailed breakdown.

## Functional Requirements (FR)

| Requirement | Status | Implementation Details |
| :--- | :---: | :--- |
| **FR1: Cycle Logging** | ✅ Compliant | Supported in `storage_manager.py` via the `add_cycle` and `update_cycle_end_date` methods. Data is stored in the `cycles` SQLite table. |
| **FR2: Symptom Tracking** | ✅ Compliant | Supported in `storage_manager.py` via `add_daily_log`. Fields include `flow_intensity`, `symptoms`, `mood`, and `notes`. |
| **FR3: Cycle Prediction** | ✅ Compliant | Implemented in `prediction_engine.py`. It accurately calculates averages to predict the next period start, estimated end date, and ovulation window. |
| **FR4: Calendar View** | ✅ Compliant | Implemented using KivyMD in `calendar_view.py`. It correctly populates a grid calendar, color-coding past periods (Red), predicted periods (Light Pink), predicted ovulation (Light Blue), and logged symptoms (Green Outline). |
| **FR5: Data Export/Backup** | ✅ Compliant | Included in `storage_manager.py` with the `export_data` function, exporting cycle and symptom data seamlessly to a standard JSON format. |
| **FR6: Notifications** | ✅ Compliant | Handled via `notification_manager.py` using `plyer.notification`, sending local reminders (e.g., "Upcoming Period", "Period Starts Today"). |

## Non-Functional Requirements (NFR)

| Requirement | Status | Implementation Details |
| :--- | :---: | :--- |
| **NFR1: Privacy & Security** | ✅ Compliant | All data is stored locally in an SQLite database. Furthermore, sensitive health data (symptoms, mood, notes) is encrypted using AES-256 (via `crypto_manager.py`). No cloud syncing is present. |
| **NFR2: Performance** | ⚠️ Needs Manual Testing | The UI is built responsively with `Clock.schedule_once` used efficiently in views to avoid locking the main thread. Specific 3-second launch times should be tested on target hardware. |
| **NFR3: Portability** | ✅ Compliant | Built with Python 3 and Kivy/KivyMD, fulfilling cross-platform (Windows, Linux, Android) needs with a single codebase. Build logs in the root directory indicate active Android/iOS testing. |
| **NFR4: Usability** | ✅ Compliant | Leverages Material Design (`KivyMD`) for an intuitive UI, minimizing the learning curve for users without the need for extensive tutorials. |

> [!TIP]
> While NFR2 (Performance) appears solid from a codebase architectural standpoint, it is highly recommended to run automated profiling during startup and perform UI frame-rate testing on lower-end Android devices to guarantee the sub-3-second launch time.
