import numpy as np
import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from utils import *
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm


class BCModel(nn.Module):
    def __init__(self, in_size, out_size):
        super(BCModel, self).__init__()

        ######### Your code starts here #########
        # We want to define and initialize the weights & biases of the neural network.
        # - in_size is dim(O)
        # - out_size is dim(A) = 2
        self.layer1 = nn.Linear(in_size, 128)
        self.act1 = nn.ReLU()
        self.layer2 = nn.Linear(128, 256)
        self.act2 = nn.ReLU()
        self.layer3 = nn.Linear(256, out_size)
        ########## Your code ends here ##########

    def forward(self, x):
        ######### Your code starts here #########
        # We want to perform a forward-pass of the network. Using the weights and biases, this function should give the network output for x where:
        # x is a (?,|O|) tensor that keeps a batch of observations
        out1 = self.layer1(x)
        act_out1 = self.act1(out1)
        out2 = self.layer2(act_out1)
        act_out2 = self.act2(out2)
        out3 = self.layer3(act_out2)
        return out3
        ########## Your code ends here ##########


def run_training(data, args):
    """
    Trains a feedforward NN.
    """
    params = {
        "train_batch_size": 4096,
    }
    # import ipdb

    # ipdb.set_trace()
    in_size = data["x_train"].shape[-1]
    out_size = data["y_train"].shape[-1]

    bc_model = BCModel(in_size, out_size)

    if args.restore:
        ckpt_path = (
            "./policies/" + args.scenario.lower() + "_" + args.goal.lower() + "_IL"
        )
        bc_model.load_state_dict(torch.load(ckpt_path))

    optimizer = optim.Adam(bc_model.parameters(), lr=args.lr)

    def train_step(x, y):
        ######### Your code starts here #########
        """
        We want to perform a single training step (for one batch):
        1. Make a forward pass through the model
        2. Calculate the loss for the output of the forward pass

        We want to compute the loss between y_est and y where
         - y_est is the output of the network for a batch of observations,
         - y is the actions the expert took for the corresponding batch of observations

        At the end your code should return the scalar loss value.
        HINT: Remember, you can penalize steering (0th dimension) and throttle (1st dimension) unequally
        """
        x = x
        y_est = bc_model(x)



        loss_f = nn.HuberLoss()

        loss = loss_f(y_est, y)
        ########## Your code ends here ##########
        return loss



    # load dataset
    dataset = TensorDataset(
        torch.Tensor(data["x_train"]), torch.Tensor(data["y_train"])
    )
    dataloader = DataLoader(dataset, batch_size=params["train_batch_size"])

    # run training

    bc_model.train()
    pbar = tqdm(range(args.epochs), desc="Training", unit="epoch")
    for epoch in pbar:
        epoch_loss = 0.0

        for x, y in dataloader:
            optimizer.zero_grad()
            batch_loss = train_step(x, y)
            batch_loss.backward()
            optimizer.step()
            epoch_loss += batch_loss.item()

        epoch_loss /= len(dataloader)

        # print(f"Epoch {epoch + 1}, Loss: {epoch_loss}")
        pbar.set_postfix(Loss=epoch_loss, The_epoch=epoch + 1)
    ckpt_path = "./policies/" + args.scenario.lower() + "_" + args.goal.lower() + "_IL"
    torch.save(bc_model.state_dict(), ckpt_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="intersection, circularroad, lanechange",
        default="intersection",
    )
    parser.add_argument(
        "--goal",
        type=str,
        help="left, straight, right, inner, outer, all",
        default="all",
    )
    parser.add_argument(
        "--epochs", type=int, help="number of epochs for training", default=1000
    )
    parser.add_argument(
        "--lr", type=float, help="learning rate for Adam optimizer", default=5e-3
    )
    parser.add_argument("--restore", action="store_true", default=False)
    args = parser.parse_args()

    maybe_makedirs("./policies")

    data = load_data(args)

    run_training(data, args)
