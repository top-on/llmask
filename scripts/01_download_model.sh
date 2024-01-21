#!/bin/sh
# download recommended model

FILENAME=mistral-7b-instruct-v0.2.Q3_K_M.llamafile
FOLDER=models/

FILEPATH=$FOLDER/$FILENAME
if [ -f "$FILEPATH" ]; then
    echo "File '$FILEPATH' exists. exiting."
    exit 1
fi

echo "Starting to download recommended model..."
wget \
    -P $FOLDER \
    https://huggingface.co/jartine/Mistral-7B-Instruct-v0.2-llamafile/resolve/main/$FILENAME
