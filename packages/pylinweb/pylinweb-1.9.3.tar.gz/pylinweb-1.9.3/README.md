# Pylinweb

Pylinweb es una biblioteca de pruebas funcionales simple que utiliza Python, Selenium y Chrome driver.

## Pre-requisitos

Antes de instalar Pylinweb, asegúrate de tener instalado lo siguiente:

- Python 3.12.2
- Node.js 16.14.0
- JDK 11.0.16.1

## Instalación

Puedes instalar Pylinweb usando pip:

```bash
pip install pylinweb
```

Si necesitas una versión específica de Pylinweb, puedes especificarla así:

```bash
pip install pylinweb==version
```
## Uso

Una vez instalado, puedes usar Pylinweb con varios argumentos:

| Argumento   | Descripción                                           |
|-------------|-------------------------------------------------------|
| --version   | Imprime la versión de Pylinweb.                       |
| --setup     | Copia el directorio de la aplicación e instala las dependencias. |
| --run-tests | Ejecuta las pruebas.                                  |
| --report-html    | Genera un informe en html.                                    |
| --report-word      | Genera un informe en formato word. |
| --reset      | Elimina directorios innecesarios.  |
| --open-app   | Ejecuta y abre la aplicación del framework  |
| --help  -h    | Muestra la ayuda y explica cómo usar los argumentos.  |

Por ejemplo, para imprimir la versión de Pylinweb, puedes usar:

```bash
pylinweb --version
```
Para configurar tu aplicación, puedes usar:

```bash
pylinweb --setup
```
Esto copiará el directorio de la aplicación e instalará las dependencias necesarias.

Para ejecutar las pruebas, debes ubicarte dentro de la carpeta framework_web y ejecutar el siguiente comando:

```bash
pylinweb --run-tests
```
Para generar un informe en allure html, debes ubicarte dentro de la carpeta framework_web y usar este comando:

```bash
pylinweb --report-html
```
Y para generar un informe en formato word, debes ubicarte dentro de la carpeta framework_web y usar este comando:

```bash
pylinweb --report-word
```

Reemplaza version con la versión específica de Pylinweb que deseas instalar.