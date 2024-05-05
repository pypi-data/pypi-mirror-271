"""
File for data loading from the standard datasets implemented in the pytorch_geometric #
library. The DataSet loader is implemented as a base class and other subclasses include loaders for standardized benchmarks
as well as custom datasets.

:author: Julian M. Kleber
"""
from typing import Type, Optional, List, Any
from abc import ABC, abstractclassmethod, abstractmethod

import numpy as np
import torch
import torch_geometric
from torch_geometric.loader import DataLoader
from torch_geometric.datasets import MoleculeNet, TUDataset

import rdkit as rdkit

from carate.default_interface import DefaultObject


import logging



logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="carate.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


class DatasetObject(ABC, DefaultObject, torch.utils.data.Dataset):
    """
    Interface for DataLoading objects
    """

    def __init__(
        self,
        dataset_name: str,
        dataset_save_path: str,
        test_ratio: int,
        batch_size: int,
        shuffle: bool,
        custom_size: Optional[int],
        normalize: Optional[bool] = False,
    ) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractclassmethod
    def load_data(
        self,
        dataset_name: str,
        dataset_save_path: str,
        test_ratio: int,
        batch_size: int,
        shuffle: bool,
        normalize:bool = False,
    ) -> None:
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def __repr__(self):
        raise NotImplementedError  # pragme: no cover
    

    def normalize(self, data_set: Any, num_classes: int):

       
        if len(data_set.y.shape) == 1: 
            mean = np.mean(data_set.y.numpy())
            min = np.min(data_set.y.numpy())
            max = np.max(data_set.y.numpy())
            span = max - min
            data_set.y = (data_set.y + span) / span
        else: 
            y = np.zeros((len(data_set), 1, num_classes))
            for i in range(len(data_set)):
                y[i, :, :] = data_set[i].y

            norm_factor = np.zeros((num_classes))
            for i in range(num_classes):
                #norm = np.linalg.norm(y[:, 0, i], ord=2)/(np.abs(np.max(y[:, 0, i])-np.min(y[:, 0, i])))
                #norm = np.min(y[:, 0, i]) / (np.abs(np.max(y[:, 0, i])-np.min(y[:, 0, i])))

                mean = np.mean(y[:, 0, i])
                min = np.min(y[:, 0, i])
                max = np.max(y[:, 0, i])
                span = max - min
                y[:, 0, i] = (y[:, 0, i] + span) / span
            for i in range(len(data_set)): 
                data_set[i].y =  y[i, :, :]
        return data_set


    def get_full_dataset(self, normalize=False): 
        if self.shuffle:
            dataset = self.DataSet(self.dataset_save_path, name=self.dataset_name).shuffle()
        else:
            dataset = self.DataSet(self.dataset_save_path, name=self.dataset_name)

        if normalize: 
            dataset = self.normalize(dataset, dataset.num_classes)
        else: 
            dataset = dataset

        return dataset


