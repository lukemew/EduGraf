import Logo from "../../assets/logo.png";

import Navbar from "../../components/Navbar/Navbar";

const Home = () => {
  return (
    <div>
      <header>
        <Navbar />
      </header>
      <div className="banner">
        <Banner />
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
          <img src="" alt="Imagem ilustrativa do tópico de dicas" />
        </div>
      </footer>
    </div>
  );
};

export default Home;
