"""
    Seguem-se algumas considerações que podem ajudar na sua implementação:

# A cache pode ser implementada à custa duma estrutura de dados equivalente a uma tabela com
nove colunas/campos, em que cada linha/posição representa uma entrada completa (ou DNS
Resource Record).

Os nove campos/colunas são:
(a) parâmetro/Name,
(b) tipo do valor/Type,
(c) valor/Value,
(d) tempo de validade/TTL ,
(e) prioridade/Order,
(f) origem da entrada/Origin (FILE, SP, OTHERS),
(g) tempo em segundos que passou desde o arranque do servidor até ao momento em que
    a entrada foi registada na cache/TimeStamp,
(h) número da entrada/Index (as entradas válidas são numeradas/indexadas de 1 até N,
em que N é o número total de entradas na cache, incluindo as entradas livres/FREE) e
(i) estado da entrada/Status (FREE, VALID).

# Quando o servidor arranca a cache deve ser inicializada com, pelo menos, uma entrada/posição
FREE (se o tamanho da cache for gerido dinamicamente, o que não é relevante no contexto do
trabalho) ou então com N entradas FREE (se o tamanho é fixo a N entradas).

# Deve ser implementada uma função para procurar uma entrada VALID a partir de três valores
Index, Name e Type. A função deve devolver o índice da primeira entrada encontrada que faça o
match com Name e Type. A procura deve começar a partir da entrada com o índice Index. Sempre
que é necessário encontrar todas as entradas que façam match ao tuplo [Name,Type] deve
começar-se com Index=1 e repetir-se até o índice devolvido ser igual a N+1. Esta função deve
também verificar se as entradas visitadas com Origin igual a OTHERS estão expiradas (i.e., se
o tempo que já passou desde o momento do registo da entrada guardado em TimeStamp for
superior a TTL). Nesse caso deve colocar-se essas entradas como FREE. Assim, a função de
procura serve também para atualizar as entradas da cache e desativar as entradas expiradas.

# Deve ser implementada uma função para registar/atualizar uma entrada na cache. Se o campo
Origin da entrada for igual a FILE ou SP, então deve ser registada a entrada na primeira posição
FREE da cache, com o TimeStamp calculado no momento do registo e com Status igual a VALID.
Se o campo Origin da entrada a registar for igual a OTHERS, primeiro é necessário procurar se
a entrada completa já existe ou não na cache (i.e., se faz o match dos campos Name, Type, Value,
TTL, e Order): (i) se já existir e o campo Origin da entrada existente for igual a FILE ou SP,
ignora-se o pedido de registo; (ii) se já existir e o campo Origin da entrada existente for igual a
OTHERS atualiza-se o campo TimeStamp com o valor calculado no momento e atualiza-se o
campo Status para VALID; (iii) se não existir, então regista-se a nova entrada na última posição
FREE, com o TimeStamp calculado no momento e com Status igual a VALID.

# Quando um SP arranca deve registar na cache todas as entradas dos seus ficheiros de bases de
dados dos domínios para o qual é primário, utilizando repetidamente a função anterior com o
campo Origin igual a FILE.

# Quando um SS arranca deve fazer uma transferência de zona dos SP respetivos e deve registar
na sua cache todas as entradas recebidas do SP, utilizando repetidamente a função anterior com
o campo Origin igual a SP.

# Quando uma entrada é registada ou atualizada na cache deve ser gerada uma entrada
correspondente no ficheiro de logs (se o modo de funcionamento for de debug essa entrada deve
também ser impressa no standard output).

# Deve ser implementada uma função que atualize, em todas as entradas da cache com Name igual
ao domínio passado como argumento, o campo Status para FREE. Quando o temporizador
associado à idade da base de dados dum SS relativo a um domínio atinge o valor de SOAEXPIRE,
então o SS deve executar esta função para esse domínio. Esta função é exclusiva dos servidores
do tipo secundário.

# Não é importante os grupos terem preocupações de otimização destas funções de procura, registo
e atualização da cache, quer em termos de velocidade de execução quer em termos de ocupação
de memória.

# Todas as respostas a queries devem ser procuradas na cache, independentemente do tipo de
servidor, uma vez que a cache armazena todas os resource records disponíveis num servidor.

"""


