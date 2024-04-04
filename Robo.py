import docker
import time
import threading

class Robo:
        
    @staticmethod
    def sobe_container_chrome():
        cliente = docker.from_env()
        container_config = {
            'image': 'selenium/standalone-chrome',  # Imagem com o Chrome para Selenium
            'detach': True,  # Executar o contêiner em segundo plano
            'volumes': {'/tmp/.X11-unix': {'bind': '/tmp/.X11-unix', 'mode': 'rw'}},  # Monta o socket X11
            'environment': ['DISPLAY=:0']  # Define a variável de ambiente DISPLAY
        }

        container = cliente.containers.run(**container_config)

        print(f"ID do container: {container.id}")

        # Loop infinito para manter o programa em execução enquanto o contêiner estiver aberto
        while True:
            if container.status == 'exited':
                print("O contêiner foi encerrado. Encerrando o programa.")
                break
            time.sleep(5)  # Verifica a cada 5 segundos se o contêiner ainda está em execução

    @staticmethod
    def inicia_container(quantidade):
        threads = []

        for _ in range(quantidade):
            thread = threading.Thread(target=Robo.sobe_container_chrome)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    @staticmethod
    def derruba_containers():
        cliente = docker.from_env()
        containers = cliente.containers.list()
        
        for container in containers:
            container.stop()


if __name__ == "__main__":
    containers = int(input("Digite a quantidade de containers que deseja subir: "))
    Robo.inicia_container(quantidade=containers)

    Robo.derruba_containers()