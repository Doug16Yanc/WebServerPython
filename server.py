import socket
from threading import Thread

host = '127.0.0.1' #Localhost (Dizem as boas e más línguas que as coisas só funcionam corretamente aqui)
port = 8000     #Número da porta para acessar o servidor

#Criamos o nosso socket para a camada de aplicação
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
serversocket.bind((host , port)) 
serversocket.listen(1)  

#Enquanto o cliente ou uma interrupção abrupta não encerrar a conexão.
while True:
    #Aceita a conexão porque o TCP é organizado
    connection , address = serversocket.accept()
    request = connection.recv(1024).decode('utf-8') #Para só então receber 
    string_list = request.split(' ')

    #Validação de requisição
    if len(string_list) < 2:
        connection.close()
        continue

    #Obtenção do método para processar o arquivo solicitado
    method = string_list[0]
    requesting_file = string_list[1]

    print('Client request',requesting_file)

    #Obtenção do nome do arquivo
    myfile = requesting_file.split('?')[0]
    myfile = myfile.lstrip('/')

    #Padrãozinho básico HTML
    if(myfile == ''):
        myfile = 'index.html'
    
    #Tratamento de exceção para que as coisas ocorram adequadamente
    try:
        file = open(myfile , 'rb')
        response = file.read()
        file.close()

        #Resposta do servidor mais esperada de todos os tempos
        header = 'HTTP/1.1 200 OK\n'

        #Para processar outros tipos de arquivos
        if(myfile.endswith('.jpg')):
            mimetype = 'image/jpg'
        elif(myfile.endswith('.css')):
            mimetype = 'text/css'
       
        else:
            mimetype = 'text/html'

        header += 'Content-Type: '+str(mimetype)+'\n\n'

    #O retorno da exceção caso dê erro
    except Exception as e:
        print("-")
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body>Error 404: File not found</body></html>'.encode('utf-8')

    #Tudo para fechar a conexão adequadamente
    final_response = header.encode('utf-8')
    final_response += response
    connection.send(final_response)
    connection.close()
