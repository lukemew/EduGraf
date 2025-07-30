import { useState } from "react";
import "./FileUpload.css";

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
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

      <span className={`file-name ${!selectedFile ? "no-file" : ""}`}>
        {selectedFile ? selectedFile.name : "Nenhum arquivo selecionado"}
      </span>
    </div>
  );
};

export default FileUpload;
