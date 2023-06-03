import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import re as re

# Palavras reservadas
reserved_words = {
    (r'0x[0-9a-fA-F]{4}', '#8B8000'),
    (r'0x[0-9a-fA-F]{2}', '#8B8000'),
    (r'\"(%d|-%d|%s)\"', '#A0D6B4'),
    (r'(byte)', '#A0D6B4'),
    (r'(word)', '#A0D6B4'),
    (r'(str)', '#A0D6B4'),
    (r'"[^"\n]*"', '#C19A6B'),
    (r',', 'white'),
    (r':', 'white'),
    (r'(JMP|jmp|Jmp)', '#F62217'),
    (r'_[a-zA-Z]*', 'yellow'),
    (r'\$[a-zA-Z]', "#C35817"),
    (r'(MOVP|movp|Movp)', "#3090C7"),
    (r'(MOV|mov|Mov)', "#3090C7"),
    (r'(LXI|lxi|Lxi)', "#56A5EC"),
    (r'(LDW|ldw|Ldw)', "#7CFC00"),
    (r'(STW|stw|Stw)', "#7CFC00"),
    (r'(ADD|add|SUB|sub|MUL|mul|DIV|div|MOD|mod|CMP|cmp|ANA|ana|ORA|ora|XRA|xra)', "#C2E5D3"),
    (r'(OUT|out|Out)', "#E9AB17"),
    (r'(<|>)', "#E799A3"),
    (r'(\(|\))', "yellow"),
    (r'(\[|\])', "#E799A3"),
    (r'(((B|b|D|d|H|h|W|w)+(C|c|E|e|L|l|Z|z))|pbx|pdx|phx|pwx|eax|EAX|ebx|EBX)', "red"),
    (r'(A|a|B|b|C|c|D|d|E|e|H|h|L|l|Z|z)', "#FF6700"),
    (r'//.*', "#5EFB6E"),
    (r'[a-zA-Z0-9]+\:', "yellow")
}
def open_file():
    filename = askopenfilename(filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
    if filename:
        try:
            with open(filename, "r") as file:
                text.delete("1.0", tk.END)
                text.insert(tk.END, file.read())
                update_line_numbers()
                highlight_reserved_words()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def save_file():
    filename = asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
    if filename:
        try:
            with open(filename, "w") as file:
                file.write(text.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

def compile_code():
    # Aqui você pode adicionar a ação de compilação do código
    update_info_area("Compilação concluída.")
    update_hex_area("Código compilado em hexadecimal.")

def update_info_area(text):
    info_area.config(state=tk.NORMAL)
    info_area.delete("1.0", tk.END)
    info_area.insert(tk.END, text)
    info_area.config(state=tk.DISABLED)

def update_hex_area(text):
    hex_area.config(state=tk.NORMAL)
    hex_area.delete("1.0", tk.END)
    hex_area.insert(tk.END, text)
    hex_area.config(state=tk.DISABLED)

def copy_hex():
    hex_text = hex_area.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(hex_text)

root = tk.Tk()
root.title("Editor de Texto")

# Frame principal
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Números das linhas
line_numbers = tk.Text(frame, width=4, fg="gray50", background="#1f1f1f", font=("Consolas", 14, "normal"), state=tk.DISABLED)
line_numbers.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

# Texto principal
text = tk.Text(frame, wrap=tk.NONE, fg="white", background="#1f1f1f", insertbackground="white", font=("Consolas", 14, "normal"))
text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar do texto principal
text_scrollbar = tk.Scrollbar(frame)
text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text.config(yscrollcommand=text_scrollbar.set)
text_scrollbar.config(command=text.yview)


# Atualizar números das linhas
def update_line_numbers(*args):
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete("1.0", tk.END)
    line_count = text.get("1.0", tk.END).count("\n")
    for i in range(1, line_count + 1):
        line_numbers.insert(tk.END, str(i) + "\n")
    line_numbers.config(state=tk.DISABLED)

    # Obter o valor de deslocamento da barra de rolagem vertical
    y_offset = text.yview()[0]

    # Ajustar o deslocamento da área de números de linha
    line_numbers.yview_moveto(y_offset)

text_scrollbar.config(command=lambda *args: (text.yview(*args), update_line_numbers()))

# Menu "Arquivo"
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Abrir", command=open_file)
file_menu.add_command(label="Salvar", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=root.quit)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)

# Menu "Compilar"
comp_menu = tk.Menu(menu_bar, tearoff=0)
comp_menu.add_command(label="Compilar", command=compile_code)
menu_bar.add_cascade(label="Compilar", menu=comp_menu)

root.config(menu=menu_bar)

# Info Area
info_frame = tk.Frame(root, bg="gray25")
info_frame.pack(side=tk.BOTTOM, fill=tk.X)

info_label = tk.Label(info_frame, text="Informações:", fg="white", bg="gray25")
info_label.pack(side=tk.LEFT, padx=5, pady=2)

info_area = tk.Text(info_frame, height=1, fg="white", bg="gray25", state=tk.DISABLED)
info_area.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

# Hex Area
hex_frame = tk.Frame(root, bg="gray25")
hex_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

hex_label = tk.Label(hex_frame, text="Código Hexadecimal:", fg="white", bg="gray25")
hex_label.pack(side=tk.TOP, padx=5, pady=2)

hex_scrollbar = tk.Scrollbar(hex_frame)
hex_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

hex_area = tk.Text(hex_frame, fg="white", bg="gray25", state=tk.DISABLED)
hex_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

hex_area.config(yscrollcommand=hex_scrollbar.set)
hex_scrollbar.config(command=hex_area.yview)

def find_regex_patterns(text):
    # Lista para armazenar as correspondências encontradas
    matches = []
    # Itera sobre os padrões de regex
    for pattern, pattern_color in reserved_words:
        # Compila o padrão de regex
        regex = re.compile(pattern)
        # Encontra todas as correspondências no texto
        pattern_matches = regex.findall(text)
        # Adiciona as correspondências encontradas à lista principal
        matches.extend([(match, pattern_color) for match in pattern_matches])
    return matches

# Realce de palavras reservadas
def highlight_reserved_words(event=None):
    text.tag_remove("reserved", "1.0", tk.END)
    content = text.get("1.0", "end-1c")
    # Lista para armazenar as correspondências encontradas
    words = find_regex_patterns(content)
    
    for word, color in words:
        start = "1.0"
        while True:
            start = text.search(word, start, stopindex=tk.END)
            if not start:
                break
            end = f"{start}+{len(word)}c"
            text.tag_add(word, start, end)
            start = end
            text.tag_config(word, foreground=color)

#text.bind('<Return>', highlight_reserved_words)
#text.bind('<space>', highlight_reserved_words)
text.bind('<Key>', highlight_reserved_words)
text.bind("<<Modified>>", update_line_numbers)
text.bind("<Configure>", update_line_numbers)
text.bind("<KeyRelease>", update_line_numbers)
update_line_numbers()

root.mainloop()
