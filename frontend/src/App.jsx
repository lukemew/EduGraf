import { useState } from "react";
import Navbar from "./components/Navbar/Navbar";
import Banner from "./components/Banner/Banner";
import Button from "./components/Button/Button";
import Tips from "./components/Dicks/Tips";
import Home from "./pages/Home/Home";

import "./App.css";
import SmallButton from "./components/SmallButton/SmallButton";

function App() {
  return (
    <div>
      <SmallButton filled={true} description={"Salvar Tabela"} />
    </div>
  );
}

export default App;
