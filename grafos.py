from abc import ABC, abstractmethod
import heapq

# ------------------------------------------------------------------
# CLASSE ABSTRATA (MODELO OBRIGATÓRIO)
# ------------------------------------------------------------------
class AbstractGraph(ABC):
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.vertex_weights = [0.0] * num_vertices
        self.vertex_labels = [""] * num_vertices

    def get_vertex_count(self):
        return self.num_vertices

    def set_vertex_weight(self, v, weight):
        if 0 <= v < self.num_vertices:
            self.vertex_weights[v] = weight

    def get_vertex_weight(self, v):
        if 0 <= v < self.num_vertices:
            return self.vertex_weights[v]
        return 0.0

    # --- MÉTODOS ABSTRATOS (API OBRIGATÓRIA - PDF) ---
    @abstractmethod
    def add_edge(self, u, v, weight=1.0): pass

    @abstractmethod
    def remove_edge(self, u, v): pass

    @abstractmethod
    def has_edge(self, u, v): pass

    @abstractmethod
    def get_edge_count(self): pass

    @abstractmethod
    def get_edge_weight(self, u, v): pass

    @abstractmethod
    def set_edge_weight(self, u, v, weight): pass

    @abstractmethod
    def get_vertex_in_degree(self, u): pass

    @abstractmethod
    def get_vertex_out_degree(self, u): pass

    # --- LÓGICA DE RELACIONAMENTO (Implementação Padrão) ---
    def is_sucessor(self, u, v):
        return self.has_edge(u, v)

    def is_predecessor(self, u, v):
        return self.has_edge(u, v)

    def is_incident(self, u, v, x):
        return self.has_edge(u, v) and (x == u or x == v)

    def is_divergent(self, u1, v1, u2, v2):
        return self.has_edge(u1, v1) and self.has_edge(u2, v2) and (u1 == u2) and (v1 != v2)

    def is_convergent(self, u1, v1, u2, v2):
        return self.has_edge(u1, v1) and self.has_edge(u2, v2) and (v1 == v2) and (u1 != u2)

    # --- PROPRIEDADES GLOBAIS ---
    def is_empty_graph(self):
        return self.get_edge_count() == 0

    def is_complete_graph(self):
        max_edges = self.num_vertices * (self.num_vertices - 1)
        return self.get_edge_count() == max_edges

    @abstractmethod
    def is_connected(self): pass

