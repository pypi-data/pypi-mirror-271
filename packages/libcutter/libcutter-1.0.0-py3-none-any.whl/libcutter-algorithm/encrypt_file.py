from PIL import Image
from uuid import uuid4

_8_bit_mask = 0b11111111
_24_bit_mask = 0b111111111111111111111111


def load_image(filename: str):
    ''' Загружает изображение в массив пикселей
    '''
    im = Image.open(filename)
    width, height = im.size
    pixel_array = im.load()
    return pixel_array, width, height, im


def str_to_bytes(msg):
    return ''.join(format(ord(char), '08b') for char in msg) + '1111111111111110'


def insert_msg(pixel_array_tuple, msg):
    ''' Вставляет переданное сообщение в изображение
    '''
    pixel_array, width, height, im = pixel_array_tuple
    msg_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixel_array[x, y]

            if msg_index < len(msg):
                im.putpixel((x, y), (r & 0xFE | int(msg[msg_index]), g, b))
                msg_index += 1

    im.save('encrypted.png')


def gen_key():
    ''' Генерация ключа для шифрования с помощью сети Фейстеля
    '''
    u = uuid4()
    return (
            ((u.node & _24_bit_mask) << 40)
            + ((u.clock_seq_hi_variant & _8_bit_mask) << 32)
            + ((u.clock_seq_low & _8_bit_mask) << 24)
            + ((u.time_hi_version & _8_bit_mask) << 16)
            + ((u.time_mid & _8_bit_mask) << 8)
            + u.time_low
    )


def feistel_cipher(block, key, n):
    ''' Применение функции шифрования блока сообщения
    '''
    L = block[:4]
    R = block[4:]

    for _ in range(n):
        new_R = bytes([L[j] ^ key[j] for j in range(4)])
        L, R = R, new_R

    return R + L


def encrypt_image(filename_in, filename_out, key, n):
    ''' Шифрование изображения с помощью сети Фейстеля
    '''
    with open(filename_in, 'rb') as f:
        data = f.read()

    encrypted_data = b''
    for i in range(0, len(data), 8):
        block = data[i:i + 8]
        if len(block) < 8:
            block += b'\0' * (8 - len(block))
        encrypted_block = feistel_cipher(block, key, n)
        encrypted_data += encrypted_block

    with open(filename_out, 'wb') as f:
        f.write(encrypted_data)
