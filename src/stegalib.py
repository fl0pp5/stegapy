import sys

from PIL import Image


def get_text_mask(key: int) -> int:
    return (255 << 8 - key) % 256


def get_image_mask(key: int) -> int:
    return 255 >> key << key


def hide(in_filename: str, out_filename: str, text_filename: str, key: int) -> None:
    with open(text_filename, 'r') as text_file:
        out_image = Image.open(in_filename)

        image_pixels = out_image.load()
        coord_x, coord_y = 0, 0

        text_hide_mask = get_text_mask(key)
        image_hide_mask = get_image_mask(key)

        while True:
            if (symbol := text_file.read(1)) is not None and len(symbol) != 0:
                r, g, b, a = image_pixels[coord_x, coord_y]
                symbol = ord(symbol)

                for i in range(0, 8, key):
                    bits = (symbol & text_hide_mask) >> (8 - key)
                    b = b & image_hide_mask | bits
                    symbol <<= key

                    image_pixels[coord_x, coord_y] = r, g, b, a

                    if coord_x + 1 == out_image.width:
                        coord_x, coord_y = -1, coord_y + 1
                    coord_x += 1
            else:
                break

        out_image.save(out_filename)


def unhide(in_filename: str, out_filename: str, key: str, length: str) -> None:
    with open(out_filename, 'w') as text_file:
        in_image = Image.open(in_filename)
        image_pixels = in_image.load()

        image_unhide_mask = ~get_image_mask(key)
        coord_x, coord_y = 0, 0

        for _ in range(length):
            symbol = 0
            for _ in range(0, 8, key):
                _, _, b, _ = image_pixels[coord_x, coord_y]
                symbol = symbol << key | b & image_unhide_mask

                if coord_x + 1 == in_image.width:
                    coord_x, coord_y = -1, coord_y + 1
                coord_x += 1

            text_file.write(chr(symbol))

    