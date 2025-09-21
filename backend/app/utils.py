import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Dict, Any
import io
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo

# Configuração do matplotlib para não usar interface gráfica
plt.switch_backend('Agg')

# Configurar estilo dos gráficos
plt.style.use('default')
sns.set_palette("husl")

def aplicar_formatacao_excel(worksheet, df, titulo, cor_cabecalho='1abc9c', tipo_dados='leitura'):
    """
    Aplica formatação profissional a uma planilha Excel
    
    Args:
        worksheet: Worksheet do openpyxl
        df: DataFrame com os dados
        titulo: Título da planilha
        cor_cabecalho: Cor do cabeçalho (hex)
        tipo_dados: 'leitura' ou 'escrita' para adicionar legendas
    """
    # Cores do projeto EduGraf
    cores = {
        'primaria': '3d626d',
        'secundaria': '165b70', 
        'destaque': '1abc9c',
        'fundo_claro': 'f8f9fa',
        'texto_escuro': '333333',
        'borda': 'dee2e6'
    }
    
    # Estilos de fonte
    fonte_titulo = Font(name='Arial', size=16, bold=True, color='FFFFFF')
    fonte_cabecalho = Font(name='Arial', size=12, bold=True, color='FFFFFF')
    fonte_normal = Font(name='Arial', size=11, color=cores['texto_escuro'])
    fonte_numero = Font(name='Arial', size=11, color=cores['texto_escuro'])
    
    # Estilos de preenchimento
    preenchimento_titulo = PatternFill(start_color=cores['secundaria'], end_color=cores['secundaria'], fill_type='solid')
    preenchimento_cabecalho = PatternFill(start_color=cor_cabecalho, end_color=cor_cabecalho, fill_type='solid')
    preenchimento_linha_par = PatternFill(start_color=cores['fundo_claro'], end_color=cores['fundo_claro'], fill_type='solid')
    
    # Estilos de alinhamento
    alinhamento_centro = Alignment(horizontal='center', vertical='center')
    alinhamento_esquerda = Alignment(horizontal='left', vertical='center')
    alinhamento_direita = Alignment(horizontal='right', vertical='center')
    
    # Estilos de borda
    borda_fina = Border(
        left=Side(style='thin', color=cores['borda']),
        right=Side(style='thin', color=cores['borda']),
        top=Side(style='thin', color=cores['borda']),
        bottom=Side(style='thin', color=cores['borda'])
    )
    
    # Adicionar título
    # Calcular o número de colunas necessárias para o título
    num_colunas = len(df.columns) if len(df.columns) > 0 else 8
    ultima_coluna = chr(65 + num_colunas - 1)  # A, B, C, etc.
    
    worksheet.merge_cells(f'A1:{ultima_coluna}1')
    cell_titulo = worksheet['A1']
    cell_titulo.value = titulo
    cell_titulo.font = fonte_titulo
    cell_titulo.fill = preenchimento_titulo
    cell_titulo.alignment = alinhamento_centro
    
    # Função para formatar nomes das colunas
    def formatar_nome_coluna(nome):
        """Formata o nome da coluna para melhor apresentação"""
        formatacoes = {
            'ano': 'Ano',
            'total alunos': 'Total de Alunos',
            'nl': 'NL',
            'ls': 'LS', 
            'lp': 'LP',
            'lf': 'LF',
            'lsf': 'LSF',
            'lcf': 'LCF',
            'p': 'P',
            's': 'S',
            's.a.': 'S.A.',
            'a': 'A',
            'o': 'O',
            'nl_%': 'NL %',
            'ls_%': 'LS %',
            'lp_%': 'LP %',
            'lf_%': 'LF %',
            'lsf_%': 'LSF %',
            'lcf_%': 'LCF %',
            'p_%': 'P %',
            's_%': 'S %',
            's.a._%': 'S.A. %',
            'a_%': 'A %',
            'o_%': 'O %'
        }
        return formatacoes.get(nome.lower(), nome.title())
    
    # Aplicar formatação aos cabeçalhos
    for col_num, column_title in enumerate(df.columns, 1):
        cell = worksheet.cell(row=2, column=col_num)
        cell.value = formatar_nome_coluna(column_title)
        cell.font = fonte_cabecalho
        cell.fill = preenchimento_cabecalho
        cell.alignment = alinhamento_centro
        cell.border = borda_fina
    
    # Aplicar formatação aos dados
    for row_num in range(3, len(df) + 3):
        for col_num in range(1, len(df.columns) + 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.font = fonte_normal
            cell.border = borda_fina
            
            # Alternar cores das linhas
            if row_num % 2 == 0:
                cell.fill = preenchimento_linha_par
            
                 # Alinhamento baseado no tipo de dados
            if col_num == 1:  # Primeira coluna (Métrica)
                cell.alignment = alinhamento_esquerda
            else:  # Segunda coluna (Valor)
                cell.alignment = alinhamento_centro 
                
                # --- LÓGICA ESPECIAL PARA A ABA DE ESTATÍSTICAS ---
                if "RESUMO ESTATÍSTICO" in titulo.upper():
                    # Pega o nome da métrica na primeira coluna da mesma linha
                    celula_metrica = worksheet.cell(row=row_num, column=1).value
                    
                    # Se a métrica for "Total Alunos", adiciona o (100%)
                    if "TOTAL ALUNOS" in str(celula_metrica).upper():
                        valor_numerico = cell.value
                        cell.value = f"{valor_numerico} (100%)"
                        cell.number_format = '@'  # Força a célula a ser tratada como texto
                    else:
                        # Para as outras linhas (que já são %), mantém o valor
                        # e aplica o formato de texto para garantir consistência.
                        cell.number_format = '@'
                
                # --- Lógica original para as outras abas (Leitura/Escrita) ---
                else:
                    if isinstance(cell.value, (int, float)):
                        if cell.value < 1:  # Percentuais
                            cell.number_format = '0'
                        else:  # Números inteiros
                            cell.number_format = '#,##0'
    
    # Ajustar largura das colunas com valores mínimos
    larguras_minimas = {
        'A': 8,   # Ano
        'B': 25,  # Total de Alunos
        'C': 8,   # NL, LS, etc.
        'D': 8,   # Percentuais
        'E': 8,
        'F': 8,
        'G': 8,
        'H': 8,
        'I': 10,
        'J': 10,
        'K': 10,
        'L': 10,
        'M': 12,
        'N': 12
    }
    
    for col_idx, column in enumerate(worksheet.columns):
        max_length = 0
        column_letter = None
        
        # Encontrar a primeira célula não mesclada para obter a letra da coluna
        for cell in column:
            try:
                if hasattr(cell, 'column_letter'):
                    column_letter = cell.column_letter
                    break
            except:
                continue
        
        if column_letter is None:
            continue
            
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        
        # Usar largura mínima ou calculada, o que for maior
        largura_minima = larguras_minimas.get(column_letter, 10)
        adjusted_width = max(largura_minima, min(max_length + 3, 25))
        worksheet.column_dimensions[column_letter].width = adjusted_width
    
    # Adicionar filtros
    if len(df) > 0 and len(df.columns) > 0:
        ultima_coluna = chr(65 + len(df.columns) - 1)
        ultima_linha = len(df) + 2
        worksheet.auto_filter.ref = f"A2:{ultima_coluna}{ultima_linha}"
    
    # Adicionar legendas explicativas
    linha_legenda = len(df) + 4  # 2 linhas após os dados
    
    # Título da legenda
    cell_legenda_titulo = worksheet.cell(row=linha_legenda, column=1)
    cell_legenda_titulo.value = " LEGENDA - SIGNIFICADO DAS ABREVIAÇÕES"
    cell_legenda_titulo.font = Font(name='Arial', size=12, bold=True, color='FFFFFF')
    cell_legenda_titulo.fill = PatternFill(start_color=cores['secundaria'], end_color=cores['secundaria'], fill_type='solid')
    cell_legenda_titulo.alignment = alinhamento_centro
    
    # Mesclar células do título da legenda
    ultima_coluna_legenda = chr(65 + min(len(df.columns) - 1, 6))  # Máximo 7 colunas
    worksheet.merge_cells(f'A{linha_legenda}:{ultima_coluna_legenda}{linha_legenda}')
    
    if tipo_dados == 'leitura':
        # Legendas para leitura
        legendas_leitura = [
            ("NL", "Não Leitor - Aluno que não consegue ler"),
            ("LS", "Leitor Silábico - Lê sílaba por sílaba"),
            ("LP", "Leitor Palavra - Lê palavra por palavra"),
            ("LF", "Leitor Frase - Lê frase por frase"),
            ("LSF", "Leitor Silábico com Fluência - Lê sílabas com fluência"),
            ("LCF", "Leitor com Fluência - Lê com fluência total")
        ]
        
        for idx, (abrev, descricao) in enumerate(legendas_leitura):
            linha_atual = linha_legenda + 1 + idx
            
            # Abreviação
            cell_abrev = worksheet.cell(row=linha_atual, column=1)
            cell_abrev.value = abrev
            cell_abrev.font = Font(name='Arial', size=11, bold=True, color=cores['texto_escuro'])
            cell_abrev.fill = PatternFill(start_color='f0f8ff', end_color='f0f8ff', fill_type='solid')
            cell_abrev.alignment = alinhamento_centro
            cell_abrev.border = borda_fina
            
            # Descrição
            cell_desc = worksheet.cell(row=linha_atual, column=2)
            cell_desc.value = descricao
            cell_desc.font = Font(name='Arial', size=10, color=cores['texto_escuro'])
            cell_desc.fill = PatternFill(start_color='f0f8ff', end_color='f0f8ff', fill_type='solid')
            cell_desc.alignment = alinhamento_esquerda
            cell_desc.border = borda_fina
            
            # Mesclar células da descrição
            worksheet.merge_cells(f'B{linha_atual}:{ultima_coluna_legenda}{linha_atual}')
    
    elif tipo_dados == 'escrita':
        # Legendas para escrita
        legendas_escrita = [
            ("P", "Pré-Silábico - Não relaciona som e letra"),
            ("S", "Silábico - Escreve uma letra por sílaba"),
            ("S.A.", "Silábico Alfabético - Mistura sílaba e letra"),
            ("A", "Alfabético - Escreve todas as letras"),
            ("O", "Ortográfico - Escreve corretamente")
        ]
        
        for idx, (abrev, descricao) in enumerate(legendas_escrita):
            linha_atual = linha_legenda + 1 + idx
            
            # Abreviação
            cell_abrev = worksheet.cell(row=linha_atual, column=1)
            cell_abrev.value = abrev
            cell_abrev.font = Font(name='Arial', size=11, bold=True, color=cores['texto_escuro'])
            cell_abrev.fill = PatternFill(start_color='f0f8ff', end_color='f0f8ff', fill_type='solid')
            cell_abrev.alignment = alinhamento_centro
            cell_abrev.border = borda_fina
            
            # Descrição
            cell_desc = worksheet.cell(row=linha_atual, column=2)
            cell_desc.value = descricao
            cell_desc.font = Font(name='Arial', size=10, color=cores['texto_escuro'])
            cell_desc.fill = PatternFill(start_color='f0f8ff', end_color='f0f8ff', fill_type='solid')
            cell_desc.alignment = alinhamento_esquerda
            cell_desc.border = borda_fina
            
            # Mesclar células da descrição
            worksheet.merge_cells(f'B{linha_atual}:{ultima_coluna_legenda}{linha_atual}')
    
    # Congelar painéis (cabeçalho sempre visível)
    worksheet.freeze_panes = 'A3'
    print("Ajustando dimensões personalizadas...")
    if "RESUMO ESTATÍSTICO" in titulo.upper():
        print("Aplicando dimensões personalizadas para a aba de Resumo Estatístico...")

        # LARGURA DAS COLUNAS para a aba de estatísticas
        worksheet.column_dimensions['A'].width = 40  # Coluna 'Métrica'
        worksheet.column_dimensions['B'].width = 25  # Coluna 'Valor'

        # ALTURA DAS LINHAS para a aba de estatísticas
        worksheet.row_dimensions[1].height = 40  # Linha do Título Principal
        worksheet.row_dimensions[2].height = 30  # Linha do Cabeçalho ('Métrica', 'Valor')
    
    else:
        # Dimensões para as outras abas (Leitura e Escrita)
        print(f"Aplicando dimensões padrão para a aba '{titulo}'...")
        worksheet.column_dimensions['A'].width = 15 # Coluna 'Ano'
        worksheet.column_dimensions['B'].width = 20 # Coluna 'Total de Alunos'


    print(f"--- FIM DO DIAGNÓSTICO PARA A ABA: '{titulo}' ---\n")
    
    return worksheet

def criar_dataframe(arquivo_em_bytes, linhas_a_serem_puladas, colunas_a_serem_usadas):
    """
    Cria DataFrame a partir de bytes do arquivo Excel
    
    Args:
        arquivo_em_bytes: Bytes do arquivo Excel
        linhas_a_serem_puladas: Lista de linhas para pular
        colunas_a_serem_usadas: Lista de colunas para usar
    
    Returns:
        DataFrame processado
    """
    df = pd.read_excel(BytesIO(arquivo_em_bytes), 
                       skiprows=linhas_a_serem_puladas,
                       usecols=colunas_a_serem_usadas)
    return df

def process_excel_file_real(df: pd.DataFrame, polo: str) -> Dict[str, Any]:
    """
    Processa planilha Excel real da prefeitura e consolida dados
    CORRIGIDO: Agora lê todas as linhas disponíveis, não apenas 5
    
    Args:
        df: DataFrame com os dados da planilha
        polo: Nome do polo para filtrar
    
    Returns:
        Dicionário com dados processados
    """
    try:
        print(f"🔍 DEBUG: Iniciando processamento do formato real")
        print(f"🔍 DEBUG: DataFrame original shape: {df.shape}")
        
        # Configurações para leitura (suas configurações originais)
        linhas_para_pular_leitura = [0, 1, 2, 3, 4, 5, 12, 17, 20, 21, 22, *range(23, 45)]
        linhas_para_pular_escrita = [*range(0, 27), 33, 38, 41, 42, 43, 44]
        cols_leitura = list(range(0, 14))
        cols_escrita = list(range(0, 12))
        
        columns_leitura = ["ano", "total alunos", "nl", "nl%", "ls", "ls%", "lp", "lp%", "lf", "lf%", "lsf", "lsf%", "lcf", "lcf%"]
        columns_escrita = ["ano", "total alunos", "p", "p%", "s", "s%", "s.a.", "s.a%", "a", "a%", "o", "o%"]
        
        print(f"🔍 DEBUG: Linhas para pular leitura: {linhas_para_pular_leitura}")
        print(f"🔍 DEBUG: Linhas para pular escrita: {linhas_para_pular_escrita}")
        
        # SEÇÃO DE LEITURA - Identificar todas as linhas válidas
        print(f"🔍 DEBUG: === PROCESSANDO SEÇÃO DE LEITURA ===")
        
        # Encontrar a linha inicial da seção de leitura (procurar por indicadores)
        inicio_leitura = None
        for idx in range(min(50, len(df))):
            if idx >= len(df):
                break
            row = df.iloc[idx]
            for value in row:
                if pd.notna(value):
                    value_str = str(value).upper()
                    if "DIAGNÓSTICO DE LEITURA" in value_str or "LEITURA" in value_str:
                        inicio_leitura = idx
                        print(f"🔍 DEBUG: Seção de leitura encontrada na linha {idx}")
                        break
            if inicio_leitura is not None:
                break
        
        # Se não encontrar, usar posição padrão
        if inicio_leitura is None:
            inicio_leitura = 6
            print(f"🔍 DEBUG: Usando posição padrão para leitura: {inicio_leitura}")
        
        # Ler dados de leitura - encontrar todas as linhas com dados válidos
        df_leitura_raw = []
        max_linha_leitura = min(inicio_leitura + 50, len(df))  # Buscar nas próximas 50 linhas
        
        for idx in range(inicio_leitura, max_linha_leitura):
            if idx in linhas_para_pular_leitura:
                continue
                
            if idx >= len(df):
                break
                
            row = df.iloc[idx, :len(cols_leitura)]  # Pegar apenas as colunas necessárias
            
            # Verificar se a linha tem dados válidos (pelo menos o primeiro campo não vazio)
            if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip() != '':
                # Verificar se parece ser uma linha de dados (tem números ou anos)
                primeiro_valor = str(row.iloc[0]).strip()
                pv_upper = primeiro_valor.upper()

                # A nova lógica é: a linha é válida se começar com 'EJA', ou se o primeiro caractere for um número,
                # ou se for a palavra exata 'ANO' ou 'SÉRIE' (para pegar o cabeçalho).
                if (pv_upper.startswith('EJA') or
                    (len(primeiro_valor) > 0 and primeiro_valor[0].isdigit()) or
                    pv_upper == 'ANO' or
                    pv_upper == 'SÉRIE'):
                    df_leitura_raw.append(row.tolist())
                    print(f"🔍 DEBUG: Linha de leitura válida {idx}: {primeiro_valor}")
        
        print(f"🔍 DEBUG: Total de linhas de leitura encontradas: {len(df_leitura_raw)}")
        
        # Criar DataFrame de leitura
        if df_leitura_raw:
            df_leitura = pd.DataFrame(df_leitura_raw, columns=columns_leitura[:len(df_leitura_raw[0])])
            # Completar colunas faltantes se necessário
            for col in columns_leitura:
                if col not in df_leitura.columns:
                    df_leitura[col] = 0
            df_leitura = df_leitura[columns_leitura]  # Reordenar colunas
        else:
            # Fallback para método original se não encontrar dados
            print("🔍 DEBUG: Usando método fallback para leitura")
            df_leitura = df.iloc[inicio_leitura:inicio_leitura+15, 0:14].copy()
            df_leitura.columns = columns_leitura
        
        print(f"🔍 DEBUG: DataFrame de leitura shape: {df_leitura.shape}")
        print(f"🔍 DEBUG: Primeiras linhas de leitura:\n{df_leitura.head()}")
        
        # SEÇÃO DE ESCRITA - Identificar todas as linhas válidas
        print(f"🔍 DEBUG: === PROCESSANDO SEÇÃO DE ESCRITA ===")
        
        # Encontrar a linha inicial da seção de escrita
        inicio_escrita = None
        for idx in range(min(50, len(df))):
            if idx >= len(df):
                break
            row = df.iloc[idx]
            for value in row:
                if pd.notna(value):
                    value_str = str(value).upper()
                    if "DIAGNÓSTICO DE ESCRITA" in value_str or ("ESCRITA" in value_str and "LEITURA" not in value_str):
                        inicio_escrita = idx
                        print(f"🔍 DEBUG: Seção de escrita encontrada na linha {idx}")
                        break
            if inicio_escrita is not None:
                break
        
        # Se não encontrar, usar posição padrão
        if inicio_escrita is None:
            inicio_escrita = 28
            print(f"🔍 DEBUG: Usando posição padrão para escrita: {inicio_escrita}")
        
        # Ler dados de escrita - encontrar todas as linhas com dados válidos
        df_escrita_raw = []
        max_linha_escrita = min(inicio_escrita + 50, len(df))  # Buscar nas próximas 50 linhas
        
        for idx in range(inicio_escrita, max_linha_escrita):
            if idx in linhas_para_pular_escrita:
                continue
                
            if idx >= len(df):
                break
                
            row = df.iloc[idx, :len(cols_escrita)]  # Pegar apenas as colunas necessárias
            
            # Verificar se a linha tem dados válidos
            if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip() != '':
                primeiro_valor = str(row.iloc[0]).strip()
                pv_upper = primeiro_valor.upper()

                # A nova lógica é: a linha é válida se começar com 'EJA', ou se o primeiro caractere for um número,
                # ou se for a palavra exata 'ANO' ou 'SÉRIE' (para pegar o cabeçalho).
                if (pv_upper.startswith('EJA') or
                    (len(primeiro_valor) > 0 and primeiro_valor[0].isdigit()) or
                    pv_upper == 'ANO' or
                    pv_upper == 'SÉRIE'):

                    df_escrita_raw.append(row.tolist())
                    print(f"🔍 DEBUG: Linha de escrita válida {idx}: {primeiro_valor}")
        
        print(f"🔍 DEBUG: Total de linhas de escrita encontradas: {len(df_escrita_raw)}")
        
        # Criar DataFrame de escrita
        if df_escrita_raw:
            df_escrita = pd.DataFrame(df_escrita_raw, columns=columns_escrita[:len(df_escrita_raw[0])])
            # Completar colunas faltantes se necessário
            for col in columns_escrita:
                if col not in df_escrita.columns:
                    df_escrita[col] = 0
            df_escrita = df_escrita[columns_escrita]  # Reordenar colunas
        else:
            # Fallback para método original se não encontrar dados
            print("🔍 DEBUG: Usando método fallback para escrita")
            df_escrita = df.iloc[inicio_escrita:inicio_escrita+15, 0:12].copy()
            df_escrita.columns = columns_escrita
        
        print(f"🔍 DEBUG: DataFrame de escrita shape: {df_escrita.shape}")
        print(f"🔍 DEBUG: Primeiras linhas de escrita:\n{df_escrita.head()}")
        
        # PROCESSAMENTO DOS DADOS
        print(f"🔍 DEBUG: === PROCESSANDO DADOS NUMÉRICOS ===")
        
        # Converter colunas numéricas para leitura
        numeric_cols_leitura = ['total alunos', 'nl', 'ls', 'lp', 'lf', 'lsf', 'lcf']
        numeric_cols_escrita = ['total alunos', 'p', 's', 's.a.', 'a', 'o']
        
        for col in numeric_cols_leitura:
            if col in df_leitura.columns:
                df_leitura[col] = pd.to_numeric(df_leitura[col], errors='coerce')
        
        for col in numeric_cols_escrita:
            if col in df_escrita.columns:
                df_escrita[col] = pd.to_numeric(df_escrita[col], errors='coerce')
        
        # Preencher NaN com 0
        df_leitura = df_leitura.fillna(0).infer_objects(copy=False)
        df_escrita = df_escrita.fillna(0).infer_objects(copy=False)
        
        # Remover linhas completamente vazias (onde todas as colunas numéricas são 0)
        df_leitura = df_leitura[df_leitura[numeric_cols_leitura].sum(axis=1) > 0]
        df_escrita = df_escrita[df_escrita[numeric_cols_escrita].sum(axis=1) > 0]
        
        print(f"🔍 DEBUG: Após limpeza - Leitura: {len(df_leitura)} linhas, Escrita: {len(df_escrita)} linhas")
        
        # Processar dados de leitura - agrupar se necessário
        if 'ano' in df_leitura.columns:
            df_leitura_soma = df_leitura.groupby('ano').agg({
                col: 'sum' for col in numeric_cols_leitura
            }).reset_index()
        else:
            df_leitura_soma = df_leitura.copy()
        
        # Recalcular percentuais de leitura
        if len(df_leitura_soma) > 0:
            total_col = df_leitura_soma['total alunos'] 
            df_leitura_soma['nl_%'] = (df_leitura_soma['nl'] / total_col * 100).fillna(0).round(2)
            df_leitura_soma['ls_%'] = (df_leitura_soma['ls'] / total_col * 100).fillna(0).round(2)
            df_leitura_soma['lp_%'] = (df_leitura_soma['lp'] / total_col * 100).fillna(0).round(2)
            df_leitura_soma['lf_%'] = (df_leitura_soma['lf'] / total_col * 100).fillna(0).round(2)
            df_leitura_soma['lsf_%'] = (df_leitura_soma['lsf'] / total_col * 100).fillna(0).round(2)
            df_leitura_soma['lcf_%'] = (df_leitura_soma['lcf'] / total_col * 100).fillna(0).round(2)
        
        # Processar dados de escrita - agrupar se necessário
        if 'ano' in df_escrita.columns:
            df_escrita_soma = df_escrita.groupby('ano').agg({
                col: 'sum' for col in numeric_cols_escrita
            }).reset_index()
        else:
            df_escrita_soma = df_escrita.copy()
        
        # Recalcular percentuais de escrita
        if len(df_escrita_soma) > 0:
            total_col = df_escrita_soma['total alunos']
            df_escrita_soma['p_%'] = (df_escrita_soma['p'] / total_col * 100).fillna(0).round(2)
            df_escrita_soma['s_%'] = (df_escrita_soma['s'] / total_col * 100).fillna(0).round(2)
            df_escrita_soma['s.a._%'] = (df_escrita_soma['s.a.'] / total_col * 100).fillna(0).round(2)
            df_escrita_soma['a_%'] = (df_escrita_soma['a'] / total_col * 100).fillna(0).round(2)
            df_escrita_soma['o_%'] = (df_escrita_soma['o'] / total_col * 100).fillna(0).round(2)
        
        print(f"🔍 DEBUG: === RESULTADO FINAL ===")
        print(f"🔍 DEBUG: Linhas finais de leitura: {len(df_leitura_soma)}")
        print(f"🔍 DEBUG: Linhas finais de escrita: {len(df_escrita_soma)}")
        print(f"🔍 DEBUG: Dados de leitura:\n{df_leitura_soma}")
        print(f"🔍 DEBUG: Dados de escrita:\n{df_escrita_soma}")
        
        return {
            'leitura': df_leitura_soma,
            'escrita': df_escrita_soma,
            'polo': polo
        }
        
    except Exception as e:
        print(f"🔍 DEBUG: Erro no processamento da planilha real: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Erro no processamento da planilha real: {str(e)}")

# Função auxiliar para debugging melhorado
def debug_dataframe_sections(df: pd.DataFrame):
    """Debug detalhado das seções do DataFrame"""
    print(f"🔍 DEBUG: === ANÁLISE DETALHADA DO DATAFRAME ===")
    print(f"🔍 DEBUG: Shape total: {df.shape}")
    
    # Procurar seções
    secoes_encontradas = []
    
    for idx in range(len(df)):
        if idx >= len(df):
            break
            
        row = df.iloc[idx]
        for col_idx, value in enumerate(row):
            if pd.notna(value):
                value_str = str(value).upper()
                
                if "LEITURA" in value_str:
                    secoes_encontradas.append(f"LEITURA na linha {idx}, coluna {col_idx}: '{value}'")
                elif "ESCRITA" in value_str:
                    secoes_encontradas.append(f"ESCRITA na linha {idx}, coluna {col_idx}: '{value}'")
                elif any(ano in value_str for ano in ["1° ANO", "2° ANO", "3° ANO", "4° ANO", "5° ANO", "6° ANO", "7° ANO", "8° ANO", "9° ANO"]):
                    secoes_encontradas.append(f"ANO na linha {idx}, coluna {col_idx}: '{value}'")
    
    print(f"🔍 DEBUG: Seções encontradas:")
    for secao in secoes_encontradas[:20]:  # Mostrar apenas as primeiras 20
        print(f"🔍 DEBUG:   {secao}")
    
    # Mostrar estatísticas por linha
    print(f"🔍 DEBUG: === ESTATÍSTICAS POR LINHA (primeiras 50) ===")
    for idx in range(min(50, len(df))):
        if idx >= len(df):
            break
            
        row = df.iloc[idx]
        valores_nao_vazios = [str(v)[:20] for v in row if pd.notna(v) and str(v).strip() != '']
        
        if valores_nao_vazios:
            print(f"🔍 DEBUG: L{idx:2d}: {' | '.join(valores_nao_vazios[:3])}{'...' if len(valores_nao_vazios) > 3 else ''}")


def process_excel_file(df: pd.DataFrame, polo: str) -> pd.DataFrame:
    """
    Processa planilha Excel e consolida dados por escola e polo (formato antigo)
    
    Args:
        df: DataFrame com os dados da planilha
        polo: Nome do polo para filtrar
    
    Returns:
        DataFrame processado com dados consolidados
    """
    try:
        # Limpar dados
        df = df.dropna()
        
        # Validar colunas
        required_columns = ['Nome da escola', 'Modalidade', 'Niveis de Leitura', 'Niveis de Escrita']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Coluna obrigatória '{col}' não encontrada")
        
        # Filtrar por polo (se necessário)
        if polo and polo != "Geral":
            df = df[df['Nome da escola'].str.contains(polo, case=False, na=False)]
        
        # Calcular estatísticas por escola
        consolidated_data = []
        
        for escola in df['Nome da escola'].unique():
            escola_data = df[df['Nome da escola'] == escola]
            
            # Calcular médias e totais
            total_alunos = len(escola_data)
            
            # Níveis de Leitura
            leitura_stats = escola_data['Niveis de Leitura'].value_counts()
            leitura_baixo = leitura_stats.get('Baixo', 0)
            leitura_medio = leitura_stats.get('Médio', 0)
            leitura_alto = leitura_stats.get('Alto', 0)
            
            # Níveis de Escrita
            escrita_stats = escola_data['Niveis de Escrita'].value_counts()
            escrita_baixo = escrita_stats.get('Baixo', 0)
            escrita_medio = escrita_stats.get('Médio', 0)
            escrita_alto = escrita_stats.get('Alto', 0)
            
            # Calcular percentuais
            leitura_baixo_pct = (leitura_baixo / total_alunos * 100) if total_alunos > 0 else 0
            leitura_medio_pct = (leitura_medio / total_alunos * 100) if total_alunos > 0 else 0
            leitura_alto_pct = (leitura_alto / total_alunos * 100) if total_alunos > 0 else 0
            
            escrita_baixo_pct = (escrita_baixo / total_alunos * 100) if total_alunos > 0 else 0
            escrita_medio_pct = (escrita_medio / total_alunos * 100) if total_alunos > 0 else 0
            escrita_alto_pct = (escrita_alto / total_alunos * 100) if total_alunos > 0 else 0
            
            # Modalidade mais comum
            modalidade_mais_comum = escola_data['Modalidade'].mode().iloc[0] if not escola_data['Modalidade'].mode().empty else "N/A"
            
            consolidated_data.append({
                'Nº': len(consolidated_data) + 1,
                'Escola': escola,
                'Modalidade': modalidade_mais_comum,
                'Total Alunos': total_alunos,
                'Nível de Leitura - Baixo': f"{leitura_baixo} ({leitura_baixo_pct:.1f}%)",
                'Nível de Leitura - Médio': f"{leitura_medio} ({leitura_medio_pct:.1f}%)",
                'Nível de Leitura - Alto': f"{leitura_alto} ({leitura_alto_pct:.1f}%)",
                'Nível de Escrita - Baixo': f"{escrita_baixo} ({escrita_baixo_pct:.1f}%)",
                'Nível de Escrita - Médio': f"{escrita_medio} ({escrita_medio_pct:.1f}%)",
                'Nível de Escrita - Alto': f"{escrita_alto} ({escrita_alto_pct:.1f}%)"
            })
        
        return pd.DataFrame(consolidated_data)
        
    except Exception as e:
        raise Exception(f"Erro no processamento da planilha: {str(e)}")

def generate_charts_real(data: Dict[str, Any], quant_trimestre: int) -> Dict[str, Any]:
    """
    Gera gráficos estilizados e profissionais baseados no formato real da planilha da prefeitura
    
    Args:
        data: Dados processados (leitura e escrita)
        quant_trimestre: Número do trimestre
    
    Returns:
        Dicionário com gráficos e análises
    """
    try:
        print(f"🔍 DEBUG: Iniciando geração de gráficos para {quant_trimestre}º trimestre")
        
        charts_data = {}
        
        df_leitura = data['leitura']
        df_escrita = data['escrita']
        
        # Configurar estilo global dos gráficos
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Cores do sistema EduGraf
        cores_sistema = {
            'primaria': '#165b70',
            'secundaria': '#3d626d', 
            'destaque': '#1abc9c',
            'accent': '#3498db',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'success': '#2ecc71',
            'info': '#9b59b6'
        }
        
        # Cores específicas para os níveis
        cores_leitura = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71', '#9b59b6', '#1abc9c']
        cores_escrita = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71', '#1abc9c']
        
        # Garantir que o diretório temp existe
        os.makedirs("temp", exist_ok=True)
        
        # Gráfico 1: Níveis de Leitura por Ano (Estilizado)
        print("🔍 DEBUG: Gerando gráfico de leitura...")
        fig1, ax1 = plt.subplots(figsize=(14, 9))
        fig1.patch.set_facecolor('white')
        
        anos = df_leitura['ano'].astype(str)
        x = np.arange(len(anos))
        width = 0.12
        
        # Criar gráfico de barras estilizado para leitura
        bars1 = ax1.bar(x - 2.5*width, df_leitura['nl'], width, label='NL (Não Leitor)', 
                       color=cores_leitura[0], alpha=0.8, edgecolor='white', linewidth=1)
        bars2 = ax1.bar(x - 1.5*width, df_leitura['ls'], width, label='LS (Leitor de Sílabas)', 
                       color=cores_leitura[1], alpha=0.8, edgecolor='white', linewidth=1)
        bars3 = ax1.bar(x - 0.5*width, df_leitura['lp'], width, label='LP (Leitor de Palavras)', 
                       color=cores_leitura[2], alpha=0.8, edgecolor='white', linewidth=1)
        bars4 = ax1.bar(x + 0.5*width, df_leitura['lf'], width, label='LF (Leitor de Frases)', 
                       color=cores_leitura[3], alpha=0.8, edgecolor='white', linewidth=1)
        bars5 = ax1.bar(x + 1.5*width, df_leitura['lsf'], width, label='LSF (Leitor Sem Fluência)', 
                       color=cores_leitura[4], alpha=0.8, edgecolor='white', linewidth=1)
        bars6 = ax1.bar(x + 2.5*width, df_leitura['lcf'], width, label='LCF (Leitor Com Fluência)', 
                       color=cores_leitura[5], alpha=0.8, edgecolor='white', linewidth=1)
        
        # Estilizar eixos e títulos
        ax1.set_xlabel('Anos/Séries', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax1.set_ylabel('Quantidade de Alunos', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax1.set_title(f'Diagnóstico de Leitura - {quant_trimestre}º Trimestre', 
                     fontsize=16, fontweight='bold', color=cores_sistema['primaria'], pad=20)
        
        # Configurar ticks
        ax1.set_xticks(x)
        ax1.set_xticklabels(anos, rotation=45, ha='right', fontsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        
        # Configurar legenda
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9, frameon=True, 
                  fancybox=True, shadow=True)
        
        # Configurar grid
        ax1.grid(True, alpha=0.3, linestyle='--', color=cores_sistema['secundaria'])
        ax1.set_axisbelow(True)
        
        # Adicionar valores nas barras
        for bars in [bars1, bars2, bars3, bars4, bars5, bars6]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{int(height)}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # Configurar layout
        plt.tight_layout()
        
        # Salvar gráfico
        chart1_path = f"temp/leitura_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig1.savefig(chart1_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close(fig1)
        
        charts_data['leitura_chart'] = {
            'path': chart1_path,
            'title': f'Diagnóstico de Leitura - {quant_trimestre}º Trimestre',
            'description': f'Análise detalhada da distribuição dos níveis de leitura por ano/série. O gráfico apresenta {len(df_leitura)} anos/séries avaliados, mostrando a evolução do desenvolvimento da leitura desde não leitores até leitores com fluência total.'
        }
        
        # Gráfico 2: Níveis de Escrita por Ano (Estilizado)
        print("🔍 DEBUG: Gerando gráfico de escrita...")
        fig2, ax2 = plt.subplots(figsize=(14, 9))
        fig2.patch.set_facecolor('white')
        
        anos_escrita = df_escrita['ano'].astype(str)
        x = np.arange(len(anos_escrita))
        
        # Criar gráfico de barras estilizado para escrita
        bars1 = ax2.bar(x - 2*width, df_escrita['p'], width, label='P (Pré-Silábico)', 
                       color=cores_escrita[0], alpha=0.8, edgecolor='white', linewidth=1)
        bars2 = ax2.bar(x - width, df_escrita['s'], width, label='S (Silábico)', 
                       color=cores_escrita[1], alpha=0.8, edgecolor='white', linewidth=1)
        bars3 = ax2.bar(x, df_escrita['s.a.'], width, label='S.A. (Silábico Alfabético)', 
                       color=cores_escrita[2], alpha=0.8, edgecolor='white', linewidth=1)
        bars4 = ax2.bar(x + width, df_escrita['a'], width, label='A (Alfabético)', 
                       color=cores_escrita[3], alpha=0.8, edgecolor='white', linewidth=1)
        bars5 = ax2.bar(x + 2*width, df_escrita['o'], width, label='O (Ortográfico)', 
                       color=cores_escrita[4], alpha=0.8, edgecolor='white', linewidth=1)
        
        # Estilizar eixos e títulos
        ax2.set_xlabel('Anos/Séries', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax2.set_ylabel('Quantidade de Alunos', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax2.set_title(f'Diagnóstico de Escrita - {quant_trimestre}º Trimestre', 
                     fontsize=16, fontweight='bold', color=cores_sistema['primaria'], pad=20)
        
        # Configurar ticks
        ax2.set_xticks(x)
        ax2.set_xticklabels(anos_escrita, rotation=45, ha='right', fontsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        
        # Configurar legenda
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9, frameon=True, 
                  fancybox=True, shadow=True)
        
        # Configurar grid
        ax2.grid(True, alpha=0.3, linestyle='--', color=cores_sistema['secundaria'])
        ax2.set_axisbelow(True)
        
        # Adicionar valores nas barras
        for bars in [bars1, bars2, bars3, bars4, bars5]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                            f'{int(height)}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        
        # Configurar layout
        plt.tight_layout()
        
        # Salvar gráfico
        chart2_path = f"temp/escrita_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig2.savefig(chart2_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close(fig2)
        
        charts_data['escrita_chart'] = {
            'path': chart2_path,
            'title': f'Diagnóstico de Escrita - {quant_trimestre}º Trimestre',
            'description': f'Análise detalhada da distribuição dos níveis de escrita por ano/série. O gráfico apresenta {len(df_escrita)} anos/séries avaliados, mostrando a evolução do desenvolvimento da escrita desde pré-silábicos até ortográficos.'
        }
        
        # Gráfico 3: Comparação Geral Leitura vs Escrita (Estilizado)
        print("🔍 DEBUG: Gerando gráfico de comparação...")
        fig3, ax3 = plt.subplots(figsize=(12, 8))
        fig3.patch.set_facecolor('white')
        
        # Calcular totais gerais
        total_leitura = df_leitura[['nl', 'ls', 'lp', 'lf', 'lsf', 'lcf']].sum()
        total_escrita = df_escrita[['p', 's', 's.a.', 'a', 'o']].sum()
        
        categorias_leitura = ['NL', 'LS', 'LP', 'LF', 'LSF', 'LCF']
        categorias_escrita = ['P', 'S', 'S.A.', 'A', 'O']
        
        # Usar apenas as primeiras 5 categorias para comparação
        categorias_comparacao = categorias_leitura[:5]
        total_leitura_comparacao = total_leitura.values[:5]
        total_escrita_comparacao = total_escrita.values
        
        x_pos = np.arange(len(categorias_comparacao))
        
        # Criar gráfico de comparação estilizado
        bars1 = ax3.bar(x_pos - 0.2, total_leitura_comparacao, 0.4, label='📚 Leitura', 
                       color=cores_sistema['destaque'], alpha=0.8, edgecolor='white', linewidth=1)
        bars2 = ax3.bar(x_pos + 0.2, total_escrita_comparacao, 0.4, label='✍️ Escrita', 
                       color=cores_sistema['accent'], alpha=0.8, edgecolor='white', linewidth=1)
        
        # Estilizar eixos e títulos
        ax3.set_xlabel('Níveis de Desenvolvimento', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax3.set_ylabel('Quantidade de Alunos', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax3.set_title('Comparação Geral: Leitura vs Escrita', 
                     fontsize=16, fontweight='bold', color=cores_sistema['primaria'], pad=20)
        
        # Configurar ticks
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(categorias_comparacao, fontsize=10)
        ax3.tick_params(axis='y', labelsize=10)
        
        # Configurar legenda
        ax3.legend(fontsize=11, frameon=True, fancybox=True, shadow=True)
        
        # Configurar grid
        ax3.grid(True, alpha=0.3, linestyle='--', color=cores_sistema['secundaria'])
        ax3.set_axisbelow(True)
        
        # Adicionar valores nas barras
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax3.text(bar.get_x() + bar.get_width()/2., height + max(total_leitura_comparacao.max(), total_escrita_comparacao.max()) * 0.01,
                            f'{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Configurar layout
        plt.tight_layout()
        
        # Salvar gráfico
        chart3_path = f"temp/comparacao_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig3.savefig(chart3_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close(fig3)
        
        charts_data['comparacao_chart'] = {
            'path': chart3_path,
            'title': 'Comparação Geral: Leitura vs Escrita',
            'description': 'Análise comparativa entre os níveis de leitura e escrita, permitindo identificar correlações e áreas que necessitam de atenção pedagógica específica.'
        }
        
        # Gráfico 4: Resumo Estatístico (Novo - mais simples)
        print("🔍 DEBUG: Gerando gráfico de resumo...")
        fig4, ax4 = plt.subplots(figsize=(12, 8))
        fig4.patch.set_facecolor('white')
        
        # Dados para o gráfico de resumo
        categorias = ['Não Leitores', 'Leitores Fluentes', 'Pré-Silábicos', 'Ortográficos']
        valores = [
            total_leitura['nl'],
            total_leitura['lcf'], 
            total_escrita['p'],
            total_escrita['o']
        ]
        cores_resumo = ['#e74c3c', '#2ecc71', '#f39c12', '#3498db']
        
        # Criar gráfico de barras horizontal
        bars = ax4.barh(categorias, valores, color=cores_resumo, alpha=0.8, edgecolor='white', linewidth=1)
        
        # Estilizar
        ax4.set_xlabel('Quantidade de Alunos', fontsize=12, fontweight='bold', color=cores_sistema['primaria'])
        ax4.set_title('Resumo dos Principais Indicadores', fontsize=16, fontweight='bold', color=cores_sistema['primaria'], pad=20)
        
        # Adicionar valores nas barras
        for i, (bar, valor) in enumerate(zip(bars, valores)):
            if valor > 0:
                ax4.text(bar.get_width() + max(valores) * 0.01, bar.get_y() + bar.get_height()/2,
                        f'{int(valor)}', ha='left', va='center', fontsize=11, fontweight='bold')
        
        # Configurar grid
        ax4.grid(True, alpha=0.3, linestyle='--', color=cores_sistema['secundaria'], axis='x')
        ax4.set_axisbelow(True)
        
        # Configurar layout
        plt.tight_layout()
        
        # Salvar gráfico
        chart4_path = f"temp/resumo_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig4.savefig(chart4_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close(fig4)
        
        charts_data['resumo_chart'] = {
            'path': chart4_path,
            'title': 'Resumo dos Principais Indicadores',
            'description': 'Visão geral dos principais indicadores educacionais, destacando os pontos que necessitam de maior atenção pedagógica.'
        }
        
        # Adicionar análises estatísticas
        total_alunos_leitura = df_leitura['total alunos'].sum()
        total_alunos_escrita = df_escrita['total alunos'].sum()
        
        charts_data['analises'] = {
            'total_alunos_leitura': total_alunos_leitura,
            'total_alunos_escrita': total_alunos_escrita,
            'total_anos': len(df_leitura),
            'media_leitura_nl': (total_leitura['nl'] / total_alunos_leitura * 100) if total_alunos_leitura > 0 else 0,
            'media_leitura_lcf': (total_leitura['lcf'] / total_alunos_leitura * 100) if total_alunos_leitura > 0 else 0,
            'media_escrita_p': (total_escrita['p'] / total_alunos_escrita * 100) if total_alunos_escrita > 0 else 0,
            'media_escrita_o': (total_escrita['o'] / total_alunos_escrita * 100) if total_alunos_escrita > 0 else 0
        }
        
        print(f"🔍 DEBUG: Gráficos gerados com sucesso! Total: {len(charts_data) - 1} gráficos")
        
        return charts_data
        
    except Exception as e:
        print(f"🔍 DEBUG: Erro na geração dos gráficos reais: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Erro na geração dos gráficos reais: {str(e)}")

def generate_charts(df: pd.DataFrame, quant_trimestre: int) -> Dict[str, Any]:
    """
    Gera gráficos de barras comparativos e retorna dados para PDF (formato antigo)
    
    Args:
        df: DataFrame com os dados
        quant_trimestre: Quantidade de trimestres
    
    Returns:
        Dicionário com gráficos e análises
    """
    try:
        charts_data = {}
        
        # Gráfico 1: Níveis de Leitura por Escola
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        
        # Preparar dados para leitura
        leitura_data = []
        escolas = df['Nome da escola'].unique()
        
        for escola in escolas:
            escola_data = df[df['Nome da escola'] == escola]
            leitura_stats = escola_data['Niveis de Leitura'].value_counts()
            
            leitura_data.append({
                'Escola': escola,
                'Baixo': leitura_stats.get('Baixo', 0),
                'Médio': leitura_stats.get('Médio', 0),
                'Alto': leitura_stats.get('Alto', 0)
            })
        
        leitura_df = pd.DataFrame(leitura_data)
        
        # Criar gráfico de barras empilhadas para leitura
        x = np.arange(len(leitura_df))
        width = 0.25
        
        ax1.bar(x - width, leitura_df['Baixo'], width, label='Baixo', color='#ff6b6b')
        ax1.bar(x, leitura_df['Médio'], width, label='Médio', color='#4ecdc4')
        ax1.bar(x + width, leitura_df['Alto'], width, label='Alto', color='#45b7d1')
        
        ax1.set_xlabel('Escolas')
        ax1.set_ylabel('Quantidade de Alunos')
        ax1.set_title(f'Diagnóstico de Leitura - {quant_trimestre}º Trimestre')
        ax1.set_xticks(x)
        ax1.set_xticklabels(leitura_df['Escola'], rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart1_path = f"temp/leitura_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig1.savefig(chart1_path, dpi=300, bbox_inches='tight')
        plt.close(fig1)
        
        charts_data['leitura_chart'] = {
            'path': chart1_path,
            'title': f'Diagnóstico de Leitura - {quant_trimestre}º Trimestre',
            'description': f'Gráfico mostrando a distribuição dos níveis de leitura por escola. Total de {len(escolas)} escolas analisadas.'
        }
        
        # Gráfico 2: Níveis de Escrita por Escola
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        # Preparar dados para escrita
        escrita_data = []
        
        for escola in escolas:
            escola_data = df[df['Nome da escola'] == escola]
            escrita_stats = escola_data['Niveis de Escrita'].value_counts()
            
            escrita_data.append({
                'Escola': escola,
                'Baixo': escrita_stats.get('Baixo', 0),
                'Médio': escrita_stats.get('Médio', 0),
                'Alto': escrita_stats.get('Alto', 0)
            })
        
        escrita_df = pd.DataFrame(escrita_data)
        
        # Criar gráfico de barras empilhadas para escrita
        ax2.bar(x - width, escrita_df['Baixo'], width, label='Baixo', color='#ff6b6b')
        ax2.bar(x, escrita_df['Médio'], width, label='Médio', color='#4ecdc4')
        ax2.bar(x + width, escrita_df['Alto'], width, label='Alto', color='#45b7d1')
        
        ax2.set_xlabel('Escolas')
        ax2.set_ylabel('Quantidade de Alunos')
        ax2.set_title(f'Diagnóstico de Escrita - {quant_trimestre}º Trimestre')
        ax2.set_xticks(x)
        ax2.set_xticklabels(escrita_df['Escola'], rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart2_path = f"temp/escrita_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig2.savefig(chart2_path, dpi=300, bbox_inches='tight')
        plt.close(fig2)
        
        charts_data['escrita_chart'] = {
            'path': chart2_path,
            'title': f'Diagnóstico de Escrita - {quant_trimestre}º Trimestre',
            'description': f'Gráfico mostrando a distribuição dos níveis de escrita por escola. Total de {len(escolas)} escolas analisadas.'
        }
        
        # Gráfico 3: Comparação Geral Leitura vs Escrita
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        # Calcular totais gerais
        total_leitura = df['Niveis de Leitura'].value_counts()
        total_escrita = df['Niveis de Escrita'].value_counts()
        
        categorias = ['Baixo', 'Médio', 'Alto']
        x_pos = np.arange(len(categorias))
        
        ax3.bar(x_pos - 0.2, [total_leitura.get('Baixo', 0), total_leitura.get('Médio', 0), total_leitura.get('Alto', 0)], 
                0.4, label='Leitura', color='#1abc9c')
        ax3.bar(x_pos + 0.2, [total_escrita.get('Baixo', 0), total_escrita.get('Médio', 0), total_escrita.get('Alto', 0)], 
                0.4, label='Escrita', color='#3498db')
        
        ax3.set_xlabel('Níveis')
        ax3.set_ylabel('Quantidade de Alunos')
        ax3.set_title('Comparação Geral: Leitura vs Escrita')
        ax3.set_xticks(x_pos)
        ax3.set_xticklabels(categorias)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart3_path = f"temp/comparacao_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig3.savefig(chart3_path, dpi=300, bbox_inches='tight')
        plt.close(fig3)
        
        charts_data['comparacao_chart'] = {
            'path': chart3_path,
            'title': 'Comparação Geral: Leitura vs Escrita',
            'description': 'Comparação direta entre os níveis de leitura e escrita em todas as escolas.'
        }
        
        # Gráfico 4: Distribuição por Modalidade
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        
        modalidade_stats = df['Modalidade'].value_counts()
        
        ax4.pie(modalidade_stats.values, labels=modalidade_stats.index, autopct='%1.1f%%', 
                startangle=90, colors=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
        ax4.set_title('Distribuição por Modalidade')
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart4_path = f"temp/modalidade_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig4.savefig(chart4_path, dpi=300, bbox_inches='tight')
        plt.close(fig4)
        
        charts_data['modalidade_chart'] = {
            'path': chart4_path,
            'title': 'Distribuição por Modalidade',
            'description': f'Distribuição dos alunos por modalidade de ensino. Total de {len(df)} alunos analisados.'
        }
        
        # Adicionar análises estatísticas
        charts_data['analises'] = {
            'total_alunos': len(df),
            'total_escolas': len(escolas),
            'media_leitura_alto': (total_leitura.get('Alto', 0) / len(df) * 100),
            'media_escrita_alto': (total_escrita.get('Alto', 0) / len(df) * 100),
            'media_leitura_baixo': (total_leitura.get('Baixo', 0) / len(df) * 100),
            'media_escrita_baixo': (total_escrita.get('Baixo', 0) / len(df) * 100)
        }
        
        return charts_data
        
    except Exception as e:
        raise Exception(f"Erro na geração dos gráficos: {str(e)}")

def create_pdf_report(charts_data: Dict[str, Any], quant_trimestre: int) -> str:
    """
    Cria relatório PDF profissional com gráficos e análises detalhadas
    
    Args:
        charts_data: Dados dos gráficos
        quant_trimestre: Número do trimestre
    
    Returns:
        Caminho do arquivo PDF gerado
    """
    try:
        print(f"🔍 DEBUG: Iniciando criação do PDF para {quant_trimestre}º trimestre")
        
        # Criar nome do arquivo PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_path = f"temp/relatorio_graficos_{quant_trimestre}_trimestre_{timestamp}.pdf"
        
        # Garantir que o diretório temp existe
        os.makedirs("temp", exist_ok=True)
        
        print(f"🔍 DEBUG: Caminho do PDF: {pdf_path}")
        
        # Criar documento PDF com margens otimizadas para centralização
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=60,
            bottomMargin=60
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Estilos personalizados com cores do sistema - melhorados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=25,
            alignment=1,  # Centralizado
            textColor=colors.HexColor('#165b70'),
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=12,
            alignment=1,  # Centralizado
            textColor=colors.HexColor('#3d626d'),
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            alignment=0,  # Justificado
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica'
        )
        
        # Estilo para legendas - melhorado
        legend_style = ParagraphStyle(
            'Legend',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica-Oblique',
            alignment=1  # Centralizado
        )
        
        # Cabeçalho principal - melhorado
        story.append(Paragraph("EDUGRAF", title_style))
        story.append(Paragraph("Sistema de Diagnóstico Educacional", subtitle_style))
        story.append(Spacer(1, 30))
        
        # Informações do relatório - centralizadas
        story.append(Paragraph(f"<b>RELATÓRIO DE GRÁFICOS - {quant_trimestre}º TRIMESTRE</b>", subtitle_style))
        story.append(Spacer(1, 15))
        story.append(Paragraph(f"<b>Data de Geração:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}", normal_style))
        story.append(Paragraph(f"<b>Período:</b> {quant_trimestre}º Trimestre de {datetime.now().year}", normal_style))
        story.append(Spacer(1, 30))
        
        # Resumo executivo - simplificado
        analises = charts_data.get('analises', {})
        story.append(Paragraph("<b>RESUMO EXECUTIVO</b>", subtitle_style))
        story.append(Spacer(1, 15))
        
        # Verificar se é formato real ou antigo - simplificado
        if 'total_alunos_leitura' in analises:
            # Formato real da prefeitura - simplificado
            resumo_text = f"""
            <b>DADOS DE LEITURA:</b><br/>
            • Total de Alunos: <b>{analises['total_alunos_leitura']}</b><br/>
            • Anos/Séries Avaliados: <b>{analises['total_anos']}</b><br/>
            • Não Leitores: <b>{analises['media_leitura_nl']:.1f}%</b><br/>
            • Leitores com Fluência: <b>{analises['media_leitura_lcf']:.1f}%</b><br/><br/>
            
            <b>DADOS DE ESCRITA:</b><br/>
            • Total de Alunos: <b>{analises['total_alunos_escrita']}</b><br/>
            • Pré-Silábicos: <b>{analises['media_escrita_p']:.1f}%</b><br/>
            • Ortográficos: <b>{analises['media_escrita_o']:.1f}%</b>
            """
        else:
            # Formato antigo - simplificado
            resumo_text = f"""
            <b>DADOS GERAIS:</b><br/>
            • Total de Alunos: <b>{analises.get('total_alunos', 0)}</b><br/>
            • Total de Escolas: <b>{analises.get('total_escolas', 0)}</b><br/>
            • Alto Nível em Leitura: <b>{analises.get('media_leitura_alto', 0):.1f}%</b><br/>
            • Alto Nível em Escrita: <b>{analises.get('media_escrita_alto', 0):.1f}%</b>
            """
        
        story.append(Paragraph(resumo_text, normal_style))
        story.append(Spacer(1, 30))
        
        # Adicionar cada gráfico com descrições detalhadas
        chart_count = 0
        for chart_key, chart_info in charts_data.items():
            if chart_key == 'analises':
                continue
                
            chart_count += 1
            print(f"🔍 DEBUG: Processando gráfico {chart_count}: {chart_key}")
            
            # Título do gráfico - centralizado
            story.append(Paragraph(f"<b>{chart_info['title']}</b>", subtitle_style))
            story.append(Spacer(1, 15))
            
            # Descrição simplificada
            story.append(Paragraph(chart_info['description'], normal_style))
            story.append(Spacer(1, 15))
            
            # Adicionar imagem do gráfico
            if os.path.exists(chart_info['path']):
                try:
                    from reportlab.platypus import Image
                    # Redimensionar imagem para caber na página - centralizada
                    img = Image(chart_info['path'], width=480, height=360)
                    story.append(img)
                    story.append(Spacer(1, 12))
                    
                    # Adicionar legenda explicativa simplificada
                    if 'leitura' in chart_key.lower():
                        legend_text = """
                        <b>Interpretação:</b> Distribuição dos níveis de leitura por ano/série, 
                        mostrando a evolução do desenvolvimento da leitura.
                        """
                    elif 'escrita' in chart_key.lower():
                        legend_text = """
                        <b>Interpretação:</b> Distribuição dos níveis de escrita por ano/série, 
                        mostrando a evolução do desenvolvimento da escrita.
                        """
                    elif 'comparacao' in chart_key.lower():
                        legend_text = """
                        <b>Interpretação:</b> Comparação direta entre leitura e escrita, 
                        permitindo identificar correlações e áreas de atenção.
                        """
                    elif 'resumo' in chart_key.lower():
                        legend_text = """
                        <b>Interpretação:</b> Visão geral dos principais indicadores, 
                        destacando pontos que necessitam de atenção pedagógica.
                        """
                    else:
                        legend_text = """
                        <b>Interpretação:</b> Dados consolidados do diagnóstico educacional 
                        para o período analisado.
                        """
                    
                    story.append(Paragraph(legend_text, legend_style))
                    story.append(Spacer(1, 25))
                    
                except Exception as e:
                    print(f"🔍 DEBUG: Erro ao adicionar imagem {chart_info['path']}: {e}")
                    story.append(Paragraph(f"<i>Erro ao carregar gráfico: {chart_info['path']}</i>", styles['Italic']))
                    story.append(Spacer(1, 20))
            else:
                print(f"🔍 DEBUG: Arquivo de gráfico não encontrado: {chart_info['path']}")
                story.append(Paragraph(f"<i>Gráfico não disponível: {chart_info['path']}</i>", styles['Italic']))
                story.append(Spacer(1, 20))
        
        # Análise e recomendações - simplificada
        story.append(Paragraph("<b>ANÁLISE E RECOMENDAÇÕES</b>", subtitle_style))
        story.append(Spacer(1, 15))
        
        if 'total_alunos_leitura' in analises:
            # Formato real da prefeitura - simplificado
            analise_final = f"""
            <b>PONTOS POSITIVOS:</b><br/>
            • {analises['total_anos']} anos/séries avaliados<br/>
            • {analises['total_alunos_leitura']} alunos em leitura<br/>
            • {analises['media_leitura_lcf']:.1f}% com leitura fluente<br/>
            • {analises['media_escrita_o']:.1f}% com escrita ortográfica<br/><br/>
            
            <b>ÁREAS DE MELHORIA:</b><br/>
            • {analises['media_leitura_nl']:.1f}% precisam de apoio em leitura<br/>
            • {analises['media_escrita_p']:.1f}% precisam de apoio em escrita<br/><br/>
            
            <b>RECOMENDAÇÕES:</b><br/>
            • Programas de reforço para não leitores<br/>
            • Atividades específicas por nível<br/>
            • Monitoramento contínuo<br/>
            • Estratégias personalizadas por série
            """
        else:
            # Formato antigo - simplificado
            analise_final = f"""
            <b>PONTOS POSITIVOS:</b><br/>
            • {analises.get('total_escolas', 0)} escolas avaliadas<br/>
            • {analises.get('total_alunos', 0)} alunos analisados<br/>
            • {analises.get('media_leitura_alto', 0):.1f}% com alto nível de leitura<br/>
            • {analises.get('media_escrita_alto', 0):.1f}% com alto nível de escrita<br/><br/>
            
            <b>ÁREAS DE MELHORIA:</b><br/>
            • {analises.get('media_leitura_baixo', 0):.1f}% precisam de apoio em leitura<br/>
            • {analises.get('media_escrita_baixo', 0):.1f}% precisam de apoio em escrita<br/><br/>
            
            <b>RECOMENDAÇÕES:</b><br/>
            • Programas de reforço<br/>
            • Atividades específicas por modalidade<br/>
            • Monitoramento contínuo<br/>
            • Grupos de estudo diferenciados
            """
        
        story.append(Paragraph(analise_final, normal_style))
        story.append(Spacer(1, 25))
        
        # Metodologia - simplificada
        story.append(Paragraph("<b>METODOLOGIA</b>", subtitle_style))
        story.append(Spacer(1, 15))
        
        metodologia_text = f"""
        <b>Instrumentos:</b> Diagnóstico de Leitura e Escrita<br/>
        <b>Análise:</b> Classificação por níveis de desenvolvimento<br/>
        <b>Período:</b> {quant_trimestre}º Trimestre de {datetime.now().year}<br/>
        <b>Sistema:</b> EduGraf - Diagnóstico Educacional
        """
        
        story.append(Paragraph(metodologia_text, normal_style))
        story.append(Spacer(1, 30))
        
        # Rodapé simplificado
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,
            textColor=colors.HexColor('#666666'),
            fontName='Helvetica-Oblique'
        )
        
        story.append(Paragraph("─" * 60, footer_style))
        story.append(Paragraph("Sistema EduGraf - Diagnóstico Educacional", footer_style))
        story.append(Paragraph(f"Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", footer_style))
        
        print(f"🔍 DEBUG: Construindo PDF...")
        
        # Gerar PDF
        doc.build(story)
        
        print(f"🔍 DEBUG: PDF gerado com sucesso: {pdf_path}")
        
        # Verificar se o arquivo foi criado
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"🔍 DEBUG: Tamanho do arquivo PDF: {file_size} bytes")
            return pdf_path
        else:
            raise Exception("PDF não foi criado corretamente")
        
    except Exception as e:
        print(f"🔍 DEBUG: Erro na criação do PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Erro na criação do PDF: {str(e)}")

def consolidate_data(dataframes: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Consolida múltiplos DataFrames em um único
    
    Args:
        dataframes: Lista de DataFrames para consolidar
    
    Returns:
        DataFrame consolidado
    """
    try:
        if not dataframes:
            raise ValueError("Lista de DataFrames vazia")
        
        # Concatenar todos os DataFrames
        consolidated = pd.concat(dataframes, ignore_index=True)
        
        # Remover duplicatas se houver
        consolidated = consolidated.drop_duplicates()
        
        return consolidated
        
    except Exception as e:
        raise Exception(f"Erro na consolidação dos dados: {str(e)}")

def validate_excel_structure(df: pd.DataFrame) -> bool:
    """
    Valida se a estrutura do Excel está correta
    
    Args:
        df: DataFrame para validar
    
    Returns:
        True se válido, False caso contrário
    """
    required_columns = ['Nome da escola', 'Modalidade', 'Niveis de Leitura', 'Niveis de Escrita']
    
    # Verificar se todas as colunas obrigatórias existem
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False
    
    # Verificar se há dados
    if df.empty:
        return False
    
    # Verificar se os níveis são válidos
    niveis_validos = ['Baixo', 'Médio', 'Alto']
    
    leitura_invalidos = df[~df['Niveis de Leitura'].isin(niveis_validos)]
    escrita_invalidos = df[~df['Niveis de Escrita'].isin(niveis_validos)]
    
    if not leitura_invalidos.empty or not escrita_invalidos.empty:
        return False
    
    return True