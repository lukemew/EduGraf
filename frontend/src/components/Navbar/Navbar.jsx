import React from "react";
import "./Navbar.css";
import Logo from "../../assets/logo.png";

const Navbar = () => {
  return (
    <nav className="navbar">
      <img src={Logo} alt="Logo do Edugraf" />
      <div>
        <ul>
          <li>
            <a href="">Início</a>
          </li>
          <li>
            <a href="">Dicas</a>
          </li>
          <li>
            <a href="">Tabelas</a>
          </li>
          <li>
            <a href="">Gráficos</a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
