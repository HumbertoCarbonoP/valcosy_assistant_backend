import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras._tf_keras.keras.models import Sequential, load_model
from keras._tf_keras.keras.layers import Dense

data = {
    'num_personas': [2, 4, 2, 1, 5, 5, 1, 2, 2, 2, 2, 5, 5, 5, 5, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 5, 5, 5, 5, 3, 3, 3, 1, 1, 1, 1, 2, 2, 4, 4, 4, 2, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 2, 3, 1, 1, 5, 5, 1, 1, 1, 2, 4, 2, 7, 7, 2, 5, 4, 5, 6, 2, 2, 6, 1, 3, 2, 1, 5, 5, 5, 3, 3, 3, 1, 1, 1, 1, 2, 2, 4, 4, 4, 2, 2, 2, 2, 1, 1, 1, 1, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 6, 6, 3, 3, 3, 3, 3, 3, 4, 4, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 2, 3, 4, 4, 4, 2, 1, 1, 1, 2, 2, 4, 4, 6, 1, 1, 6, 5, 4, 4, 7, 2, 5, 4, 5, 6, 2, 1, 2, 5, 4, 4, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 4, 3, 1, 1, 5, 5, 1, 1, 1, 2, 4, 2],
    'presupuesto': [220, 880, 120, 60, 3850, 2100, 120, 440, 300, 500, 240, 600, 1100, 2000, 1000, 330, 340, 320, 180, 200, 720, 1320, 1200, 2000, 1000, 2750, 1500, 1700, 3000, 1300, 2400, 2000, 80, 120, 200, 400, 400, 700, 300, 500, 250, 900, 1600, 600, 1200, 350, 600, 550, 400, 600, 1000, 990, 800, 800, 991, 240, 890, 123, 599, 3840, 2100, 900, 800, 700, 500, 660, 600, 1100, 2000, 1000, 900, 540, 670, 1000, 300, 720, 1320, 1200, 2000, 1000, 2750, 1500, 1700, 3000, 1300, 2400, 2000, 80, 120, 200, 400, 400, 700, 300, 500, 250, 900, 1600, 600, 1200, 350, 600, 550, 400, 600, 1000, 990, 800, 800, 800, 990, 800, 850, 810, 750, 600, 990, 800, 850, 810, 750, 800, 1920, 2120, 1999, 1950, 1980, 1970, 1920, 2120, 1999, 1950, 1980, 1970, 400, 270, 940, 1620, 605, 1220, 340, 590, 690, 593, 300, 700, 500, 660, 660, 630, 887, 121, 73, 213, 340, 390, 600, 400, 700, 880, 240, 60, 3050, 2100, 530, 700, 1987, 500, 906, 580, 680, 770, 250, 170, 360, 960, 1700, 1500, 930, 1480, 630, 1240, 1530, 1460, 970, 1370, 620, 1320, 70, 110, 190, 380, 360, 600, 400, 880, 142, 579, 3710, 2200, 860, 740, 730, 450, 640, 690],
    'dias_hospedaje': [1, 2, 1, 1, 7, 7, 1, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7, 7, 1, 1, 3, 3, 3, 3, 1, 1, 1, 7, 7, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 2, 3, 1, 2, 7, 7, 10, 10, 10, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5, 5, 5, 7, 7, 7, 1, 1, 3, 3, 3, 3, 1, 1, 1, 7, 7, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 1, 1, 7, 7, 5, 5, 5, 5, 5, 5, 5, 4, 3, 2, 2, 2, 2, 1, 1, 3, 3, 3, 3, 1, 1, 2, 4, 1, 8, 6, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 5, 6, 6, 3, 5, 3, 5, 6, 6, 3, 5, 3, 1, 1, 3, 3, 3, 3, 1, 3, 1, 2, 7, 7, 10, 10, 10, 2, 2, 2],
    'tipo_habitacion': ['suite', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'suite', 'suite', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'suite', 'suite', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'suite', 'estandar', 'estandar', 'estandar', 'estandar', 'estandar', 'suite', 'estandar', 'suite']
}

df = pd.DataFrame(data)

# Codificar la variable categórica 'tipo_habitacion'
df['tipo_habitacion'] = pd.Categorical(df['tipo_habitacion'])
df['tipo_habitacion'] = df['tipo_habitacion'].cat.codes

# Verificación rápida de los datos
print(df.head())
print(df.describe())

X = df[['num_personas', 'presupuesto', 'dias_hospedaje']]
y = df['tipo_habitacion']

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construir y entrenar el modelo solo si no está guardado
import os

if not os.path.exists('modelo_habitacion.h5'):
    model = Sequential([
        Dense(10, activation='relu', input_shape=(3,)),  # 3 características de entrada
        Dense(10, activation='relu'),
        Dense(1, activation='sigmoid')  # Clasificación binaria
    ])

    model.compile(optimizer='adam',
                    loss='binary_crossentropy',
                    metrics=['accuracy'])

    model.fit(X_train, y_train, epochs=70, batch_size=1)
    model.save('modelo_habitacion.h5')  # Guardar el modelo después del entrenamiento
else:
    model = load_model('modelo_habitacion.h5')  # Cargar el modelo guardado

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Loss: {loss}, Accuracy: {accuracy}')

def recomendar_habitacion(num_personas, presupuesto, dias_hospedaje):
    entrada = np.array([[num_personas, presupuesto, dias_hospedaje]])
    prediccion = model.predict(entrada)
    print('Predicción:', prediccion)
    tipo_habitacion = 'suite' if prediccion >= 0.5 else 'estandar'
    return tipo_habitacion
