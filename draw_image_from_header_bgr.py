import numpy as np
from PIL import Image

# Funkcja do konwersji RGB565 na RGB
def rgb565_to_rgb(swapped_rgb565):
    rgb565 = ((swapped_rgb565 & 0xFF) << 8) | ((swapped_rgb565 >> 8) & 0xFF)
    r = (rgb565 >> 11) & 0x1F     # 5 bitów czerwonego
    g = (rgb565 >> 5) & 0x3F      # 6 bitów zielonego
    b = rgb565 & 0x1F             # 5 bitów niebieskiego

    # Skala wartości RGB do zakresu 0-255
    r = int((r << 3) | (r >> 2))  # 5-bitowy do 8-bitowego
    g = int((g << 2) | (g >> 4))  # 6-bitowy do 8-bitowego
    b = int((b << 3) | (b >> 2))  # 5-bitowy do 8-bitowego

    return (r, g, b)

# Funkcja do odczytu i rysowania obrazu
def draw_image_from_header(file_path, width):
    # Odczytanie pliku "obraz.h", zawierającego tablicę
    with open(file_path, 'r') as file:
        # Szukamy tablicy 'obraz[]' w pliku i pobieramy jej wartości
        data = file.read()
        start_index = data.find('const uint16_t obraz[] = {') + len('const uint16_t obraz[] = {')
        end_index = data.find('};', start_index)
        
        # Wyciągamy część z danymi i dzielimy na liczby
        raw_data = data[start_index:end_index].strip()
        obraz = list(map(lambda x: int(x, 16), raw_data.split(',')))
    
    # Obliczamy wysokość obrazu na podstawie długości tablicy
    height = len(obraz) // width

    # Tworzymy obraz na podstawie tablicy RGB565
    image_data = []
    for pixel in obraz:
        image_data.append(rgb565_to_rgb(pixel))
    
    # Tworzymy obraz przy użyciu Pillow
    image = Image.new("RGB", (width, height))
    image.putdata(image_data)

    # Wyświetlamy obraz
    image.show()

# Przykładowe wywołanie funkcji
draw_image_from_header('obraz.h', 240)
