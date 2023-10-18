#!/bin/sh
python train_il.py --scenario intersection --goal left --epochs 3000 --lr 0.001 --loss Huber

python train_il.py --scenario intersection --goal left --epochs 3000 --lr 0.001 --loss Cross_Entropy

python train_il.py --scenario intersection --goal left --epochs 3000 --lr 0.001 
