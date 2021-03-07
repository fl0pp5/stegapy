from PIL import Image


def get_image_copy(filename: str) -> Image.Image:
    return Image.open(filename).copy()


def get_text_mask(key: int) -> int:
    return (255 << 8 - key) % 256


def get_image_mask(key: int) -> int:
    return 255 >> key << key


def hide(in_filename: str, out_filename: str, text_filename: str, key: int) -> None:
    out_image = get_image_copy(in_filename)
    text_file = open(text_filename, 'r')

    image_pixels = out_image.load()
    coord_x, coord_y = 0, 0

    while True:
        if (symbol := text_file.read(1)) is not None and len(symbol) != 0:
            r, g, b, a = image_pixels[coord_x, coord_y]
            symbol = ord(symbol)

            for bits_size in range(0, 8, key):
                bits = (symbol & get_text_mask(key)) >> (8 - key)
                b = b & get_image_mask(key) | bits
                symbol <<= key

                image_pixels[coord_x, coord_y] = r, g, b, a

                if coord_x + 1 == out_image.width:
                    coord_x, coord_y = -1, coord_y + 1
                coord_x += 1
        else:
            break

    out_image.save(out_filename)
    text_file.close()
