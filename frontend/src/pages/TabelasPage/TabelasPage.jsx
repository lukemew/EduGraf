import "./TabelasPage.css";
import Navbar from "../../components/Navbar/Navbar";
import Select from "../../components/Select/Select";
import SmallButton from "../../components/SmallButton/SmallButton";
import FileUpload from "../../components/FileUpload/FileUpload";
import Tips from "../../components/Dicks/Tips";
import { useState } from "react";
import axios from "axios";

const TabelasPage = () => {
  // 1. Estado para guardar o valor do polo selecionado.
  //    Inicializamos com 'Polo 1' como padrão.
  const [selectedPolo, setSelectedPolo] = useState("Polo 1");
  const [selectedFile, setSelectedFile] = useState(null);
  // 2. Estado para guardar o arquivo selecionado (vindo do componente FileUpload).

  const handlePoloChange = (e) => {
    setSelectedPolo(e.target.value);
  };

  // Manipulador para o envio do formulário
  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Por favor, selecione um arquivo primeiro.");
      return;
    }

    // 1. Criar o FormData
    const formData = new FormData();

    // 2. Adicionar AMBOS os dados ao FormData
    //    A chave 'polo' e 'file' devem ser as que seu backend espera receber
    formData.append("polo", selectedPolo);
    formData.append("file", selectedFile);

    console.log("Enviando para o backend:", {
      polo: selectedPolo,
      file: selectedFile.name,
    });

    try {
      // 3. Enviar a requisição (lógica de envio e download continua a mesma)
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `tabela_${selectedPolo.replace(" ", "_")}.xlsx`
      ); // Nome dinâmico para o download
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Erro ao fazer upload:", error);
      alert("Ocorreu um erro ao gerar a tabela.");
    }
  };

  return (
    <div>
      <header>
        <Navbar />
      </header>
      <main>
        <h2>Gerar tabela do Polo</h2>
        <div className="select_container--polo">
          <p>Selecione o polo:</p>
          <Select value={selectedPolo} onChange={handlePoloChange} />
          <div className="select_container--upload">
            <FileUpload onFileSelect={setSelectedFile} />
            <SmallButton
              className="upload_button"
              description={"Gerar tabela"}
              filled={true}
              onClick={handleUpload}
            />
          </div>
        </div>
      </main>
      <footer>{/* <Tips /> */}</footer>
    </div>
  );
};

export default TabelasPage;
