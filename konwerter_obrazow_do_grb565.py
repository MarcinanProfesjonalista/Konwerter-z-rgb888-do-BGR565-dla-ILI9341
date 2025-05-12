from PIL import Image

def rgb888_to_bgr565(b, g, r):
 
    r5 = (r * 31) // 255
    g6 = (g * 63) // 255
    b5 = (b * 31) // 255
    return (r5 << 11) | (g6 << 5) | b5

def bitmapa_do_rgb565(plik_wejsciowy, plik_wyjsciowy, szerokosc=240):
    # Wczytaj obraz jako RGBA (dla obsługi przezroczystości)
    image = Image.open(plik_wejsciowy).convert("RGBA")
    width, height = image.size

    if width != szerokosc:
        print(f"⚠️ Uwaga: szerokość bitmapy ({width}px) różni się od oczekiwanej ({szerokosc}px).")

    with open(plik_wyjsciowy, "w") as output_file:
        output_file.write("const uint16_t obraz[] = {\n")

        for y in range(height):
            linia = []
            for x in range(szerokosc):
                if x >= width:
                    r, g, b = 255, 255, 255  # uzupełnienie bielą
                else:
                    r, g, b, a = image.getpixel((x, y))
                    if a < 10:
                        r, g, b = 255, 255, 255  # przezroczyste traktuj jako biały

                bgr565 = rgb888_to_bgr565(r, g, b)
                linia.append(f"0x{bgr565:04X}")

            # Zapisz linijkę z przecinkami, bez przecinka na końcu ostatniego wiersza
            output_file.write("  " + ", ".join(linia))
            if y < height - 1:
                output_file.write(",\n")
            else:
                output_file.write("\n")

        output_file.write("};\n")

    print(f"✅ Zapisano dane rgb565 do pliku '{plik_wyjsciowy}' jako tablicę C (const uint16_t[]).")

# Przykładowe użycie:
if __name__ == "__main__":
    bitmapa_do_rgb565("obraz.png", "obraz.h", szerokosc=240)
