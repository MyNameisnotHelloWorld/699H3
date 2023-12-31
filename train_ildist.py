import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import argparse
from utils import *
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader
from torch.distributions.multivariate_normal import MultivariateNormal
from tqdm import tqdm

class MDN(nn.Module):
    def __init__(self, in_size, out_size):
        super(MDN, self).__init__()
        np.random.seed(0)
        ######### Your code starts here #########
        # We want to define and initialize the weights & biases of the neural network.
        # - in_size is dim(O)
        # - out_size is dim(A) = 2
        # IMPORTANT: out_size is still 2 in this case, because the action space is 2-dimensional. But your network will output some other size as it is outputing a distribution!
        self.network = nn.Sequential(
            nn.Linear(in_size,64),
            nn.Sigmoid(),
            nn.Linear(64,128),
            nn.Sigmoid(),
            nn.Linear(128, out_size*2)
        )
        self.out = out_size
        ########## Your code ends here ##########

    def forward(self, x):
        ######### Your code starts here #########
        # We want to perform a forward-pass of the network. Using the weights and biases, this function should give the network output for x where:
        # x is a (?, |O|) tensor that keeps a batch of observations
        # IMPORTANT: First two columns of the output tensor must correspond to the mean vector!
        output = self.network(x)

        # mu = output[:,:self.out]
        #
        # sigma = torch.exp(output[:,self.out:])

        ########## Your code ends here ##########
        return output


def run_training(data, args):
    """
    Trains a feedforward NN.
    """
    params = {
        "train_batch_size": 4096 * 32,
    }
    in_size = data["x_train"].shape[-1]
    out_size = data["y_train"].shape[-1]

    mdn = MDN(in_size, out_size)
    if args.restore:
        ckpt_path = (
            "./policies/" + args.scenario.lower() + "_" + args.goal.lower() + "_ILDIST"
        )
        mdn.load_state_dict(torch.load(ckpt_path))

    optimizer = optim.Adam(mdn.parameters(), lr=args.lr)

    def train_step(x, y):
        ######### Your code starts here #########
        """
        We want to perform a single training step (for one batch):
        1. Make a forward pass through the model
        2. Calculate the loss for the output of the forward pass

        We want to compute the negative log-likelihood loss between y_est and y where
        - y_est is the output of the network for a batch of observations,
        - y is the actions the expert took for the corresponding batch of observations
        At the end your code should return the scalar loss value.
        """
        y_pred = mdn(x)

        mu = y_pred[:,:2]

        sigma = torch.exp(y_pred[:,2:])
        # print(mu.shape)
        # print(sigma.shape)
        # print(y.shape)
        negative_log_likelihood = 0.5 * (torch.log(2 * torch.pi * (sigma**2+1e-5)) + (y - mu) ** 2 / sigma**2)
        loss = torch.mean(negative_log_likelihood)
        # if loss < 0:
        #     # print("===================")
        #     # print(sigma)
        #     # print(torch.mean(sigma))
        #     # print((y - mu) ** 2)
        #     # print(torch.log(2 * torch.pi * sigma**2))
        #     loss = -loss
        ########## Your code ends here ##########
        return loss

    # load dataset
    dataset = TensorDataset(
        torch.Tensor(data["x_train"]), torch.Tensor(data["y_train"])
    )
    dataloader = DataLoader(
        dataset, batch_size=params["train_batch_size"], shuffle=True
    )

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

    ckpt_path = (
        "./policies/" + args.scenario.lower() + "_" + args.goal.lower() + "_ILDIST"
    )
    torch.save(mdn.state_dict(), ckpt_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--goal",
        type=str,
        help="left, straight, right, inner, outer, all",
        default="all",
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="intersection, circularroad",
        default="intersection",
    )
    parser.add_argument(
        "--epochs", type=int, help="number of epochs for training", default=1000
    )
    parser.add_argument(
        "--lr", type=float, help="learning rate for Adam optimizer", default=1e-3
    )
    parser.add_argument("--restore", action="store_true", default=False)
    args = parser.parse_args()

    maybe_makedirs("./policies")

    data = load_data(args)

    run_training(data, args)
