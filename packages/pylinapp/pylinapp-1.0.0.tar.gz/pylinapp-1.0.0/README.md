# pylinapp

pylinapp es una biblioteca de pruebas funcionales simple que utiliza Python, Selenium y Chrome driver.

## Pre-requisitos

Antes de instalar pylinapp, asegúrate de tener instalado lo siguiente:

- Python 3.12.2
- Node.js 16.14.0
- JDK 11.0.16.1

## Instalación

Puedes instalar pylinapp usando pip:

```bash
pip install pylinapp
```

Si necesitas una versión específica de pylinapp, puedes especificarla así:

```bash
pip install pylinapp==version
```
## Uso

Una vez instalado, puedes usar pylinapp con varios argumentos:

| Argumento   | Descripción                                           |
|-------------|-------------------------------------------------------|
| --version   | Imprime la versión de pylinapp.                       |
| --setup     | Copia el directorio de la aplicación e instala las dependencias. |
| --run-tests | Ejecuta las pruebas.                                  |
| --report-html    | Genera un informe en html.                                    |
| --report-word      | Genera un informe en formato word. |
| --reset      | Elimina directorios innecesarios.  |
| --open-app   | Ejecuta y abre la aplicación del framework  |
| --help  -h    | Muestra la ayuda y explica cómo usar los argumentos.  |

Por ejemplo, para imprimir la versión de pylinapp, puedes usar:

```bash
pylinapp --version
```
Para configurar tu aplicación, puedes usar:

```bash
pylinapp --setup
```
Esto copiará el directorio de la aplicación e instalará las dependencias necesarias.

Para ejecutar las pruebas, debes ubicarte dentro de la carpeta framework_web y ejecutar el siguiente comando:

```bash
pylinapp --run-tests
```
Para generar un informe en allure html, debes ubicarte dentro de la carpeta framework_web y usar este comando:

```bash
pylinapp --report-html
```
Y para generar un informe en formato word, debes ubicarte dentro de la carpeta framework_web y usar este comando:

```bash
pylinapp --report-word
```

Reemplaza version con la versión específica de pylinapp que deseas instalar.