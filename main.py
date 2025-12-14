import csv
import os
import sys
from grafos import AdjacencyListGraph

# --- FUNÇÃO DE CARREGAMENTO ---
def carregar_grafo(caminho_arquivo, indice_peso):
    if not os.path.exists(caminho_arquivo):
        print(f"ERRO: Arquivo não encontrado: {caminho_arquivo}")
        return None

    # 1. Identificar vértices
    usuarios = set()
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        leitor = csv.reader(f)
        next(leitor, None)
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
        next(leitor, None)
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
        # Densidade no cabeçalho (rápido)
        try:
            densidade_info = f"{grafo.calcular_densidade():.6f}"
        except:
            densidade_info = "N/A"

        print(f"\n==============================================")
        print(f"GRAFO SELECIONADO: {nome_grafo}")
        print(f"----------------------------------------------")
        print(f"  > Total Vértices: {grafo.get_vertex_count()}")
        print(f"  > Total Arestas:  {grafo.get_edge_count()}")
        print(f"  > Densidade:      {densidade_info}")
        print(f"==============================================")
        print("Escolha uma métrica para calcular:")
        print("1. Grau Médio Ponderado por Conectividade Efetiva (GMCE)")
        print("2. Coeficiente de Proximidade Estrutural Global (Dijkstra)")
        print("3. Taxa de Reciprocidade (Colaboração Mútua)")
        print("4. Densidade da Rede (Detalhada)")
        print("5. PageRank (Influência / Importância dos usuários)")
        print("0. Voltar ao Menu Principal")
        print("----------------------------------------------")

        opcao = input("Digite sua opção: ")

        if opcao == '1':
            print("\n--- Calculando Grau Médio Ponderado (GMCE)... ---")
            try:
                resultado = grafo.calcular_gmce()
                print(f">>> Resultado GMCE: {resultado:.6f}")
                print("Interpretação: Indica a conectividade média considerando o peso das interações.")
            except AttributeError:
                print("ERRO: Método 'calcular_gmce' não encontrado em grafos.py")
            input("\nPressione Enter para continuar...")

        elif opcao == '2':
            print("\n--- Calculando Coeficiente de Proximidade (Dijkstra)... ---")
            print("Aviso: Isso pode levar alguns instantes (algoritmo complexo).")
            try:
                resultado = grafo.calcular_coeficiente_proximidade()
                print(f">>> Resultado Proximidade Global: {resultado:.6f}")
                print("Interpretação: Média de quão perto (em custo) cada nó está de todos os outros alcançáveis.")
            except AttributeError:
                print("ERRO: Método 'calcular_coeficiente_proximidade' não encontrado em grafos.py")
            input("\nPressione Enter para continuar...")

        elif opcao == '3':
            print("\n--- Calculando Taxa de Reciprocidade... ---")
            try:
                resultado = grafo.calcular_reciprocidade()
                print(f">>> Resultado Reciprocidade: {resultado:.2%}")
                if resultado < 0.3:
                    print("Interpretação: Baixa reciprocidade (Hierarquia, suporte ou poucos pares mútuos).")
                else:
                    print("Interpretação: Alta reciprocidade (Equipe mais colaborativa).")
            except AttributeError:
                print("ERRO: Método 'calcular_reciprocidade' não encontrado em grafos.py")
            input("\nPressione Enter para continuar...")

        elif opcao == '4':
            print("\n--- Calculando Densidade da Rede... ---")
            try:
                resultado = grafo.calcular_densidade()
                print(f">>> Resultado Densidade: {resultado:.8f}")
                if resultado < 0.05:
                    print("Interpretação: Rede Esparsa (típico de comunidades grandes/Open Source).")
                else:
                    print("Interpretação: Rede Densa (muitas conexões possíveis presentes).")
            except AttributeError:
                print("ERRO: Método 'calcular_densidade' não encontrado em grafos.py")
            input("\nPressione Enter para continuar...")

        elif opcao == '5':
            print("\n--- Calculando PageRank (Influência)... ---")
            print("Aviso: Pode levar alguns instantes dependendo do tamanho da rede.")
            try:
                top = grafo.top_pagerank(k=10, damping=0.85, max_iter=100, tol=1e-6)
                print("Top 10 usuários por influência (PageRank):")
                for pos, (vid, label, score) in enumerate(top, start=1):
                    print(f"{pos:02d}. {label} (id={vid}) -> {score:.6f}")
                print("Interpretação: nós com alto PageRank recebem interações de nós também influentes.")
            except AttributeError:
                print("ERRO: Métodos 'calcular_pagerank/top_pagerank' não encontrados em grafos.py")
            input("\nPressione Enter para continuar...")

        elif opcao == '0':
            break
        else:
            print("Opção inválida!")

# --- MENU PRINCIPAL ---
def main():
    pasta = "dados_coletados"
    print("\n--- INICIALIZANDO SISTEMA ---")
    print("Carregando grafos na memória, aguarde...")

    g1 = carregar_grafo(os.path.join(pasta, "grafo_1_comentarios.csv"), indice_peso=3)
    g2 = carregar_grafo(os.path.join(pasta, "grafo_2_fechamentos.csv"), indice_peso=2)
    g3 = carregar_grafo(os.path.join(pasta, "grafo_3_pr_reviews.csv"), indice_peso=3)

    if not g1 or not g2 or not g3:
        print("ERRO CRÍTICO: Não foi possível carregar os arquivos CSV.")
        print("Verifique se a pasta 'dados_coletados' existe e se rodou o 'coleta.py'.")
        return

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
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
