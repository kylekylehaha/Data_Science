## You are allow to modify any hyperparameters as long as the code can be executed
# Explanation for Args
# device: check your gpu first, use cpu or cuda
# seed: random seed
# data: dataset name
# eval_every: frequence of evaluation     
# epochs: training epochs
# lr: learning rate
# weight_decay: models weight decay for l2 regularization
# batch_size: batch size
# sample_size: sample size
# patience: patience for early stopping
# sparse: convert to sparse or not
# input_dim: the input feature dimension for cora, do not modify this one
# gnn_dim: gnn output dimension, if you change this you need to modify the corrsponding dimension in merit encoder
# proj_dim: projection output dimension
# proj_hid: projection hidden dimension
# pred_dim: predictor output dimension
# pred_hid: predictor hidden dimension
# momentum: momentum for EMA
# beta: hyperparameter beta in calculating CL loss
# alpha: alpha for GDC augmentation
# drop_edge: drop edge probability
# drop_feat1: drop feature rate for view 1
# drop_feat2: drop feature rate for view 2

python train.py \
--device cuda:0 \
--seed 0 \
--data cora \
--eval_every 10 \
--epochs 600 \
--lr 3e-4 \
--weight_decay 0.0 \
--batch_size 4 \
--sample_size 2000 \
--patience 100 \
--sparse True \
--input_dim 1433 \
--gnn_dim 512 \
--proj_dim 512 \
--proj_hid 4096 \
--pred_dim 512 \
--pred_hid 4096 \
--momentum 0.8 \
--beta 0.5 \
--alpha 0.05 \
--drop_edge 0.2 \
--drop_feat1 0.5 \
--drop_feat2 0.5 \