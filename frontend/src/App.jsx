import { useState } from "react";
import Navbar from "./components/Navbar/Navbar";
import Banner from "./components/Banner/Banner";
import Home from "./pages/Home/Home";

import "./App.css";

function App() {
  return (
    <div>
      <Navbar />
      <Banner />
    </div>
  );
}

export default App;
