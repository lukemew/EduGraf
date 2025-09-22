import React, { useState, useId } from "react";
import "./FileUpload.css";

const FileUpload = ({ onFileSelect }) => {
  // Estado interno para guardar o nome do arquivo e exibi-lo na tela
  const [fileName, setFileName] = useState("");

  // MUDANÇA 1: Usar o hook `useId` para gerar um ID único para cada componente
  const uniqueId = useId();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name); // Atualiza o nome do arquivo para exibição
      onFileSelect(file); // Envia o objeto do arquivo completo para o componente pai (GraficoPage)
    } else {
      setFileName("");
      onFileSelect(null);
    }
  };

  return (
    <div className="file-upload-container">
      {/* A label agora envolve o input e o texto, tornando toda a área clicável.
        O texto muda dinamicamente para mostrar o nome do arquivo ou a mensagem inicial.
      */}
      <label htmlFor={uniqueId} className="file-upload-label">
        {fileName || "Clique para selecionar o arquivo"}
      </label>
      <input
        id={uniqueId} // MUDANÇA 2: Usa o ID único gerado
        type="file"
        onChange={handleFileChange}
        accept=".xlsx, .xls"
        className="file-upload-input" // Este input fica escondido, a label é a parte visível
        // MUDANÇA 3: O atributo `multiple` foi removido
      />
    </div>
  );
};

export default FileUpload;
