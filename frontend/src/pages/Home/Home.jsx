import Logo from "../../assets/logo.png";

import Navbar from "../../components/Navbar/Navbar";

const Home = () => {
  return (
    <div>
      <header>
        <Navbar />
      </header>
      <main>
        <Banner />
        <div className="container">
          <Button
            filled={false}
            link={""}
            description={"Gerar tabelas do polo"}
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
