import ply.lex as lex
import ply.yacc as yacc
from colorama import Fore, Style

# Lista de tokens
tokens = [
    'HEX_NUMBER_WORD',
    'HEX_NUMBER_BYTE',
    'FORMAT',
    'DATAFORMAT',
    'STRING',
    'COMMA',
    'COLON',
    'JUMP',
    'LABEL',
    'VARIABLE',
    'REGISTER',
    'MOV',
    'MVA',
    'LXI',
    'LOAD',
    'STORE',
    'ARITHMETICB',
    'OUT',
    'OPENPARENTHESIS',
    'CLOSEPARENTHESIS',
    'OPENBRACKET',
    'CLOSEBRACKET',
    'COMMENT',
    'INDENT',
    'DEDENT'
]

# Expressões regulares para os tokens (já definidas anteriormente)
def t_HEX_NUMBER_WORD(t):
    r'0x[0-9a-fA-F]{4}'
    return t
def t_HEX_NUMBER_BYTE(t):
    r'0x[0-9a-fA-F]{2}'
    return t
def t_FORMAT(t):
    r'\"(%d|-%d|%s)\"'
    return t
def t_DATAFORMAT(t):
    r'\_[wbWB]'
    t.value = '8-BITS'
    if '_w' in t.value:
        t.value = '16-BITS'
    return t
def t_STRING(t):
    r'"[^"\n]*"'
    return t
def t_COMMA(t):
    r','
    #t.lexer.skip(1)
    return t
def t_COLON(t):
    r':'
    return t
def t_JUMP(t):
    r'(JMP|jmp|Jmp)'
    return t
def t_LABEL(t):
    r'_[a-zA-Z]+(?=:|$)|_[a-zA-Z]+(:[a-zA-Z]+)*'
    global current_block, error_found
    if not error_found:
        current_block = t.value
    return t
def t_VARIABLE(t):
    r'\$[a-zA-Z]+(?=:|$||\n)'
    return t
def t_MOV(t):
    r'(MOV|mov|Mov)'
    return t
def t_MVA(t):
    r'(MVA|mva|Mva)'
    return t
def t_LXI(t):
    r'(LXI|lxi|Lxi)'
    return t
def t_LOAD(t):
    r'(LOAD|load|Load)'
    return t
def t_STORE(t):
    r'(STORE|store|Store)'
    return t
def t_ARITHMETICB(t):
    r'(ADD8|add8|SUB8|sub8|MUL8|mul8|DIV8|div8|MOD8|mod8)'
    return t
def t_OUT(t):
    r'(OUT|out|Out)'
    return t
def t_OPENPARENTHESIS(t):
    r'\('
    return t
def t_CLOSEPARENTHESIS(t):
    r'\)'
    return t
def t_OPENBRACKET(t):
    r'\['
    return t
def t_CLOSEBRACKET(t):
    r'\]'
    return t
def t_REGISTER(t):
    r'(B|b|C|c|D|d|E|e|H|h|L|l|eax|EAX|ebx|EBX)'
    return t
def t_COMMENT(t):
    r'//.*'
    #print(f'Comentario: {t.value}')
    pass
# Contador de indentação
indent_count = 0
last_line = 0
# Tratamento de indentação e desindentação
def t_indent(t):
    r'\n[ \t]*'
    global indent_count
    indent_spaces = len(t.value) - 1
    indent_level = indent_spaces // 4
    if '\n' in t.value:# Incrementar o número de linha
        t.lexer.lineno += 1  

    if indent_spaces % 4 != 0 or indent_level > indent_count:
        t.type = 'INDENT'
        indent_count += 1
        return t
    elif indent_level < indent_count:
        t.type = 'DEDENT'
        indent_count -= 1
        return t
# Tratamento de nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1
# Ignorar espaços em branco
t_ignore = ' '

error_found = False
error_lineno = None
token_error = None
production_error = False
current_block = None
lines = 0

def countLines(data):
    global lines
    for l in data:
        if l == "\n":
            lines += 1
