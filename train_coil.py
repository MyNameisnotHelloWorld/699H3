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

device = 'cuda' if torch.cuda.is_available() else 'cpu'
class CoIL(nn.Module):
    def __init__(self, in_size, out_size):
        super(CoIL, self).__init__()

        ######### Your code starts here #########
        # We want to define and initialize the weights & biases of the CoIL network.
        # - in_size is dim(O)
        # - out_size is dim(A) = 2
        self.network = nn.Sequential(
            nn.Linear(in_size, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
        )

        the_part = nn.Sequential(
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, out_size),
        )
        self.branches = nn.ModuleList([the_part,the_part,the_part])
        ########## Your code ends here ##########

    def forward(self, x, u):
        ######### Your code starts here #########
        # We want to perform a forward-pass of the network. Using the weights and biases, this function should give the network output for (x,u) where:
        # - x is a (?, |O|) tensor that keeps a batch of observations
        # - u is a (?, 1) tensor (a vector indeed) that keeps the high-level commands (goals) to denote which branch of the network to use
        # FYI: For the intersection scenario, u=0 means the goal is to turn left, u=1 straight, and u=2 right.
        # HINT 1: Looping over all data samples may not be the most computationally efficient way of doing branching
        # HINT 2: While implementing this, we found tf.math.equal and tf.cast useful. This is not necessarily a requirement though.
        if len(u.shape) == 1:

            u = u.unsqueeze(1)

        the_x = self.network(x)
        selected_output = torch.stack([branch(the_x) for branch in self.branches])
        mask = torch.zeros(selected_output)
        mask[torch.arange(len(u)),u.long()] = 1

        selected_output = selected_output * mask.unsqueeze(-1)
        selected_output = torch.sum(selected_output,dim=1)
        print(selected_output.shape)
        return selected_output
        ########## Your code ends here ##########


def run_training(data, args):
    """
    Trains a feedforward NN.
    """
    params = {
        "train_batch_size": 4096,
    }
    in_size = data["x_train"].shape[-1]
    out_size = data["y_train"].shape[-1]

    coil = CoIL(in_size, out_size)
    if args.restore:
        ckpt_path = (
            "./policies/" + args.scenario.lower() + "_" + args.goal.lower() + "_CoIL"
        )
        coil.load_state_dict(torch.load(ckpt_path))

    optimizer = optim.Adam(coil.parameters(), lr=args.lr)

    def train_step(x, y, u):
        ######### Your code starts here #########
        """
        We want to perform a single training step (for one batch):
        1. Make a forward pass through the model
        2. Calculate the loss for the output of the forward pass

        We want to compute the loss between y_est and y where
        - y_est is the output of the network for a batch of observations & goals,
        - y is the actions the expert took for the corresponding batch of observations & goals
        
        At the end your code should return the scalar loss value.
        HINT: Remember, you can penalize steering (0th dimension) and throttle (1st dimension) unequally
        """
        r = coil(x.to(device),u.to(device)).to(device)
        # l_func = nn.HuberLoss()
        # loss = l_func(r, y)
        steer_p, thro_pred = r.split(1, dim=1)
        steer_g, thro_g = y.split(1, dim=1)
        sloss = (steer_g-steer_p)**2
        tloss = (thro_g-thro_pred)**2
        loss = torch.mean((sloss+tloss))
        # y_est = coil(x, u)
        # # print(y_est.shape)
        # l_func = nn.HuberLoss()
        # loss = l_func(y_est, y)
        ########## Your code ends here ##########
        return loss

    dataset = TensorDataset(
        torch.Tensor(data["x_train"]),
        torch.Tensor(data["y_train"]),
        torch.Tensor(data["u_train"]),
    )
    dataloader = DataLoader(
        dataset, batch_size=params["train_batch_size"], shuffle=True
    )
    pbar = tqdm(range(args.epochs), desc="Training", unit="epoch")
    for epoch in pbar:
        epoch_loss = 0.0

        for x, y, u in dataloader:
            optimizer.zero_grad()
            batch_loss = train_step(x, y, u)
            batch_loss.backward()
            optimizer.step()
            epoch_loss += batch_loss.item()

        epoch_loss /= len(dataloader)

        # print(f"Epoch {epoch + 1}, Loss: {epoch_loss}")
        pbar.set_postfix(Loss=epoch_loss, The_epoch=epoch + 1)
    ckpt_path = (
        "./policies/" + args.scenario.lower() + "_" + args.goal.lower() + "_CoIL"
    )
    torch.save(coil.state_dict(), ckpt_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
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
        "--lr", type=float, help="learning rate for Adam optimizer", default=5e-3
    )

    parser.add_argument("--restore", action="store_true", default=False)
    args = parser.parse_args()
    args.goal = "all"

    maybe_makedirs("./policies")

    data = load_data(args)

    run_training(data, args)
