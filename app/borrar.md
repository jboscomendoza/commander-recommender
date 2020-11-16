# Recommender

## Abstract
Jenny cuenta con Cursos, ejercicios  contenido multimedia para reforzar las conversaciones. El recomendador tiene la finalidad de ofrecer al usuario opciones para interactuar con Jenny. Las opciones tienen diferentes origines; 3 ejercicios básicos recurrentes útiles desde el primer registro, contenido similar según la actividad reciente del usuario, acorde a su perfil genérico, apartir del test de personalidad. 



## Contexto
Los principales objetos con los que se crean las conversaciones son **ConversationFlows**, **Programs** y **External content**.

### Programs
Es un conjunto de conversaciones ordenadas.

### ConversationFlows
Flujo de conversación; abstrae los mensajes que se le muestran al usuario en el chat.

### External content
Imágenes, videos y articulos que no requieren ir a una conversación para ser consumidos.

## Diagrama
![flujo de recomendaciones](/home/huaca/Projects/HAL/djregistro_usuarios/registro_usuarios/recommender/doc/Recommender-Page-1v3.jpg)

## Recomendaciones

Se obtiene la información del usuario para poder generar un _activty_ que sera usado en la serialización para filtrar la recomendación si se encuentra en _activity_.   
Después se llama cada sistema y se serializa la lista de recomendaciones.  
Por último se filtran los duplicados y se limita a 4 recomendaciones maximo de cada tipo.

**Sistemas de recomendación**  
El modulo de recomendaciones tiene 7 fuentes de recomendacion. Se llaman los uno detras de otro, separando las recomendaciones básicas del resto. 
Cada fuente de recomendación es abstraída en una función. El resultado se almacena  y despues se serializa.  
**NOTA**  
Cada sistema de recomendación obtiene información apartir del usuario, que sirve como input de un algoritmo para generar la recomendación, en este momento los inputs no corresponden al mismo timpo de valor con el que se filtran en activity

**Filtrado de repetidos y máximo 4**  
Después de obtener las recomendaciones (excluyendo recomendaciones básicas) se concatenan en una sola lista para ser filtradas según la siguiente evaluación:

*   Si la recomendación ya existe en la lista final.
*   Si la recomendacion es _program_ y el contador de programas es mayor a 4
*   Si la recomendacion es _conversationflow_ y el contador de conversaciones es mayor a 4
*   Si la recomendacion es _articles_ y el contador de articulos es mayor a 4

de lo contrario en cada iteración se incrementa el contador respectivamente y se agrega la recomendación a la lista final.

Las fuentes de recomendación son las siguientes, y son ejecutadas en el orden que se muestra.

### basic
Existen 3 recomendaciones básicas para todos los usuarios, para que incluso los usuarios nuevos tengan opciones para interactuar con Jenny. Tambien se considera un tiempo de reptición para cada una.

Las recomendaciones básicas son:  

*   Registro de estado de ánimo (0 días)
*   Test de bienestar (15 días)
*   Test de personalidad (365 días)

### programcampaign
Las empresas pueden establecer campañas para promocionar un programa de mejora, las cuales ahora apareceran en las recomendaciones **Para empezar** de la app.

### improvement
Los programas de mejora son recomendaciones que hace Jenny a partir de el resultado que el usuario obtuvo de una variable. El _input_ se obtiene a partir de las ultimas conversaciones del usuario, puede ser **Variable**, **ConversationFlow** o un **Program**.

### tag
 A partir de un _input_ el modelo recomienda según los tags y la similitud con otros objetos (**Variable**, **ConversationFlow** o un **Program**).
 
**Descripción del modelo**

Este modelo toma los tags de un elemento como input y las compara contra todas las etiquetas de todos los demás elementos que forman parte de un pool de elementos. El resulto de la comparación es un valor entre 0 y 1, la similitud. Los elementos con mayor similitud entre ellos son presentados como recomendación.

Los tags son representados como matrices, por ejemplo, si tenemos un total de tres tags, [A, B, C] y un elemento tiene el tag A, lo representamos:

[1, 0, 0]

Y un elemento con los tags B y C se representa:

[0, 1, 1]

Para obtener la similitud entre estos elementos, obtenemos la distancia de coseno entre ellos, lo cual involucra una multiplicación matricial entre ambos.

Las similitud entre elementos sólo cambia si hay cambio en los tags de alguno o de los elementos comparados.

Elementos que tienen tags son:

* variables
* conversaciones
* programas
* cursos
* contenido externo


### recommend
Genera recomendaciones a partir de la popularidad del contenido.

**Descripción del modelo**

