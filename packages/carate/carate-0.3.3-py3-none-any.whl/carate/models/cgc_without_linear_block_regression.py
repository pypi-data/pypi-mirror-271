"""
cgc_regression model is named after the structure of the graph neural network.
The graph neural network is structured with a convolutional , graph attention,
and another convolutional layer. The cgc_classificatin model was the model tested int the publication
Introducing CARATE: Finally speaking chemistry.
"""
import numpy as np
import torch
import torch.nn.functional as F
from torch.nn import Linear
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
        num_heads: int = 16,
        dropout_gat: float = 0.6,
        dropout_forward:float = 0.5,
        dropout_forward2:float = 0.5,
        *args,
        **kwargs,
    ) -> None:
        super(Net, self).__init__(
            dim=dim, num_classes=num_classes, num_features=num_features
        )
        self.factor = factor
        self.num_heads = num_heads
        self.dropout_gat = dropout_gat
        self.dropout_forward = dropout_forward
        self.dropout_forward2 = dropout_forward2

        self.conv1 = GraphConv(self.num_features, int(self.dim))
        self.gat1 = GATConv(self.dim, self.dim, dropout=self.dropout_gat)
        self.conv2 = GraphConv(self.dim, self.dim)

        self.fc1 = Linear(self.dim, self.num_classes)
        
    def forward(self, x: float, edge_index: int, batch: int, edge_weight=None) -> float:
        x = F.relu(self.conv1(x, edge_index, edge_weight))

        x = F.dropout(x, p=self.dropout_forward, training=self.training)
        x = F.relu(self.gat1(x, edge_index, edge_weight))
        x = F.relu(self.conv2(x, edge_index, edge_weight))
        x = global_add_pool(x, batch)
        x = self.fc1(x)

        return x

    def __str__(self): 
        return "cgc_regression_without_linear_layer"