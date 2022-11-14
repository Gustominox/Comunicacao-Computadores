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

            
    def getlines(self):
        return self.lines
    


        # else:
        #     print(char,end="")

    # details_dict = dict(config.)
