import testply as compilador

data = '''
ldw bc, [$a]
'''

compilador.compile_data(data)