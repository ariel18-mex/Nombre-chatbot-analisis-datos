
import streamlit as st
import spacy
import random

nlp = spacy.load("es_core_news_sm")

# ==========================================
# PALABRAS ESPECIALES
# ==========================================

palabras_especiales = {
    "hola",
    "gracias",
    "adios",
    "adiós",
    "buenos",
    "buenas",
    "hasta",
    "luego",
    "onda"
}


# ==========================================
# INTENCIONES
# ==========================================

intenciones = {
    'agradecimiento': {
    'preguntas': ['gracias','muchas gracias','te agradezco','gracias por ayudarme'],
    'respuestas': ['¡De nada! Me alegra poder ayudarte.','¡Con gusto!','No hay de qué. Puedes hacerme otra pregunta cuando quieras.'],
    'palabras_clave': ['gracias', 'agradecer']
},
    'saludo': {
        'preguntas':['Que onda', 'hola', 'buenos dias', 'buenas tardes', 'buenas noches'],
        'respuestas':['Hola, ¿en qué puedo ayudarte?','Que onda, como estas?'],
        'palabras_clave': ['hola', 'onda', 'buenos', 'buenas']
    },
    'despedida':{
        'preguntas':['Adios', 'Hasta luego', 'Hasta pronto', 'bye', 'sale', 'sales'],
        'respuestas':['Hasta luego, espero haberte ayudado', 'Que tengas un buen día'],
        'palabras_clave': ['adios', 'hasta', 'luego', 'vemos']
    },
    'python': {
        'preguntas':['¿Que es python?', '¿Para que sirve python?', '¿Que se puede hacer con python?'],
        'respuestas':['Python es un lenguaje de programación muy popular, caracterizada por ser de alto nivel y propósito general. Los desarrolladores lo utilizan en una amplia variedad de aplicaciones, desde desarrollo web y científico, hasta en inteligencia artificial y análisis de datos. Python se destaca por su sintaxis clara y legible, lo que facilita la escritura y comprensión del código. Es un lenguaje versátil que se adapta a diferentes necesidades y escenarios fácilmente.'],
        'palabras_clave': ['lenguaje']
    },
        
    'pandas': {
        'preguntas':['¿Que es pandas?', '¿Para que sirve pandas?', '¿Que se puede hacer con pandas?'],
        'respuestas':['Pandas es una biblioteca de Python diseñada para el análisis y manipulación de datos. Ofrece estructuras de datos rápidas y flexibles, como Series y DataFrames, que facilitan el trabajo con datos etiquetados o relacionales. Es ampliamente utilizada en ciencia de datos, estadísticas y análisis de series temporales.'],
        'palabras_clave':['pandas', 'panda']
    },
    'numpy': {
        'preguntas':['¿Que es numpy?', '¿Para que sirve numpy?', '¿Que se puede hacer con numpy?'],
        'respuestas':['NumPy es una biblioteca fundamental para la computación científica en Python. Su nombre proviene de "Numerical Python" y es ampliamente utilizada para trabajar con arreglos N-dimensionales y realizar cálculos matemáticos de manera eficiente. NumPy es la base de muchas otras bibliotecas como pandas y scipy, lo que la convierte en una herramienta esencial para desarrolladores y científicos de datos.'],
        'palabras_clave':['numpy']
    },
    'sql' : {
        'preguntas':['¿Que es sql?', '¿Para que sirve sql?', '¿Que se puede hacer con sql?'],
        'respuestas':['SQL (Structured Query Language) es un lenguaje de programación declarativo diseñado para interactuar con bases de datos relacionales. Permite realizar operaciones como almacenar, recuperar, actualizar y eliminar datos organizados en tablas. Estas tablas están compuestas por filas y columnas que representan atributos y relaciones entre los datos.'],
        'palabras_clave':['sql', 'consulta', 'base de datos']
    },
    'dataframe': {
        'preguntas':['¿Que es un dataframe?', '¿Para que sirve un dataframe?', '¿Que se puede hacer con un dataframe?'],
        'respuestas':['Un DataFrame es una estructura de datos bidimensional utilizada principalmente por la biblioteca pandas. Organiza la información en filas y columnas, de manera similar a una tabla de Excel o una tabla de una base de datos. Permite almacenar, consultar, filtrar, modificar y analizar datos de forma eficiente.'],
        'palabras_clave':['dataframe', 'tabla', 'datos','fila','filas','columnas']
    },
    'series': {
        'preguntas':['¿Que es una serie?', '¿Para que sirve una serie?', '¿Que se puede hacer con una serie?'],
        'respuestas':['Una Series de pandas es una estructura de datos unidimensional que almacena una colección de valores asociados a un índice. Puede considerarse similar a una sola columna de un DataFrame y permite realizar operaciones como filtrado, cálculos estadísticos y transformación de datos.'],
        'palabras_clave':['serie', 'columna', 'datos']
    },
    'limpieza_datos': {
        'preguntas':['¿Que es la limpieza de datos?', '¿Para que sirve la limpieza de datos?', '¿Que se puede hacer para limpiar datos?'],
        'respuestas':['La limpieza de datos es el proceso de identificar y corregir problemas en un conjunto de datos antes de analizarlo. Puede incluir el tratamiento de valores nulos, eliminación de duplicados, corrección de formatos y detección de datos incorrectos. Su objetivo es mejorar la calidad y confiabilidad de la información utilizada en el análisis.'],
        'palabras_clave':['limpieza', 'datos', 'corregir']
    },
    'visualizacion_datos': {
        'preguntas':['¿Que es la visualizacion de datos?', '¿Para que sirve la visualizacion de datos?', '¿Que se puede hacer para visualizar datos?'],
        'respuestas':['La visualización de datos consiste en representar información mediante elementos gráficos como gráficas de barras, líneas, histogramas, mapas o dashboards. Su objetivo es facilitar la interpretación de los datos, identificar patrones y comunicar los resultados de un análisis de manera clara.'],
        'palabras_clave':['visualizacion', 'datos', 'graficas']
    },
    'machine_learning': {
        'preguntas':['¿Que es machine learning?', '¿Para que sirve machine learning?', '¿Que se puede hacer con machine learning?'],
        'respuestas':['Machine Learning o aprendizaje automático es una rama de la inteligencia artificial que permite desarrollar modelos capaces de aprender patrones a partir de datos. Se utiliza para realizar tareas como clasificación, predicción, detección de anomalías, sistemas de recomendación y reconocimiento de patrones.'],
        'palabras_clave':['machine', 'learning', 'modelos']
    },
    'estadistica': {
        'preguntas':['¿Que es estadistica?', '¿Para que sirve estadistica?', '¿Que se puede hacer con estadistica?'],
        'respuestas':['La estadística es una disciplina que permite recopilar, organizar, analizar e interpretar datos. En análisis de datos se utiliza para describir información, identificar relaciones, medir variabilidad, realizar inferencias y apoyar la toma de decisiones basadas en evidencia.'],
        'palabras_clave':['estadistica', 'datos', 'analisis']
    },
    'regresion_lineal': {
        'preguntas':['¿Que es la regresion lineal?', '¿Para que sirve la regresion lineal?', '¿Que se puede hacer con la regresion lineal?'],
        'respuestas':['La regresión lineal es una técnica estadística y de Machine Learning utilizada para estudiar la relación entre una variable dependiente y una o más variables independientes. Puede utilizarse para realizar predicciones de valores numéricos y analizar cómo determinadas variables influyen sobre otra.'],
        'palabras_clave':['regresion', 'lineal', 'prediccion']
    }
}


