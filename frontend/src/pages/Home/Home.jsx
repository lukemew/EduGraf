import "./Home.css";
import Navbar from "../../components/Navbar/Navbar";
import Banner from "../../components/Banner/Banner";
import Button from "../../components/Button/Button";
import Tips from "../../components/Dicks/Tips";

const Home = () => {
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
            filled={false}
            link={""}
            description={"Gerar tabelas do polo"}
          />
          <Button
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

export default Home;
