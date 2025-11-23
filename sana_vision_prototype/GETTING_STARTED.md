# Getting Started with SANA Vision Prototype

## Prerequisites

Before running this Flutter app, ensure you have Flutter installed on your system.

### Installing Flutter

**macOS:**
```bash
# Download Flutter SDK
cd ~/development
git clone https://github.com/flutter/flutter.git -b stable

# Add Flutter to PATH
export PATH="$PATH:`pwd`/flutter/bin"

# Verify installation
flutter doctor
```

**Windows:**
1. Download Flutter SDK from https://flutter.dev/docs/get-started/install/windows
2. Extract the zip file
3. Add `flutter\bin` to your PATH
4. Run `flutter doctor` in Command Prompt

**Linux:**
```bash
# Download and extract Flutter
cd ~/development
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.x.x-stable.tar.xz
tar xf flutter_linux_3.x.x-stable.tar.xz

# Add to PATH
export PATH="$PATH:`pwd`/flutter/bin"

# Verify installation
flutter doctor
```

### Additional Requirements

- **Android Studio** (for Android development)
  - Download from https://developer.android.com/studio
  - Install Android SDK and Android Emulator

- **Xcode** (for iOS development - macOS only)
  - Install from Mac App Store
  - Run `sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer`
  - Run `sudo xcodebuild -runFirstLaunch`

- **VS Code** or **Android Studio** with Flutter extensions

## Running the App

### Step 1: Clone or Navigate to Project

```bash
cd sana_vision_prototype
```

### Step 2: Install Dependencies

```bash
flutter pub get
```

This will download all required packages:
- `fl_chart` - For charts and graphs
- `google_fonts` - For Inter font family
- `intl` - For date formatting
- `flutter_animate` - For animations
- `smooth_page_indicator` - For indicators

### Step 3: Check Your Setup

```bash
flutter doctor -v
```

This command checks if you have all the necessary tools installed. Fix any issues it reports.

### Step 4: List Available Devices

```bash
flutter devices
```

This will show all connected devices and emulators.

### Step 5: Run the App

**For Physical Device (Connected via USB):**
```bash
flutter run
```

**For Specific Device:**
```bash
# Android Emulator
flutter run -d <device-id>

# iOS Simulator
flutter run -d iPhone

# Chrome (Web - for quick preview)
flutter run -d chrome
```

**For Release Build (Better Performance):**
```bash
# Android
flutter run --release

# iOS (macOS only)
flutter run --release -d iPhone
```

## Quick Start for Demo

### Option 1: Android Physical Device
1. Enable Developer Options on Android device
2. Enable USB Debugging
3. Connect via USB
4. Run: `flutter run`

### Option 2: iOS Physical Device (macOS)
1. Connect iPhone/iPad via USB
2. Trust the computer on device
3. Run: `flutter run`

### Option 3: Android Emulator
1. Open Android Studio
2. Tools → Device Manager → Create Device
3. Start the emulator
4. In terminal: `flutter run`

### Option 4: iOS Simulator (macOS)
1. Open Xcode → Preferences → Components
2. Download iOS Simulator
3. Run: `open -a Simulator`
4. In terminal: `flutter run`

### Option 5: Web Browser (Quick Preview)
```bash
flutter run -d chrome
```
*Note: Charts and some features may look different on web*

## Troubleshooting

### Issue: "Flutter command not found"
**Solution:** Ensure Flutter is added to your PATH. Re-run the PATH export command or restart your terminal.

### Issue: "Unable to locate Android SDK"
**Solution:**
```bash
flutter config --android-sdk /path/to/android/sdk
```

### Issue: "CocoaPods not installed" (macOS/iOS)
**Solution:**
```bash
sudo gem install cocoapods
cd ios
pod install
cd ..
```

### Issue: "Gradle build failed" (Android)
**Solution:**
```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

### Issue: Network images not loading
**Solution:**
- Ensure device/emulator has internet connection
- Check firewall settings
- Images use https://i.pravatar.cc which should work globally

### Issue: Build taking too long
**Solution:** Use release mode for faster performance:
```bash
flutter run --release
```

## Building for Distribution

### Android APK
```bash
flutter build apk --release
```
APK location: `build/app/outputs/flutter-apk/app-release.apk`

### iOS IPA (macOS only)
```bash
flutter build ios --release
```
Then open in Xcode to create IPA

### Web Build
```bash
flutter build web
```
Output: `build/web/`

## App Features to Demo

### Main Navigation (Bottom Bar):
1. **Home** - Wellness summary, quick actions, activity feed
2. **Health Graph** - 360° wellness with radar charts and timeline
3. **Journal** - AI-powered reflection with 4 personas
4. **Appointments** - Session management
5. **Profile** - Settings and portal access

### Special Portals (Access via Profile):
6. **Evidence Dashboard** - Practitioner analytics
7. **Research Portal** - Institutional data access
8. **Enterprise Dashboard** - NHS/Corporate integration (2 tabs)

### Demo Flow Suggestion:
1. Start on **Home** screen - Show overall wellness (78/100, "Thriving" status)
2. Navigate to **Health Graph** - Show 6-dimension radar chart and 12-month timeline
3. Tap **Top 3 Levers** - Show AI recommendations
4. Go to **Journal** - Demonstrate 4 AI personas (select each one)
5. Go to **Profile** → **Evidence Dashboard** - Show practitioner view
6. **Profile** → **Research Portal** - Show institutional access
7. **Profile** → **Enterprise Dashboard** - Show both NHS and Corporate tabs
8. Return to **Home** → Tap a practitioner card → Show **SANA Index breakdown**

## Performance Tips

- **Use Release Mode** for demos: `flutter run --release`
- **Hot Reload** during development: Press `r` in terminal after code changes
- **Hot Restart**: Press `R` if hot reload doesn't work
- **Clear Cache** if issues: `flutter clean && flutter pub get`

## Demo Data

All data is hardcoded dummy data showing:
- **Health Score:** 78/100 (Thriving)
- **SANA Index:** 87/100 (Top 10%)
- **Improvement Rate:** 44% average
- **NHS Savings:** £124,000
- **Research Data Points:** 12,450+

The "DEMO DATA" watermark appears in the top-right corner of all screens.

## Support

For issues with:
- **Flutter setup:** Visit https://flutter.dev/docs/get-started/install
- **App-specific issues:** Check README.md in project root
- **Chart rendering:** Ensure `fl_chart` package is properly installed

## Quick Commands Reference

```bash
# Get dependencies
flutter pub get

# Run app
flutter run

# Run in release mode
flutter run --release

# Hot reload (during run)
Press 'r' in terminal

# Hot restart (during run)
Press 'R' in terminal

# List devices
flutter devices

# Clean build
flutter clean

# Check setup
flutter doctor

# Upgrade Flutter
flutter upgrade

# Analyze code
flutter analyze

# Format code
flutter format lib/

# Build APK
flutter build apk --release
```

---

**Ready to Wow Your Audience!** 🚀

The app is fully functional with realistic dummy data and professional design. All features are accessible and navigation is intuitive. Perfect for demonstrating SANA's complete vision to investors and stakeholders.
