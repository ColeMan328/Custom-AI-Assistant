from PIL import Image

def convert_png_to_ico(png_path, ico_path, icon_sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]):
    img = Image.open(png_path)

    # Convert the image to an ICO file with specified sizes
    img.save(ico_path, format='ICO', sizes=icon_sizes)

# Example usage
convert_png_to_ico('static/icon.png', 'static/icon.ico')