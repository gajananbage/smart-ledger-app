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
# अँड्रॉइड १० आणि वरच्या व्हर्जनवर क्रॅश टाळण्यासाठी फक्त इंटरनेट परमिशन पुरेशी आहे
android.permissions = INTERNET

# 🛠️ [अँड्रॉइड १० क्रॅश फिक्स] Scoped Storage ब्लॉक टाळण्यासाठी हे मेटा-डेटा जोडणे आवश्यक आहे:
android.meta_data = android.requestLegacyExternalStorage=true

# (int) Target Android API (अँड्रॉइड १४ साठी API 34 नुसार अपग्रेडेड)
android.api = 34

# (int) Minimum API your APK will support (अँड्रॉइड ५.० आणि त्यावरील सर्व फोनसाठी)
android.minapi = 21

# (str) Android NDK version to use (Flet आणि Python 3.11 साठी सर्वात स्थिर व्हर्जन)
android.ndk = 25b

# (bool) Use this to accept SDK licenses automatically (AIDL Fix साठी अत्यंत महत्त्वाचे)
android.accept_sdk_license = True

# (list) The Android architectures to build for (सर्व आधुनिक ६४-बिट फोन्ससाठी)
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug and big outputs)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
