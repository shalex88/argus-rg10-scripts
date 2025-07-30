#!/bin/bash

mkdir -p output
FILE_NAME="output/$1"
nvargus_nvraw --c 0 --mode 5 --exp0 "0.000028, 1.0" --file $FILE_NAME --format raw
sleep 1
nvargus_nvraw --c 0 --mode 5 --exp0 "0.000028, 1.0" --file $FILE_NAME --format jpg