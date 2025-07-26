import Ilustracao from "../../assets/Ilustracao.png";
import "./Banner.css";

const Banner = () => {
  return (
    <div className="banner">
      <div className="banner-container">
        <h2>Bem-Vindo ao EduGraf</h2>
        <p>Sistema completo para Gestão de Polos</p>
      </div>
      <img src={Ilustracao} alt="Imagem ilustrativa do banner" />
    </div>
  );
};

export default Banner;
