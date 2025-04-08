import multiprocessing
import threading
import time
import random


def aluno_thread(queue, lock, aluno_id):
    nome_prova = f"\nAluno {aluno_id} - prova sobre SO"
    with lock:
        print(f"\n[Aluno {aluno_id}] Entregando prova.")
        queue.put((aluno_id, nome_prova))


def professor_processo(queue, lock, professor_id):
    while True:
        try:
            with lock:
                if queue.empty():
                    break
                aluno_id, prova = queue.get()
                print(f"\n[Professor {professor_id}] Começando a corrigir a prova do Aluno {aluno_id}")

            tempo_inicio = time.time()
            tempo_correcao = random.randint(2, 5)
            time.sleep(tempo_correcao)
            tempo_fim = time.time()

            print(
                f"\n[Professor {professor_id}] Terminou de corrigir a prova do Aluno {aluno_id} (Tempo: {tempo_fim - tempo_inicio:.2f}s)")
        except Exception as e:
            print(f"\n[Professor {professor_id}] Erro: {e}")


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    fila_provas = multiprocessing.Queue()
    lock = multiprocessing.Lock()

    professores = []
    for i in range(2):
        p = multiprocessing.Process(target=professor_processo, args=(fila_provas, lock, i + 1))
        p.start()
        professores.append(p)

    threads_alunos = []
    for i in range(10):
        t = threading.Thread(target=aluno_thread, args=(fila_provas, lock, i + 1))
        t.start()
        threads_alunos.append(t)

    for t in threads_alunos:
        t.join()

    time.sleep(20)
    for p in professores:
        p.terminate()