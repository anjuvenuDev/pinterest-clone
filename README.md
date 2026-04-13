# Pinterest Clone (Expo + React Native)

A Pinterest-style mobile app built with Expo Router, React Native, and TypeScript.

## Tech Stack

- Expo SDK 54
- Expo Router
- React Native 0.81
- React 19
- TypeScript

## Project Structure

- `app/(tabs)/HomeScreen.tsx` - home feed (masonry-style layout)
- `app/PinScreen.tsx` - pin details view
- `app/(tabs)/CreatePinScreen.tsx` - create/insert pin flow
- `app/(tabs)/ProfileScreen.tsx` - profile screen
- `app/data/pins.ts` and `assets/data/pins.ts` - local seed data
- `components/Pin.tsx` - reusable pin card component

## Getting Started

### 1) Install dependencies

```bash
npm install
```

### 2) Run dev server

```bash
npm start
```

### 3) Open target platform

```bash
npm run android
npm run ios
npm run web
```

## Scripts

From `package.json`:

- `npm start` -> `expo start`
- `npm run android` -> `expo start --android`
- `npm run ios` -> `expo start --ios`
- `npm run web` -> `expo start --web`

## Development Log

Detailed creation/build/dev timeline for Notion is available in:

- `NOTION_DEV_LOGS.txt`

## Git Timeline (Current)

- `2623b9e` Created a new Expo app
- `4065715` Pins
- `dd6ea6e` Home Screen: Masonry Layout
- `de780ec` Pin Screen
- `d041153` Profile & insert pin sceen
