import ply.lex as lex
from colorama import Fore, Style

class Lexer:
    # Dicionário para mapear instruções e registradores com seus códigos binários
    binary_codes = {
        'MOV': '01',
        'ADD': '10',
        'B': '000',
        'C': '001',
    }
    variables = {}

    tokens = (
        'NOP',
        'MOV',
        'LOAD',
        'STO',
        'MVA',
        'LXI', 
        'ARITHMETICWORD',
        'ARITHMETICBYTE',
        'LABEL',
        'NL',
        'VARIABLE',
        'ENDLABEL',
    )

    # Expressão regular para ignorar espaços em branco e comentários
    t_ignore = ' ,<:\t'
    t_ignore_COMMENT = r'\/\/.*'

    def t_NL(self, t):
        r'\n'
        return t

    def t_newline(self, t):
        r'\n'
        t.lexer.lineno += len(t.value)

    def checkVariable(self, t): 
        inst = t.value.split(' ')
        have = False
        value = ''
        for char in inst:
            if '@' in char:
                have = True
                value = char
                break
        if have:
            if (value+':') in self.variables:
                return t
            else:
                #pass
                t.value = value
                t.type = 'VARNOTFOUND'
                lexer.t_error(t)
        else:
            return t

    def t_NOP(self, t):
        r'(NOP\b)'
        return t

    def t_MOV(self, t):
        r'(?<=(\t|\s))MOV\s+(B|C|D|E|H|L|W|Z)+,\s+((B|C|D|E|H|L|W|Z)|@[a-zA-Z]+|0x[0-9a-fA-F]{1,2})\b'
        return self.checkVariable(t)
    
    def t_STO(self, t):
        r'(?<=(\t|\s))STO\s+(F)+\sat\s+(@[a-zA-Z]+|0x[0-9a-fA-F]{4,4})\b'
        return self.checkVariable(t) 
    
    def t_LOAD(self, t):
        r'(?<=(\t|\s))LOAD\s+(B|D|H|W)+&+(C|E|L|Z)+\sat\s+(F|G)\b'
        return t
    
    def t_MVA(self, t):
        r'(?<=(\t|\s))MVA\s+((B|C|D|E|H|L|W|Z)|@[a-zA-Z]+|0x[0-9a-fA-F]{1,2})\b'
        return t

    def t_LXI(self, t):
        r'(?<=(\t|\s))LXI\s+(B|D|H|W),\s+(0x[0-9a-fA-F]{4,4})\b'
        return t

    def t_ARITHMETICWORD(self, t):
        #existem dois tipos de operações aritiméticas
        #operaçoes com apenas 8 bits e operaçoes com 16 bits
        #as duas operaçoes funcionam de formas ligeira mente diferentes
        #mas na sintax vamos tentar deixa-las mais parecidas
        r'(?<=(\t|\s))(ADD|MULT|OPA|DIV|ANA|XRA|ORA|MOD|add|mult|opa|div|ana|xra|ora|mod)\s+(WORD|word)\s+(B|D|H|W|b|d|h|w),\s+(0x[0-9a-fA-F]{4,4})\b'
        return t  

    def t_ARITHMETICBYTE(self, t):
        r'(?<=(\t|\s))(ADD|MULT|OPA|DIV|ANA|XRA|ORA|MOD|add|mult|opa|div|ana|xra|ora|mod)\s+(BYTE|byte)\s+(B|C|D|E|H|L|W|Z|b|c|d|e|h|l|w|z),\s+(0x[0-9a-fA-F]{2,2})\b'
        return t  
    
    def t_VARIABLE(self, t):
        r'(?<=(\t|\s))VAR\s+@[a-zA-Z]+:\s+(0x[0-9A-Fa-f]+|"[^"]*")\b'
        var = t.value.split(' ')
        type = var[0]
        name = var[1]
        value = var[2]
        self.variables[name] = (value, type, t.lexer.lineno)
        return t

    def t_LABEL(self, t):
        '[a-zA-Z_][a-zA-Z0-9_]*:'
        return t

    def t_ENDLABEL(self, t):
        '(?<=:)END'
        return t
    
    def t_error(self, t):
        count = 0
        errorWords = ''
        for i in t.value:
            if i == '\n':
                break
            count += 1
            errorWords += i
        if t.type == 'VARNOTFOUND':
            v = t.value
            print(f'{Fore.RED}Você chamou uma variavel: {Fore.BLUE}{v}{Fore.RED}\n\tQue não foi declarada{Style.RESET_ALL}')
        else:
            print(f"{Fore.RED}Erro na linha {t.lexer.lineno}:\n\tcaractere ilegal {Style.RESET_ALL}'{errorWords}'")
        t.lexer.skip(len(t.value))

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self, data):
        binary_codes = []
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
            binary_codes.append(tok.value)

        code = ''.join(binary_codes)
        return code

filename = 'c:/Users/kelwp/Downloads/pasta de programação/sagaCPU/Compilador teste/code.saga'
with open(filename, 'r') as file:
    lines = file.readlines()
    txtFormated = ''

    for line in lines:
        txtFormated += line

print(txtFormated)
lexer = Lexer()
code = lexer.tokenize(txtFormated)
print(code)