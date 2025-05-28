# 🧩 Puzzle 8 - Agentes Inteligentes con Búsqueda Informada y No Informada

Este proyecto implementa una solución autónoma al clásico Puzzle 8 utilizando dos tipos de agentes inteligentes desarrollados en Python:

Agente No Informado: Búsqueda en Anchura (BFS)  
Agente Informado: Búsqueda A* con heurística de distancia Manhattan

Cuenta con una interfaz gráfica interactiva desarrollada con Pygame, que permite visualizar en tiempo real el comportamiento y rendimiento de ambos agentes.

---

## 🚀 Requisitos del Entorno

Antes de ejecutar el proyecto, asegúrate de contar con el siguiente entorno de desarrollo:

Python: versión 3.8 o superior (recomendado Python 3.10 para mejor compatibilidad)  
Pip: gestor de paquetes para instalar dependencias  
Sistema operativo: Windows, Linux o macOS  
Bibliotecas necesarias: pygame para la visualización e interacción gráfica

---

## 📦 Instalación de dependencias

Desde la terminal o consola, ejecuta el siguiente comando:

pip install pygame

Nota: Si trabajas en un entorno virtual (recomendado), actívalo antes de instalar las dependencias.

---

## 📁 Estructura del Proyecto

main.py                 Punto de entrada del programa  
interfaz.py             Interfaz gráfica e interacción con el usuario  
agente_informado.py     Implementación del agente A* (búsqueda informada)  
agente_no_informado.py  Implementación del agente BFS (búsqueda no informada)  
modelo.py               Lógica del tablero, validación y generación de estados

---

## ▶️ ¿Cómo ejecutar?

Clona este repositorio o descarga los archivos.

Instala las dependencias necesarias.

Ejecuta el archivo principal desde la terminal con:

python main.py

---

## 🎮 ¿Cómo jugar?

Al iniciar, selecciona el tipo de agente que deseas utilizar.

Se generará un tablero inicial aleatorio (solo si es resoluble).

El agente resolverá el puzzle automáticamente paso a paso.

Visualizarás:

Tiempo de ejecución  
Número de movimientos  
Nodos expandidos

Al finalizar, podrás volver al menú y probar otro agente o tablero.

---

## 🎯 Estado Objetivo

El objetivo del puzzle está definido como:

[1, 2, 3,  
 8, 0, 4,  
 7, 6, 5]

El sistema detecta automáticamente si un tablero es irresoluble y lo informa en pantalla.

---

## 👨‍💻 Autor

Richard Suárez  
Proyecto académico para la materia de Inteligencia Artificial  
Ingeniería en Informática – Universidad Nacional Experimental de Guayana
