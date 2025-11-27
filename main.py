import csv
import os
from grafos import AdjacencyListGraph, AdjacencyMatrixGraph

# Função auxiliar para carregar o grafo a partir do CSV
def carregar_grafo(caminho_arquivo, indice_peso):
    """
    Lê um CSV, mapeia usuários para IDs numéricos e retorna o grafo montado.
    :param caminho_arquivo: String com o path do arquivo
    :param indice_peso: Qual coluna do CSV contém o peso (varia entre os arquivos)
    :return: (grafo, mapa_nomes)
    """
    print(f"\n--- Carregando: {caminho_arquivo} ---")
    
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo não encontrado: {caminho_arquivo}")
        return None, None

    # 1. PRIMEIRA PASSADA: Identificar todos os vértices (usuários) únicos
    usuarios = set()
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor) # Pular cabeçalho
        for linha in leitor:
            if len(linha) >= 2:
                # Coluna 0 é Origem, Coluna 1 é Destino
                usuarios.add(linha[0])
                usuarios.add(linha[1])
    
    # Ordenar para garantir que o ID 0 seja sempre o mesmo usuário em execuções diferentes
    lista_usuarios = sorted(list(usuarios))
    num_vertices = len(lista_usuarios)
    print(f"Total de Vértices detectados: {num_vertices}")

    # Criar Dicionário de Mapeamento: "Nome" -> ID (Int)
    mapa_nome_id = {nome: i for i, nome in enumerate(lista_usuarios)}

    # 2. INSTANCIAR O GRAFO
    # Usamos Lista de Adjacência pois é mais eficiente para milhares de usuários
    grafo = AdjacencyListGraph(num_vertices)
    
    # Opcional: Guardar os nomes dentro do objeto grafo para facilitar depois
    grafo.vertex_labels = lista_usuarios

    # 3. SEGUNDA PASSADA: Adicionar as arestas
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor) # Pular cabeçalho
        for linha in leitor:
            try:
                origem_nome = linha[0]
                destino_nome = linha[1]
                peso = float(linha[indice_peso]) # Pega o peso da coluna correta

                u = mapa_nome_id[origem_nome]
                v = mapa_nome_id[destino_nome]

                grafo.add_edge(u, v, peso)
            except Exception as e:
                # Ignora linhas mal formatadas
                continue

    print(f"Grafo carregado com sucesso! Arestas processadas: {grafo.get_edge_count()}")
    return grafo, mapa_nome_id

def analisar_grafo(grafo, nome_grafo):
    if not grafo: return

    print(f"\nANÁLISE RÁPIDA: {nome_grafo}")
    print(f"- Vértices: {grafo.get_vertex_count()}")
    print(f"- Arestas: {grafo.get_edge_count()}")
    
    # Exemplo de uso da API Obrigatória
    if grafo.get_vertex_count() > 0:
        # Pega o primeiro usuário (geralmente quem tem nome começando com número ou A)
        id_teste = 0
        nome_teste = grafo.vertex_labels[id_teste]
        grau_saida = grafo.get_vertex_out_degree(id_teste)
        grau_entrada = grafo.get_vertex_in_degree(id_teste)
        
        print(f"- Exemplo de Usuário: '{nome_teste}' (ID {id_teste})")
        print(f"  - Grau de Entrada (recebeu interação): {grau_entrada}")
        print(f"  - Grau de Saída (fez interação): {grau_saida}")

# --- BLOCO PRINCIPAL ---
if __name__ == "__main__":
    pasta = "dados_coletados"
    
    # ATENÇÃO: Os índices do peso mudam dependendo do arquivo gerado pelo coleta.py
    # Grafo 1 (Comentários): origem, destino, tipo, PESO(3), numero
    caminho_g1 = os.path.join(pasta, "grafo_1_comentarios.csv")
    grafo1, _ = carregar_grafo(caminho_g1, indice_peso=3)
    analisar_grafo(grafo1, "Grafo 1: Comentários")

    # Grafo 2 (Fechamentos): origem, destino, PESO(2), numero
    caminho_g2 = os.path.join(pasta, "grafo_2_fechamentos.csv")
    grafo2, _ = carregar_grafo(caminho_g2, indice_peso=2)
    analisar_grafo(grafo2, "Grafo 2: Fechamentos de Issue")

    # Grafo 3 (Reviews): origem, destino, acao, PESO(3), numero
    caminho_g3 = os.path.join(pasta, "grafo_3_pr_reviews.csv")
    grafo3, _ = carregar_grafo(caminho_g3, indice_peso=3)
    analisar_grafo(grafo3, "Grafo 3: Reviews e Merges")

    # --- EXPORTAÇÃO PARA GEPHI (Requisito Obrigatório) ---
    print("\n------------------------------------------------")
    print("GERANDO ARQUIVOS PARA O GEPHI (.gexf)")
    print("Estes arquivos devem ser abertos no software Gephi para gerar os diagramas.")
    print("------------------------------------------------")

    if grafo1:
        grafo1.export_to_gephi("gephi_grafo_1_comentarios.gexf")
    
    if grafo2:
        grafo2.export_to_gephi("gephi_grafo_2_fechamentos.gexf")
        
    if grafo3:
        grafo3.export_to_gephi("gephi_grafo_3_reviews.gexf")
    
    print("\nProcesso finalizado com sucesso!")