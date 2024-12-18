import paramiko
import time
from ping3 import ping

# Solicitar o número da filial
numero_filial=input('Digite o número da Filial:')
# Configurações do servidor
hostname = f'172.16.{numero_filial}.254'   # Substitua pelo endereço IP ou hostname do seu servidor
port = 22  # Porta padrão do SSH
username = ''
password = ''

def restart_server():
    try:
        # Cria uma instância de SSHClient
        client = paramiko.SSHClient()
        
        # Carrega as chaves do sistema
        client.load_system_host_keys()
        
        # Adiciona a chave do servidor (não recomendado para produção)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Conecta ao servidor
        # systemctl restart openvpn-client comando para reistartar vnpn
        client.connect(hostname, port, username, password)
        
        # Comando para reiniciar o servidor
        command = 'sudo reboot'
        
        # Executa o comando
        stdin, stdout, stderr = client.exec_command(command)
                
    
        # Lê a saída e erros
        
        print(stdout.read().decode())
        print("Erros:")
        print(stderr.read().decode())
        
        # Fecha a conexão
        client.close()
 # Monitoramento para verificar quando o servidor voltar online
        print("Monitorando o servidor...")
        time.sleep(15)  # Espera 10 segundos antes de tentar novamente
        while True:
            
            response = ping(hostname)
            
            if response is not None:
                print("Servidor reiniciado e está online!")
                break
            else:
                print("Servidor ainda offline. Aguardando...")
                time.sleep(10)  # Espera 10 segundos antes de tentar novamente
        
    except paramiko.SSHException as e:
        print(f"Erro de SSH: {e}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    restart_server()
