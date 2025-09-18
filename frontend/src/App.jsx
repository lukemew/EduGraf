import { Navigate, Route, Routes } from "react-router-dom";
import "./App.css";
import NotificationContainer from "./components/NotificationContainer/NotificationContainer";
import { AuthProvider, useAuth } from "./contexts/AuthContext.jsx";
import {
  NotificationProvider,
  useNotificationContext,
} from "./contexts/NotificationContext";
import Login from "./pages/Auth/Login.jsx";
import Register from "./pages/Auth/Register.jsx";
import GraficoPage from "./pages/GraficoPage/GraficoPage";
import TabelasPage from "./pages/TabelasPage/TabelasPage";
import HomePage from "./pages/HomePage/HomePage.jsx";

function PrivateRoute({ children }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
}

function AppContent() {
  const { notifications, removeNotification } = useNotificationContext();

  return (
    <div>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/"
          element={
            <PrivateRoute>
              <HomePage />
            </PrivateRoute>
          }
        />
        <Route
          path="/TabelasPage"
          element={
            <PrivateRoute>
              <TabelasPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/GraficoPage"
          element={
            <PrivateRoute>
              <GraficoPage />
            </PrivateRoute>
          }
        />
      </Routes>
      <NotificationContainer
        notifications={notifications}
        onRemove={removeNotification}
      />
    </div>
  );
}

function App() {
  return (
    <NotificationProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </NotificationProvider>
  );
}

export default App;
