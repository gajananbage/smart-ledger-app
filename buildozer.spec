[app]

# (string) Title of your application
title = Smart Ledger Pro

# (string) Package name
package.name = smartledger

# (string) Package domain (needed for android package name)
package.domain = org.example

# (string) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (string) Application version
version = 0.1

# (list) Application requirements
# Flet ॲप व्यवस्थित चालण्यासाठी python3 आणि flet आवश्यक आहेत
requirements = python3,flet

# (str) Supported orientations (valid options are: landscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# भविष्यात इंटरनेट किंवा स्टोरेज वापरायचे असेल तर या परवानग्या कामाला येतील
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use this to accept SDK licenses automatically (AIDL Fix साठी अत्यंत महत्त्वाचे)
android.accept_sdk_license = True

# (list) The Android architectures to build for
android.archs = arm64-v8a

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add space between the paths
#android.add_jars = foo.jar,bar.jar

# (list) List of Java files to add to the android project
#android.add_src =

# (list) Android AAR archives to add (must be local string paths)
#android.add_aars =

# (str) Path to a custom whitelist file
#android.whitelist =

# (str) Android logcat filters to use
#android.logcat_filters = *:S python:D

# (bool) Copy old style assets to allow fallback access (deprecated)
#android.copy_libs = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and big outputs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build output (default is ./bin)
# bin_dir = ./bin
