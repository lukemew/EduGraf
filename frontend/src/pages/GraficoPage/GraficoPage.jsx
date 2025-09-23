import "./GraficoPage.css";
import Navbar from "../../components/Navbar/Navbar";
import Select from "../../components/Select/Select";
import SmallButton from "../../components/SmallButton/SmallButton";
import FileUpload from "../../components/FileUpload/FileUpload";
import Tips from "../../components/Tips/Tips";
import { useNotificationContext } from "../../contexts/NotificationContext";
import { useState } from "react";
import axios from "axios";

const GraficoPage = () => {
  // ESTADO PRINCIPAL: controla quantos campos de upload aparecem (1 ou 2)
  const [selectedAmount, setSelectedAmount] = useState(1);
  // MUDANÇA 1: O estado agora guarda uma LISTA (array) de arquivos
  const [selectedFiles, setSelectedFiles] = useState([]);
  const { showSuccess, showError } = useNotificationContext();

  const handleAmountChange = (e) => {
    const amount = parseInt(e.target.value, 10);
    setSelectedAmount(amount);
    // Limpa a lista de arquivos sempre que a quantidade de períodos muda
    setSelectedFiles([]);
  };

  // MUDANÇA 2: Nova função que lida com a seleção de um arquivo em um índice específico
  const handleFileSelect = (file, index) => {
    // Cria uma cópia da lista de arquivos
    const newFiles = [...selectedFiles];
    // Adiciona o arquivo na posição correta (ex: 0 para o 1º período, 1 para o 2º)
    newFiles[index] = file;
    // Atualiza o estado com a nova lista
    setSelectedFiles(newFiles);
    console.log("Arquivos selecionados:", newFiles); // Ótimo para debugar!
  };

  const handleUpload = async () => {
    // MUDANÇA 3: A verificação agora checa se a lista tem a quantidade correta de arquivos
    if (
      selectedFiles.length !== selectedAmount ||
      selectedFiles.some((f) => !f)
    ) {
      showError(
        "Arquivos Faltando",
        `Por favor, selecione ${selectedAmount} arquivo(s) Excel.`
      );
      return;
    }

    const formData = new FormData();
    formData.append("trimestre", "1"); // O trimestre pode ser fixo ou vir de outro select

    // MUDANÇA 4: O loop adiciona CADA arquivo da lista ao FormData
    selectedFiles.forEach((file) => {
      formData.append("files", file); // A chave é "files" (plural) para o backend receber uma lista
    });
    formData.append("tipo_processamento", "grafico");

    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          responseType: "blob",
        }
      );

      // Lógica de download do PDF (continua igual)
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `relatorio_graficos_${new Date().toISOString().slice(0, 10)}.pdf`
      );
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);

      showSuccess(
        "📈 Relatório Gerado!",
        "O PDF com os gráficos será baixado automaticamente."
      );
    } catch (error) {
      console.error("Erro ao fazer upload:", error);
      showError("❌ Erro ao Gerar Relatório", "Ocorreu um erro no servidor.");
    }
  };

  return (
    <div>
      <header>
        <Navbar />
      </header>
      <main className="graficos_container">
        <h2>Gerar gráfico do Polo</h2>
        <div className="select_container--polo">
          <p>Selecione a quantidade de Períodos:</p>
          <Select value={selectedAmount} onChange={handleAmountChange} />
          <p>Selecione a(s) tabela(s) do polo:</p>
          <div className="select_container--upload">
            {Array.from({ length: selectedAmount }, (_, index) => (
              <div key={index} className="fileupload-wrapper">
                <p>Tabela do {index + 1}º período: </p>
                {/* MUDANÇA 5: Passa a nova função e o índice para o FileUpload */}
                <FileUpload
                  key={index} // Adicionar a key aqui é importante para o React
                  onFileSelect={(file) => handleFileSelect(file, index)}
                />
              </div>
            ))}
            <SmallButton
              description={"Gerar gráfico"}
              filled={true}
              onClick={handleUpload}
            />
          </div>
        </div>
      </main>
      <footer>
        <Tips pagina={3} />
      </footer>
    </div>
  );
};

export default GraficoPage;
