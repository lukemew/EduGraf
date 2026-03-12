import "./GraficoPage.css";
import Navbar from "../../components/Navbar/Navbar";
import Select from "../../components/Select/Select";
import SmallButton from "../../components/SmallButton/SmallButton";
import FileUpload from "../../components/FileUpload/FileUpload";
import Tips from "../../components/Tips/Tips";
import { useNotificationContext } from "../../contexts/NotificationContext";
import { useState } from "react";
import axios from "axios";
import Tabela from "../../assets/tabela-exemplo.png";

const GraficoPage = () => {
  // ESTADO PRINCIPAL: controla quantos campos de upload aparecem (1 ou 2)
  const [selectedAmount, setSelectedAmount] = useState(1);
  // MUDANÇA 1: O estado agora guarda uma LISTA (array) de arquivos
  const [selectedFiles, setSelectedFiles] = useState([]);
  const { showSuccess, showError } = useNotificationContext();
  const [isLoading, setIsLoading] = useState(false);

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
        `Por favor, selecione ${selectedAmount} arquivo(s) Excel.`,
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

    setIsLoading(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          responseType: "blob",
        },
      );

      // Lógica de download do PDF (continua igual)
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `relatorio_graficos_${new Date().toISOString().slice(0, 10)}.pdf`,
      );
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);

      showSuccess(
        "📈 Relatório Gerado!",
        "O PDF com os gráficos será baixado automaticamente.",
      );
    } catch (error) {
      console.error("Erro ao fazer upload:", error);
      showError("❌ Erro ao Gerar Relatório", "Ocorreu um erro no servidor.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadTemplate = () => {
    // O caminho '/' aponta diretamente para a pasta 'public'
    const fileUrl = "/modelo-planilha-base.xlsx";
    const link = document.createElement("a");
    link.href = fileUrl;
    link.setAttribute("download", "modelo-planilha-base.xlsx");
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
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
            <div
              className="botao-gerar-container"
              style={{
                marginTop: "20px",
                display: "flex",
                justifyContent: "flex-start",
              }}
            >
              <SmallButton
                description={"Gerar gráfico"}
                filled={true}
                onClick={handleUpload}
                disabled={isLoading}
                isLoading={isLoading} /* Passando a nova prop para animar */
              />
            </div>
          </div>
        </div>
        <h2>Exemplo de modelo da tabela:</h2>
        <img src={Tabela} alt="Pré visualização da tabela" />

        <div>
          <SmallButton
            description={"Baixar Planilha Base"}
            filled={false} // Deixei 'false' para ele ficar com o visual transparente/borda, dando contraste com o botão principal
            onClick={handleDownloadTemplate}
          />
        </div>
      </main>
      <footer>
        <Tips pagina={3} />
      </footer>
    </div>
  );
};

export default GraficoPage;