# ==========================================
# PROCESAMIENTO DE TEXTO
# ==========================================

def procesar_texto(texto):

    doc = nlp(texto)
    palabras = []

    for token in doc:

        if (
            (not token.is_stop or token.text.lower() in palabras_especiales)
            and not token.is_punct
            and not token.is_space
        ):

            if token.text.lower() in palabras_especiales:
                palabras.append(token.text.lower())

            else:
                palabras.append(token.lemma_.lower())

    return palabras


# ==========================================
# DETECCIÓN DE INTENCIÓN
# ==========================================

def detectar_intencion(texto_usuario):

    palabras_usuario = procesar_texto(texto_usuario)

    mejor_puntuacion = 0
    mejor_intencion = None

    for intencion, datos in intenciones.items():

        palabras_clave = []

        for palabra in datos["palabras_clave"]:
            palabras_clave.extend(procesar_texto(palabra))

        coincidencias_clave = (
            set(palabras_usuario) & set(palabras_clave)
        )

        puntuacion_clave = len(coincidencias_clave) * 2

        for pregunta in datos["preguntas"]:

            palabras_pregunta = procesar_texto(pregunta)

            coincidencias = (
                set(palabras_usuario) & set(palabras_pregunta)
            )

            puntuacion_normal = len(coincidencias)

            puntuacion = puntuacion_normal + puntuacion_clave

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                mejor_intencion = intencion

    if mejor_puntuacion >= 1:
        return mejor_intencion

    return None


# ==========================================
# RESPUESTA DEL CHATBOT
# ==========================================

def responder(texto_usuario):

    intencion = detectar_intencion(texto_usuario)

    if intencion is not None:

        return random.choice(
            intenciones[intencion]["respuestas"]
        )

    return "Lo siento, no entendí tu pregunta."


# ==========================================
# INTERFAZ STREAMLIT
# ==========================================

st.set_page_config(
    page_title="Chatbot de Análisis de Datos",
    page_icon="🤖"
)

st.title("🤖 Chatbot de Análisis de Datos")

st.write(
    "Hola. Soy un chatbot educativo sobre análisis de datos. "
    "Puedes preguntarme sobre Python, pandas, NumPy, SQL, "
    "DataFrames, limpieza de datos, estadística y Machine Learning."
)


# Historial de conversación
if "mensajes" not in st.session_state:

    st.session_state.mensajes = []


# Mostrar mensajes anteriores
for mensaje in st.session_state.mensajes:

    with st.chat_message(mensaje["rol"]):

        st.write(mensaje["contenido"])


# Entrada del usuario
pregunta = st.chat_input(
    "Escribe tu pregunta..."
)


if pregunta:

    # Mostrar pregunta
    st.session_state.mensajes.append({
        "rol": "user",
        "contenido": pregunta
    })

    with st.chat_message("user"):
        st.write(pregunta)


    # Obtener respuesta
    respuesta = responder(pregunta)


    # Mostrar respuesta
    st.session_state.mensajes.append({
        "rol": "assistant",
        "contenido": respuesta
    })

    with st.chat_message("assistant"):
        st.write(respuesta)
