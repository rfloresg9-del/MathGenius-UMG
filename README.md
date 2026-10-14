# MathGenius UMG — Asistente Virtual de Cálculo y Precálculo

## Publicar gratis para el docente
1. Crea una cuenta gratuita en GitHub y un repositorio público nuevo, por ejemplo `mathgenius-umg`.
2. Sube `app.py` y `requirements.txt` a la raíz del repositorio.
3. En https://share.streamlit.io/ inicia sesión y selecciona **Create app / Deploy a public app from GitHub**.
4. Selecciona el repositorio, rama `main` y archivo principal `app.py`; pulsa **Deploy**.
5. Abre el enlace `https://...streamlit.app` que te entregue Streamlit, prueba todos los módulos en ventana privada y envíalo en Canvas.
6. En la barra lateral de la aplicación, cambia los nombres de los dos integrantes y la sección. Para que queden permanentes en la app, cambia los valores `value=` en `app.py` antes de publicarla.

## Ejecutar en tu computadora
Instala Python 3.10 o posterior. Abre una terminal en la carpeta del proyecto y ejecuta:
```
pip install -r requirements.txt
streamlit run app.py
```

## Prueba del documento
En **Aplicaciones**, usa `x^3-6*x^2+9*x+1`. Obtendrás f'(x)=3x²−12x+9, f''(x)=6x−12, máximo relativo en (1,5) y mínimo relativo en (3,1).

## Informe de entrega (máximo tres páginas)
Incluye: portada breve con los dos nombres, asignatura y sección; herramientas (Python, Streamlit, SymPy, NumPy y Plotly); funciones de los siete módulos; capturas de pantalla de los módulos y del enlace público; pruebas de ecuaciones, límites, derivadas, integrales, gráficas y puntos críticos; limitaciones conocidas. Exporta el informe a PDF o Word.

**Importante:** El archivo entregado es el código fuente y las instrucciones. Para tener el enlace público requerido por el profesor, es necesario realizar el despliegue indicado. No se ha publicado automáticamente.
