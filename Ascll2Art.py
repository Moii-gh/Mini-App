from PIL import Image

def image_to_ascii(image_path, width=50):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width)
    img = img.resize((width, new_height))
    img = img.convert("L")
    pixels = list(img.getdata())
    chars = "@%#+=:."
    ascii_str = ''.join([chars[pixel * len(chars) // 256] for pixel in pixels])
    ascii_str_len = len(ascii_str)
    img_ascii = "\n".join([ascii_str[index:index + width] for index in range(0, ascii_str_len, width)])
    print(img_ascii)

image_to_ascii("image.png")
