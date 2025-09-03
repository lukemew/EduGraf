import "./App.css";
import GraficoPage from "./pages/GraficoPage/GraficoPage";
import HomePage from "./pages/HomePage/HomePage";
import TabelasPage from "./pages/TabelasPage/TabelasPage";
import NotificationContainer from "./components/NotificationContainer/NotificationContainer";
import { NotificationProvider, useNotificationContext } from "./contexts/NotificationContext";
import { Routes, Route } from "react-router-dom";

function AppContent() {
  const { notifications, removeNotification } = useNotificationContext();

  return (
    <div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/TabelasPage" element={<TabelasPage />} />
        <Route path="/GraficoPage" element={<GraficoPage />} />
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
      <AppContent />
    </NotificationProvider>
  );
}

export default App;
