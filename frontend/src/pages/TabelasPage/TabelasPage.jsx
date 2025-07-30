import "./TabelasPage.css";
import Navbar from "../../components/Navbar/Navbar";
import Select from "../../components/Select/Select";
import SmallButton from "../../components/SmallButton/SmallButton";
import FileUpload from "../../components/FileUpload/FileUpload";

const TabelasPage = () => {
  return (
    <div>
      <header>
        <Navbar />
        <FileUpload />
      </header>
      {/* <main>
        <h2>Gerar tabela do Polo</h2>
        <div className="select_container--polo">
          <p>Selecione o polo:</p>
          <Select />
        </div>
        <div className="select_container--escolas">
           <SmallButton description={"Gerar tabela"} />
        </div>
      </main> */}
    </div>
  );
};

export default TabelasPage;
