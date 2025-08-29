import "./Tips.css";
import Ilustracao2 from "../../assets/ilustracao2.png";

const DicasHome = [
  "Vá para a de opção criar tabelas",
  "Você irá fazer o upload da planilha Excel de um polo específico.",
  "O sistema irá processar e padronizar os dados, gerando uma nova planilha organizada como resultado.",
  "Vai ser gerado gráficos de vários polos",
];
const DicasTabela = [
  "As planilhas devem estar no formato Excel (.xlsx).",
  "As planilhas devem conter: nome da escola, modalidade, niveis de leitura e niveis de escrita",
];
const DicasGrafico = [
  "Primeiro é necessário fazer o processo de gerar tabelas",
  "Após elas serem geradas, reúna todas as planilhas e as insira na outra funcionalidade para gerar o gráfico",
];

const Tips = ({ pagina }) => {
  function seletorDeDicas() {
    if (pagina == 1) {
      return DicasHome.map((dica, index) => <li key={index}>{dica}</li>);
    } else if (pagina == 2) {
      return DicasTabela.map((dica, index) => <li key={index}>{dica}</li>);
    } else if (pagina == 3) {
      return DicasGrafico.map((dica, index) => <li key={index}>{dica}</li>);
    }
  }

  return (
    <div id="dicas" className="tips">
      <h2>Instruções</h2>
      <div className="tips-container">
        <img src={Ilustracao2} alt="Ilustração da seção de dicas" />
        <ul>{seletorDeDicas()}</ul>
      </div>
    </div>
  );
};

export default Tips;
