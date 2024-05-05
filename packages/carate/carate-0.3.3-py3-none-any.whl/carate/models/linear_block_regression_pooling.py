"""
cgc_regression model is named after the structure of the graph neural network.
The graph neural network is structured with a convolutional , graph attention,
and another convolutional layer. The cgc_classificatin model was the model tested int the publication
Introducing CARATE: Finally speaking chemistry.
"""
import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Linear, BatchNorm1d
from torch_geometric.nn import global_add_pool, GraphConv, GATConv
import sklearn.metrics as metrics

import logging

from carate.models.base_model import Model


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="carate.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


class Net(Model):
    def __init__(
        self,
        dim: int,
        num_features: int,
        num_classes: int,
        factor:int, 
        dropout_forward:float =0.5,
        batch_size = 64,
        *args,
        **kwargs,
    ) -> None:
        super(Net, self).__init__(
            dim=dim, num_classes=num_classes, num_features=num_features
        )

        self.dropout_forward = dropout_forward
        self.fc1 = Linear(self.num_features, int(factor*self.dim))
        self.bin1 = BatchNorm1d(num_features= int(factor*self.dim))
        self.fc2 = Linear( int(factor*self.dim), self.num_classes)

    def forward(self, x: float, edge_index: int, batch: int, edge_weight=None) -> float:

        x = F.relu(self.fc1(x))
        x = F.dropout(x, p=self.dropout_forward, training=self.training)
        x = global_add_pool(x, batch)
        x = self.fc2(x)
        return x

    def __str__(self): 
        return "linear_block_regression"