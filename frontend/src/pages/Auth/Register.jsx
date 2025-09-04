import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import useNotification from "../../hooks/useNotification";
import api from "../../services/api";
import "./auth.css";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { showError, showSuccess } = useNotification();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      showError("Erro!", "As senhas não coincidem!");
      return;
    }

    if (password.length < 6) {
      showError("Erro!", "A senha deve ter pelo menos 6 caracteres!");
      return;
    }

    setLoading(true);
    try {
      await api.post("/auth/register", { name, email, password });
      showSuccess("Sucesso!", "Cadastro realizado com sucesso! Faça login.");
      navigate("/login");
    } catch (err) {
      showError("Erro!", "Erro no cadastro. Tente outro e-mail.");
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
            <h2>Criar sua conta</h2>
            <p>Preencha os dados abaixo para começar a usar o sistema</p>
          </div>

          <form onSubmit={handleSubmit} className="auth_form">
            <div className="form_group">
              <label htmlFor="name">Nome completo</label>
              <div className="input_container">
                <span className="input_icon">👤</span>
                <input 
                  id="name"
                  type="text" 
                  value={name} 
                  onChange={(e) => setName(e.target.value)} 
                  placeholder="Seu nome completo"
                  required 
                />
              </div>
            </div>

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
                  placeholder="Mínimo 6 caracteres"
                  required 
                />
              </div>
            </div>

            <div className="form_group">
              <label htmlFor="confirmPassword">Confirmar senha</label>
              <div className="input_container">
                <span className="input_icon">🔒</span>
                <input 
                  id="confirmPassword"
                  type="password" 
                  value={confirmPassword} 
                  onChange={(e) => setConfirmPassword(e.target.value)} 
                  placeholder="Digite a senha novamente"
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
                  Criando conta...
                </>
              ) : (
                <>
                  <span>Criar conta</span>
                  <span>→</span>
                </>
              )}
            </button>
          </form>

          <div className="auth_footer">
            <p>Já tem uma conta? <Link to="/login" className="auth_link">Faça login aqui</Link></p>
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


