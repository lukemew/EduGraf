import "./App.css";
import HomePage from "./pages/HomePage/HomePage";
import TabelasPage from "./pages/TabelasPage/TabelasPage";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/TabelasPage" element={<TabelasPage />} />
      </Routes>
    </div>
  );
}

export default App;
