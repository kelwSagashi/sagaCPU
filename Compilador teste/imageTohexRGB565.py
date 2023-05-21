from PIL import Image
#this algorithm generates hexadecimal rgb values in rgb565 format, 
# where it is possible to copy the hex codes and paste them in logisim 
# to print an image in the "video rgb" component

def converter_medida(valor):
    valor_convertido = (valor * 31) // 255
    return valor_convertido

def converter_rgb_para_565(r, g, b):
    binaryR = format(converter_medida(r), '05b')
    binaryG = format(converter_medida(g), '06b')
    binaryB = format(converter_medida(b), '05b')
    binaries = [binaryR, binaryG, binaryB]
    bit16 = ''.join(binaries)
    valor_hexadecimal = hex(int(bit16, 2))
    valor_hexadecimal = valor_hexadecimal[2:]
    return valor_hexadecimal.zfill(4)

caminho_imagem = "file path/image.jpg"

imagem = Image.open(caminho_imagem)

imagem_rgb = imagem.convert("RGB")

pixels = list(imagem_rgb.getdata())

i = 0
valor_hexadecimal = []

arquivo = open("file path/image.jpg", "w")
i = 0
for pixel in pixels:
    r, g, b = pixel
    v = converter_rgb_para_565(r, g, b)
    valor_hexadecimal.append(v)
    arquivo.write(str(v))
    arquivo.write(" ")
    i += 1
    if i == 8:
        arquivo.write("\n")
        i = 0

arquivo.close()