import "./Tips.css";
import Ilustracao2 from "../../assets/ilustracao2.png";

const DicasHome = [
  "Vá para a de opção criar tabelas",
  "Irá ser criado a tabela de um polo",
  "Agora vá para segunda opção",
  "Vai ser gerado gráficos de vários polos",
];
const DicasTabela = [
  "As planilhas devem estar no formato Excel (.xlsx).",
  "Planilha preenchida com o modelo padrão",
  "As planilhas deve conter,Nome da escola,Modalidade,Niveis de Leitura e Niveis de Escrita",
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
      <h2>Dicas</h2>
      <div className="tips-container">
        <img src={Ilustracao2} alt="Ilustração da seção de dicas" />
        <ul>{seletorDeDicas()}</ul>
      </div>
    </div>
  );
};

export default Tips;
