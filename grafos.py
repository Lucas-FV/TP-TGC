from abc import ABC, abstractmethod

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

    # --- MÉTODOS ABSTRATOS (API OBRIGATÓRIA) ---
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

    # --- LÓGICA DE RELACIONAMENTO ---
    def is_sucessor(self, u, v):
        # v é sucessor de u se existe aresta u -> v
        return self.has_edge(u, v)

    def is_predecessor(self, u, v):
        # u é predecessor de v se existe aresta u -> v
        return self.has_edge(u, v)

    def is_incident(self, u, v, x):
        # A aresta (u,v) incide em x se x é u ou x é v
        return self.has_edge(u, v) and (x == u or x == v)

    def is_divergent(self, u1, v1, u2, v2):
        # Divergência: Duas arestas saem do mesmo lugar (u1 == u2) para lugares diferentes
        return self.has_edge(u1, v1) and self.has_edge(u2, v2) and (u1 == u2) and (v1 != v2)

    def is_convergent(self, u1, v1, u2, v2):
        # Convergência: Duas arestas chegam no mesmo lugar (v1 == v2) de lugares diferentes
        return self.has_edge(u1, v1) and self.has_edge(u2, v2) and (v1 == v2) and (u1 != u2)

    # --- PROPRIEDADES GLOBAIS ---
    def is_empty_graph(self):
        return self.get_edge_count() == 0

    def is_complete_graph(self):
        # Grafo completo simples direcionado: n * (n-1) arestas
        max_edges = self.num_vertices * (self.num_vertices - 1)
        return self.get_edge_count() == max_edges

    @abstractmethod
    def is_connected(self): pass
    
    # O método abstrato para exportação é opcional na classe pai, 
    # mas obrigatório na implementação segundo o enunciado. 
    # Vamos defini-lo na AdjacencyListGraph.


# ------------------------------------------------------------------
# IMPLEMENTAÇÃO 1: MATRIZ DE ADJACÊNCIA (Melhor para grafos densos)
# ------------------------------------------------------------------
class AdjacencyMatrixGraph(AbstractGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        # Matriz NxN inicializada com 0
        self.matrix = [[0.0] * num_vertices for _ in range(num_vertices)]
        self._edge_count = 0

    def add_edge(self, u, v, weight=1.0):
        # Restrições: Grafo simples (sem laços)
        if u == v: return 
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            if self.matrix[u][v] == 0:
                self._edge_count += 1
            self.matrix[u][v] = weight # Idempotente: atualiza se já existe

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
        # Verificação simples de conectividade (BFS a partir do 0 ignorando direção - Conectividade Fraca)
        if self.num_vertices == 0: return True
        visited = [False] * self.num_vertices
        queue = [0]
        visited[0] = True
        count_visited = 0
        
        while queue:
            u = queue.pop(0)
            count_visited += 1
            for v in range(self.num_vertices):
                # Verifica aresta indo ou vindo (grafo subjacente não direcionado)
                if (self.matrix[u][v] != 0 or self.matrix[v][u] != 0) and not visited[v]:
                    visited[v] = True
                    queue.append(v)
                    
        return count_visited == self.num_vertices


# ------------------------------------------------------------------
# IMPLEMENTAÇÃO 2: LISTA DE ADJACÊNCIA (Melhor para grafos esparsos - SEU CASO)
# ------------------------------------------------------------------
class AdjacencyListGraph(AbstractGraph):
    def __init__(self, num_vertices):
        super().__init__(num_vertices)
        # Lista de listas. Cada item é [vizinho, peso]
        self.adj_list = [[] for _ in range(num_vertices)]
        self._edge_count = 0

    def add_edge(self, u, v, weight=1.0):
        if u == v: return # Sem laços
        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            # Verificar se já existe (Idempotência)
            for i, edge in enumerate(self.adj_list[u]):
                if edge[0] == v:
                    self.adj_list[u][i][1] = weight # Atualiza peso
                    return
            # Se não existe, adiciona
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
        # Na lista de adjacência, calcular grau de entrada é lento (precisa varrer tudo)
        for i in range(self.num_vertices):
            for edge in self.adj_list[i]:
                if edge[0] == u:
                    count += 1
        return count

    def is_connected(self):
        # Conectividade Fraca via BFS
        if self.num_vertices == 0: return True
        visited = [False] * self.num_vertices
        queue = [0]
        visited[0] = True
        count_visited = 0

        while queue:
            curr = queue.pop(0)
            count_visited += 1
            
            # Vizinhos diretos (curr -> v)
            for edge in self.adj_list[curr]:
                v = edge[0]
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
            
            # Vizinhos inversos (v -> curr) - Custo alto na lista, mas necessário
            for i in range(self.num_vertices):
                if not visited[i]: # Só verifica se ainda não visitou
                    for edge in self.adj_list[i]:
                        if edge[0] == curr:
                            visited[i] = True
                            queue.append(i)
                            break
                            
        return count_visited == self.num_vertices

    # --- MÉTODO OBRIGATÓRIO PARA O RELATÓRIO E AVALIAÇÃO ---
    def export_to_gephi(self, path_arquivo):
        print(f"--- Exportando grafo para: {path_arquivo} ---")
        try:
            with open(path_arquivo, 'w', encoding='utf-8') as f:
                # 1. Cabeçalho obrigatório do GEXF
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">\n')
                f.write('    <meta lastmodifieddate="2025-01-01">\n')
                f.write('        <creator>Trabalho Grafos Python</creator>\n')
                f.write('        <description>Exportação automática</description>\n')
                f.write('    </meta>\n')
                f.write('    <graph mode="static" defaultedgetype="directed">\n')
                
                # 2. Escrever os Nós (Vértices)
                f.write('        <nodes>\n')
                for i in range(self.num_vertices):
                    # Tenta pegar o nome do usuário. Se não tiver, usa o ID número.
                    if hasattr(self, 'vertex_labels') and i < len(self.vertex_labels):
                        rotulo = self.vertex_labels[i]
                        # Limpeza de segurança: XML quebra se tiver "&", "<" ou ">"
                        rotulo = rotulo.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                        rotulo = rotulo.replace("\"", "&quot;").replace("'", "&apos;")
                    else:
                        rotulo = str(i)
                    
                    f.write(f'            <node id="{i}" label="{rotulo}" />\n')
                f.write('        </nodes>\n')

                # 3. Escrever as Arestas
                f.write('        <edges>\n')
                id_aresta = 0
                for u in range(self.num_vertices):
                    for aresta in self.adj_list[u]:
                        v = aresta[0]     # Destino
                        peso = aresta[1]  # Peso
                        f.write(f'            <edge id="{id_aresta}" source="{u}" target="{v}" weight="{peso}" />\n')
                        id_aresta += 1
                f.write('        </edges>\n')
                
                # Fechamento do arquivo
                f.write('    </graph>\n')
                f.write('</gexf>\n')
                
            print(f"Sucesso! Arquivo '{path_arquivo}' gerado.")
            
        except Exception as e:
            print(f"Erro ao exportar para Gephi: {e}")