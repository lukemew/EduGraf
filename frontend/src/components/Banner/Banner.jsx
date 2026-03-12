import Ilustracao from "../../assets/ilustracao.png";
import "./Banner.css";

const Banner = () => {
  return (
    <div className="banner">
      <div className="banner-container">
        <h2>Bem-Vindo ao EdugrafBV</h2>
        <p>Sistema completo para Gestão de Planilhas e Gráficos</p>
      </div>
      <img src={Ilustracao} alt="Imagem ilustrativa do banner" />
    </div>
  );
};

export default Banner;
