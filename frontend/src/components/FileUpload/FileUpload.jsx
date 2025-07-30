import { useState } from "react";
import "./FileUpload.css";

const FileUpload = ({ onFileSelect }) => {
  const [fileName, setFileName] = useState("Nenhum arquivo selecionado");
  const [isError, setIsError] = useState(true);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFileName(file.name);
      setIsError(false);
      onFileSelect(file); // 👈 AQUI! Chama a função do pai com o arquivo selecionado
    } else {
      setFileName("Nenhum arquivo selecionado");
      setIsError(true);
      onFileSelect(null); // Informa o pai que nenhum arquivo está selecionado
    }
  };

  return (
    <div className="file-upload-container">
      <input
        type="file"
        id="file-input"
        className="file-input"
        onChange={handleFileChange}
        accept=".xlsx"
      />

      <label htmlFor="file-input" className="file-label">
        Enviar arquivo
      </label>

      <span className={`file-name ${!isError ? "no-file" : ""}`}>
        {fileName}
      </span>
    </div>
  );
};

export default FileUpload;
