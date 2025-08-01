#!/usr/bin/env python3
"""
Script para criar planilha modelo com dados de exemplo
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_sample_excel():
    """Cria planilha Excel com dados de exemplo"""
    
    # Dados de exemplo
    escolas = [
        "Escola Municipal João da Silva",
        "Escola Municipal Maria Santos",
        "Escola Municipal Pedro Oliveira",
        "Escola Municipal Ana Costa",
        "Escola Municipal Carlos Lima",
        "Escola Municipal Lucía Ferreira",
        "Escola Municipal Roberto Alves",
        "Escola Municipal Fernanda Silva"
    ]
    
    modalidades = ["Fundamental", "Médio", "Fundamental", "Médio", "Fundamental", "Médio", "Fundamental", "Médio"]
    niveis = ["Baixo", "Médio", "Alto"]
    
    # Criar dados aleatórios
    data = []
    
    for escola in escolas:
        # Gerar 10-20 alunos por escola
        num_alunos = np.random.randint(10, 21)
        
        for _ in range(num_alunos):
            # Selecionar modalidade baseada na escola
            modalidade = modalidades[escolas.index(escola)]
            
            # Gerar níveis aleatórios
            nivel_leitura = np.random.choice(niveis, p=[0.3, 0.4, 0.3])  # 30% baixo, 40% médio, 30% alto
            nivel_escrita = np.random.choice(niveis, p=[0.25, 0.45, 0.3])  # 25% baixo, 45% médio, 30% alto
            
            data.append({
                'Nome da escola': escola,
                'Modalidade': modalidade,
                'Niveis de Leitura': nivel_leitura,
                'Niveis de Escrita': nivel_escrita
            })
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Salvar como Excel
    filename = f"planilha_modelo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Dados', index=False)
        
        # Adicionar instruções em uma nova aba
        instrucoes = pd.DataFrame({
            'Instruções': [
                'Esta planilha contém dados de exemplo para testar o sistema EduGraf',
                '',
                'Colunas obrigatórias:',
                '- Nome da escola: Nome da instituição',
                '- Modalidade: Tipo de ensino (Fundamental, Médio, etc.)',
                '- Niveis de Leitura: Baixo, Médio ou Alto',
                '- Niveis de Escrita: Baixo, Médio ou Alto',
                '',
                'Como usar:',
                '1. Faça upload desta planilha no sistema',
                '2. Selecione o polo desejado',
                '3. Clique em "Gerar tabela" ou "Gerar gráfico"',
                '',
                'Dados de exemplo incluídos:',
                f'- {len(escolas)} escolas diferentes',
                f'- {len(df)} alunos no total',
                '- Distribuição realística de níveis'
            ]
        })
        instrucoes.to_excel(writer, sheet_name='Instruções', index=False)
    
    print(f"✅ Planilha modelo criada: {filename}")
    print(f"📊 Total de registros: {len(df)}")
    print(f"🏫 Escolas incluídas: {len(escolas)}")
    print(f"📈 Distribuição de níveis de leitura:")
    print(df['Niveis de Leitura'].value_counts())
    print(f"📝 Distribuição de níveis de escrita:")
    print(df['Niveis de Escrita'].value_counts())
    
    return filename

if __name__ == "__main__":
    create_sample_excel() 