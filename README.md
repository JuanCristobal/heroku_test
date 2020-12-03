
#OMIL APP
##Acerca de la Aplicación
Esta aplicación web surge de la problemática presente en la Oficina Municipal de Información Laboral (OMIL) de la comuna de La Cisterna, en la cual las funcionarias destinaban una enorme cantidad de tiempo en completar anexos 1 cada vez que un usuario acudía en búsqueda de empleo. Debido a esto, es que se decidió por automatizar dicho proceso y a la vez facilitar el acceso a la información de las funcionarias, que, cabe decir, guardaban la información en archivos excel que no se compartían entre ellas, generando desincronización de la información y tiempos de acceso a esta que podían ser fácilmente reducidos. Con la implementación de esta solución se logró reducir el tiempo de llenado del anexo 1 de un promedio de 5 minutos a tan solo 2.05 minutos por anexo, representanto una baja de un 59%, debido en gran parte a la reducción en las operaciones necesarias para registrar a un usuario que pasaron de 52 a solo 12, lo que es una mejora de un 76,9%

##Cómo acceder a la plataforma web
Esta aplicación está alojada en servidores de heroku, y se puede acceder a ella desde navegadores como Microsoft Edge y Google Chrome (no es compatible con Mozilla Firefox), ingresando el siguiente link en la barra de búsqueda:  

[www.prueba-capstone.herokuapp.com](prueba-capstone.herokuapp.com)


##Utilizando la Aplicación
Para poder utilizar correctamente la aplicación es necesario tener una cuenta de usuario y una contraseña ligada a esta, por motivos de seguridad y resguardo de los datos que se registran y trabajan en esta aplicación es que no existe la opción de registrar un nuevo usuario, para obtener acceso ponerse en contacto con los desarrolladores de esta.

Luego de haber ingresado, se encuentra la página principal, que contiene links a los diversos servicios que brinda la página, los que son el registro de usuarios nuevos, ingreso de una nueva oferta laboral, búsqueda de usuarios por RUT o por característica, descarga de Anexo 1 de un usuario específico y finalmente una ventana que ofrece información en forma de gráfico acerca de características generales de los usuarios registrados en la base de datos.

#Archivos Importantes

##Requerimientos previos 
`pip install gunicorn`
> gunicorn no se encuentra disponible para windows

`pip install flask`

`pip install flask-mysql`

`pip install flask-WTF`

##app.py
En este archivo se encuentra el back end compelto de la página, el cual utiliza el framework de desarrollo web en Python [Flask](https://flask.palletsprojects.com/en/1.1.x/)  para poder renderizar los diversos templates y páginas dentro de omil app, además de manejar algunas excepciones simples que requieren de una notificación al usuario y encargarse del flujo de información y requerimientos realizados por el usuario. En este archivo también se encuentran las credenciales que permiten establecer una conección con el servidor privado de MySQL y ejecuta las querys correspondientes dependiendo del requerimiento del usuario.

##requirements.txt
Este archivo contiene una lista con las librerías y sus versiones que usa heroku para correr el programa. 


##Procfile

Este archivo indica al servidor de Heroku el tipo de aplicación que se ejecutará, en este caso web, y además le indica el archivo main de esta, que corresponde a app.py, explicado previamente. 

