import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from typing import Union
import warnings
warnings.filterwarnings('ignore')

# 1° Función

# Objetivo: Generar una regresión linear recibiendo como argumentos
# data: DataFrame
# X: Nombre de la columna - variable independiente
# y: Nombre de la columna - variable dependiente


def linear_regression(data: pd.DataFrame, X: str, y: str) -> Union[pd.DataFrame, None]:
    try:
        data = data[[X, y]]
        X = data[X].values
        X = X.reshape(-1, 1)
        y = data[y].values
        lr = LinearRegression()
        lr.fit(X, y)
        predictions = lr.predict(X)
        predictions = pd.DataFrame(predictions, columns=["Predictions"])
        results = pd.concat([data, predictions], axis=1)
        return results
    except ValueError as ve:
        print(f'ValueError: {ve}')
    except KeyError as ke:
        print(f'KeyError: {ke}')
    except Exception as e:
        print(f'Exception: {e}')

# 2° Función


# Objetivo: Generar una regresión linear recibiendo como argumentos
# data: DataFrame
# X: Nombre de la columna - variable independiente
# y: Nombre de la columna - variable dependiente

def linear_regression_plot(data_predictions: pd.DataFrame, X: str, y: str) -> None:
    try:
        fig, ax = plt.subplots(figsize=(4, 2))
        plt.title("")
        plt.scatter(data_predictions[X], data_predictions[y])
        plt.plot(data_predictions[X].values,
                 data_predictions["Predictions"].values, color='red')
        plt.xlabel(X)
        plt.ylabel(y)
        plt.show()
    except KeyError as ke:
        print(f'KeyError: {ke}.')
    except TypeError as te:
        print(f'TypeError: {te}')
    except ValueError as ve:
        print(f'ValueError: {ve}')
    except Exception as e:
        print(f'Ocurrió un error no esperado: {e}')
