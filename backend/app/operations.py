import pandas as pd
import os
import tempfile
from datetime import datetime
from typing import List
from fastapi import UploadFile
import io

# Importar as funções do sistema original
from app.utils import (
    process_excel_file_real,
    process_excel_file,
    generate_charts_real,
    generate_charts,
    create_pdf_report,
    debug_dataframe_sections,
    aplicar_formatacao_excel
)

class Operations:
    """Classe simplificada para operações de processamento"""
    
    def __init__(self):
        self.temp_dir = "temp"
        self.upload_dir = "uploads"
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def gerar_tabela_do_polo(self, files: List[UploadFile], polo: str = "Geral") -> str:
        """
        Gera tabela consolidada do polo especificado
        
        Args:
            files: Lista de arquivos Excel
            polo: Nome do polo para filtrar
            
        Returns:
            Caminho do arquivo Excel gerado
        """
        try:
            print(f"📊 Processando tabela para polo: {polo}")
            
            # Processar o primeiro arquivo (ou consolidar múltiplos se necessário)
            file = files[0]
            
            # Ler arquivo
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents), header=None)
            
            print(f"📄 Arquivo lido: {file.filename} - Shape: {df.shape}")
            
            # Detectar formato
            is_real_format = self._check_if_real_format(df)
            print(f"🔍 Formato detectado: {'Real da Prefeitura' if is_real_format else 'Formato Antigo'}")
            
            if is_real_format:
                # Processar formato real
                processed_data = process_excel_file_real(df, polo)
                output_file = self._save_real_format_table(processed_data, polo)
            else:
                # Processar formato antigo
                # Tentar encontrar cabeçalho
                header_row = self._find_header_row(df)
                if header_row is not None:
                    df = pd.read_excel(io.BytesIO(contents), header=header_row)
                
                processed_data = process_excel_file(df, polo)
                output_file = self._save_old_format_table(processed_data, polo)
            
            print(f"✅ Tabela salva em: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Erro no processamento da tabela: {e}")
            raise e
    
    async def gerar_graficos(self, files: List[UploadFile], trimestre: int) -> str:
        """
        Gera gráficos e relatório PDF
        
        Args:
            files: Lista de arquivos Excel
            trimestre: Número do trimestre
            
        Returns:
            Caminho do arquivo PDF gerado
        """
        try:
            print(f"📈 Gerando gráficos para o {trimestre}º trimestre")
            
            # Processar o primeiro arquivo
            file = files[0]
            contents = await file.read()
            df = pd.read_excel(io.BytesIO(contents), header=None)
            
            print(f"📄 Arquivo lido: {file.filename} - Shape: {df.shape}")
            
            # Debug detalhado
            debug_dataframe_sections(df)
            
            # Detectar formato e processar
            is_real_format = self._check_if_real_format(df)
            print(f"🔍 Formato detectado: {'Real da Prefeitura' if is_real_format else 'Formato Antigo'}")
            
            if is_real_format:
                # Processar formato real
                processed_data = process_excel_file_real(df, "Geral")
                charts_data = generate_charts_real(processed_data, trimestre)
            else:
                # Processar formato antigo
                header_row = self._find_header_row(df)
                if header_row is not None:
                    df = pd.read_excel(io.BytesIO(contents), header=header_row)
                
                charts_data = generate_charts(df, trimestre)
            
            # Criar PDF
            pdf_path = create_pdf_report(charts_data, trimestre)
            
            print(f"✅ Relatório PDF gerado: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            print(f"❌ Erro na geração de gráficos: {e}")
            raise e
    
    async def processar_planilhas_simples(self, files: List[UploadFile]) -> dict:
        """
        Versão simplificada que retorna dados em JSON
        Para compatibilidade com o código original
        
        Args:
            files: Lista de arquivos Excel
            
        Returns:
            Dicionário com dados processados
        """
        try:
            results = []
            
            for file in files:
                print(f"📄 Processando arquivo: {file.filename}")
                
                contents = await file.read()
                df = pd.read_excel(io.BytesIO(contents))
                
                # Processar dados básicos
                file_info = {
                    "filename": file.filename,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "columns_names": df.columns.tolist(),
                    "sample_data": df.head(3).to_dict('records') if len(df) > 0 else []
                }
                
                # Tentar detectar tipo de dados
                if self._has_education_columns(df):
                    file_info["type"] = "dados_educacionais"
                    
                    # Estatísticas básicas se for dados educacionais
                    if 'Nome da escola' in df.columns:
                        file_info["total_escolas"] = df['Nome da escola'].nunique()
                    
                    if 'Niveis de Leitura' in df.columns:
                        file_info["distribuicao_leitura"] = df['Niveis de Leitura'].value_counts().to_dict()
                    
                    if 'Niveis de Escrita' in df.columns:
                        file_info["distribuicao_escrita"] = df['Niveis de Escrita'].value_counts().to_dict()
                else:
                    file_info["type"] = "planilha_generica"
                
                results.append(file_info)
            
            return {
                "total_files": len(files),
                "processed_at": datetime.now().isoformat(),
                "files": results
            }
            
        except Exception as e:
            print(f"❌ Erro no processamento simples: {e}")
            raise e
    
    def _check_if_real_format(self, df: pd.DataFrame) -> bool:
        """Verifica se é formato real da prefeitura"""
        try:
            for idx, row in df.head(50).iterrows():
                for value in row:
                    if isinstance(value, str):
                        value_str = str(value).upper()
                        if "DIAGNÓSTICO DE LEITURA" in value_str or "DIAGNÓSTICO DE ESCRITA" in value_str:
                            return True
                        if "NL" in value_str and "LS" in value_str and "LP" in value_str:
                            return True
            return False
        except:
            return False
    
    def _find_header_row(self, df: pd.DataFrame) -> int:
        """Encontra a linha do cabeçalho no formato antigo"""
        try:
            for idx in range(min(20, len(df))):
                row = df.iloc[idx]
                row_str = ' '.join([str(cell).upper() for cell in row if not pd.isna(cell)])
                
                if "NOME DA ESCOLA" in row_str and "MODALIDADE" in row_str:
                    return idx
            return None
        except:
            return None
    
    def _has_education_columns(self, df: pd.DataFrame) -> bool:
        """Verifica se tem colunas educacionais"""
        education_keywords = [
            'nome da escola', 'modalidade', 'niveis de leitura', 
            'niveis de escrita', 'escola', 'polo', 'diagnóstico'
        ]
        
        columns_str = ' '.join(df.columns.astype(str)).lower()
        return any(keyword in columns_str for keyword in education_keywords)
    
    def _save_real_format_table(self, processed_data: dict, polo: str) -> str:
        """Salva tabela do formato real com formatação profissional"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(
            self.temp_dir, 
            f"tabela_real_{polo.replace(' ', '_')}_{timestamp}.xlsx"
        )
        
        # Criar workbook com openpyxl para formatação avançada
        from openpyxl import Workbook
        from openpyxl.utils.dataframe import dataframe_to_rows
        
        wb = Workbook()
        
        # Remover planilha padrão
        wb.remove(wb.active)
        
        # Aba de Leitura
        ws_leitura = wb.create_sheet("Dados de Leitura")
        # INSERE OS DADOS A PARTIR DA LINHA 3
        rows_leitura = dataframe_to_rows(processed_data['leitura'], index=False, header=False)
        for r_idx, row in enumerate(rows_leitura, 3):  # O '3' aqui faz começar da linha 3
            for c_idx, value in enumerate(row, 1):
                ws_leitura.cell(row=r_idx, column=c_idx, value=value)
        # AGORA CHAMA A FORMATAÇÃO
        aplicar_formatacao_excel(ws_leitura, processed_data['leitura'], 
                                f" DADOS DE LEITURA - {polo.upper()}", '1abc9c', 'leitura')

        # Aba de Escrita
        ws_escrita = wb.create_sheet("Dados de Escrita")
        # INSERE OS DADOS A PARTIR DA LINHA 3
        rows_escrita = dataframe_to_rows(processed_data['escrita'], index=False, header=False)
        for r_idx, row in enumerate(rows_escrita, 3): # O '3' aqui faz começar da linha 3
            for c_idx, value in enumerate(row, 1):
                ws_escrita.cell(row=r_idx, column=c_idx, value=value)
        # AGORA CHAMA A FORMATAÇÃO
        aplicar_formatacao_excel(ws_escrita, processed_data['escrita'], 
                                f" DADOS DE ESCRITA - {polo.upper()}", '3498db', 'escrita')
        
       # CÓDIGO COMPLETO E CORRIGIDO PARA A ABA DE ESTATÍSTICAS

        # 1. CRIA o dicionário com os dados, exatamente como antes
        stats_data = {
            'Métrica': [
                'Total de Anos/Séries',
                'Total Alunos (Leitura)',
                'Total Alunos (Escrita)',
                'Média % Não Leitores',
                'Média % Leitores Fluentes',
                'Média % Pré-Silábicos',
                'Média % Ortográficos'
            ],
            'Valor': [
                len(processed_data['leitura']),
                processed_data['leitura']['total alunos'].sum(),
                processed_data['escrita']['total alunos'].sum(),
                f"{processed_data['leitura']['nl_%'].mean():.1f}%",
                f"{processed_data['leitura']['lcf_%'].mean():.1f}%",
                f"{processed_data['escrita']['p_%'].mean():.1f}%",
                f"{processed_data['escrita']['o_%'].mean():.1f}%"
            ]
        }

        # 2. CONVERTE o dicionário para um DataFrame pandas (A LINHA QUE FALTAVA)
        stats_df = pd.DataFrame(stats_data)

        # 3. CRIA a nova aba na planilha
        ws_stats = wb.create_sheet("Resumo Estatístico")

        # 4. ESCREVE o DataFrame manualmente, célula por célula
        # Escreve o cabeçalho
        for c_idx, value in enumerate(stats_df.columns, 1):
            ws_stats.cell(row=2, column=c_idx, value=str(value).title())

        # Escreve as linhas de dados
        for r_idx, row in enumerate(stats_df.itertuples(), 3):
            # row[0] é o índice, row[1] é a Métrica, row[2] é o Valor
            ws_stats.cell(row=r_idx, column=1, value=row[1])
            ws_stats.cell(row=r_idx, column=2, value=row[2])

        # 5. APLICA a formatação final usando a função que já tínhamos
        aplicar_formatacao_excel(ws_stats, stats_df, 
                                f"📈 RESUMO ESTATÍSTICO - {polo.upper()}", 'e74c3c')
        
        # Salvar arquivo
        wb.save(output_file)
        
        return output_file
    
    def _save_old_format_table(self, processed_data: pd.DataFrame, polo: str) -> str:
        """Salva tabela do formato antigo com formatação profissional"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(
            self.temp_dir, 
            f"tabela_antiga_{polo.replace(' ', '_')}_{timestamp}.xlsx"
        )
        
        # Criar workbook com openpyxl para formatação avançada
        from openpyxl import Workbook
        from openpyxl.utils.dataframe import dataframe_to_rows
        
        wb = Workbook()
        
        # Remover planilha padrão
        wb.remove(wb.active)
        
        # Aba de Dados Consolidados
        ws_dados = wb.create_sheet("Dados Consolidados")
        for r in dataframe_to_rows(processed_data, index=False, header=True):
            ws_dados.append(r)
        aplicar_formatacao_excel(ws_dados, processed_data, 
                               f" DADOS CONSOLIDADOS - {polo.upper()}", '1abc9c', 'leitura')
        
        # Estatísticas básicas
        if not processed_data.empty:
            stats_data = {
                'Métrica': [
                    'Total de Escolas',
                    'Total de Alunos',
                    'Média Alunos/Escola',
                    'Escola com Mais Alunos',
                    'Escola com Menos Alunos'
                ],
                'Valor': [
                    len(processed_data),
                    processed_data['Total Alunos'].sum() if 'Total Alunos' in processed_data.columns else 0,
                    f"{processed_data['Total Alunos'].mean():.1f}" if 'Total Alunos' in processed_data.columns else "N/A",
                    processed_data.loc[processed_data['Total Alunos'].idxmax(), 'Escola'] if 'Total Alunos' in processed_data.columns else "N/A",
                    processed_data.loc[processed_data['Total Alunos'].idxmin(), 'Escola'] if 'Total Alunos' in processed_data.columns else "N/A"
                ]
            }
            
            ws_stats = wb.create_sheet("Resumo Estatístico")

            # Vamos escrever o DataFrame manualmente, nos dando controle total.
            # Escreve o cabeçalho primeiro
            for c_idx, value in enumerate(stats_df.columns, 1):
                ws_stats.cell(row=2, column=c_idx, value=value)

            # Escreve as linhas de dados
            for r_idx, row in enumerate(stats_df.itertuples(), 3):
                # row[1] é a Métrica, row[2] é o Valor
                ws_stats.cell(row=r_idx, column=1, value=row[1])
                ws_stats.cell(row=r_idx, column=2, value=row[2])

            # AGORA, a formatação vai funcionar sobre células que já têm o valor correto.
            aplicar_formatacao_excel(ws_stats, stats_df, 
                                    f"📈 RESUMO ESTATÍSTICO - {polo.upper()}", 'e74c3c')
                    
        # Salvar arquivo
        wb.save(output_file)
        
        return output_file

# A classe Operations está pronta para ser instanciada