# Contador de número de linhas
def t_error(t):
    global error_found, error_lineno, token_error
    count = 0
    errorWords = ''
    for i in t.value:
        if i == '\n': 
            break
        count += 1
        errorWords += i
    if not error_found:
        error_lineno = t.lineno
        token_error = errorWords
        print(f"ERROR lexico: Caractere inválido '{token_error}' na linha {error_lineno}")
        t.type = 'ERROR'
        t.lineno = error_lineno
        t.value = token_error
        error_found = True
    t.lexer.skip(count)
    return t

# Criação do lexer
lexer = lex.lex()

# Definição das regras de produção
def p_program(p):
    '''
    program : blocks
    '''
    global production_error
    if not production_error:
        print(f"{Fore.GREEN}Programa valido!{Style.RESET_ALL}")
def p_blocks(p):
    '''
    blocks : blocks block
           | blocks label_block
           | block
    '''
def p_label_block(p):
    '''
    label_block : label_colon label_instruction
    '''
def p_label_instruction(p):
    '''
    label_instruction : INDENT instructions DEDENT 
    '''
def p_label_colon(p):
    '''
    label_colon : LABEL COLON 
    '''
def p_block(p):
    '''
    block : instructions
    '''
def p_instructions(p):
    '''
    instructions : instructions instruction
                 | instruction
    '''
def p_instruction(p):
    '''
    instruction : mov_registers
                | mov_register_number
                | mva_number
                | lxi_register_number
                | load_variable_address
                | store_value
                | arithmeticb
                | out_format_var
                | jump
                | variable
                | empty
    '''

def p_mov_registers(p):
    '''
    mov_registers : MOV REGISTER COMMA REGISTER
    '''
def p_mov_register_number(p):
    '''
    mov_register_number : MOV REGISTER COMMA HEX_NUMBER_BYTE
                        | MOV REGISTER COMMA VARIABLE
    '''
def p_mva_number(p):
    '''
    mva_number : MVA HEX_NUMBER_BYTE
    '''
def p_lxi_register_number(p):
    '''
    lxi_register_number : LXI REGISTER COMMA HEX_NUMBER_WORD
    '''
def p_load_variable_address(p):
    '''
    load_variable_address : LOAD OPENBRACKET VARIABLE CLOSEBRACKET
                          | LOAD OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET
    '''
def p_store_value(p):
    '''
    store_value : STORE REGISTER COMMA OPENBRACKET VARIABLE CLOSEBRACKET
                | STORE REGISTER COMMA OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET
    '''
def p_arithmeticb(p):
    '''
    arithmeticb : ARITHMETICB REGISTER
    '''
def p_out_format_var(p):
    '''
    out_format_var : OUT OPENPARENTHESIS FORMAT COMMA VARIABLE CLOSEPARENTHESIS
                   | OUT OPENPARENTHESIS STRING CLOSEPARENTHESIS
                   | OUT OPENPARENTHESIS CLOSEPARENTHESIS
    '''
def p_jump(p):
    '''
    jump : JUMP OPENBRACKET LABEL CLOSEBRACKET
         | JUMP OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET
    '''
def p_variable(p):
    '''
    variable : VARIABLE COLON HEX_NUMBER_WORD
             | VARIABLE COLON STRING
    '''
def p_empty(p):
    '''
    empty :
    '''


# Tratamento de erros
def p_error(p):
    count = 0
    errorWords = ''
    countEnd = 0
    for i in p.value:
        if i == '\n': 
            break
        count += 1
        errorWords += i
    global production_error, token_error, current_block, lines
    line_error = (lines - countEnd)+1
    if p:
        production_error = True
        if p.type == 'INDENT' or p.type == 'DEDENT':
            print(f"{Fore.RED}Erro de Indentação: Indentação inesperada{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Instrução inesperada:\n{Fore.GREEN}----> {error_lineno}{Style.RESET_ALL} {errorWords}")
    elif not p:
        print(f"Erro de sintaxe: \n\tFim inesperado na linha: {error_lineno}")

# Criação do parser
parser = yacc.yacc()

# Teste
data = '''
load [$a]
mov b, 0x00
'''
countLines(data)
lexer.input(data)
for token in lexer:
    print(token)

parser.parse(data)