class StandardPytorchGeometricDataset(DatasetObject):
    DataSet: torch.utils.data.Dataset

    def load_data(
        self,
        dataset_name: str,
        test_ratio: int,
        dataset_save_path: str,
        batch_size: int = 64,
        shuffle: bool = True,
        custom_size: Optional[int] = None,
        normalize:bool = False,
    ) -> List[torch.utils.data.DataLoader | torch.utils.data.Dataset]:
        """
        The load_dataset function loads a standard dataset, splits it into a training and testing set,
        and returns the appropriate dataloaders for each. The test_ratio parameter specifies what percentage of
        the original dataset should be used as the testing set. The batch_size parameter specifies how many samples
        should be in each batch.

        :param path:str: Used to Define the path where the dataset is located.
        :param dataset_name:str: Used to Specify which dataset to load.
        :param test_ratio:int: Used to divide the dataset into a training and test set.
        :param batch_size:int: Used to set the batch size for training.
        :return: A train_loader and a test_loader.

        :doc-author: Julian M. Kleber
        """

        if shuffle:
            dataset = self.DataSet(dataset_save_path, name=dataset_name).shuffle()
        else:
            dataset = self.DataSet(dataset_save_path, name=dataset_name)

        if normalize: 
            print("Data normalized")
            dataset = self.normalize(dataset, dataset.num_classes)
        else: 
            print("Data not normalized")
            dataset = dataset

        test_dataset, train_dataset, test_loader, train_loader = self.make_split(
            dataset=dataset,
            test_ratio=test_ratio,
            batch_size=batch_size,
            custom_size=custom_size,
        )
        logging.info(
            self.dataset_name
            + " has num_features: "
            + str(train_dataset.num_features)
            + " and classes: "
            + str(train_dataset.num_classes)
        )
        return test_dataset, train_dataset, test_loader, train_loader, dataset

    def make_split(
        self,
        dataset: torch.utils.data.Dataset,
        test_ratio: int,
        batch_size: int,
        custom_size: Optional[int] = None,
    ) -> List[torch.utils.data.DataLoader | torch.utils.data.Dataset]:
        if custom_size == None:
            custom_size = len(dataset)

        dataset = dataset[: int(custom_size)]  # make sure the size is an int

        test_dataset = dataset[: len(dataset) // test_ratio]
        train_dataset = dataset[len(dataset) // test_ratio :]
        test_loader = DataLoader(test_dataset, batch_size=batch_size)
        train_loader = DataLoader(train_dataset, batch_size=batch_size)

        return [test_dataset, train_dataset, test_loader, train_loader]

    
    def get_full_dataset(self, normalize=False): 
        if self.shuffle:
            dataset = self.DataSet(self.dataset_save_path, name=self.dataset_name).shuffle()
        else:
            dataset = self.DataSet(self.dataset_save_path, name=self.dataset_name)

        if normalize: 
            dataset = self.normalize(dataset, dataset.num_classes)
        else: 
            dataset = dataset

        return dataset


class StandardDatasetMoleculeNet(StandardPytorchGeometricDataset):
    """
    Implementation of the Dataset interaface with focus on the models implemented in pytorch_geometric
    and provided by the MoleculeNet collection of datasets.
    """

    DataSet = MoleculeNet

    def __init__(
        self,
        dataset_save_path: str,
        dataset_name: str,
        test_ratio: int,
        batch_size: int,
        shuffle: bool = True,
        custom_size: Optional[int] = None,
        normalize:bool = False,
    ):
        """
        The __init__ function is called the constructor and is automatically called when you create a new instance of this class.
        The __init__ function allows us to set attributes that are specific to each object created from the class.
        In our case, we want each data_set object to have a path, dataset_name, test_ratio and batch size attribute.

        :param self: Used to Reference the object to which the function is applied.
        :param path:str: Used to Specify the path to the dataset.
        :param dataset_name:str: Used to Store the name of the data set.
        :param test_ratio:int: Used to Split the data set into a training and testing set.
        :param batch_size:int: Used to Set the batch size.
        :return: The object of the class.

        :doc-author: Julian M. Kleber
        """

        self.dataset_save_path = dataset_save_path
        self.dataset_name = dataset_name
        self.test_ratio = test_ratio
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __repr__(self):
        return "StandardMoleculeNet"


class StandardDatasetTUDataset(StandardPytorchGeometricDataset):
    """
    class for loading standard datasates from the TU Dataset collection implemented
    by PyTorch Geometric.

    author: Julian M. Kleber
    """

    DataSet = TUDataset

    def __init__(
        self,
        dataset_save_path: str,
        dataset_name: str,
        test_ratio: int,
        batch_size: int,
        shuffle: bool = True,
        normalize:bool = False,
    ):
        """
        The __init__ function is called the constructor and is automatically called when you create a new instance of this class.
        The __init__ function allows us to set attributes that are specific to each object created from the class.
        In our case, we want each data_set object to have a path, dataset_name, test_ratio and batch size attribute.

        :param self: Used to Reference the object to which the function is applied.
        :param path:str: Used to Specify the path to the dataset.
        :param dataset_name:str: Used to Store the name of the data set.
        :param test_ratio:int: Used to Split the data set into a training and testing set.
        :param batch_size:int: Used to Set the batch size.
        :return: The object of the class.

        :doc-author: Julian M. Kleber
        """

        self.dataset_save_path = dataset_save_path
        self.dataset_name = dataset_name
        self.test_ratio = test_ratio
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __repr__(self):
        return "StandardTUDataset"


class PyGZINC(StandardPytorchGeometricDataset): 

    def __init__(
        self,
        dataset_save_path: str,
        dataset_name: str,
        test_ratio: int,
        batch_size: int,
        shuffle: bool = True,
        custom_size: Optional[int] = None,
        normalize:bool = False,
    ):
        """
        The __init__ function is called the constructor and is automatically called when you create a new instance of this class.
        The __init__ function allows us to set attributes that are specific to each object created from the class.
        In our case, we want each data_set object to have a path, dataset_name, test_ratio and batch size attribute.

        :param self: Used to Reference the object to which the function is applied.
        :param path:str: Used to Specify the path to the dataset.
        :param dataset_name:str: Used to Store the name of the data set.
        :param test_ratio:int: Used to Split the data set into a training and testing set.
        :param batch_size:int: Used to Set the batch size.
        :return: The object of the class.

        :doc-author: Julian M. Kleber
        """

        self.dataset_save_path = dataset_save_path
        self.dataset_name = dataset_name
        self.test_ratio = test_ratio
        self.batch_size = batch_size
        self.shuffle = shuffle

    def load_data(
        self,
        dataset_name: str,
        test_ratio: int,
        dataset_save_path: str,
        batch_size: int = 64,
        shuffle: bool = True,
        custom_size: Optional[int] = None,
        normalize:bool = False,
    ) -> List[torch.utils.data.DataLoader | torch.utils.data.Dataset]:
        """
        The load_dataset function loads a standard dataset, splits it into a training and testing set,
        and returns the appropriate dataloaders for each. The test_ratio parameter specifies what percentage of
        the original dataset should be used as the testing set. The batch_size parameter specifies how many samples
        should be in each batch.

        :param path:str: Used to Define the path where the dataset is located.
        :param dataset_name:str: Used to specify which dataset to load.
        :param test_ratio:int: Used to divide the dataset into a training and test set.
        :param batch_size:int: Used to set the batch size for training.
        :return: A train_loader and a test_loader.

        :doc-author: Julian M. Kleber
        """
        from torch_geometric.datasets import ZINC

        if shuffle:
            dataset = ZINC(root=dataset_name).shuffle()
        else:
            dataset = ZINC(root=dataset_name).shuffle()

        if normalize: 
            dataset = self.normalize(dataset, dataset.num_classes)
        else: 
            dataset = dataset

        test_dataset, train_dataset, test_loader, train_loader = self.make_split(
            dataset=dataset,
            test_ratio=test_ratio,
            batch_size=batch_size,
            custom_size=custom_size,
        )
        logging.info(
            self.dataset_name
            + " has num_features: "
            + str(train_dataset.num_features)
            + " and classes: "
            + str(train_dataset.num_classes)
        )
        return test_dataset, train_dataset, test_loader, train_loader, dataset
    def __repr__(self):
        return "PyGStandardZINCDataset"
