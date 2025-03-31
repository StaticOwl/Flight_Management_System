# ✈️ Flights Frontend

This project is a React-based frontend for the Flights Management System. It was bootstrapped with [Create React App](https://github.com/facebook/create-react-app) and communicates with a Flask backend via a proxy.

---

## 🚀 Getting Started

### ✅ Prerequisites

- [Node.js](https://nodejs.org/) (v18+ recommended)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
- Backend server running at [http://127.0.0.1:5000](http://127.0.0.1:5000) (see [backend setup](../backend/README.md))

---

### ⚙️ Setup Instructions

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend/flights
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the frontend**:
   ```bash
   npm start
   ```

   This runs the app in development mode at [http://localhost:3000](http://localhost:3000). All API requests to `/api` are proxied to `http://127.0.0.1:5000`.

---

## 🧪 Running Tests

To launch the test runner in interactive watch mode:

```bash
npm test
```

---

## 🏗️ Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

---

## 🔧 Additional Scripts

| Script           | Description                                           |
|------------------|-------------------------------------------------------|
| `npm start`      | Start development server                              |
| `npm test`       | Run tests using Jest and React Testing Library        |
| `npm run build`  | Create a production build                             |
| `npm run eject`  | Eject CRA configuration (not recommended)             |

---

## 🔁 Proxy Configuration

The frontend communicates with the backend via a proxy:

```json
"proxy": "http://127.0.0.1:5000"
```

If your backend runs on a different URL or port, modify this in `frontend/flights/package.json`.
