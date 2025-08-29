import "./Tips.css";
import Ilustracao2 from "../../assets/ilustracao2.png";

const DicasHome = [
  "Bem-vindo ao EduGraf, sua ferramenta para automatizar a análise de dados da educação.",
  "O sistema funciona em duas etapas principais: primeiro as Tabelas, depois os Gráficos.",
  "ETAPA 1: Comece em 'Tabelas' para organizar os dados de cada polo individualmente.",
  "ETAPA 2: Em seguida, vá para 'Gráficos' para criar a visualização com os dados de todos os polos juntos.",
  "Siga a ordem recomendada (Tabelas -> Gráficos) para garantir que os resultados estejam corretos.",
];

const DicasTabela = [
  "Nesta etapa, você irá preparar e organizar os dados de um polo por vez.",
  "FORMATO DO ARQUIVO: É necessário que a planilha esteja no formato Excel (.xlsx).",
  "COLUNAS DA PLANILHA: O arquivo precisa ter exatamente estas colunas: 'nome da escola', 'modalidade', 'niveis de leitura' e 'niveis de escrita'.",
  "COMO FUNCIONA: O sistema irá conferir e arrumar os dados, liberando um novo arquivo organizado para download.",
  "RESULTADO: O arquivo gerado aqui será o arquivo base que você usará para criar os gráficos.",
];

const DicasGrafico = [
  "Esta etapa final junta todas as informações para criar os gráficos do projeto.",
  "ANTES DE COMEÇAR: É importante já ter passado todas as planilhas dos polos pela etapa 'Tabelas'.",
  "ARQUIVO PARA UPLOAD: Utilize a planilha geral, que une os dados de todos os arquivos que você já organizou.",
  "O QUE ACONTECE: A ferramenta irá ler a planilha com todos os dados para poder criar os gráficos de desempenho.",
  "RESULTADO FINAL: Os gráficos serão mostrados na tela e você poderá baixar um relatório em Excel com tudo consolidado.",
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
