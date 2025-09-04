import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext.jsx";
import useNotification from "../../hooks/useNotification";
import api from "../../services/api";
import "./auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { showError, showSuccess } = useNotification();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);
      const { data } = await api.post("/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      login(data.access_token, data.user);
      showSuccess("Sucesso!", "Login realizado com sucesso!");
      navigate("/");
    } catch (err) {
      showError("Erro!", "Falha no login. Verifique suas credenciais.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth_page">
      <div className="auth_background">
        <div className="auth_pattern"></div>
      </div>
      
      <div className="auth_content">
        <div className="auth_header">
          <div className="auth_logo">
            <div className="logo_icon">🎓</div>
            <h1>EduGraf</h1>
          </div>
          <p className="auth_tagline">Sistema de Análise Educacional</p>
        </div>

        <div className="auth_card">
          <div className="auth_card_header">
            <h2>Bem-vindo de volta!</h2>
            <p>Entre com suas credenciais para acessar o sistema</p>
          </div>

          <form onSubmit={handleSubmit} className="auth_form">
            <div className="form_group">
              <label htmlFor="email">E-mail</label>
              <div className="input_container">
                <span className="input_icon">📧</span>
                <input 
                  id="email"
                  type="email" 
                  value={email} 
                  onChange={(e) => setEmail(e.target.value)} 
                  placeholder="seu@email.com"
                  required 
                />
              </div>
            </div>

            <div className="form_group">
              <label htmlFor="password">Senha</label>
              <div className="input_container">
                <span className="input_icon">🔒</span>
                <input 
                  id="password"
                  type="password" 
                  value={password} 
                  onChange={(e) => setPassword(e.target.value)} 
                  placeholder="Sua senha" 
                  required 
                />
              </div>
            </div>

            <button 
              type="submit" 
              className={`auth_button ${loading ? 'loading' : ''}`}
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Entrando...
                </>
              ) : (
                <>
                  <span>Entrar</span>
                  <span>→</span>
                </>
              )}
            </button>
          </form>

          <div className="auth_footer">
            <p>Não tem uma conta? <Link to="/register" className="auth_link">Cadastre-se aqui</Link></p>
          </div>
        </div>

        <div className="auth_features">
          <div className="feature_item">
            <span className="feature_icon">📊</span>
            <span>Análise de Dados</span>
          </div>
          <div className="feature_item">
            <span className="feature_icon">📈</span>
            <span>Relatórios Visuais</span>
          </div>
          <div className="feature_item">
            <span className="feature_icon">🎯</span>
            <span>Insights Educacionais</span>
          </div>
        </div>
      </div>
    </div>
  );
}


