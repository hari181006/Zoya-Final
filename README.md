# Zoya Services — Public Website + Android App Ready

This package is prepared from the working Zoya Services project.

## 1. Public website deployment (Render)
1. Create/sign in to a Render account.
2. Put this project in a GitHub repository.
3. In Render choose **New → Blueprint** and select the repository.
4. Render reads `render.yaml`, creates the web service and PostgreSQL database, installs the backend, and starts FastAPI.
5. Open the generated `https://...onrender.com/` URL.

The website frontend is served by FastAPI, so browser API calls use the same HTTPS origin.

### Production admin
Initial demo admin: `admin` / `ZoyaAdmin@2026`. Change the password in Render environment variables after deployment.

## 2. Android app
The Android WebView project is in `android/ZoyaServices`.
After the website has a real HTTPS URL, replace `ZOYA_URL` in `MainActivity.java` with that URL, then open the `android/ZoyaServices` folder in Android Studio and build the APK with **Build → Build APK(s)**.

The app includes microphone permission and the voice bridge already used by the website.

## 3. Local test
Use `START_ZOYA.bat` for the local version.

## Important
A public deployment cannot be completed inside this ZIP without access to your hosting/GitHub account. The package is deployment-ready; the final public URL and signed release APK are created after your account performs the deployment/build step.
