import argparse
import imageio.v2 as imageio
import os

parser = argparse.ArgumentParser(description='Create a video from PNG images.')
parser.add_argument('--folder', type=str, help='The folder containing the PNG images.')

# Analizar los argumentos de la línea de comando
args = parser.parse_args()


# Crear una lista para almacenar las imágenes
images = []

# Cargar las imágenes
for i in range(10):
    filename = os.path.join(args.folder, f'iteration_{i}.png')
    images.append(imageio.imread(filename))

# Crear el video
imageio.mimsave('Assignment_4/video.mp4', images, fps=1)