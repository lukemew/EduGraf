import { useState } from "react";
import Navbar from "./components/Navbar/Navbar";
import Banner from "./components/Banner/Banner";
import Button from "./components/Button/Button";
import Home from "./pages/Home/Home";

import "./App.css";

function App() {
  return (
    <div>
      <Navbar />
      <Banner />
      <Button filled={false} link={""} description={"Gerar tabelas do polo"} />
    </div>
  );
}

export default App;
