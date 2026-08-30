[app]

# (str) Title of your application
title = MenstrualTracker

# (str) Package name
package.name = mrkumar

# (str) Package domain (needed for android/ios packaging)
package.domain = anonymous.menstrual.tracker

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests,bin,.buildozer,.github,docs,playstore_assets,build,dist,.venv,.git,__pycache__

# (list) List of exclusions using pattern matching
source.exclude_patterns = *.pyc,*_log*.txt,*.db,*.key,*.spec

# (str) Application versioning
version = 0.1.1

# (numeric) Application version code (method 2)
android.numeric_version = 4

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,kivymd==1.1.1,plyer,pycryptodome,pillow

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (list) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API, should be as high as possible.
android.api = 35

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
android.ndk_api = 24

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) Accept Android SDK license
android.accept_sdk_license = True

# (str) Android release artifact type (aab or apk)
android.release_artifact = aab

# (str) The format used to log messages. See python logging module documentation for details
#log_level = 2

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios

# (str) Alternately, specify the URL of a git repository
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios

# (str) Branch to use for the kivy-ios repository
#ios.kivy_ios_branch = master

# (bool) Whether or not to sign the code
ios.codesign.allowed = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
