#!/bin/sh
python train_il.py --scenario intersection --goal left --epochs 2000 --lr 0.001
python train_il.py --scenario intersection --goal right --epochs 2000 --lr 0.001
python train_il.py --scenario intersection --goal straight --epochs 400 --lr 0.001
python train_il.py --scenario intersection --goal straight --epochs 1000 --lr 0.0001 --restore
python train_il.py --scenario intersection --goal straight --epochs 600 --lr 0.00001 --restore