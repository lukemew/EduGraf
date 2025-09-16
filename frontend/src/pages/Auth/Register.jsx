import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useNotification from "../../hooks/useNotification";
import api from "../../services/api";
import "./auth.css";

export default function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const { showError, showSuccess } = useNotification();
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      const msg = "As senhas não coincidem!";
      showError("Erro!", msg);
      setErrorMessage(msg);
      return;
    }

    if (password.length < 6) {
      const msg = "A senha deve ter pelo menos 6 caracteres!";
      showError("Erro!", msg);
      setErrorMessage(msg);
      return;
    }

    setLoading(true);
    try {
      setErrorMessage("");
      await api.post("/auth/register", { name, email, password });
      showSuccess("Sucesso!", "Cadastro realizado com sucesso! Faça login.");
      navigate("/login");
    } catch (err) {
      const msg = err?.response?.data?.detail || "Erro no cadastro. Tente novamente.";
      if (msg === "E-mail já cadastrado") {
        showError("E-mail já cadastrado", "Use outro e-mail para se registrar.");
        setErrorMessage("E-mail já cadastrado. Use outro endereço.");
      } else if (msg === "Campos obrigatórios: name, email, password") {
        showError("Campos obrigatórios", "Preencha nome, e-mail e senha.");
        setErrorMessage("Preencha nome, e-mail e senha.");
      } else {
        showError("Erro no cadastro", msg);
        setErrorMessage(msg);
      }
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
                  type={showPassword ? "text" : "password"}
                  value={password} 
                  onChange={(e) => { setPassword(e.target.value); if (errorMessage) setErrorMessage(""); }} 
                  placeholder="Mínimo 6 caracteres"
                  required 
                />
                <button
                  type="button"
                  className="toggle_password"
                  onClick={() => setShowPassword((v) => !v)}
                  aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
                  title={showPassword ? "Ocultar senha" : "Mostrar senha"}
                >
                  {showPassword ? (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
                      <path d="M3 3L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M10.584 10.59C10.2106 10.9632 9.99994 11.4696 10 12C10 12.5304 10.2106 13.0368 10.584 13.41C10.9573 13.7834 11.4637 13.994 11.9941 13.994C12.5245 13.994 13.0309 13.7834 13.4042 13.41" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M17.94 17.94C16.226 19.011 14.17 19.666 12 19.75C7 19.75 3 15 3 12C3.522 10.423 4.516 8.996 5.86 7.94M9.9 5.74C10.583 5.583 11.289 5.5 12 5.5C17 5.5 21 10.25 21 13.25C20.741 14.05 20.358 14.804 19.866 15.486" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
                      <path d="M2 12C2 12 6 5.5 12 5.5C18 5.5 22 12 22 12C22 12 18 18.5 12 18.5C6 18.5 2 12 2 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M15.5 12C15.5 13.933 13.933 15.5 12 15.5C10.067 15.5 8.5 13.933 8.5 12C8.5 10.067 10.067 8.5 12 8.5C13.933 8.5 15.5 10.067 15.5 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  )}
                </button>
              </div>
            </div>

            <div className="form_group">
              <label htmlFor="confirmPassword">Confirmar senha</label>
              <div className="input_container">
                <span className="input_icon">🔒</span>
                <input 
                  id="confirmPassword"
                  type={showConfirmPassword ? "text" : "password"}
                  value={confirmPassword} 
                  onChange={(e) => { setConfirmPassword(e.target.value); if (errorMessage) setErrorMessage(""); }} 
                  placeholder="Digite a senha novamente"
                  required 
                />
                <button
                  type="button"
                  className="toggle_password"
                  onClick={() => setShowConfirmPassword((v) => !v)}
                  aria-label={showConfirmPassword ? "Ocultar senha" : "Mostrar senha"}
                  title={showConfirmPassword ? "Ocultar senha" : "Mostrar senha"}
                >
                  {showConfirmPassword ? (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
                      <path d="M3 3L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M10.584 10.59C10.2106 10.9632 9.99994 11.4696 10 12C10 12.5304 10.2106 13.0368 10.584 13.41C10.9573 13.7834 11.4637 13.994 11.9941 13.994C12.5245 13.994 13.0309 13.7834 13.4042 13.41" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M17.94 17.94C16.226 19.011 14.17 19.666 12 19.75C7 19.75 3 15 3 12C3.522 10.423 4.516 8.996 5.86 7.94M9.9 5.74C10.583 5.583 11.289 5.5 12 5.5C17 5.5 21 10.25 21 13.25C20.741 14.05 20.358 14.804 19.866 15.486" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  ) : (
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
                      <path d="M2 12C2 12 6 5.5 12 5.5C18 5.5 22 12 22 12C22 12 18 18.5 12 18.5C6 18.5 2 12 2 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M15.5 12C15.5 13.933 13.933 15.5 12 15.5C10.067 15.5 8.5 13.933 8.5 12C8.5 10.067 10.067 8.5 12 8.5C13.933 8.5 15.5 10.067 15.5 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {errorMessage ? (
              <div className="form_error" role="alert">{errorMessage}</div>
            ) : null}

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

          {/* Rodapé opcional removido na tela de cadastro, conforme solicitação de tela separada */}
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


