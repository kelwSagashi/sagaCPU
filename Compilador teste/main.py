import testply as compilador

data = '''
_data:
    $x <word>: 0x1234
    out("%d", $x)
    load [$x], eax
    store [$x], b
'''

compilador.compile_data(data)