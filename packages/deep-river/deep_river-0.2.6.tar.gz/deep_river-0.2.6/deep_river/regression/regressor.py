from typing import Callable, List, Type, Union

import pandas as pd
import torch
from river import base
from river.base.typing import RegTarget

from deep_river.base import DeepEstimator
from deep_river.utils.tensor_conversion import (
    df2tensor,
    dict2tensor,
    float2tensor,
)


class _TestModule(torch.nn.Module):
    def __init__(self, n_features):
        super().__init__()

        self.dense0 = torch.nn.Linear(n_features, 10)
        self.nonlin = torch.nn.ReLU()
        self.dropout = torch.nn.Dropout(0.5)
        self.dense1 = torch.nn.Linear(10, 5)
        self.output = torch.nn.Linear(5, 1)
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, X, **kwargs):
        X = self.nonlin(self.dense0(X))
        X = self.dropout(X)
        X = self.nonlin(self.dense1(X))
        X = self.softmax(self.output(X))
        return X


class Regressor(DeepEstimator, base.MiniBatchRegressor):
    """
    Wrapper for PyTorch regression models that enables
    compatibility with River.

    Parameters
    ----------
    module
        Torch Module that builds the autoencoder to be wrapped.
        The Module should accept parameter `n_features` so that the
        returned model's input shape can be determined based on the number
        of features in the initial training example.
    loss_fn
        Loss function to be used for training the wrapped model.
        Can be a loss function provided by `torch.nn.functional` or one of
        the following: 'mse', 'l1', 'cross_entropy', 'binary_crossentropy',
        'smooth_l1', 'kl_div'.
    optimizer_fn
        Optimizer to be used for training the wrapped model.
        Can be an optimizer class provided by `torch.optim` or one of the
        following: "adam", "adam_w", "sgd", "rmsprop", "lbfgs".
    lr
        Learning rate of the optimizer.
    device
        Device to run the wrapped model on. Can be "cpu" or "cuda".
    seed
        Random seed to be used for training the wrapped model.
    **kwargs
        Parameters to be passed to the `Module` or the `optimizer`.

    Examples
    --------

    """

    def __init__(
        self,
        module: Type[torch.nn.Module],
        loss_fn: Union[str, Callable] = "mse",
        optimizer_fn: Union[str, Callable] = "sgd",
        lr: float = 1e-3,
        device: str = "cpu",
        seed: int = 42,
        **kwargs,
    ):
        super().__init__(
            module=module,
            loss_fn=loss_fn,
            device=device,
            optimizer_fn=optimizer_fn,
            lr=lr,
            seed=seed,
            **kwargs,
        )

    @classmethod
    def _unit_test_params(cls):
        """
        Returns a dictionary of parameters to be used for unit
        testing the respective class.

        Yields
        -------
        dict
            Dictionary of parameters to be used for unit testing the
            respective class.
        """

        yield {
            "module": _TestModule,
            "loss_fn": "l1",
            "optimizer_fn": "sgd",
        }

    @classmethod
    def _unit_test_skips(cls) -> set:
        """
        Indicates which checks to skip during unit testing.
        Most estimators pass the full test suite. However, in some cases,
        some estimators might not
        be able to pass certain checks.
        Returns
        -------
        set
            Set of checks to skip during unit testing.
        """
        return {
            "check_shuffle_features_no_impact",
            "check_emerging_features",
            "check_disappearing_features",
            "check_predict_proba_one",
            "check_predict_proba_one_binary",
        }

    def learn_one(self, x: dict, y: RegTarget, **kwargs) -> "Regressor":
        """
        Performs one step of training with a single example.

        Parameters
        ----------
        x
            Input example.
        y
            Target value.

        Returns
        -------
        Regressor
            The regressor itself.
        """
        if not self.module_initialized:
            self.kwargs["n_features"] = len(x)
            self.initialize_module(**self.kwargs)
        x_t = dict2tensor(x, self.device)
        y_t = float2tensor(y, device=self.device)
        self._learn(x_t, y_t)
        return self

    def _learn(self, x: torch.Tensor, y: torch.Tensor):
        self.module.train()
        self.optimizer.zero_grad()
        y_pred = self.module(x)
        loss = self.loss_fn(y_pred, y)
        loss.backward()
        self.optimizer.step()

    def predict_one(self, x: dict) -> RegTarget:
        """
        Predicts the target value for a single example.

        Parameters
        ----------
        x
            Input example.

        Returns
        -------
        RegTarget
            Predicted target value.
        """
        if not self.module_initialized:
            self.kwargs["n_features"] = len(x)
            self.initialize_module(**self.kwargs)
        x_t = dict2tensor(x, self.device)
        self.module.eval()
        with torch.inference_mode():
            y_pred = self.module(x_t).item()
        return y_pred

    def learn_many(self, X: pd.DataFrame, y: pd.Series) -> "Regressor":
        """
        Performs one step of training with a batch of examples.

        Parameters
        ----------
        x
            Input examples.
        y
            Target values.

        Returns
        -------
        Regressor
            The regressor itself.
        """
        if not self.module_initialized:
            self.kwargs["n_features"] = len(X.columns)
            self.initialize_module(**self.kwargs)
        X_t = df2tensor(X, device=self.device)
        y_t = torch.tensor(
            y, device=self.device, dtype=torch.float32
        ).unsqueeze(1)
        self._learn(X_t, y_t)
        return self

    def predict_many(self, X: pd.DataFrame) -> List:
        """
        Predicts the target value for a batch of examples.

        Parameters
        ----------
        x
            Input examples.

        Returns
        -------
        List
            Predicted target values.
        """
        if not self.module_initialized:
            self.kwargs["n_features"] = len(X.columns)
            self.initialize_module(**self.kwargs)

        X = df2tensor(X, device=self.device)
        self.module.eval()
        with torch.inference_mode():
            y_preds = self.module(X).detach().squeeze().tolist()
        return y_preds
