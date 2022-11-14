import logging as log

class config:

    def __init__(self):
        self.lines = []
                
        
    def read(self,filename):
        
        uncutLines = []
        remove = False
        fich = open(filename, "r")
        text = fich.read()

        string = ""

        for char in text:
            if char == '\n':
                if not remove and string != "":
                    uncutLines.append(string)
                string = ""
                remove = False
                continue
            
            string = string + char
            if char == '#':
                remove = True
        
        string = ""
        
        tokenLine = []
        
        for line in uncutLines:
            tokenLine = []
            for char in line:
                if char == ' ':
                    tokenLine.append(string)
                    string = ""
                    continue
                string = string + char
            
            tokenLine.append(string)
            string = ""
            self.lines.append(tokenLine)
            
        self.process_lines()

    
    def process_lines(self):
        for line in self.lines:
            # DB - O valor indica o ficheiro da base de dados com a informação 
            # do domínio indicado no parâmetro
            if line[1] == 'DB':     
                print("BASE DE DADOS")
                
            # SS - O valor indica o endereço IP[:porta] dum SS do domínio indicado
            # no parâmetro (o servidor assume o papel de SP para este domínio)
            # e que passa a ter autorização para pedir a transmissão da
            # informação da base de dados (transferência de zona);
            # podem existir várias entradas para o mesmo parâmetro (uma por cada SS do domínio)    
            if line[1] == 'SS':
                print("BASE DE DADOS")
            
            # DD – O valor indica o endereço IP[:porta] dum SR, dum SS ou dum SP do
            # domínio por defeito indicado no parâmetro; 
            # quando os servidores que assumem o papel de SR usam este parâmetro é para indicar quais  
            # os domínios para os quais devem contactar diretamente os  
            # servidores indicados se receberem queries sobre estes domínios (quando 
            # a resposta não está em cache), em vez de contactarem um dos ST; podem
            # existir várias entradas para o mesmo parâmetro (uma por cada servidor 
            # do domínio por defeito); quando os servidores que assumem o papel de 
            # SP ou SS usam este parâmetro é para indicar os únicos domínios para 
            # os quais respondem (quer a resposta esta em cache ou não), i.e., nestes 
            # casos, o parâmetro serve para restringir o funcionamento dos SP ou 
            # SS a responderem apenas a queries sobre os domínios indicados neste parâmetro
            if line[1] == 'DD':
                print("BASE DE DADOS")
            
    def getlines(self):
        return self.lines
    
