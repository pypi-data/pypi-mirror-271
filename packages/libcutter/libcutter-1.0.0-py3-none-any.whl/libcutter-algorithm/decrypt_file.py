from bitarray import bitarray
from PIL import Image


def load_image(filename: str):
    ''' Загружает изображение в массив пикселей
    '''
    im = Image.open(filename)
    width, height = im.size
    pixel_array = im.load()
    return pixel_array, width, height, im


def extract_msg_from_image(pixel_array_tuple):
    ''' Выделяет биты исходного сообщения
    '''
    pixel_array, width, height, im = pixel_array_tuple
    binary_message = ''

    for y in range(height):
        for x in range(width):
            r, _, _ = im.getpixel((x, y))
            binary_message += str(r & 1)

            if binary_message[-16:] == '1111111111111110':
                break
        else:
            continue
        break

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))
        if byte == '11111111':
            break

    return message


def feistel_decipher(block, key, n):
    ''' Применение функции расшифрования блока сообщения
    '''
    L = block[:4]
    R = block[4:]

    for _ in range(n):
        new_L = bytes([R[j] ^ key[j] for j in range(4)])
        L, R = new_L, L

    return R + L


def decrypt_file(filename_in, filename_out, key, n):
    ''' Расшифровать файл с помощью переданного ключа и количества раундов
    '''
    with open(filename_in, 'rb') as f:
        data = f.read()

    decrypted_data = b''
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        decrypted_block = feistel_decipher(block, key, n)
        decrypted_data += decrypted_block

    with open(filename_out, 'wb') as f:
        f.write(decrypted_data)
