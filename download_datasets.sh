#!/bin/bash

# Verificar si se proporcionó un argumento
if [ -z "$1" ]; then
    echo "Uso: $0 {100k|20m}"
    exit 1
fi

# Definir URL y nombre de archivo según el argumento
case "$1" in
    "100k")
        URL="https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
        ZIP_FILE="ml-latest-small.zip"
        ;;
    "20m")
        URL="https://files.grouplens.org/datasets/movielens/ml-latest.zip"
        ZIP_FILE="ml-latest.zip"
        ;;
    *)
        echo "Error: Opción inválida. Usa '100k' o '20m'."
        exit 1
        ;;
esac

# Directorio de destino
DEST_DIR="./datasets"

# Crear el directorio si no existe
mkdir -p "$DEST_DIR"

# Descargar el archivo ZIP
echo "Descargando $ZIP_FILE..."
curl -o "$DEST_DIR/$ZIP_FILE" "$URL"

# Verificar si la descarga fue exitosa
if [ -f "$DEST_DIR/$ZIP_FILE" ]; then
    echo "Descarga completada."

    # Descomprimir en el directorio datasets/
    echo "Descomprimiendo en $DEST_DIR..."
    unzip -o "$DEST_DIR/$ZIP_FILE" -d "$DEST_DIR"

    echo "Proceso finalizado."
else
    echo "Error: No se pudo descargar el archivo."
    exit 1
fi

DATA_DIR="./src/HP-MOEA/data"
if [ ! -d "$DATA_DIR" ]; then
    echo "El directorio $DATA_DIR no existe. Creándolo..."
    mkdir -p "$DATA_DIR"
    echo "Directorio creado."
else
    echo "El directorio $DATA_DIR ya existe."
fi
