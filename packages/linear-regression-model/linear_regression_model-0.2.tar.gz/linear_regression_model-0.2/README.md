## **Modelo de Regresión Lineal Simple**

<img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/jupyter-%23000000.svg?style=for-the-badge&logo=jupyter&logoColor=white">
<img src="https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white">
<a href="https://medium.com/@sebasurdanegui">
    <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white">
</a>

### **Descripción**
Proyecto de prueba para explicar cuáles son los pasos que se deben seguir para la creación de una librería en Python usando como herramienta PYPI para almacenar los metadatos y distribuirlos.

### **Pasos a seguir**
Link para leer el artículo en Medium: <a href="https://medium.com/@sebasurdanegui/desarrolla-tu-conjunto-de-herramientas-creaci%C3%B3n-de-biblioteca-en-python-05d717da147f">¿Cómo crear una librería en Python?</a>

### **Instalación**
Puedes instalar la librería 'linear_regression_model' usando pip.
```Power Shell
pip install linear_regression_model
```

### **Uso**
A continuación, se muestra un ejemplo de cómo utilizar la librería:
```python
from linear_regression_model import linear_regression
from linear_regression_model import linear_regression_plot
```
```python
# Importar datos de prueba
import pandas as pd
from sklearn.datasets import load_diabetes
data_x, data_y = load_diabetes(return_X_y=True)

data_x = pd.DataFrame(data_x)
data_y = pd.DataFrame(data_y).rename(columns = {0:'Target'})
data = pd.concat([data_x, data_y], axis = 1)

# Aplicar la primera función
data_regression = linear_regression(data = data, X = 1, y = 'Target')
data_regression

# Aplicar la segunda función
linear_regression_plot(data_predictions = data_regression, X = 1, y = 'Target')
```

### **Licencia**
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE.md para más detalles.

---