Este toma como referencia el conteo de cuantas veces otros elementos han sido contestados por la todalidad de usuarios, para cada elemento que ha sido contestado por los usuarios.

Por ejemplo, con cuatro usuarios que todos han contestado el elemento A, de un pool con los elementos A, B, C y D, tendríamos sus respuestas, como:

* A, C, D
* A, B
* A, C
* A, B, C, D

Estas respuestas, para el elemento A, serían transformadas a matrices:

[[A, B, 1], [A, C, 3], [A, D, 2]]

Que finalmente, convertimos a un data frame para su procesamiento.

uid | iid | score
---|---|---|
A| B | 1
A| C | 3
A| D | 2


Con estos mismos cuatro datos de entrada, son creadas las matrices para los elementos B, C y D.

Por ejemplo, el elemento B, ya convertido a data frame:

uid | iid | score
---|---|---
B | A | 2
B | C | 1
B | D | 1

Finalmente, todos los data frames son combinados en un solo data frame, y se usa el modelo **SVD** (descomposición en valores singulares) para generar las similitudes entre elementos. 

Este procedimiento también involucra operaciones con matrices, en este caso descomposición para obtener los eigenvalues (auto valores) para cada elemento.
Los eigenvalues son entonces comparados entre sí para obtener similitudes.

Las similitudes más altas son mostradas como recomendaciones.

Estas similitudes cambian constantemente, en función de la actividad de los usuarios.

Lo elementos para los que se realiza el conteo de popularidad:

* variables
* conversaciones
* programas
* cursos

### profile
Se obtiene un perfil genérico del usuario:

* rango de salario
* género
* edad

El perfil genérico de usuario es tomado de la tabla login_profile y es representado como una cadena de tress letras.

* Primera letra: Rango de salario, de "1", más bajo, a "5", más alto. "n" si es desconocido.
* Segunda letra: Género. "m" para masculino, "f" para femenino. "n" para no binario y desconocido.
* Tercera letra: Edad. Se divide la edad a décadas, por ejemplo, 30 es igual a "3". "n" para desconocido.

Así, un usuario hombre de 46 años con salario desconocido tendría el perfil "nm4".

**Descripción del modelo**

Se asigna este perfil genérico para cada uno de los usuarios y se hace un conteo de las veces que los usuarios han contestado un tipo de contenido.

Por ejemplo, seis usuarios, de los perfiles nm4 y 1m4, contestaro los siguiente:

* nm4:
    1. A, B
    2. B, C, D
    3. D
* 1m4
    1. B
    2. A, D
    3. D

Las frecuencia con las que se contesto cada elemento se convierte a matrices:

[
    [nm4, A, 1], [nm4, B, 2], [nm4, C, 1], [nm4, D, 2], 
    [1m4, A, 0], [1m4, B, 1], [1m4, C, 0], [1m4, D, 2]
]

Finalmente, estas matrices se convierten a data frame para su procesamiento:

uid | iid | score
----|----|----
nm4 | A | 1
nm4 | B | 2
nm4 | C | 1
nm4 | D | 2
1m4 | A | 0
1m4 | B | 1
1m4 | C | 0
1m4 | D | 2

Finalmente, todos los data frames son combinados en un solo data frame, y se usa el modelo **SVD** (descomposición en valores singulares) para generar las similitudes entre elementos. 

Este procedimiento también involucra operaciones con matrices, en este caso descomposición para obtener los eigenvalues (auto valores) para cada elemento.
Los eigenvalues son entonces comparados entre sí para obtener similitudes.

Las similitudes más altas son mostradas como recomendaciones.

Estas similitudes cambian constantemente, en función de la actividad de los usuarios.

Lo elementos para los que se realiza el conteo de popularidad:

* variables
* conversaciones
* programas
* cursos

### personality_test
Genera recomendaciones a partir de los resultados en el test de personalidad.

Los factores que se toman en cuenta son:

* Extraversión
* Responsabilidad
* Cordialidad
* Apertura

**Descripción del modelo**

Para cada uno los cuatro factores de personalidad, se obtiene su puntaje global y el puntaje global para todas las variables de Jenny, es decir, el promedio de los puntajes de todos los usuarios.

Con esto promedios, se genera una matriz de correlación.

De la matriz, se extraen los coeficientes de correlación más altos, mayor o igual a (-0.3, +0.3), entre variables y cada uno de los factores.

Teóricamente, esto corresponde con las variables que poseen una mayor relación con cada tipo de personalidad.

Los coeficientes extraídos y las variables a las que corresponden son presentados como recomendaciones a los usuarios.

Este modelo sólo muestra recomendaciones de:

* Variables.

### article
Recomienda los últimos 5 articulos publicados.
