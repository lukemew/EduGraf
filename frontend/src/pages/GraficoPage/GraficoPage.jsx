import "./GraficoPage.css";
import Navbar from "../../components/Navbar/Navbar";
import Select from "../../components/Select/Select";
import SmallButton from "../../components/SmallButton/SmallButton";
import FileUpload from "../../components/FileUpload/FileUpload";
import Tips from "../../components/Tips/Tips";
import { useNotificationContext } from "../../contexts/NotificationContext";
import { useState } from "react";
import axios from "axios";
import Grafico from "../../assets/grafico-exemplo.png";

const GraficoPage = () => {
  // 1. Estado para guardar o valor do polo selecionado.
  //    Inicializamos com 'Polo 1' como padrão.
  const [selectedAmount, setSelectedAmount] = useState(1);
  const [selectedFile, setSelectedFile] = useState(null);
  const { showSuccess, showError } = useNotificationContext();
  // 2. Estado para guardar o arquivo selecionado (vindo do componente FileUpload).

  const handleAmountChange = (e) => {
    const amount = parseInt(e.target.value, 10);
    setSelectedAmount(amount);
    setSelectedFile(null);
  };

  // Manipulador para o envio do formulário
  const handleUpload = async () => {
    if (!selectedFile) {
      showError(
        "Arquivo não selecionado",
        "Por favor, selecione um arquivo Excel (.xlsx) antes de continuar."
      );
      return;
    }

    const formData = new FormData();
    formData.append("quant_trimestre", selectedAmount.toString());
    formData.append("file", selectedFile);
    formData.append("tipo_processamento", "grafico");  // Forçar processamento como gráfico

    console.log("🔍 DEBUG: Enviando para o backend:", {
      quant_trimestre: selectedAmount,
      file: selectedFile.name,
    });

    // Debug: verificar se quant_trimestre é um número
    console.log("🔍 DEBUG: Tipo de quant_trimestre:", typeof selectedAmount);
    console.log("🔍 DEBUG: Valor de quant_trimestre:", selectedAmount);
    console.log("🔍 DEBUG: Esta é a página de GRÁFICOS - deve gerar .pdf");
    console.log("🔍 DEBUG: Se você quer .xlsx, vá para a página de TABELAS");

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

      // Debug: Verificar headers da resposta
      console.log("🔍 DEBUG: Headers da resposta:", response.headers);
      console.log("🔍 DEBUG: Content-Type:", response.headers["content-type"]);
      console.log(
        "🔍 DEBUG: Content-Disposition:",
        response.headers["content-disposition"]
      );
      console.log("🔍 DEBUG: Status code:", response.status);

      // Verificar se a resposta é válida
      if (response.data.size === 0) {
        throw new Error("Resposta vazia do servidor");
      }

      // Debug: Verificar se é realmente um PDF
      const blob = new Blob([response.data]);
      console.log("📏 Tamanho do blob:", blob.size, "bytes");

      // Verificar os primeiros bytes para confirmar se é PDF
      const arrayBuffer = await blob.arrayBuffer();
      const uint8Array = new Uint8Array(arrayBuffer);
      const firstBytes = uint8Array.slice(0, 4);
      const header = String.fromCharCode(...firstBytes);
      console.log("🔍 Primeiros bytes:", header);

      if (header === "%PDF") {
        console.log("✅ Confirmed: É um PDF válido");
      } else {
        console.log("❌ Warning: Não parece ser um PDF válido");
      }

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `relatorio_graficos_${selectedAmount}_trimestre_${new Date()
          .toISOString()
          .slice(0, 10)}.pdf`
      ); // Nome dinâmico para o download
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);

      // Mensagem de sucesso
      showSuccess(
        "📈 Relatório de Gráficos Gerado!",
        `O relatório do ${selectedAmount}º trimestre foi processado com sucesso! O PDF com gráficos e análises detalhadas será baixado automaticamente.`
      );
    } catch (error) {
      console.error("Erro ao fazer upload:", error);

      // Tentar ler a mensagem de erro do backend
      let errorMessage = "Ocorreu um erro ao gerar o gráfico.";

      if (error.response && error.response.data) {
        try {
          const errorText = await error.response.data.text();
          if (errorText) {
            errorMessage = `Erro: ${errorText}`;
          }
        } catch (e) {
          // Se não conseguir ler o erro, usar mensagem padrão
        }
      }

      showError(
        "❌ Erro ao Gerar Relatório",
        errorMessage
      );
    }
  };

  return (
    <div>
      <header>
        <Navbar />
      </header>
      <main className="tabelas_container">
        <h2>Gerar gráficos do Polo</h2>
        <div className="select_container--polo">
          <p>Qual trimestre você deseja?</p>
          <Select
            type={"trimestre"}
            value={selectedAmount}
            onChange={handleAmountChange}
          />
          <p>Selecione a planilha do trimestre:</p>
          <div className="select_container--upload">
            <FileUpload onFileSelect={setSelectedFile} />
            <SmallButton
              className="upload_button"
              description={"Gerar gráfico"}
              filled={true}
              onClick={handleUpload}
            />
          </div>
        </div>

        <img src={Grafico} alt="Pré visualização da tabela" />
      </main>
      <footer>
        <Tips pagina={3} />
      </footer>
    </div>
  );
};

export default GraficoPage;
