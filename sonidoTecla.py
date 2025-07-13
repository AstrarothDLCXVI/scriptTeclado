import pygame
from pynput import keyboard
import os
import random

pygame.init()
pygame.mixer.init()


SOUND_FOLDER = "sounds"  # Carpeta donde están los archivos de sonido
VOLUME = 0.5  # Volumen (0.0 a 1.0)

# Diccionario para almacenar los sonidos cargados
sounds = {}

def load_sounds():
    """Carga todos los archivos de sonido de la carpeta especificada"""
    if not os.path.exists(SOUND_FOLDER):
        print(f"Creando carpeta '{SOUND_FOLDER}'...")
        os.makedirs(SOUND_FOLDER)
        print(f"Por favor, coloca archivos de sonido (.wav, .mp3, .ogg) en la carpeta '{SOUND_FOLDER}'")
        return False
    
    sound_files = [f for f in os.listdir(SOUND_FOLDER) 
                   if f.endswith(('.wav', '.mp3', '.ogg'))]
    
    if not sound_files:
        print(f"No se encontraron archivos de sonido en la carpeta '{SOUND_FOLDER}'")
        print("Por favor, agrega archivos .wav, .mp3 o .ogg")
        return False
    
    print(f"Cargando {len(sound_files)} archivos de sonido...")
    for file in sound_files:
        try:
            sound_path = os.path.join(SOUND_FOLDER, file)
            sounds[file] = pygame.mixer.Sound(sound_path)
            sounds[file].set_volume(VOLUME)
            print(f"✓ Cargado: {file}")
        except Exception as e:
            print(f"✗ Error al cargar {file}: {e}")
    
    return len(sounds) > 0

def play_random_sound():
    """Reproduce un sonido aleatorio de los cargados"""
    if sounds:
        sound = random.choice(list(sounds.values()))
        sound.play()

def play_specific_sound(key):
    """Reproduce un sonido específico basado en la tecla presionada"""
    # Puedes personalizar qué sonido se reproduce para cada tecla
    # Por ejemplo:
    key_sound_map = {
        'a': 'click1.wav',
        's': 'click2.wav',
        'd': 'click3.wav',
        # Agrega más mapeos según tus archivos de sonido
    }
    
    key_char = None
    try:
        key_char = key.char
    except AttributeError:
        # Teclas especiales (espacio, enter, etc.)
        key_char = str(key).replace('Key.', '')
    
    if key_char in key_sound_map and key_sound_map[key_char] in sounds:
        sounds[key_sound_map[key_char]].play()
    else:
        # Si no hay un sonido específico para la tecla, reproduce uno aleatorio
        play_random_sound()

def on_press(key):
    """Función que se ejecuta cuando se presiona una tecla"""
    try:
        # Opción 1: Reproducir un sonido aleatorio para cada tecla
        play_random_sound()
        
        # Opción 2: Reproducir sonidos específicos por tecla (descomenta para usar)
        # play_specific_sound(key)
        
    except Exception as e:
        print(f"Error al reproducir sonido: {e}")

def on_release(key):
    """Función que se ejecuta cuando se suelta una tecla"""
    # Salir con ESC
    if key == keyboard.Key.esc:
        print("\nSaliendo del programa...")
        return False

def main():
    """Función principal del programa"""
    print("=== Reproductor de Sonidos por Teclado ===")
    print("Presiona cualquier tecla para reproducir un sonido")
    print("Presiona ESC para salir\n")
    
    # Cargar sonidos
    if not load_sounds():
        print("\nNo se pudieron cargar sonidos. Saliendo...")
        return
    
    print(f"\n✓ {len(sounds)} sonidos cargados correctamente")
    print("Comenzando a escuchar el teclado...\n")
    
    # Crear el listener del teclado
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:
        listener.join()
    
    print("Programa terminado.")

if __name__ == "__main__":
    # Verificar instalación de dependencias
    try:
        import pygame
        from pynput import keyboard
    except ImportError:
        print("Por favor instala las dependencias necesarias:")
        print("pip install pygame pynput")
        exit(1)
    
    main()