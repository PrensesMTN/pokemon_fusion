from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image
import os


def load_sprites(folder):
    sprites = {}
    for filename in os.listdir(folder):
        if filename.endswith(".png"):
            pokemon_name = filename.split('.')[0]
            sprites[pokemon_name] = Image.open(os.path.join(folder, filename))
    return sprites


def blend_pixels_randomly(pixel1, pixel2, blend_ratio=0.5):
    blended_pixel = tuple(
        int(p1 * blend_ratio + p2 * (1 - blend_ratio))
        for p1, p2 in zip(pixel1, pixel2)
    )
    return blended_pixel


def fuse_pokemon(pokemon1, pokemon2, sprites):
    sprite1 = sprites[pokemon1].resize((96, 96)).convert("RGBA")
    sprite2 = sprites[pokemon2].resize((96, 96)).convert("RGBA")

    fused_image = Image.new('RGBA', (96, 96))

    for x in range(96):
        for y in range(96):
            pixel1 = sprite1.getpixel((x, y))
            pixel2 = sprite2.getpixel((x, y))

            if pixel1[3] == 0:  
                fused_image.putpixel((x, y), pixel2)
            elif pixel2[3] == 0:  
                fused_image.putpixel((x, y), pixel1)
            else:
                blended_pixel = blend_pixels_randomly(pixel1, pixel2)
                fused_image.putpixel((x, y), blended_pixel)

    return fused_image


def create_fusion_name(pokemon1, pokemon2):
    split1 = len(pokemon1) // 2
    split2 = len(pokemon2) // 2
    new_name = pokemon1[:split1] + pokemon2[split2:]
    return new_name.capitalize()


class PokemonFusionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokémon Fusion")
        self.sprites = load_sprites('pokemon_resimler')

        # Layout
        layout = QVBoxLayout()

        # Input fields
        self.pokemon1_input = QLineEdit(self)
        self.pokemon1_input.setPlaceholderText("Enter first Pokémon name")
        self.pokemon2_input = QLineEdit(self)
        self.pokemon2_input.setPlaceholderText("Enter second Pokémon name")
        layout.addWidget(self.pokemon1_input)
        layout.addWidget(self.pokemon2_input)

        # Buttons
        self.fuse_button = QPushButton("Fuse Pokémon")
        self.fuse_button.clicked.connect(self.fuse_pokemon)
        layout.addWidget(self.fuse_button)

        # Result
        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        # Set layout
        self.setLayout(layout)

    def fuse_pokemon(self):
        pokemon1 = self.pokemon1_input.text().strip()
        pokemon2 = self.pokemon2_input.text().strip()

        if pokemon1 in self.sprites and pokemon2 in self.sprites:
            fused_image = fuse_pokemon(pokemon1, pokemon2, self.sprites)

            # Save fused image temporarily
            save_path = 'fused_pokemon.png'
            fused_image.save(save_path)

            # Display fused image
            pixmap = QPixmap(save_path)
            self.result_label.setPixmap(pixmap)

            # Display fusion name
            fusion_name = create_fusion_name(pokemon1, pokemon2)
            self.setWindowTitle(f"Fusion Result: {fusion_name}")
        else:
            self.result_label.setText("Invalid Pokémon names!")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = PokemonFusionApp()
    window.show()
    sys.exit(app.exec_())
