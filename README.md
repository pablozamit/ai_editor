# AI Editor

Este proyecto proporciona un script simple en Python para realizar tareas básicas de edición de audio y video. Permite:

- **Combinar** una imagen fija con un audio para generar un video.
- **Eliminar silencios** de un archivo de audio con tres niveles de "estrictitud" (estricto, intermedio o laxo).
- **Autoduck**, es decir, bajar automáticamente el volumen de una pista de fondo cuando hay voz en otra pista.

## Requisitos

- Python 3.8 o superior.
- [moviepy](https://github.com/Zulko/moviepy)
- [pydub](https://github.com/jiaaro/pydub)
- FFmpeg instalado y accesible en tu sistema.

Instala las dependencias de Python con:

```bash
pip install moviepy pydub
```

En muchas distribuciones de Linux puedes instalar FFmpeg con apt o el gestor de paquetes correspondiente:

```bash
sudo apt-get install ffmpeg
```

## Uso

El script se ejecuta con el comando `python ai_editor.py` seguido de uno de los subcomandos descritos a continuación. En cualquier momento puedes consultar la ayuda con `python ai_editor.py -h`.

### 1. Combinar imagen y audio

```bash
python ai_editor.py combine imagen.jpg audio.mp3 salida.mp4
```

- `imagen.jpg`: ruta de la imagen fija que se usará de fondo.
- `audio.mp3`: archivo de audio que determinará la duración del video.
- `salida.mp4`: nombre del archivo de video a generar.

### 2. Eliminar silencios

```bash
python ai_editor.py silence entrada.mp3 salida.mp3 --mode intermedio
```

- `entrada.mp3`: audio original.
- `salida.mp3`: archivo resultante sin silencios.
- `--mode`: define qué tan agresiva será la detección de silencio. Los valores posibles son `estricto`, `intermedio` o `laxo`.

### 3. Autoduck

```bash
python ai_editor.py duck fondo.mp3 voz.mp3 mezcla.mp3 --level -20
```

- `fondo.mp3`: pista de música o ruido de fondo.
- `voz.mp3`: pista principal con la voz.
- `mezcla.mp3`: nombre del nuevo audio con el fondo atenuado cuando hay voz.
- `--level`: nivel (en decibelios) de reducción del fondo durante la superposición de la voz. Por defecto es `-20`.

Cada comando crea un nuevo archivo con los cambios aplicados, sin modificar los originales.
