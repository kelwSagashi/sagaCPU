import ply.lex as lex
import ply.yacc as yacc
from colorama import Fore, Style

#variavei globais
error_found = False
error_lineno = None
token_error = None
production_error = False
current_block = None
lines = 0
# Contador de indentação
indent_count = 0
last_line = 0

# Lista de tokens
tokens = [
    'HEX_NUMBER_WORD',
    'HEX_NUMBER_BYTE',
    'FORMAT',
    'BYTE',
    'WORD',
    'STR',
    'STRING',
    'COMMA',
    'COLON',
    'JUMP',
    'LABEL',
    'VARIABLE',
    'REGISTERPAIR',
    'REGISTER',
    'EXTENDEDREGISTER',
    'MOVP',
    'MOV',
    'LXI',
    'LOAD',
    'STORE',
    'ARITHMETIC',
    'LOGIC',
    'OUT',
    'OPENTAG',
    'CLOSETAG',
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
def t_BYTE(t):
    r'(byte)'
    return t
def t_WORD(t):
    r'(word)'
    return t
def t_STR(t):
    r'(str)'
    return t
def t_STRING(t):
    r'"[^"\n]*"'
    return t
def t_COMMA(t):
    r','
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
def t_MOVP(t):
    r'(MOVP|movp|Movp)'
    return t
def t_MOV(t):
    r'(MOV|mov|Mov)'
    return t
def t_LXI(t):
    r'(LXI|lxi|Lxi)'
    return t
def t_LOAD(t):
    r'(LDW|ldw|Ldw)'
    return t
def t_STORE(t):
    r'(STW|stw|Stw)'
    return t
def t_ARITHMETIC(t):
    r'(ADD|add|SUB|sub|MUL|mul|DIV|div|MOD|mod)'
    return t
def t_LOCIC(t):
    r'(CMP|cmp|ANA|ana|XRA|xra|ORA|ora)'
    return t
def t_OUT(t):
    r'(OUT|out|Out)'
    return t
def t_OPENTAG(t):
    r'<'
    return t
def t_CLOSETAG(t):
    r'>'
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
def t_EXTENDEDREGISTER(t):
    r'(eax|EAX|ebx|EBX)'
    return t
def t_REGISTERPAIR(t):
    r'((B|b|D|d|H|h|W|w)+(C|c|E|e|L|l|Z|z)|pbx|pdx|phx|pwx)'
    return t
def t_REGISTER(t):
    r'(A|a|B|b|C|c|D|d|E|e|H|h|L|l|Z|z)'
    return t
def t_COMMENT(t):
    r'//.*'
    pass
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
                | mov_register_variable
                | movp_registerpair_registerpair
                | movp_extendedregister_registerpair
                | lxi_register_number
                | load_registerpair_variable
                | load_registerpair_address
                | load_extendedregister_address
                | load_extendedregister_variable
                | load_registerpair_number
                | load_extendedregister_number
                | store_variable_registerpair
                | store_address_registerpair
                | store_address_extendedregister
                | store_variable_extendedregister
                | arithmetic_byte_register_register
                | logic_byte_register_register
                | out_format_var
                | out_string
                | out
                | jump_label
                | jump_address
                | variable_byte
                | variable_word
                | variable_str
                | empty
    '''

def p_mov_registers(p):
    '''
    mov_registers : MOV REGISTER COMMA REGISTER
    '''
def p_mov_register_number(p):
    '''
    mov_register_number : MOV REGISTER COMMA HEX_NUMBER_BYTE
    '''
def p_mov_register_variable(p):
    '''
    mov_register_variable : MOV REGISTER COMMA VARIABLE
    '''
def p_movp_registerpair_registerpair(p):
    '''
    movp_registerpair_registerpair : MOVP REGISTERPAIR COMMA REGISTERPAIR
    '''
def p_movp_extendedregister_registerpair(p):
    '''
    movp_extendedregister_registerpair : MOVP EXTENDEDREGISTER COMMA REGISTERPAIR
    '''
def p_lxi_register_number(p):
    '''
    lxi_register_number : LXI REGISTER COMMA HEX_NUMBER_WORD
    '''
def p_load_registerpair_variabl(p):
    '''
    load_registerpair_variable : LOAD REGISTERPAIR COMMA OPENBRACKET VARIABLE CLOSEBRACKET
    '''
def p_load_registerpair_address(p):
    '''
    load_registerpair_address : LOAD REGISTERPAIR COMMA OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET
    '''
def p_load_extendedregister_address(p):
    '''
    load_extendedregister_address : LOAD EXTENDEDREGISTER COMMA OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET
    '''
def p_load_extendedregister_variable(p):
    '''
    load_extendedregister_variable : LOAD EXTENDEDREGISTER COMMA OPENBRACKET VARIABLE CLOSEBRACKET
    '''
def p_load_registerpair_number(p):
    '''
    load_registerpair_number : LOAD REGISTERPAIR COMMA HEX_NUMBER_WORD 
    '''
def p_load_extendedregister_number(p):
    '''
    load_extendedregister_number : LOAD EXTENDEDREGISTER COMMA HEX_NUMBER_WORD 
    '''
def p_store_variable_registerpair(p):
    '''
    store_variable_registerpair : STORE OPENBRACKET VARIABLE CLOSEBRACKET COMMA REGISTERPAIR
    '''
def p_store_address_registerpair(p):
    '''
    store_address_registerpair : STORE OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET COMMA REGISTERPAIR
    '''
def p_store_variable_extendedregister(p):
    '''
    store_variable_extendedregister : STORE OPENBRACKET VARIABLE CLOSEBRACKET COMMA EXTENDEDREGISTER
    '''
def p_store_address_extendedregister(p):
    '''
    store_address_extendedregister : STORE OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET COMMA EXTENDEDREGISTER
    '''
def p_arithmetic_byte_register_register(p):
    '''
    arithmetic_byte_register_register : ARITHMETIC OPENTAG BYTE CLOSETAG REGISTER COMMA REGISTER
    '''
def p_logic_byte_register_register(p):
    '''
    logic_byte_register_register : LOGIC OPENTAG BYTE CLOSETAG REGISTER COMMA REGISTER
    '''
def p_out_format_var(p):
    '''
    out_format_var : OUT OPENPARENTHESIS FORMAT COMMA VARIABLE CLOSEPARENTHESIS
    '''
def p_out_string(p):
    '''
    out_string : OUT OPENPARENTHESIS STRING CLOSEPARENTHESIS
    '''
def p_out(p):
    '''
    out : OUT OPENPARENTHESIS CLOSEPARENTHESIS
    '''
def p_jump_label(p):
    '''
    jump_label : JUMP OPENBRACKET LABEL CLOSEBRACKET
    '''
def p_jump_address(p):
    '''
    jump_address : JUMP OPENBRACKET HEX_NUMBER_WORD CLOSEBRACKET
    '''
def p_variable_byte(p):
    '''
    variable_byte : VARIABLE OPENTAG BYTE CLOSETAG COLON HEX_NUMBER_BYTE
    '''
def p_variable_word(p):
    '''
    variable_word : VARIABLE OPENTAG WORD CLOSETAG COLON HEX_NUMBER_WORD
    '''
def p_variable_str(p):
    '''
    variable_str : VARIABLE OPENTAG STR CLOSETAG COLON STRING
    '''
def p_empty(p):
    '''
    empty :
    '''
# Tratamento de erros das regras de produção
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

def compile_data(data):
    # Criação do parser
    parser = yacc.yacc()
    #contar as linhas do codigo
    countLines(data)
    # Criação do lexer
    lexer.input(data)
    # tokenize
    for token in lexer:
        print(token)
    # Análise sintática
    parser.parse(data)