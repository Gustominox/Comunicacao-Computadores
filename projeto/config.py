import logging as log

class Config:

    def __init__(self,file_name):
        self.lines = []
        self.logFile = "NOLOGFILE"
        self.DBFile = "NODBFILE"
        
        self.read(file_name)
        
        
    def __str__(self):
        string = "[ CONFIG FILE:\n"
        for line in self.lines:
            string = string + str(line) + "," + "\n"
        string = string + "]"
        return string
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
                self.setDBFile(line[2])
                
                 
                
            # SS - O valor indica o endereço IP[:porta] dum SS do domínio indicado
            # no parâmetro (o servidor assume o papel de SP para este domínio)
            # e que passa a ter autorização para pedir a transmissão da
            # informação da base de dados (transferência de zona);
            #
            # Podem existir várias entradas para o mesmo parâmetro (uma por cada SS do domínio)    
            if line[1] == 'SS':
                print("BASE DE DADOS")
            
            # DD – O valor indica o endereço IP[:porta] dum SR, dum SS ou dum SP do
            # domínio por defeito indicado no parâmetro; 
            # 
            # Quando os servidores que assumem o papel de SR usam este parâmetro é
            # para indicar quais os domínios para os quais devem contactar diretamente
            # os servidores indicados se receberem queries sobre estes domínios (quando 
            # a resposta não está em cache), em vez de contactarem um dos ST;
            # 
            # Podem existir várias entradas para o mesmo parâmetro (uma por cada 
            # servidor do domínio por defeito);
            # 
            # Quando os servidores que assumem o papel de SP ou SS usam este parâmetro
            # é para indicar os únicos domínios para os quais respondem (quer a 
            # resposta esta em cache ou não), i.e., nestes casos, o parâmetro serve 
            # para restringir o funcionamento dos SP ou SS a responderem apenas a 
            # queries sobre os domínios indicados neste parâmetro
            if line[1] == 'DD':
                print("BASE DE DADOS")
            
            # SP – o valor indica o endereço IP[:porta] do SP do domínio indicado 
            # no parâmetro (o servidor assume o papel de SS para este domínio); 
            if line[1] == 'SP':
                print("BASE DE DADOS")
            
            # ST – o valor indica o ficheiro com a lista dos ST (o parâmetro
            # deve ser igual a “root”); 
            if line[1] == 'ST':
                print("BASE DE DADOS")
            
            # LG – o valor indica o ficheiro de log que o servidor deve utilizar
            # para registar a atividade do servidor associada ao domínio indicado 
            # no parâmetro;
            # 
            # Só podem ser indicados domínios para o qual o servidor é SP ou SS; 
            # 
            # Tem de existir pelo menos uma entrada a referir um ficheiro de log 
            # para toda a atividade que não seja diretamente  referente aos domínios
            # especificados noutras entradas LG (neste caso o parâmetro deve ser 
            # igual a “all”).
            if line[1] == 'LG':
                print("BASE DE DADOS")
        
            self.setLogFile(line[2])
            
    def getLogFile(self):
        return self.logFile
        
    def setLogFile(self,new_name):
        self.logFile = new_name
        
        
    def getDBFile(self):
        return self.DBFile
        
    def setDBFile(self,new_name):
        self.DBFile = new_name
        
    def getlines(self):
        return self.lines
    
