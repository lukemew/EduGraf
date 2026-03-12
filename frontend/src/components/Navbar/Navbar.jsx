import React from "react";
import { Link, useNavigate } from "react-router-dom";
import Logo from "../../assets/logo.png";
import { useAuth } from "../../contexts/AuthContext.jsx";
import "./Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const { logout, isAuthenticated } = useAuth();

  const handleLogoClick = () => {
    navigate("../");
  };

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  const handleNewUser = () => {
    navigate("/register");
  };

  return (
    <nav className="navbar">
      <img onClick={handleLogoClick} src={Logo} alt="Logo do Edugraf" />
      <div className="nav_links">
        <ul>
          <li>
            <Link to="/">Início</Link>
          </li>
          <li>
            <a href="#dicas">Instruções</a>
          </li>
          <li>
            <Link to="/TabelasPage">Tabelas</Link>
          </li>
          <li>
            <Link to="/GraficoPage">Gráficos</Link>
          </li>
        </ul>
        {isAuthenticated ? (
          <>
            <button
              className="logout_button"
              onClick={handleNewUser}
              aria-label="Cadastrar novo usuário"
            >
              Novo Usuário
            </button>
            <button
              className="logout_button"
              onClick={handleLogout}
              aria-label="Sair"
            >
              Sair
            </button>
          </>
        ) : null}
      </div>
    </nav>
  );
};

export default Navbar;