# ------------------------------------------------------------------
# IMPLEMENTAÇÃO 1: MATRIZ DE ADJACÊNCIA
# ------------------------------------------------------------------
class AdjacencyMatrixGraph(AbstractGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        self.matrix = [[0.0] * num_vertices for _ in range(num_vertices)]
        self._edge_count = 0

    def add_edge(self, u, v, weight=1.0):
        if u == v: return 
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            if self.matrix[u][v] == 0:
                self._edge_count += 1
            self.matrix[u][v] = weight

    def remove_edge(self, u, v):
        if self.has_edge(u, v):
            self.matrix[u][v] = 0.0
            self._edge_count -= 1

    def has_edge(self, u, v):
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            return self.matrix[u][v] != 0.0
        return False

    def get_edge_count(self):
        return self._edge_count

    def get_edge_weight(self, u, v):
        if self.has_edge(u, v):
            return self.matrix[u][v]
        return 0.0

    def set_edge_weight(self, u, v, weight):
        if self.has_edge(u, v):
            self.matrix[u][v] = weight

    def get_vertex_out_degree(self, u):
        count = 0
        if 0 <= u < self.num_vertices:
            for v in range(self.num_vertices):
                if self.matrix[u][v] != 0:
                    count += 1
        return count

    def get_vertex_in_degree(self, u):
        count = 0
        if 0 <= u < self.num_vertices:
            for r in range(self.num_vertices):
                if self.matrix[r][u] != 0:
                    count += 1
        return count

    def is_connected(self):
        if self.num_vertices == 0: return True
        visited = [False] * self.num_vertices
        queue = [0]
        visited[0] = True
        count_visited = 0
        while queue:
            u = queue.pop(0)
            count_visited += 1
            for v in range(self.num_vertices):
                if (self.matrix[u][v] != 0 or self.matrix[v][u] != 0) and not visited[v]:
                    visited[v] = True
                    queue.append(v)
        return count_visited == self.num_vertices


# ------------------------------------------------------------------
# IMPLEMENTAÇÃO 2: LISTA DE ADJACÊNCIA (A PRINCIPAL)
# ------------------------------------------------------------------
class AdjacencyListGraph(AbstractGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        self.adj_list = [[] for _ in range(num_vertices)]
        self._edge_count = 0

    def add_edge(self, u, v, weight=1.0):
        if u == v: return
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            for i, edge in enumerate(self.adj_list[u]):
                if edge[0] == v:
                    self.adj_list[u][i][1] = weight
                    return
            self.adj_list[u].append([v, weight])
            self._edge_count += 1

    def remove_edge(self, u, v):
        if 0 <= u < self.num_vertices:
            for i, edge in enumerate(self.adj_list[u]):
                if edge[0] == v:
                    self.adj_list[u].pop(i)
                    self._edge_count -= 1
                    return

    def has_edge(self, u, v):
        if 0 <= u < self.num_vertices:
            for edge in self.adj_list[u]:
                if edge[0] == v:
                    return True
        return False

    def get_edge_count(self):
        return self._edge_count

    def get_edge_weight(self, u, v):
        if 0 <= u < self.num_vertices:
            for edge in self.adj_list[u]:
                if edge[0] == v:
                    return edge[1]
        return 0.0

    def set_edge_weight(self, u, v, weight):
        if 0 <= u < self.num_vertices:
            for edge in self.adj_list[u]:
                if edge[0] == v:
                    edge[1] = weight
                    return

    def get_vertex_out_degree(self, u):
        if 0 <= u < self.num_vertices:
            return len(self.adj_list[u])
        return 0

    def get_vertex_in_degree(self, u):
        count = 0
        for i in range(self.num_vertices):
            for edge in self.adj_list[i]:
                if edge[0] == u:
                    count += 1
        return count

    def is_connected(self):
        if self.num_vertices == 0: return True
        visited = [False] * self.num_vertices
        queue = [0]
        visited[0] = True
        count_visited = 0
        while queue:
            curr = queue.pop(0)
            count_visited += 1
            for edge in self.adj_list[curr]:
                v = edge[0]
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
            for i in range(self.num_vertices):
                if not visited[i]:
                    for edge in self.adj_list[i]:
                        if edge[0] == curr:
                            visited[i] = True
                            queue.append(i)
                            break
        return count_visited == self.num_vertices
    
    # ====================================================================
       # --- Métrica 3: Taxa de Reciprocidade ---
    def calcular_reciprocidade(self):
        """
        Calcula a taxa de reciprocidade do grafo direcionado.
        Mede a proporção de relações bidirecionais (u -> v e v -> u)
        em relação ao total de pares que possuem ao menos uma aresta.
        """
        pares_com_interacao = set()
        pares_reciprocos = set()

        for u in range(self.num_vertices):
            for aresta in self.adj_list[u]:
                v = aresta[0]

                # Par não ordenado (u, v) para evitar duplicidade
                par = tuple(sorted((u, v)))
                pares_com_interacao.add(par)

                # Verifica se existe a aresta inversa
                if self.has_edge(v, u):
                    pares_reciprocos.add(par)

        if len(pares_com_interacao) == 0:
            return 0.0

        return len(pares_reciprocos) / len(pares_com_interacao)

    #     # --- Métrica 4: Densidade da Rede ---
    def calcular_densidade(self):
        """
        Calcula a densidade de um grafo direcionado.
        Densidade = arestas_existentes / arestas_possíveis
        """
        n = self.num_vertices

        if n <= 1:
            return 0.0

        arestas_existentes = self.get_edge_count()
        arestas_possiveis = n * (n - 1)

        return arestas_existentes / arestas_possiveis


    # --- Métrica 1: Cálculo do Grau Médio (GMCE) ---
    def calcular_gmce(self):
        n = self.num_vertices
        if n == 0:
            return 0.0

        graus = []
        for i in range(n):
            graus.append(self.get_vertex_out_degree(i))

        soma_total_metricas = 0.0

        for u in range(n):
            grau_u = graus[u]
            if grau_u == 0:
                continue

            soma_graus_vizinhos = 0.0
            
            # Otimização: Iterar sobre a lista de adjacência
            for aresta in self.adj_list[u]:
                v = aresta[0] # [vizinho, peso]
                soma_graus_vizinhos += graus[v]

            media_vizinhos = soma_graus_vizinhos / grau_u
            valor_conectividade_u = grau_u * media_vizinhos
            soma_total_metricas += valor_conectividade_u

        gmce = soma_total_metricas / n
        return gmce
        
    # --- Métrica 2: Coeficiente de Proximidade (Usando DIJKSTRA) ---
    def _dijkstra(self, start_node):
        distancias = {i: float('inf') for i in range(self.num_vertices)}
        distancias[start_node] = 0
            
        pq = [(0, start_node)]

        while pq:
            dist_atual, u = heapq.heappop(pq)

            if dist_atual > distancias[u]:
                continue

            for aresta in self.adj_list[u]:
                v = aresta[0]
                peso = aresta[1]
                    
                # Aqui o peso é usado como distância (Custo)
                nova_dist = dist_atual + peso

                if nova_dist < distancias[v]:
                    distancias[v] = nova_dist
                    heapq.heappush(pq, (nova_dist, v))
            
        return distancias

    def calcular_coeficiente_proximidade(self):
        n = self.num_vertices
        if n == 0: return 0.0

        soma_proximidades = 0.0
        nos_processados = 0

        print(f"   > Iniciando cálculo de Dijkstra para {n} nós...")
            
        for i in range(n):
            if i % 100 == 0: print(f"     Processando nó {i}/{n}...")

            distancias = self._dijkstra(i)
                
            soma_distancias = 0
            contagem_alcancaveis = 0
                
            for d in distancias.values():
                if d != float('inf') and d > 0:
                    soma_distancias += d
                    contagem_alcancaveis += 1
                
            if soma_distancias > 0:
                proximidade = contagem_alcancaveis / soma_distancias
                soma_proximidades += proximidade
                nos_processados += 1

        if nos_processados == 0:
            return 0.0
                
        return soma_proximidades / nos_processados

    # ====================================================================
    #   Métrica NOVA: PageRank (Influência / Importância)
    #   - Sem biblioteca de grafos
    #   - Considera pesos nas arestas (normaliza por soma de pesos de saída)
    # ====================================================================
    def calcular_pagerank(self, damping=0.85, max_iter=100, tol=1e-6):
        """
        PageRank em grafo direcionado.
        Interpretação: nós "importantes" são aqueles que recebem links (arestas)
        de outros nós importantes.

        - damping: fator de amortecimento (0.85 padrão)
        - max_iter: máximo de iterações
        - tol: tolerância de convergência (L1)
        
        Retorna: lista rank[n] com o PageRank de cada vértice.
        """
        n = self.num_vertices
        if n == 0:
            return []

        # rank inicial uniforme
        rank = [1.0 / n] * n

        # pré-cálculo: soma dos pesos de saída de cada u
        out_weight_sum = [0.0] * n
        for u in range(n):
            s = 0.0
            for v, w in self.adj_list[u]:
                # garante peso positivo (se seu dataset puder ter 0/negativo, trate aqui)
                if w > 0:
                    s += w
            out_weight_sum[u] = s

        base = (1.0 - damping) / n

        for _ in range(max_iter):
            new_rank = [base] * n

            # soma do rank "pendurado" (dangling nodes: sem saída)
            dangling_mass = 0.0
            for u in range(n):
                if out_weight_sum[u] == 0.0:
                    dangling_mass += rank[u]

            # distribui massa pendurada igualmente
            if dangling_mass > 0.0:
                add = damping * (dangling_mass / n)
                for i in range(n):
                    new_rank[i] += add

            # distribui contribuições pelos links
            for u in range(n):
                su = out_weight_sum[u]
                if su == 0.0:
                    continue

                ru = rank[u]
                for v, w in self.adj_list[u]:
                    if w <= 0:
                        continue
                    # transição ponderada
                    new_rank[v] += damping * ru * (w / su)

            # checa convergência (norma L1)
            diff = 0.0
            for i in range(n):
                diff += abs(new_rank[i] - rank[i])

            rank = new_rank
            if diff < tol:
                break

        # normalização final (segurança numérica)
        s = sum(rank)
        if s > 0:
            rank = [x / s for x in rank]
        return rank

    def top_pagerank(self, k=10, damping=0.85, max_iter=100, tol=1e-6):
        """
        Retorna top-k nós por PageRank com rótulo (se existir).
        """
        pr = self.calcular_pagerank(damping=damping, max_iter=max_iter, tol=tol)
        pares = []
        for i, val in enumerate(pr):
            label = self.vertex_labels[i] if hasattr(self, 'vertex_labels') and i < len(self.vertex_labels) else str(i)
            pares.append((i, label, val))
        pares.sort(key=lambda x: x[2], reverse=True)
        return pares[:k]

    # ====================================================================
    #   Exportação para o GEPHI
    # ====================================================================
    def export_to_gephi(self, path_arquivo):
        print(f"--- Exportando para Gephi: {path_arquivo} ---")
        try:
            with open(path_arquivo, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">\n')
                f.write('    <meta><creator>Trabalho Grafos</creator></meta>\n')
                f.write('    <graph mode="static" defaultedgetype="directed">\n')
                
                f.write('        <nodes>\n')
                for i in range(self.num_vertices):
                    rotulo = str(i)
                    if hasattr(self, 'vertex_labels') and i < len(self.vertex_labels):
                        rotulo = self.vertex_labels[i].replace("&", "").replace("<", "").replace(">", "")
                    f.write(f'            <node id="{i}" label="{rotulo}" />\n')
                f.write('        </nodes>\n')

                f.write('        <edges>\n')
                id_aresta = 0
                for u in range(self.num_vertices):
                    for aresta in self.adj_list[u]:
                        f.write(f'            <edge id="{id_aresta}" source="{u}" target="{aresta[0]}" weight="{aresta[1]}" />\n')
                        id_aresta += 1
                f.write('        </edges>\n')
                f.write('    </graph>\n')
                f.write('</gexf>\n')
            print("Exportação concluída.")
        except Exception as e:
            print(f"Erro exportar Gephi: {e}")

            