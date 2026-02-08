# React Native Environment Setup and Application Creation

This guide provides step-by-step instructions to set up the environment for React Native development, create a new React Native application, and resolve common issues during the build process.

## Prerequisites

Before you begin, ensure the following:

1. **Node.js**: Install the latest LTS version of Node.js from [Node.js official website](https://nodejs.org/).
2. **Java Development Kit (JDK)**: Install the JDK 11 or later. Use [OpenJDK](https://openjdk.org/) or [Amazon Corretto](https://aws.amazon.com/corretto/).
3. **Android Studio**: Install Android Studio to set up the Android emulator and SDK tools.
   - During installation, select the following:
     - Android SDK
     - Android SDK Platform
     - Android Virtual Device (AVD)
4. **Chocolatey (Optional for Windows)**: Use Chocolatey, a package manager for Windows, to automate the installation of prerequisites like Node.js, JDK, and Android Studio:
   ```bash
   choco install nodejs.install openjdk androidstudio
   ```
   Chocolatey simplifies the setup process by automating the download and configuration of tools.
5. **Watchman (Optional for macOS)**: Install Watchman for macOS using Homebrew:
   ```bash
   brew install watchman
   ```
6. **Xcode (for iOS)**: If you plan to develop for iOS, install Xcode from the Mac App Store.

---

## Environment Setup

### Step 1: Install React Native CLI
Install React Native CLI globally:
```bash
npm install -g react-native-cli
```

### Step 2: Configure Android Environment

1. Open Android Studio and go to `Preferences > Appearance & Behavior > System Settings > Android SDK`.
2. Install the following:
   - SDK Platforms: Install the latest Android SDK Platform.
   - SDK Tools: Install Android SDK Build-Tools and Command Line Tools.
3. Set the `ANDROID_HOME` environment variable:
   ```bash
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/emulator:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools
   ```
   Add these lines to your shell configuration file (e.g., `.bashrc`, `.zshrc`, etc.).

### Step 3: Verify Installation
Verify the installation by running the following commands:
```bash
node -v
npm -v
java -version
adb --version
```

---

## Create a React Native Application

### Step 1: Create a Project
Use the following command to create a new React Native application:
```bash
npx @react-native-community/cli init skillsuptechapp
```

### Default Behavior
- By default, this command creates a **TypeScript** React Native application if TypeScript dependencies are detected.
- If you want to explicitly create a **JavaScript** project, you can pass the `--template react-native-template-legacy` flag:
  ```bash
  npx @react-native-community/cli init skillsuptechapp --template react-native-template-legacy
  ```

### Step 2: Navigate to the Project Directory
```bash
cd skillsuptechapp
```

---

## Running the Application

### Android
To run the application on an Android device or emulator, use the following command:
```bash
npm run android
```
Ensure the Android emulator is running or an Android device is connected with USB debugging enabled.

### iOS (macOS Only)
To run the application on an iOS simulator, use the following command:
```bash
npx react-native run-ios
```
Ensure you have Xcode installed and properly configured.

---

## Common Issues and Resolutions

### Error: `Could not move temporary workspace`

#### 1. **Verify Permissions**
Ensure you have the required permissions to modify and access files in the project directory. Run the terminal or command prompt as an administrator, and then try running the command again:
```bash
npm run android
```

#### 2. **Clean the Gradle Cache**
```bash
cd android
./gradlew clean
```
On Windows, use:
```bash
gradlew.bat clean
```
Then, rebuild the project:
```bash
npm run android
```

#### 3. **Check the `settings.gradle` File**
Ensure your `settings.gradle` file includes the correct plugin and no syntax errors. Open `android/settings.gradle` and verify the plugin declaration:
```gradle
pluginManagement {
    repositories {
        gradlePluginPortal()
        google()
        mavenCentral()
    }
}

rootProject.name = 'skillsuptechsessionapp'
include ':app'
```

#### 4. **Update Dependencies**
Ensure that your dependencies and Gradle version are up to date. Open `android/build.gradle` and ensure the following:
- Use the correct Gradle plugin version:
  ```gradle
  dependencies {
      classpath("com.android.tools.build:gradle:8.0.2")
      classpath("com.facebook.react:react-native-gradle-plugin")
  }
  ```
- In `android/gradle.properties`, ensure compatibility settings:
  ```properties
  org.gradle.jvmargs=-Xmx2048m
  android.useAndroidX=true
  android.enableJetifier=true
  ```
Run the following command to install all required dependencies:
```bash
npm install
```

#### 5. **Update Java and Gradle**
Ensure you are using a compatible JDK (11 or later) and Gradle version:
- Update JDK: Download JDK 11 or later from [Oracle](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) or [OpenJDK](https://openjdk.org/).
- Update Gradle Wrapper: Run the following in the `android` directory:
  ```bash
  ./gradlew wrapper --gradle-version 8.0
  ```

#### 6. **Delete `node_modules` and Reinstall**
```bash
rm -rf node_modules
npm install
```

#### 7. **Restart Metro Bundler**
```bash
npm start --reset-cache
```

#### 8. **Check Android SDK and Tools**
Ensure you have the correct SDK tools installed in Android Studio:
1. Open Android Studio.
2. Go to `Preferences > Appearance & Behavior > System Settings > Android SDK`.
3. Ensure the correct version of Android SDK Build Tools is installed.

---

## Folder Structure

The project structure will look like this:
```
skillsuptechapp
├── android
├── ios
├── node_modules
├── src
│   ├── App.tsx (for TypeScript template)
│   └── App.js (for JavaScript template)
├── package.json
└── ...
```

---

## Additional Commands

### Start the Development Server
```bash
npm start
```

### Run Lint Checks
For TypeScript projects, ensure type safety by running:
```bash
npm run tsc
```

---

Congratulations! You have successfully set up the environment, created a React Native application, and resolved common issues during the build process.
