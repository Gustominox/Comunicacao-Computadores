pduText = '''# Header
MESSAGE-ID = 3874,FLAGS = Q+R,RESPONSE-CODE = 0,N-VALUES = 0,N-AUTHORITIES = 0,N-EXTRA-VALUES = 0,;
# Data: Query Info
QUERY-INFO.NAME = example.com.,QUERY-INFO.TYPE = MX,;
# Data: List of Response, Authorities and Extra Values
RESPONSE-VALUES = (Null)
AUTHORITIES-VALUES = (Null)
EXTRA-VALUES = (Null)'''


class Pdu:

    def __init__(self,
                 messageId,
                 flags,
                 responseCode,
                 nValues,
                 nAuthorities,
                 nExtraValues,
                 queryInfo_Name,
                 queryInfo_Type,
                 responseValues,
                 authoritiesValues,
                 extraValues):
            
                self.messageId = messageId  
                self.flags = flags 
                self.responseCode = responseCode  
                self.nValues = nValues 
                self.nAuthorities = nAuthorities 
                self.nExtraValues = nExtraValues 
                self.queryInfo_Name = queryInfo_Name 
                self.queryInfo_Type = queryInfo_Type 
                self.responseValues = responseValues 
                self.authoritiesValues = authoritiesValues 
                self.extraValues = extraValues 


    def __init__(self, queryText):

        self.lines = self.fromText(queryText)

        for line in self.lines:
            typeValue = self.matchValue(line[0])
            
            # Header
            if typeValue == 0: 
                self.messageId = line[2]
            if typeValue == 1: 
                self.flags = line[2]
            if typeValue == 2: 
                self.responseCode = line[2]
            if typeValue == 3: 
                self.nValues = line[2]
            if typeValue == 4: 
                self.nAuthorities = line[2]
            if typeValue == 5: 
                self.nExtraValues = line[2]

            
            # Data: Query Info
            if typeValue == 6: 
                self.queryInfo_Name = line[2]
            if typeValue == 7: 
                self.queryInfo_Type = line[2]

            # Data: List of Response, Authorities and Extra Values
            if typeValue == 8: 
                self.responseValues = line[2]  # (Null)
            if typeValue == 9: 
                self.authoritiesValues = line[2]  # (Null)
            if typeValue == 10: 
                self.extraValues = line[2]  # (Null)

    def __str__(self):
        
        string = "# Header\n"
        string += "MESSAGE-ID = " + self.messageId + ","
        string += "FLAGS = " + self.flags + ","
        string += "RESPONSE-CODE = " + self.responseCode + ","
        string += "N-VALUES = " + self.nValues + ","
        string += "N-AUTHORITIES = " + self.nAuthorities + ","
        string += "N-EXTRA-VALUES = " + self.nExtraValues + ","+";\n"
        
        string += "# Data: Query Info\n"
        string += "QUERY-INFO.NAME = " + self.queryInfo_Name + ","
        string += "QUERY-INFO.TYPE = " + self.queryInfo_Type + ","+";\n"
        
        string += "# Data: List of Response, Authorities responseValues Extra Values\n"
        string += "RESPONSE-VALUES = " + self.responseValues + "\n"
        string += "AUTHORITIES-VALUES = " + self.authoritiesValues + "\n"
        string += "EXTRA-VALUES = " + self.extraValues
        
        
        return string

    def matchValue(self, value):

        
        if value == "MESSAGE-ID":
            return 0
        elif value == "FLAGS":
            return 1
        elif value == "RESPONSE-CODE":
            return 2
        elif value == "N-VALUES":
            return 3
        elif value == "N-AUTHORITIES":
            return 4
        elif value == "N-EXTRA-VALUES":
            return 5
        elif value == "QUERY-INFO.NAME":
            return 6
        elif value == "QUERY-INFO.TYPE":
            return 7
        elif value == "RESPONSE-VALUES":
            return 8
        elif value == "AUTHORITIES-VALUES":
            return 9
        elif value == "EXTRA-VALUES":
            return 10


    def fromText(self, pduText):
        uncutLines = []
        remove = False

        string = ""

        for char in pduText:
            if char == ';' or char == '\n':
                if not remove and string != "":
                    uncutLines.append(string)
                string = ""
                remove = False
                continue

            string = string + char
            if char == '#':
                remove = True

        if string != "":
            uncutLines.append(string)
            string = ""

        # print("UNCUT: " +   str(uncutLines))

        string = ""

        tokenLine = []
        fields = []

        for line in uncutLines:
            tokenLine = []
            for char in line:
                if char == ',':
                    tokenLine.append(string)
                    string = ""
                    continue

                string = string + char
            if string != "":
                tokenLine.append(string)
                string = ""

            fields.append(tokenLine)

        string = ""
        out = []
        for field in fields:
            for value in field:
                valueLine = []
                for char in value:
                    # print(char)

                    if char == ' ':
                        valueLine.append(string)
                        string = ""
                        continue
                    string = string + char
                if string != "":
                    valueLine.append(string)
                    string = ""
                out.append(valueLine)

        # DEBUG
        self.lines = out
        ###
        return out

# debug
pdu = Pdu(pduText)

p = Pdu(str(pdu))

print(p)


