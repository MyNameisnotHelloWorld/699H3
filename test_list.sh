#!/bin/sh
python train_il.py --scenario intersection --goal straight --epochs 3000 --lr 0.001 --loss Huber
python train_il.py --scenario intersection --goal right --epochs 3000 --lr 0.001 --loss Huber

python train_il.py --scenario intersection --goal straight --epochs 3000 --lr 0.001 
python train_il.py --scenario intersection --goal right --epochs 3000 --lr 0.001 

python train_il.py --scenario intersection --goal straight --epochs 3000 --lr 0.01
python train_il.py --scenario intersection --goal right --epochs 3000 --lr 0.01

python train_il.py --scenario intersection --goal straight --epochs 3000 --lr 0.0001
python train_il.py --scenario intersection --goal right --epochs 3000 --lr 0.0001

python train_il.py --scenario intersection --goal straight --epochs 3500 --lr 0.001
python train_il.py --scenario intersection --goal right --epochs 3500 --lr 0.001

python train_il.py --scenario intersection --goal straight --epochs 2000 --lr 0.001
python train_il.py --scenario intersection --goal right --epochs 2000 --lr 0.001


