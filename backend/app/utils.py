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

# Configuração do matplotlib para não usar interface gráfica
plt.switch_backend('Agg')

# Configurar estilo dos gráficos
plt.style.use('default')
sns.set_palette("husl")

def process_excel_file(df: pd.DataFrame, polo: str) -> pd.DataFrame:
    """
    Processa planilha Excel e consolida dados por escola e polo
    
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

def generate_charts(df: pd.DataFrame, quant_trimestre: int) -> Dict[str, Any]:
    """
    Gera gráficos de barras comparativos e retorna dados para PDF
    
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
        
        # Título principal
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Centralizado
        )
        story.append(Paragraph(f"Relatório de Gráficos - {quant_trimestre}º Trimestre", title_style))
        story.append(Spacer(1, 20))
        
        # Informações gerais
        analises = charts_data['analises']
        story.append(Paragraph("📊 <b>Resumo Executivo</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        resumo_text = f"""
        <b>Total de Alunos Analisados:</b> {analises['total_alunos']}<br/>
        <b>Total de Escolas:</b> {analises['total_escolas']}<br/>
        <b>Percentual de Alto Nível em Leitura:</b> {analises['media_leitura_alto']:.1f}%<br/>
        <b>Percentual de Alto Nível em Escrita:</b> {analises['media_escrita_alto']:.1f}%<br/>
        <b>Percentual de Baixo Nível em Leitura:</b> {analises['media_leitura_baixo']:.1f}%<br/>
        <b>Percentual de Baixo Nível em Escrita:</b> {analises['media_escrita_baixo']:.1f}%
        """
        story.append(Paragraph(resumo_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Adicionar cada gráfico
        for chart_key, chart_info in charts_data.items():
            if chart_key == 'analises':
                continue
                
            # Título do gráfico
            story.append(Paragraph(f"📈 <b>{chart_info['title']}</b>", styles['Heading3']))
            story.append(Spacer(1, 12))
            
            # Descrição
            story.append(Paragraph(chart_info['description'], styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Adicionar imagem do gráfico
            if os.path.exists(chart_info['path']):
                try:
                    from reportlab.platypus import Image
                    img = Image(chart_info['path'], width=400, height=300)
                    story.append(img)
                    story.append(Spacer(1, 12))
                except Exception as e:
                    story.append(Paragraph(f"<i>Gráfico salvo em: {chart_info['path']}</i>", styles['Italic']))
            
            story.append(Spacer(1, 20))
        
        # Análise final
        story.append(Paragraph("📋 <b>Análise e Recomendações</b>", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        analise_final = f"""
        <b>Pontos Positivos:</b><br/>
        • {analises['total_escolas']} escolas participaram do diagnóstico<br/>
        • {analises['total_alunos']} alunos foram avaliados<br/>
        • {analises['media_leitura_alto']:.1f}% dos alunos apresentam alto nível de leitura<br/>
        • {analises['media_escrita_alto']:.1f}% dos alunos apresentam alto nível de escrita<br/><br/>
        
        <b>Áreas de Melhoria:</b><br/>
        • {analises['media_leitura_baixo']:.1f}% dos alunos precisam de apoio em leitura<br/>
        • {analises['media_escrita_baixo']:.1f}% dos alunos precisam de apoio em escrita<br/><br/>
        
        <b>Recomendações:</b><br/>
        • Implementar programas de reforço para alunos com baixo nível<br/>
        • Desenvolver atividades específicas para cada modalidade<br/>
        • Manter monitoramento contínuo dos progressos
        """
        story.append(Paragraph(analise_final, styles['Normal']))
        
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