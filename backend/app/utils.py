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

# Configuração do matplotlib para não usar interface gráfica
plt.switch_backend('Agg')

# Configurar estilo dos gráficos
plt.style.use('default')
sns.set_palette("husl")

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
                # Corrigido: usar ° em vez de º e incluir anos 1° ao 9° e EJA
                if any(ano in primeiro_valor.upper() for ano in ["ANO", "SÉRIE", "1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "EJA"]) or primeiro_valor.isdigit():
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
                # Corrigido: usar ° em vez de º e incluir anos 1° ao 9° e EJA
                if any(ano in primeiro_valor.upper() for ano in ["ANO", "SÉRIE", "1°", "2°", "3°", "4°", "5°", "6°", "7°", "8°", "9°", "EJA"]) or primeiro_valor.isdigit():
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
    Gera gráficos baseados no formato real da planilha da prefeitura
    
    Args:
        data: Dados processados (leitura e escrita)
        quant_trimestre: Número do trimestre
    
    Returns:
        Dicionário com gráficos e análises
    """
    try:
        charts_data = {}
        
        df_leitura = data['leitura']
        df_escrita = data['escrita']
        
        # Gráfico 1: Níveis de Leitura por Ano
        fig1, ax1 = plt.subplots(figsize=(12, 8))
        
        anos = df_leitura['ano'].astype(str)
        x = np.arange(len(anos))
        width = 0.15
        
        # Criar gráfico de barras empilhadas para leitura
        ax1.bar(x - 2.5*width, df_leitura['nl'], width, label='NL (Não Leitor)', color='#ff6b6b')
        ax1.bar(x - 1.5*width, df_leitura['ls'], width, label='LS (Leitor de Sílabas)', color='#4ecdc4')
        ax1.bar(x - 0.5*width, df_leitura['lp'], width, label='LP (Leitor de Palavras)', color='#45b7d1')
        ax1.bar(x + 0.5*width, df_leitura['lf'], width, label='LF (Leitor de Frases)', color='#96ceb4')
        ax1.bar(x + 1.5*width, df_leitura['lsf'], width, label='LSF (Leitor Sem Fluência)', color='#feca57')
        ax1.bar(x + 2.5*width, df_leitura['lcf'], width, label='LCF (Leitor Com Fluência)', color='#ff9ff3')
        
        ax1.set_xlabel('Anos/Séries')
        ax1.set_ylabel('Quantidade de Alunos')
        ax1.set_title(f'Diagnóstico de Leitura - {quant_trimestre}º Trimestre')
        ax1.set_xticks(x)
        ax1.set_xticklabels(anos, rotation=45, ha='right')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart1_path = f"temp/leitura_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig1.savefig(chart1_path, dpi=300, bbox_inches='tight')
        plt.close(fig1)
        
        charts_data['leitura_chart'] = {
            'path': chart1_path,
            'title': f'Diagnóstico de Leitura - {quant_trimestre}º Trimestre',
            'description': f'Gráfico mostrando a distribuição dos níveis de leitura por ano/série. Total de {len(df_leitura)} anos analisados.'
        }
        
        # Gráfico 2: Níveis de Escrita por Ano
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        anos_escrita = df_escrita['ano'].astype(str)
        x = np.arange(len(anos_escrita))
        
        # Criar gráfico de barras empilhadas para escrita
        ax2.bar(x - 2*width, df_escrita['p'], width, label='P (Pré-Silábico)', color='#ff6b6b')
        ax2.bar(x - width, df_escrita['s'], width, label='S (Silábico)', color='#4ecdc4')
        ax2.bar(x, df_escrita['s.a.'], width, label='S.A. (Silábico Alfabético)', color='#45b7d1')
        ax2.bar(x + width, df_escrita['a'], width, label='A (Alfabético)', color='#96ceb4')
        ax2.bar(x + 2*width, df_escrita['o'], width, label='O (Ortográfico)', color='#feca57')
        
        ax2.set_xlabel('Anos/Séries')
        ax2.set_ylabel('Quantidade de Alunos')
        ax2.set_title(f'Diagnóstico de Escrita - {quant_trimestre}º Trimestre')
        ax2.set_xticks(x)
        ax2.set_xticklabels(anos_escrita, rotation=45, ha='right')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart2_path = f"temp/escrita_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig2.savefig(chart2_path, dpi=300, bbox_inches='tight')
        plt.close(fig2)
        
        charts_data['escrita_chart'] = {
            'path': chart2_path,
            'title': f'Diagnóstico de Escrita - {quant_trimestre}º Trimestre',
            'description': f'Gráfico mostrando a distribuição dos níveis de escrita por ano/série. Total de {len(df_escrita)} anos analisados.'
        }
        
        # Gráfico 3: Comparação Geral Leitura vs Escrita
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        # Calcular totais gerais
        total_leitura = df_leitura[['nl', 'ls', 'lp', 'lf', 'lsf', 'lcf']].sum()
        total_escrita = df_escrita[['p', 's', 's.a.', 'a', 'o']].sum()
        
        categorias_leitura = ['NL', 'LS', 'LP', 'LF', 'LSF', 'LCF']
        categorias_escrita = ['P', 'S', 'S.A.', 'A', 'O']
        
        # Usar apenas as primeiras 5 categorias para comparação (mesmo número de categorias de escrita)
        categorias_comparacao = categorias_leitura[:5]
        total_leitura_comparacao = total_leitura.values[:5]
        total_escrita_comparacao = total_escrita.values
        
        x_pos = np.arange(len(categorias_comparacao))
        
        ax3.bar(x_pos, total_leitura_comparacao, label='Leitura', color='#1abc9c', alpha=0.7)
        ax3.bar(x_pos + 0.4, total_escrita_comparacao, label='Escrita', color='#3498db', alpha=0.7)
        
        ax3.set_xlabel('Níveis')
        ax3.set_ylabel('Quantidade de Alunos')
        ax3.set_title('Comparação Geral: Leitura vs Escrita')
        ax3.set_xticks(x_pos + 0.2)
        ax3.set_xticklabels(categorias_comparacao)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Salvar gráfico
        chart3_path = f"temp/comparacao_real_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        fig3.savefig(chart3_path, dpi=300, bbox_inches='tight')
        plt.close(fig3)
        
        charts_data['comparacao_chart'] = {
            'path': chart3_path,
            'title': 'Comparação Geral: Leitura vs Escrita',
            'description': 'Comparação direta entre os níveis de leitura e escrita em todos os anos.'
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
        
        return charts_data
        
    except Exception as e:
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
    Cria relatório PDF com gráficos e análises
    
    Args:
        charts_data: Dados dos gráficos
        quant_trimestre: Número do trimestre
    
    Returns:
        Caminho do arquivo PDF gerado
    """
    try:
        # Criar nome do arquivo PDF
        pdf_path = f"temp/relatorio_graficos_{quant_trimestre}_trimestre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Criar documento PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Estilo personalizado para título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=30,
            alignment=1,  # Centralizado
            textColor=colors.HexColor('#165b70')
        )
        
        # Estilo para subtítulos
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            textColor=colors.HexColor('#3d626d')
        )
        
        # Estilo para texto normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            textColor=colors.HexColor('#333333')
        )
        
        # Cabeçalho
        story.append(Paragraph("📊 EDUGRAF - SISTEMA DE DIAGNÓSTICO EDUCACIONAL", title_style))
        story.append(Spacer(1, 20))
        
        # Informações do relatório
        story.append(Paragraph(f"📋 <b>Relatório de Gráficos - {quant_trimestre}º Trimestre</b>", subtitle_style))
        story.append(Paragraph(f"<b>Data de Geração:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}", normal_style))
        story.append(Spacer(1, 20))
        
        # Informações gerais
        analises = charts_data['analises']
        story.append(Paragraph("📊 <b>RESUMO EXECUTIVO</b>", subtitle_style))
        story.append(Spacer(1, 12))
        
        # Verificar se é formato real ou antigo
        if 'total_alunos_leitura' in analises:
            # Formato real da prefeitura
            resumo_text = f"""
            <b>📈 DADOS DE LEITURA:</b><br/>
            • Total de Alunos: <b>{analises['total_alunos_leitura']}</b><br/>
            • Total de Anos/Séries: <b>{analises['total_anos']}</b><br/>
            • Percentual de Não Leitores: <b>{analises['media_leitura_nl']:.1f}%</b><br/>
            • Percentual de Leitores com Fluência: <b>{analises['media_leitura_lcf']:.1f}%</b><br/><br/>
            
            <b>📝 DADOS DE ESCRITA:</b><br/>
            • Total de Alunos: <b>{analises['total_alunos_escrita']}</b><br/>
            • Percentual de Pré-Silábicos: <b>{analises['media_escrita_p']:.1f}%</b><br/>
            • Percentual de Ortográficos: <b>{analises['media_escrita_o']:.1f}%</b><br/><br/>
            
            <b>🎯 LEGENDAS:</b><br/>
            <b>Leitura:</b> NL=Não Leitor, LS=Leitor de Sílabas, LP=Leitor de Palavras, LF=Leitor de Frases, LSF=Leitor Sem Fluência, LCF=Leitor Com Fluência<br/>
            <b>Escrita:</b> P=Pré-Silábico, S=Silábico, S.A.=Silábico Alfabético, A=Alfabético, O=Ortográfico
            """
        else:
            # Formato antigo
            resumo_text = f"""
            <b>📈 DADOS GERAIS:</b><br/>
            • Total de Alunos Analisados: <b>{analises['total_alunos']}</b><br/>
            • Total de Escolas: <b>{analises['total_escolas']}</b><br/>
            • Percentual de Alto Nível em Leitura: <b>{analises['media_leitura_alto']:.1f}%</b><br/>
            • Percentual de Alto Nível em Escrita: <b>{analises['media_escrita_alto']:.1f}%</b><br/>
            • Percentual de Baixo Nível em Leitura: <b>{analises['media_leitura_baixo']:.1f}%</b><br/>
            • Percentual de Baixo Nível em Escrita: <b>{analises['media_escrita_baixo']:.1f}%</b>
            """
        
        story.append(Paragraph(resumo_text, normal_style))
        story.append(Spacer(1, 20))
        
        # Adicionar cada gráfico
        for chart_key, chart_info in charts_data.items():
            if chart_key == 'analises':
                continue
                
            # Título do gráfico
            story.append(Paragraph(f"📈 <b>{chart_info['title']}</b>", subtitle_style))
            story.append(Spacer(1, 12))
            
            # Descrição
            story.append(Paragraph(chart_info['description'], normal_style))
            story.append(Spacer(1, 12))
            
            # Adicionar imagem do gráfico
            if os.path.exists(chart_info['path']):
                try:
                    from reportlab.platypus import Image
                    img = Image(chart_info['path'], width=450, height=350)
                    story.append(img)
                    story.append(Spacer(1, 12))
                except Exception as e:
                    story.append(Paragraph(f"<i>Gráfico salvo em: {chart_info['path']}</i>", styles['Italic']))
            
            story.append(Spacer(1, 20))
        
        # Análise final
        story.append(Paragraph("📋 <b>ANÁLISE E RECOMENDAÇÕES</b>", subtitle_style))
        story.append(Spacer(1, 12))
        
        if 'total_alunos_leitura' in analises:
            # Formato real da prefeitura
            analise_final = f"""
            <b>✅ PONTOS POSITIVOS:</b><br/>
            • {analises['total_anos']} anos/séries participaram do diagnóstico<br/>
            • {analises['total_alunos_leitura']} alunos foram avaliados em leitura<br/>
            • {analises['total_alunos_escrita']} alunos foram avaliados em escrita<br/>
            • {analises['media_leitura_lcf']:.1f}% dos alunos apresentam leitura com fluência<br/>
            • {analises['media_escrita_o']:.1f}% dos alunos apresentam escrita ortográfica<br/><br/>
            
            <b>⚠️ ÁREAS DE MELHORIA:</b><br/>
            • {analises['media_leitura_nl']:.1f}% dos alunos precisam de apoio em leitura<br/>
            • {analises['media_escrita_p']:.1f}% dos alunos precisam de apoio em escrita<br/><br/>
            
            <b>🎯 RECOMENDAÇÕES:</b><br/>
            • Implementar programas de reforço para não leitores<br/>
            • Desenvolver atividades específicas para cada nível<br/>
            • Manter monitoramento contínuo dos progressos<br/>
            • Criar estratégias personalizadas por ano/série<br/>
            • Estabelecer metas progressivas para cada trimestre
            """
        else:
            # Formato antigo
            analise_final = f"""
            <b>✅ PONTOS POSITIVOS:</b><br/>
            • {analises['total_escolas']} escolas participaram do diagnóstico<br/>
            • {analises['total_alunos']} alunos foram avaliados<br/>
            • {analises['media_leitura_alto']:.1f}% dos alunos apresentam alto nível de leitura<br/>
            • {analises['media_escrita_alto']:.1f}% dos alunos apresentam alto nível de escrita<br/><br/>
            
            <b>⚠️ ÁREAS DE MELHORIA:</b><br/>
            • {analises['media_leitura_baixo']:.1f}% dos alunos precisam de apoio em leitura<br/>
            • {analises['media_escrita_baixo']:.1f}% dos alunos precisam de apoio em escrita<br/><br/>
            
            <b>🎯 RECOMENDAÇÕES:</b><br/>
            • Implementar programas de reforço para alunos com baixo nível<br/>
            • Desenvolver atividades específicas para cada modalidade<br/>
            • Manter monitoramento contínuo dos progressos
            """
        
        story.append(Paragraph(analise_final, normal_style))
        story.append(Spacer(1, 20))
        
        # Rodapé
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            alignment=1,
            textColor=colors.HexColor('#666666')
        )
        story.append(Paragraph("--- Relatório gerado automaticamente pelo Sistema EduGraf ---", footer_style))
        
        # Gerar PDF
        doc.build(story)
        
        return pdf_path
        
    except Exception as e:
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