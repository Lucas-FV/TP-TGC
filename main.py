import csv
import os
import sys
from grafos import AdjacencyListGraph

# --- FUNÇÃO DE CARREGAMENTO (Mantida igual) ---
def carregar_grafo(caminho_arquivo, indice_peso):
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo não encontrado: {caminho_arquivo}")
        return None

    # 1. Identificar vértices
    usuarios = set()
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor)
        for linha in leitor:
            if len(linha) >= 2:
                usuarios.add(linha[0])
                usuarios.add(linha[1])
    
    lista_usuarios = sorted(list(usuarios))
    num_vertices = len(lista_usuarios)
    mapa_nome_id = {nome: i for i, nome in enumerate(lista_usuarios)}

    # 2. Instanciar
    grafo = AdjacencyListGraph(num_vertices)
    grafo.vertex_labels = lista_usuarios

    # 3. Preencher arestas
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor)
        for linha in leitor:
            try:
                u = mapa_nome_id[linha[0]]
                v = mapa_nome_id[linha[1]]
                peso = float(linha[indice_peso])
                grafo.add_edge(u, v, peso)
            except:
                continue
    
    return grafo

# --- MENU DE MÉTRICAS (Sub-menu) ---
def menu_metricas(grafo, nome_grafo):
    while True:
        print(f"\n==============================================")
        print(f"GRAFO SELECIONADO: {nome_grafo}")
        print(f"----------------------------------------------")
        # Informações Básicas (Sempre mostradas)
        print(f"  > Total Vértices: {grafo.get_vertex_count()}")
        print(f"  > Total Arestas:  {grafo.get_edge_count()}")
        print(f"==============================================")
        print("Escolha uma métrica para calcular:")
        print("1. Grau Médio Ponderado por Conectividade Efetiva")
        print("2. Índice de Robustez por Redundância de Caminhos")
        print("3. Coeficiente de Proximidade Estrutural Global")
        print("4. Exportar para Gephi (.gexf)")
        print("0. Voltar ao Menu Principal")
        print("----------------------------------------------")
        
        opcao = input("Digite sua opção: ")

        if opcao == '1':
            print("\n--- Calculando Grau Médio Ponderado (GMCE)... ---")
            resultado = grafo.calcular_gmce()
            print(f"Resultado GMCE: {resultado:.4f}")
            input("\nPressione Enter para continuar...")

        elif opcao == '2':
            print("\n--- Calculando Índice de Robustez (IRRC)... ---")
            # print(f"Resultado: {resultado}")
            print("(Esta métrica ainda será implementada na classe AbstractGraph)")
            input("\nPressione Enter para continuar...")

        elif opcao == '3':
            print("\n--- Calculando Coeficiente de Proximidade... ---")
            # FUTURO: resultado = grafo.calcular_coeficiente_proximidade()
            # print(f"Resultado: {resultado}")
            print("(Esta métrica ainda será implementada na classe AbstractGraph)")
            input("\nPressione Enter para continuar...")

        elif opcao == '4':
            nome_arquivo = f"gephi_export_{nome_grafo.split()[1]}.gexf"
            grafo.export_to_gephi(nome_arquivo)
            input("\nPressione Enter para continuar...")

        elif opcao == '0':
            break # Sai do loop de métricas e volta pro menu principal
        else:
            print("Opção inválida!")

# --- MENU PRINCIPAL ---
def main():
    pasta = "dados_coletados"
    print("\n--- INICIALIZANDO SISTEMA ---")
    print("Carregando grafos na memória, aguarde...")

    # Carrega tudo de uma vez para não ter delay no menu
    g1 = carregar_grafo(os.path.join(pasta, "grafo_1_comentarios.csv"), indice_peso=3)
    g2 = carregar_grafo(os.path.join(pasta, "grafo_2_fechamentos.csv"), indice_peso=2)
    g3 = carregar_grafo(os.path.join(pasta, "grafo_3_pr_reviews.csv"), indice_peso=3)
    
    if not g1 or not g2 or not g3:
        print("ERRO CRÍTICO: Não foi possível carregar os arquivos CSV.")
        print("Verifique se rodou o 'coleta.py' primeiro.")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear') # Limpa tela (opcional)
        print(f"\n==============================================")
        print(f"      ANÁLISE DE REDES - XCODEGEN")
        print(f"==============================================")
        print("Selecione o Grafo para trabalhar:")
        print("1. Grafo 1: Comentários (Issues/PRs)")
        print("2. Grafo 2: Fechamento de Issues")
        print("3. Grafo 3: Reviews e Merges")
        print("0. Sair")
        print("----------------------------------------------")
        
        escolha = input("Opção: ")

        if escolha == '1':
            menu_metricas(g1, "Grafo 1 (Comentários)")
        elif escolha == '2':
            menu_metricas(g2, "Grafo 2 (Fechamentos)")
        elif escolha == '3':
            menu_metricas(g3, "Grafo 3 (Reviews)")
        elif escolha == '0':
            print("Encerrando ferramenta. Até logo!")
            sys.exit()
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()