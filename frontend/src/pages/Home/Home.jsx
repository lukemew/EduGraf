import Logo from "../../assets/logo.png";

import Navbar from "../../components/Navbar/Navbar";

const Home = () => {
  return (
    <div>
      <header>
        <Navbar />
      </header>
      <div className="banner">
        <div>
          <h2>Bem-Vindo ao EduGraf</h2>
          <p>Sistema completo para Gestão de Polos</p>
        </div>
        <img src={Ilustracao} alt="Imagem ilustrativa do banner" />
      </div>
      <div className="opcoes">
        <h2>O que você deseja fazer primeiro?</h2>
        <div className="container-opcoes">
          <a href="">Gerar tabelas do Polo</a>
          <a href="">Gerar gráficos do Polo</a>
        </div>
      </div>
      <footer>
        <h2>Dicas</h2>
        <div className="container-footer">
          <img src={Ilustracao2} alt="Imagem ilustrativa do tópico de dicas" />
        </div>
      </footer>
    </div>
  );
};

export default Home;
