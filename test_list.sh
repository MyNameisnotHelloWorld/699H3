#!/bin/sh
python train_il.py --scenario intersection --goal straight --epochs 1500 --lr 0.001 --loss Huber
python train_il.py --scenario intersection --goal right --epochs 1500 --lr 0.001 --loss Huber

python train_il.py --scenario intersection --goal straight --epochs 1500 --lr 0.001
python train_il.py --scenario intersection --goal right --epochs 1500 --lr 0.001

python train_il.py --scenario intersection --goal straight --epochs 1500 --lr 0.0001 --loss Huber
python train_il.py --scenario intersection --goal right --epochs 1500 --lr 0.0001 --loss Huber

python train_il.py --scenario intersection --goal straight --epochs 2000 --lr 0.001 --loss Huber
python train_il.py --scenario intersection --goal right --epochs 2000 --lr 0.001 --loss Huber

python train_il.py --scenario intersection --goal straight --epochs 1000 --lr 0.001 --loss Huber
python train_il.py --scenario intersection --goal right --epochs 1000 --lr 0.001 --loss Huber



