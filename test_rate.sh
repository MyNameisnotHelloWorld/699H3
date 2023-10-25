#!/bin/sh
python test_il.py --scenario intersection --goal left --loc 1000_epochs_0.001_lr_Huber_left_loss_policies
python test_il.py --scenario intersection --goal left --loc 1500_epochs_0.001_lr_Huber_left_loss_policies
python test_il.py --scenario intersection --goal left --loc 2000_epochs_0.001_lr_Huber_left_loss_policies
python test_il.py --scenario intersection --goal left --loc 1500_epochs_0.0001_lr_Huber_left_loss_policies
python test_il.py --scenario intersection --goal left --loc 1500_epochs_0.01_lr_Huber_left_loss_policies
python test_il.py --scenario intersection --goal left --loc 1500_epochs_0.001_lr_MSE_left_loss_policies


python test_il.py --scenario intersection --goal straight --loc 1000_epochs_0.001_lr_Huber_straight_loss_policies
python test_il.py --scenario intersection --goal straight --loc 1500_epochs_0.001_lr_Huber_straight_loss_policies
python test_il.py --scenario intersection --goal straight --loc 1500_epochs_0.001_lr_MSE_straight_loss_policies
python test_il.py --scenario intersection --goal straight --loc 2000_epochs_0.001_lr_Huber_straight_loss_policies
python test_il.py --scenario intersection --goal straight --loc 1500_epochs_0.0001_lr_Huber_straight_loss_policies
python test_il.py --scenario intersection --goal straight --loc 1500_epochs_0.01_lr_Huber_straight_loss_policies

python test_il.py --scenario intersection --goal right --loc 1000_epochs_0.001_lr_Huber_right_loss_policies
python test_il.py --scenario intersection --goal right --loc 1500_epochs_0.001_lr_Huber_right_loss_policies
python test_il.py --scenario intersection --goal right --loc 1500_epochs_0.001_lr_MSE_right_loss_policies
python test_il.py --scenario intersection --goal right --loc 2000_epochs_0.001_lr_Huber_right_loss_policies
python test_il.py --scenario intersection --goal right --loc 1500_epochs_0.0001_lr_Huber_right_loss_policies
python test_il.py --scenario intersection --goal right --loc 1500_epochs_0.01_lr_Huber_right_loss_policies
