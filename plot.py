import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import numpy as np

# Leer los datos del archivo CSV
data = pd.read_csv('results.csv', header=None, names=['Cost', 'Duration', 'Acceptance Ratio'])

# Crear una cuadrícula 2D de los datos de Cost y Duration
x = np.linspace(data['Cost'].min(), data['Cost'].max(), len(data['Cost'].unique()))
y = np.linspace(data['Duration'].min(), data['Duration'].max(), len(data['Duration'].unique()))
x, y = np.meshgrid(x, y)

# Interpolar los datos de Acceptance Ratio en la cuadrícula 2D
z = griddata((data['Cost'], data['Duration']), data['Acceptance Ratio'], (x, y), method='cubic')

# Crear una figura
fig = plt.figure()

# Crear un gráfico 3D
ax = fig.add_subplot(111, projection='3d')

# Añadir los datos al gráfico
ax.plot_surface(x, y, z)

# Añadir etiquetas a los ejes y un título
ax.set_xlabel('Cost')
ax.set_ylabel('Duration')
ax.set_zlabel('Acceptance Ratio')

# Mostrar el gráfico
plt.show()