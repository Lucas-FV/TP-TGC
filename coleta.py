import csv
import time
import os
from github import Github, RateLimitExceededException

# --- CONFIGURAÇÃO ---
GITHUB_TOKEN = "" 
REPO_NAME = "yonaskolb/XcodeGen"
PASTA_SAIDA = "dados_coletados" 

def coletar_dados():
    print("Conectando ao GitHub...")
    g = Github(GITHUB_TOKEN)
    
    try:
        repo = g.get_repo(REPO_NAME)
        print(f"Repositório encontrado: {repo.full_name}")
    except Exception as e:
        print(f"Erro ao acessar repositório: {e}")
        return

    # --- CRIAÇÃO DA PASTA ---
    # Verifica se a pasta existe, se não, cria
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        print(f"Pasta '{PASTA_SAIDA}' criada com sucesso.")
    else:
        print(f"Salvando arquivos na pasta '{PASTA_SAIDA}'.")

    # --- PREPARAÇÃO DOS ARQUIVOS CSV ---
    
    # Grafo 1: Comentários em issues ou pull requests
    caminho_f1 = os.path.join(PASTA_SAIDA, 'grafo_1_comentarios.csv')
    f1 = open(caminho_f1, 'w', newline='', encoding='utf-8')
    w1 = csv.writer(f1)
    w1.writerow(['origem', 'destino', 'tipo', 'peso_sugerido', 'numero_issue'])

    # Grafo 2: Fechamento de issue por outro usuário
    caminho_f2 = os.path.join(PASTA_SAIDA, 'grafo_2_fechamentos.csv')
    f2 = open(caminho_f2, 'w', newline='', encoding='utf-8')
    w2 = csv.writer(f2)
    w2.writerow(['origem', 'destino', 'peso_sugerido', 'numero_issue'])

    # Grafo 3: Revisões, aprovações e merges de PRs
    caminho_f3 = os.path.join(PASTA_SAIDA, 'grafo_3_pr_reviews.csv')
    f3 = open(caminho_f3, 'w', newline='', encoding='utf-8')
    w3 = csv.writer(f3)
    w3.writerow(['origem', 'destino', 'acao', 'peso_sugerido', 'numero_pr'])

    # --- COLETA DE ISSUES E COMENTÁRIOS ---
    print("\n--- Iniciando coleta de Issues e Comentários (Grafos 1 e 2) ---")
    issues = repo.get_issues(state='closed')
    
    # DICA: Descomente a linha abaixo para testes rápidos (pega apenas as últimas 100)
    # issues = issues[:100] 

    count = 0
    for issue in issues:
        try:
            count += 1
            if count % 50 == 0: print(f"Processando item {count}...")

            owner = issue.user.login 

            # GRAFO 2: Fechamento de Issue (Peso 3) [cite: 33]
            if issue.pull_request is None and issue.closed_by:
                closer = issue.closed_by.login
                if closer != owner:
                    w2.writerow([closer, owner, 3, issue.number])

            # GRAFO 1: Comentários (Peso 2) [cite: 32]
            if issue.comments > 0:
                comments = issue.get_comments()
                for comment in comments:
                    commenter = comment.user.login
                    if commenter != owner: 
                        tipo = "pr" if issue.pull_request else "issue"
                        w1.writerow([commenter, owner, tipo, 2, issue.number])
        
        except RateLimitExceededException:
            print("Limite da API atingido. Aguardando 60 segundos...")
            time.sleep(60)
        except Exception as e:
            print(f"Erro ao processar issue {issue.number}: {e}")
            continue

    # --- COLETA DE PULL REQUESTS (MERGES E REVIEWS) ---
    print("\n--- Iniciando coleta detalhada de Pull Requests (Grafo 3) ---")
    pulls = repo.get_pulls(state='closed')
    
    # DICA: Descomente a linha abaixo para testes rápidos
    # pulls = pulls[:100]

    count_pr = 0
    for pr in pulls:
        try:
            count_pr += 1
            if count_pr % 20 == 0: print(f"Processando PR {count_pr}...")

            pr_owner = pr.user.login 

            # GRAFO 3: Merges (Peso 5) [cite: 35]
            if pr.merged and pr.merged_by:
                merger = pr.merged_by.login
                if merger != pr_owner:
                    w3.writerow([merger, pr_owner, 'MERGE', 5, pr.number])

            # GRAFO 3: Revisões e Aprovações (Peso 4) [cite: 34]
            reviews = pr.get_reviews()
            for review in reviews:
                reviewer = review.user.login
                if reviewer != pr_owner:
                    if review.state in ['APPROVED', 'CHANGES_REQUESTED', 'COMMENTED']:
                        w3.writerow([reviewer, pr_owner, review.state, 4, pr.number])

        except RateLimitExceededException:
            print("Limite da API atingido. Aguardando 60 segundos...")
            time.sleep(60)
        except Exception as e:
            print(f"Erro ao processar PR {pr.number}: {e}")
            continue

    f1.close()
    f2.close()
    f3.close()
    print(f"\nSucesso! Arquivos salvos na pasta '{PASTA_SAIDA}'.")

if __name__ == "__main__":
    coletar_dados()