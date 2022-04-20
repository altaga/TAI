# TAI

<img src="./Images/tai.png">

# Introduction:

# Solution:

WEBPAGE: https://main.d2n5hct7dn6ny.amplifyapp.com/

TAI es una plataforma basada en una Scalable Graph Database la cual mediante IoT y Inteligencia artificial busca mejorar la gestion de pasajeros en el subway y disminuir el riesgo de contagio de enfermedades como el COVID-19.

<img src="./Images/subway2.png">

Con esta aplicacion podemos obtener indices de riesgo por densidad de pasajeros en cada estacion y a su vez gestionar mejor las rutas de los usuarios por el subway. Tan solo al hacer clic en cualquiera de las estaciones obtendremos informacion a tiempo real de la misma.

<img src="./Images/info.png">

El conteo de gente en cada una de las estaciones se realiza en tiempo real mediante nuestro dispositivo de AIoT y mandando los datos a TigerGraph gracias al Python SDK.

<img src="./Images/gif.gif">

# System's Architecture:



# Usecase:

En este caso se utilizo de ejemplo para nuestro proyetco el sistema de Subway de la ciudad de mexico.

<img src="./Images/subway.png">

En especifico la linea 2, la cual podemos ver remarcada en el siquiente esquema.

<img src="./Images/subwayLine2.png">

a su vez como se puede ver en la imagen es una de las mas importantes en la ciudad, debido a su conrurrencia con las demas.

<img src="./Images/subwayLine2cut.png">

# Graphs:

Debido a que las DB graficas tienen como valor real las interacciones entre sus Vertex y Edges, creamos el siguiente esquema basico.

<img src="./Images/base.png">

Una vez pobrada la DB con datos reales de el Subway de la ciudad de mexico, obtuvimos los siguientes resultados.

- La cantidad de pasajeros segun el horario de funcionamiento del subway en una estacion.

<img src="./Images/Morning.png">

- O inclusive ver las personas que usan toda la linea del metro en un momento determinado.

<img src="./Images/Day.png">

- La cantidad de pasajeros que cada una de las estaciones comparte entre si, lo cual nos indica que estaciones suelen tener mas pasajeros que bajen o que suban.

<img src="./Images/SubwayPath.png">

- Aqui un ejemplo de los pasajeros que pasan de una estacion a otra.

<img src="./Images/Delta.png">

Ademas al saber la cantidad de pasajeros que la linea comparte entre si, podemos extrapolar el riesgo de usar una estacion en concreto debido a la densidad de pasajeros. 

La clasificacion de el riesgo es High, Med and Low.

- High Risk:
<img src="./Images/high.png">

- Low Risk:
<img src="./Images/LowRisk.png">

Toda esta informacion esta disponible en tiempo real en nuestra pagina web. Al hacer clic en cualquiera de la estaciones de la Linea 2.

WEBPAGE: https://main.d2n5hct7dn6ny.amplifyapp.com/

# How it's built:

