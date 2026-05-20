[app]
title = Smart Ledger Pro
package.name = smartledger
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,flet
orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

# 🛠️ AIDL एरर फिक्स करण्यासाठी हे पाथ जोडणे आवश्यक आहे:
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk-bundle
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
