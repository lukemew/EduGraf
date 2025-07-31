import "./GraficoPage.css";
import Navbar from "../../components/Navbar/Navbar";
import Select from "../../components/Select/Select";
import SmallButton from "../../components/SmallButton/SmallButton";
import FileUpload from "../../components/FileUpload/FileUpload";
import Tips from "../../components/Dicks/Tips";
import { useState } from "react";
import axios from "axios";
import Grafico from "../../assets/grafico-exemplo.png";

const GraficoPage = () => {
  // 1. Estado para guardar o valor do polo selecionado.
  //    Inicializamos com 'Polo 1' como padrão.
  const [selectedAmount, setSelectedAmount] = useState(1);
  const [selectedFiles, setSelectedFiles] = useState([]);
  // 2. Estado para guardar o arquivo selecionado (vindo do componente FileUpload).

  const handleAmountChange = (e) => {
    const amount = parseInt(e.target.value, 10);
    setSelectedAmount(amount);
    setSelectedFiles([]);
  };

  const handleFileUpdate = (index, file) => {
    const newFiles = [...selectedFiles];
    newFiles[index] = file;
    setSelectedFiles(newFiles);
  };

  // Manipulador para o envio do formulário
  const handleUpload = async () => {
    // Verifica se o número de arquivos selecionados corresponde ao esperado
    if (
      selectedFiles.length !== parseInt(selectedAmount) ||
      selectedFiles.includes(undefined)
    ) {
      alert("Por favor, selecione todos os arquivos necessários.");
      return;
    }

    const formData = new FormData();
    formData.append("quant_trimestre", selectedAmount);

    // Percorre o array de arquivos e adiciona cada um
    selectedFiles.forEach((file) => {
      // É comum usar 'files[]' para indicar ao backend que é um array de arquivos
      formData.append("files[]", file);
    });

    console.log("Enviando para o backend:", {
      quant_trimestre: selectedAmount,
      files: selectedFiles.map((f) => f.name),
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
        `tabela_${selectedAmount.replace(" ", "_")}.xlsx`
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
      <main className="tabelas_container">
        <h2>Gerar gráfico do Polo</h2>
        <div className="select_container--polo">
          <p>Selecione a quantidade de trimestres:</p>
          <Select value={selectedAmount} onChange={handleAmountChange} />
          <p>Selecione a(s) tabela(s) do polo:</p>
          <div className="select_container--upload">
            {/* <FileUpload onFileSelect={setSelectedFiles} /> */}
            {Array.from({ length: selectedAmount }, (_, index) => (
              <div key={index} className="fileupload-wrapper">
                <p>Tabela do {index + 1}º trimestre: </p>
                <FileUpload
                  onFileSelect={(file) => handleFileUpdate(index, file)}
                />
              </div>
            ))}
            <SmallButton
              className="upload_button"
              description={"Gerar tabela"}
              filled={true}
              onClick={handleUpload}
            />
          </div>
        </div>

        <img src={Grafico} alt="Pré visualização da tabela" />
        <SmallButton description={"Salvar gráficos"} filled={false} />
      </main>
      <footer>
        <Tips pagina={3} />
      </footer>
    </div>
  );
};

export default GraficoPage;
