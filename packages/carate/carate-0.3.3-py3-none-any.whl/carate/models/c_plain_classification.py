"""
cc_regression model is named after the structure of the graph neural network.
The graph neural network is structured with a convolutional,
and another convolutional layer. The cgc_classificatin model was the model tested int the publication
Introducing CARATE: Finally speaking chemistry.
"""
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Linear
from torch_geometric.nn import global_add_pool, GraphConv
import sklearn.metrics as metrics

import logging

from carate.models.base_model import Model


logger = logging.getLogger(__name__)


class Net(Model):
    def __init__(
        self, dim: int, num_features: int, num_classes: int, num_heads:int,  factor: int, dropout_forward:float =0.5,*args, **kwargs
    ) -> None:
        super(Net, self).__init__(
            dim=dim, num_classes=num_classes, num_features=num_features
        )

        self.factor = factor
        self.dropout_forward = dropout_forward

        self.conv1 = GraphConv(self.num_features, int(self.dim*factor))

        self.fc1 = Linear(int(self.dim*factor), self.num_classes)

    def forward(self, x: float, edge_index: int, batch: int, edge_weight=None) -> float:

        x = F.relu(self.conv1(x, edge_index, edge_weight))
        x = F.dropout(x, p=self.dropout_forward, training=self.training)
        x = global_add_pool(x, batch)
        x = self.fc1(x)

        x = torch.sigmoid(x)
        return x

    def __str__(self): 
        return "c_plain_classification"