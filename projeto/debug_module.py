import logging as log

DEBUG_MODE = True


def innit_log(LOGFILE):
    
    
    log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s %(ip)s %(entrada)-2s %(message)s',
                    # {etiqueta temporal} {tipo de entrada} {endereço IP[:porta]} {dados da entrada}
                    filename=LOGFILE,
                    filemode='w',
                    datefmt='%d-%m-%y %H:%M:%S')

"""
Ficheiros de log - Estes ficheiros registam toda a atividade relevante do componente; 
deve existir uma entrada de log por cada linha do ficheiro; sempre que um componente 
arranca este deve verificar a existência dos ficheiros de log indicados no seu ficheiro
de configuração; se não existir algum deve ser criado e se já existirem as novas 
entradas devem ser registadas a partir da última entrada já existente no ficheiro;
a sintaxe de cada entrada é a seguinte (a etiqueta temporal é a data e hora completado 
sistema operativo na altura em que aconteceu a atividade registada e não a data e hora
em que foi registada):



Tipos de entradas aceites:
# QR/QE - foi recebida/enviada uma query do/para o endereço indicado; os dados da entrada
devem ser os dados relevantes incluídos na query; a sintaxe dos dados de entrada é a mesma que
é usada no PDU de query no modo debug de comunicação entre os elementos;
# RP/RR - foi enviada/recebida uma resposta a uma query para o/do endereço indicado; os dados
da entrada devem ser os dados relevantes incluídos na resposta à query; a sintaxe dos dados de
entrada é a mesma que é usada no PDU de resposta às queries no modo debug de comunicação
entre os elementos;
# ZT - foi iniciado e concluído corretamente um processo de transferência de zona; o endereço
deve indicar o servidor na outra ponta da transferência; os dados da entrada devem indicar qual
o papel do servidor local na transferência (SP ou SS) e, opcionalmente, a duração em
milissegundos da transferência e o total de bytes transferidos;
# EV - foi detetado um evento/atividade interna no componente; o endereço deve indicar 127.0.0.1
(ou localhost ou @); os dados da entrada devem incluir informação adicional sobre a atividade
reportada (por exemplo, ficheiro de configuração/dados/ST lido, criado ficheiro de log, etc.);
# ER - foi recebido um PDU do endereço indicado que não foi possível descodificar corretamente;
opcionalmente, os dados da entrada podem ser usados para indicar informação adicional (como,
por exemplo, o que foi possível descodificar corretamente e em que parte/byte aconteceu o erro);
# EZ - foi detetado um erro num processo de transferência de zona que não foi concluída
corretamente; o endereço deve indicar o servidor na outra ponta da transferência; os dados da
entrada devem indicar qual o papel do servidor local na transferência (SP ou SS);
# FL - foi detetado um erro no funcionamento interno do componente; o endereço deve indicar
127.0.0.1; os dados da entrada devem incluir informação adicional sobre a situação de erro (por
exemplo, um erro na descodificação ou incoerência dos parâmetros de algum ficheiro de
configuração ou de base de dados);
# TO - foi detetado um timeout na interação com o servidor no endereço indicado; os dados da
entrada devem especificar que tipo de timeout ocorreu (resposta a uma query ou tentativa de
contato com um SP para saber informações sobre a versão da base de dados ou para iniciar uma
transferência de zona);
# SP - a execução do componente foi parada; o endereço deve indicar 127.0.0.1; os dados da
entrada devem incluir informação adicional sobre a razão da paragem se for possível obtê-la;
# ST - a execução do componente foi iniciada; o endereço deve indicar 127.0.0.1; os dados da
entrada devem incluir informação sobre a porta de atendimento, sobre o valor do timeout usado
(em milissegundos) e sobre o modo de funcionamento (modo “shy” ou modo debug). 
"""
def debug(msg,ip=None,entrada=None):
    if DEBUG_MODE:
        print(msg)
    d = {'ip': ip, 'entrada': entrada}
    # d = {'ip': '192.168.0.1', 'entrada': 'FL'}
    log.debug(msg,extra=d)


def exception(msg):
    if DEBUG_MODE:
        print(msg)

    log.exception(msg)
