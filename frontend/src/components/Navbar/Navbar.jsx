import React from "react";
import "./Navbar.css";
import Logo from "../../assets/logo.png";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="navbar">
      <img src={Logo} alt="Logo do Edugraf" />
      <div>
        <ul>
          <li>
            <Link to="/">Início</Link>
          </li>
          <li>
            <a href="#dicas">Dicas</a>
          </li>
          <li>
            <Link to="/TabelasPage">Tabelas</Link>
          </li>
          <li>
            <Link to="">Gráficos</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
