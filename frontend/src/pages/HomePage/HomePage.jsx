import "./HomePage.css";
import Navbar from "../../components/Navbar/Navbar";
import Banner from "../../components/Banner/Banner";
import Button from "../../components/Button/Button";
import Tips from "../../components/Dicks/Tips";
import { useNavigate } from "react-router-dom";

const HomePage = () => {
  const navigate = useNavigate();

  const handleTableButtonPressed = () => {
    navigate("./TabelasPage");
  };
  const handleGraphButtonPressed = () => {
    navigate("./TabelasPage");
  };

  return (
    <div>
      <header>
        <Navbar />
        <Banner />
      </header>
      <main className="home_main">
        <h2>Selecione o que você deseja fazer primeiro:</h2>
        <div className="home_container">
          <Button
            onClick={handleTableButtonPressed}
            filled={false}
            description={"Gerar tabelas do polo"}
          />
          <Button
            onClick={handleGraphButtonPressed}
            filled={true}
            link={""}
            description={"Gerar gráfico do polo"}
          />
        </div>
      </main>
      <footer>
        <Tips pagina={1} />
      </footer>
    </div>
  );
};

export default HomePage;