class Cache:

    def __init__(self):

        # A cache pode ser implementada à custa duma estrutura de dados equivalente a uma tabela com
        # nove colunas/campos, em que cada linha/posição representa uma entrada completa (ou DNS
        # Resource Record).
        self.headers = ("Name",
                        "Type",
                        "Value",
                        "TTL",
                        "Order",
                        "Origin",
                        "TimeStamp",   
                        "Index",
                        "Status")
        
        self.cacheSize = 25
        self.cacheOccupancy = 0

        self.table = [("", "", "", "", "",
                       "", "", i, "FREE") for i in range(self.cacheSize)]

        # (a) parâmetro/Name,
        # (b) tipo do valor/Type,
        # (c) valor/Value,
        # (d) tempo de validade/TTL ,
        # (e) prioridade/Order,
        # (f) origem da entrada/Origin (FILE, SP, OTHERS),
        # (g) tempo em segundos que passou desde o arranque do servidor até ao momento em que
        #     a entrada foi registada na cache/TimeStamp,
        # (h) número da entrada/Index (as entradas válidas são numeradas/indexadas de 1 até N,
        # em que N é o número total de entradas na cache, incluindo as entradas livres/FREE) e
        # (i) estado da entrada/Status (FREE, VALID).

    def addEntry(self, entry, atIndex=None):
        if atIndex is None:
            i = 0
            for line in self.table:
                if line[8] == "FREE":
                    self.table[i] = entry + (i, "VALID")
                    self.cacheOccupancy += 1
                    break
                i += 1
        else:
            if self.table[atIndex][8] == "FREE":
                self.table[atIndex] = entry + (atIndex, "VALID")
                self.cacheOccupancy += 1
                
            else:
                print("CACHE ERROR: INDEX ALREADY IN USE")

    def getEntry(self, atIndex):
        i = 0
        for line in self.table:
            if i == atIndex:
                return self.table[i]
            i += 1

    def removeEntry(self, atIndex):
        i = 0
        for line in self.table:
            if i == atIndex:
                self.table[i] = ("", "", "", "",
                                 "", "", "", i, "FREE")
            i += 1

    def entryToString(self, entry):
        return
    def stringToEntry(self):
        return

    def __str__(self):
        output = "CACHE:\n"
        
        
        # Print cabecalho
        j = 0 
        for header in self.headers:
            
            if j == 2 or j == 0:
                output += "{:^26}".format(header) + "|"
            else:
                output += "{:^11}".format(header) + "|"
            j += 1 
        output += "\n"
         
        for i in range(9):
            if i == 2 or i == 0:
                output += "{:^26}".format("---------------") + "|"
            else:
                output += "{:^11}".format("---------") + "|"
                
        for line in self.table:
            output += "\n"
            
            j = 0
            for cell in line:
                if j == 2 or j == 0:
                    output +=  " {:25}".format(str(cell)) + "|"
                else:
                    output += " {:10}".format(str(cell)) + "|"  
                j += 1

        return output


def main():
    table = Cache()
    table.addEntry(("Name", "Type", "Value", "TTL", "Order",
                   "Origin", "TimeStamp"), 8)

    table.addEntry(("Name", "Type", "Value", "TTL", "Order",
                   "Origin", "TimeStamp"), 2)
    table.addEntry(("Name", "Type", "Value", "TTL", "Order",
                   "Origin", "TimeStamp"))
    table.addEntry(("Name", "Type", "Value", "TTL", "Order",
                   "Origin", "TimeStamp"), 2)

    table.removeEntry(8)
    print(table)

    print(table.getEntry(2))


if __name__ == "__main__":
    main()
