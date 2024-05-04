from __future__ import annotations

from abc import ABC, abstractmethod
import copy
import warnings

import GPy
import numpy as np
import numpy.typing as npt
from GPy.kern import Kern

from boss.utils.typing import ArrayLike1D, ArrayLike2D
from boss.utils.arrays import shape_consistent_XY


class BaseModel(ABC):
    """
    Base class for surrogate models used in Bayesian optimization.
    """

    @property
    @abstractmethod
    def kernel(self):
        pass

    @property
    @abstractmethod
    def X(self) -> npt.NDArray:
        pass

    @property
    @abstractmethod
    def Y(self) -> npt.NDArray:
        pass

    @Y.setter
    def Y(self, _) -> None:
        raise AttributeError("Cannot set read-only attribute Y")

    @X.setter
    def X(self, _) -> None:
        raise AttributeError("Cannot set read-only attribute Y")

    @abstractmethod
    def add_data(self, X_new: npt.ArrayLike, Y_new: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset appending.
        """
        pass

    @abstractmethod
    def redefine_data(self, X: npt.ArrayLike, Y: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset overwriting.
        """
        pass

    @abstractmethod
    def get_best_xy(self) -> tuple[npt.NDArray, float]:
        """
        Returns the lowest energy acquisition (x, y).
        """
        pass

    @abstractmethod
    def predict(
        self, x: npt.ArrayLike, noise: bool = True, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance at point x, with or without
        model variance (noise) and normalisation (norm).
        """
        pass

    @abstractmethod
    def predict_grads(
        self, x: npt.ArrayLike, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns prediction mean and variance gradients with respect to input
        at point x, with or without normalisation (norm).
        """
        pass

    @abstractmethod
    def predict_mean_sd_grads(
        self, x: npt.ArrayLike, noise: bool = True, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray, npt.NDArray]:
        """
        Returns the model prediction mean, standard deviation and their
        gradients at point x, with or without model variance (noise) and
        normalisation (norm).
        """
        pass

    @abstractmethod
    def predict_mean_grad(
        self, x: npt.ArrayLike, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model mean and its gradient at point x, with or without
        normalisation (norm).
        """
        pass

    @abstractmethod
    def estimate_num_local_minima(self, search_bounds: ArrayLike2D) -> int:
        """
        Returns estimated number of local minima within bounds, calculated
        based on model properties.
        """
        pass

    @abstractmethod
    def get_all_params(self) -> dict[str, float | npt.ArrayLike]:
        """
        Returns model parameters as a dictionary.
        """
        pass

    @abstractmethod
    def get_unfixed_params(self) -> npt.NDArray:
        """
        Returns the unfixed parameters of the model in an array.
        """
        pass

    @abstractmethod
    def sample_unfixed_params(self, num_samples: int):
        """
        Sample unfixed model parameters.
        """
        pass

    @abstractmethod
    def set_unfixed_params(self, params: npt.NDArray) -> None:
        """
        Sets the unfixed parameters of the model to given values.
        """
        pass

    @abstractmethod
    def optimize(self) -> None:
        """
        Updates unfixed model parameters.
        """
        pass


class STModel(BaseModel):
    """
    Functionality for creating, refitting and optimizing a GP model
    """

    def __init__(
        self,
        kernel: Kern,
        X: npt.ArrayLike | None = None,
        Y: npt.ArrayLike | None = None,
        noise: float = 1e-12,
        ynorm: bool = False,
    ) -> None:
        """
        Initializes the STModel class.
        """
        # scale normalisation is not used unless ynorm is true:
        self.use_norm = ynorm
        self._kernel = kernel
        self._noise = noise
        self._model = None
        self.normmean = 0.0
        self.normsd = 1.0
        if X is not None and Y is not None:
            self.redefine_data(X, Y)

    @property
    def kernel(self) -> Kern:
        return self._kernel

    @property
    def dim(self) -> int:
        return self._kernel.input_dim

    @property
    def X(self) -> npt.NDArray:
        if self._model is not None:
            return self._model.X
        else:
            return np.empty((0, self.dim), dtype=float)

    @property
    def Y(self) -> npt.NDArray:
        if self._model is not None:
            return self._model.Y * self.normsd + self.normmean
        else:
            return np.empty((0, 1), dtype=float)

    def __deepcopy__(self, memo: dict) -> STModel:
        if self._model is None:
            return copy.deepcopy(self)
        else:
            cls = self.__class__
            model_copy = cls.__new__(cls)
            memo[id(self)] = model_copy
            for key, val in self.__dict__.items():
                # A GPy kernel object attached to a model can't be deepcopied in the
                # usual way due to a bug so we have to use the kernel's custom copy method.
                if key == "_kernel":
                    setattr(model_copy, key, val.copy())
                else:
                    setattr(model_copy, key, copy.deepcopy(val, memo))
            return model_copy

    def _init_wrapped_model(self, X: npt.NDArray, Y: npt.NDArray) -> None:
        # normalise observation mean:
        self.normmean = np.mean(Y)
        # previous boss code used normsd to normalise observation variance:
        # if self.ynorm: self.normsd = np.std(Y)
        # current version normalises observation range:
        self.normsd = np.ptp(Y) if self.use_norm else 1.0
        # note that the choice betweeen variance or range normalisation needs
        # to be taken into account when we set kernel parameter priors
        # normalised data:
        Y_norm = (Y - self.normmean) / self.normsd
        # initialise model
        self._model = GPy.models.GPRegression(
            X, Y_norm, kernel=self._kernel, noise_var=self._noise
        )
        self._model.likelihood.fix()
        self._kernel = self._model.kern

    def add_data(self, X_new: npt.ArrayLike, Y_new: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset appending.
        """
        X_new, Y_new = shape_consistent_XY(X_new, Y_new, self.dim)
        X = np.vstack([self.X, X_new])
        Y = np.vstack([self.Y, Y_new])
        self.redefine_data(X, Y)

    def redefine_data(self, X: npt.ArrayLike, Y: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset overwriting.
        """
        # update normalisation
        X, Y = shape_consistent_XY(X, Y, self.dim)
        if self._model is None:
            self._init_wrapped_model(X, Y)
        else:
            self.normmean = np.mean(Y)
            if self.use_norm:
                self.normsd = np.ptp(Y)
            # update model
            Y_norm = (Y - self.normmean) / self.normsd
            self._model.set_XY(X, Y_norm)

    def get_best_xy(self) -> tuple[npt.NDArray, float]:
        """
        Returns the lowest energy acquisition (x, y).
        """
        x_best = np.array(self.X[np.argmin(self.Y)])
        y_best = np.min(self.Y)
        return x_best, y_best

    def predict(
        self, x: npt.ArrayLike, noise: bool = True, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance at point x, with or without
        model variance (noise).
        """
        m, v = self._model.predict(np.atleast_2d(x), include_likelihood=noise)
        v = np.clip(v, 1e-12, np.inf)
        if norm:
            return m, v
        return m * self.normsd + self.normmean, v * (self.normsd**2)

    def predict_grads(
        self, x: npt.ArrayLike, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance gradients with respect to
        input at point x.
        """
        dmdx, dvdx = self._model.predictive_gradients(np.atleast_2d(x))
        if norm:
            return dmdx, dvdx
        return dmdx * self.normsd, dvdx * (self.normsd**2)

    def predict_mean_sd_grads(
        self, x: npt.ArrayLike, noise: bool = True, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray, npt.NDArray]:
        """
        Returns the model prediction mean, standard deviation and their
        gradients at point x, with or without model variance (noise).

        This method is a wrapper used primarily during calculations
        of acquisition functions and their derivatives.
        """
        m, v = self.predict(np.atleast_2d(x), noise=noise, norm=norm)
        dmdx, dvdx = self.predict_grads(np.atleast_2d(x), norm=norm)
        dmdx = dmdx[:, :, 0]
        dsdx = dvdx / (2 * np.sqrt(v))
        return m, np.sqrt(v), dmdx, dsdx

    def predict_mean_grad(
        self, x: npt.ArrayLike, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """Returns model mean and its gradient at point x.

        This method is a wrapper used primarily when the mean function
        is minimized in order to obtain a global minimum prediction.
        """
        m, _ = self.predict(np.atleast_2d(x), norm=norm)
        dmdx, _ = self.predict_grads(np.atleast_2d(x), norm=norm)
        return m, dmdx

    def estimate_num_local_minima(self, search_bounds: ArrayLike2D) -> int:
        """
        Returns estimated number of local minima within bounds, calculated
        based on model properties.
        """
        # For the ith dimension, the number of local minima along a slice
        # is approximately n(i) = boundlength(i)/(2*lengthscale(i)). Note
        # that periodic kernels operate on normalised distances: distance
        # between inputs that are period(i)/2 apart is 1. To get the total
        # number of minima for all of the search space, multiply together
        # n(i) over all i.
        numpts = 1
        ks = self._model.kern.parameters if self.dim > 1 else [self._model.kern]
        for bounds, kern in zip(search_bounds, ks):
            if hasattr(kern, "period"):
                bound_distance = (bounds[1] - bounds[0]) / float(kern.period)
            else:
                bound_distance = (bounds[1] - bounds[0]) / 2
            numpts *= max(1, bound_distance / float(kern.lengthscale))
        return int(numpts)

    # model parameters:

    def get_all_params(self) -> dict[str, float | list]:
        """
        Returns model parameters as a dictionary with entries:
        noise, variance, lengthscales, periods
        where the last two are 1D lists. There exists a period only for those
        dimensions which are using a periodic kernel.
        """
        noise = float(self._model.likelihood.variance)
        sigma = float(self._model.kern.param_array[0])
        lss = []
        pers = []
        ks = self._model.kern.parameters if self.dim > 1 else [self._model.kern]
        for kern in ks:
            lss.append(float(kern.lengthscale))
            if hasattr(kern, "period"):
                pers.append(float(kern.period))

        # the variables are returned in a dict:
        params = {}
        params["noise"] = noise
        params["variance"] = sigma
        params["lengthscales"] = lss
        params["periods"] = pers

        return params

    def get_unfixed_params(self) -> npt.NDArray:
        """
        Returns the unfixed parameters of the model in an array.
        """
        return np.array(self._model.unfixed_param_array.copy()).astype(float)

    def sample_unfixed_params(self, num_samples: int) -> npt.NDArray:
        """
        Sample unfixed model parameters.
        """
        hmc = GPy.inference.mcmc.HMC(self._model)
        burnin = hmc.sample(int(num_samples * 0.33))
        return hmc.sample(num_samples)

    def set_unfixed_params(self, params: npt.NDArray) -> None:
        """
        Sets the unfixed parameters of the model to given values.
        """
        self._model[self._model._fixes_] = params
        self._model.parameters_changed()

    def optimize(self, restarts: int = 1) -> None:
        """
        Updates the model hyperparameters by maximizing marginal likelihood.
        """
        self._model.optimization_runs = []
        if restarts == 1:
            self._model.optimize()
        else:
            self._model.optimize_restarts(
                num_restarts=restarts, verbose=False, messages=False
            )


class GradientModel(STModel):
    """
    Functionality for creating, refitting and optimizing a GP model with
    gradient observations.

    The GradientModel utilizes the GPy MultioutputGP model class, which allows
    for multiple input and output channels. We can include observed gradient
    data in GPR by defining separate channels for partial derivatives, in
    addition to the main function value channel.

    The DiffKern kernel computes cross-covariances between channels.
    """

    def __init__(
        self,
        kernel: Kern,
        X: npt.ArrayLike | None = None,
        Y_dY: npt.ArrayLike | None = None,
        noise: float = 1e-12,
        ynorm: bool = False,
    ) -> None:
        """
        Initializes the GradientModel class.
        """
        # normalization
        self.use_norm = ynorm
        self._kernel = kernel
        self._noise = noise
        self._model = None
        self._dim = kernel.input_dim
        self.normmean = 0.0
        self.normsd = 1.0
        if X is not None and Y_dY is not None:
            self.redefine_data(X, Y_dY)

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def X(self) -> npt.NDArray:
        if self._model is not None:
            X_multioutput = self._model.X[:, :-1]
            output_index = self._model.X[:, -1]
            return X_multioutput[np.where(output_index == 0)[0]]
        else:
            return np.empty((0, self.dim))

    @property
    def Y(self) -> npt.NDArray:
        if self._model is not None:
            Y_multioutput = self._model.Y
            output_index = self._model.X[:, -1]
            Y_norm = Y_multioutput[np.where(output_index == 0)[0]]
            Y = Y_norm * self.normsd + self.normmean
            dY = np.empty((len(Y), self.dim), dtype=float)
            for d in range(self.dim):
                dY[:, d, None] = Y_multioutput[np.where(output_index == d + 1)[0]]
            return np.concatenate((Y, dY), axis=1)
        else:
            return np.empty((0, self.dim + 1))

    def _init_wrapped_model(self, X: npt.NDArray, Y_dY: npt.NDArray) -> None:
        X_list = [X] * (self.dim + 1)

        # observations
        Y, dY = Y_dY[:, :1], Y_dY[:, 1:]
        # normalization
        self.normmean = np.mean(Y)
        self.normsd = np.ptp(Y) if self.use_norm else 1
        Y_norm = (Y - self.normmean) / self.normsd
        # output channels
        Y_list = [Y_norm] + [dY[:, d, None] for d in range(self.dim)]

        # the kernel is accompanied with a DiffKern for each partial derivative.
        kernel_list = [self._kernel]
        kernel_list += [GPy.kern.DiffKern(self._kernel, d) for d in range(self.dim)]

        # noise is given to the likelihood.
        likelihood = GPy.likelihoods.Gaussian(variance=self._noise)
        likelihood_list = [likelihood] * (self.dim + 1)

        # initialize model
        self._model = GPy.models.MultioutputGP(
            X_list=X_list,
            Y_list=Y_list,
            kernel_list=kernel_list,
            likelihood_list=likelihood_list,
        )
        self._model.likelihood.fix()
        self._kernel = self._model.kern

    def add_data(self, X_new: npt.ArrayLike, Y_dY_new: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset appending.
        """
        # construct new unnormalized dataset
        X_new, Y_dY_new = shape_consistent_XY(X_new, Y_dY_new, self.dim, ygrad=True)
        X = np.vstack([self.X, X_new])
        Y_dY = np.vstack([self.Y, Y_dY_new])
        # update model
        self.redefine_data(X, Y_dY)

    def redefine_data(self, X: npt.ArrayLike, Y_dY: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset overwriting.
        """
        X, Y_dY = shape_consistent_XY(X, Y_dY, self.dim, ygrad=True)
        if self._model is None:
            self._init_wrapped_model(X, Y_dY)
            return

        Y, dY = Y_dY[:, :1], Y_dY[:, 1:]
        # update normalization
        self.normmean = np.mean(Y)
        if self.use_norm:
            self.normsd = np.ptp(Y)
        # update model
        Y_norm = (Y - self.normmean) / self.normsd
        X_list = [X] * (self.dim + 1)
        Y_list = [Y_norm] + [dY[:, d, None] for d in range(self.dim)]
        self._model.set_XY(X_list, Y_list)

    def get_best_xy(self) -> tuple[npt.NDArray, float]:
        """
        Returns the lowest energy acquisition (x, y).
        """
        x_best = np.array(self.X[np.argmin(self.Y[:, 0])])
        y_best = np.min(self.Y[:, 0])
        return x_best, y_best

    def predict(
        self, x: npt.ArrayLike, noise: bool = True, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance at point x, with or without
        model variance (noise) and normalisation (norm).
        """
        m, v = self._model.predict([np.atleast_2d(x)], include_likelihood=noise)
        v = np.clip(v, 1e-12, np.inf)
        if norm:
            return m, v
        return m * self.normsd + self.normmean, v * (self.normsd**2)

    def predict_grads(
        self, x: npt.ArrayLike, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance gradients with respect to
        input at point x, with or without normalisation (norm).
        """
        dmdx, dvdx = self._model.predictive_gradients([np.atleast_2d(x)])
        if norm:
            return dmdx[:, :, None], dvdx
        return (dmdx * self.normsd)[:, :, None], dvdx * (self.normsd**2)

    def estimate_num_local_minima(self, search_bounds: ArrayLike2D) -> int:
        """
        Returns estimated number of local minima within bounds, calculated
        based on model properties.
        """
        # For the ith dimension, the number of local minima along a slice
        # is approximately n(i) = boundlength(i)/(2*lengthscale(i)). Note
        # that periodic kernels operate on normalised distances: distance
        # between inputs that are period(i)/2 apart is 1. To get the total
        # number of minima for all of the search space, multiply together
        # n(i) over all i.
        numpts = 1

        # For the GradientModel, the self.model.kern is the
        # MultioutputDerivativeKern. If self.dim > 1, the Prod kernel which
        # contains the individual kernels is located by
        # self.model.kern.parts[0]. If self.dim == 1, the individual kernel is
        # located by self.model.kern.parts.
        if self.dim > 1:
            ks = self._model.kern.parts[0].parts
        else:
            ks = self._model.kern.parts
        for bounds, kern in zip(search_bounds, ks):
            if hasattr(kern, "period"):
                bound_distance = (bounds[1] - bounds[0]) / float(kern.period)
            else:
                bound_distance = (bounds[1] - bounds[0]) / 2
            numpts *= max(1, bound_distance / float(kern.lengthscale))
        return int(numpts)

    def get_all_params(self) -> dict[str, float | list]:
        """
        Returns model parameters as a dictionary with entries::
        noise, variance, lengthscales, periods
        where the last two are 1D lists. There exists a period only for those
        dimensions which are using a periodic kernel.
        """
        # The MultioutputGP model can contain multiple likelihoods
        # We only use one, and access the noise through model.likelihood[0]
        noise = self._model.likelihood[0]
        sigma = float(self._model.kern.param_array[0])
        lss = []
        pers = []
        # For the GradientModel, the self.model.kern is the
        # MultioutputDerivativeKern. If self.dim > 1, the Prod kernel which
        # contains the individual kernels is located by
        # self.model.kern.parts[0]. If self.dim == 1, the individual kernel is
        # located by self.model.kern.parts.
        if self.dim > 1:
            ks = self._model.kern.parts[0].parts
        else:
            ks = self._model.kern.parts
        for kern in ks:
            lss.append(float(kern.lengthscale))
            if hasattr(kern, "period"):
                pers.append(float(kern.period))

        # the variables are returned in a dict:
        params = {}
        params["noise"] = noise
        params["variance"] = sigma
        params["lengthscales"] = lss
        params["periods"] = pers

        return params


class MTModel(STModel):
    """
    Functionality for creating, refitting and optimizing a multi-task GP model.
    """

    def __init__(
        self,
        kernel: Kern,
        X: npt.ArrayLike | None = None,
        Y: npt.ArrayLike | None = None,
        noise: float = 1e-12,
        ynorm: bool = False,
    ) -> None:
        """
        Initializes the MTModel class.
        """
        self._kernel = kernel
        self.num_tasks = kernel.parameters[-1].output_dim
        self.use_norm = ynorm
        self._noise = noise
        self.normmean = [0.0] * self.num_tasks
        self.normsd = [1.0] * self.num_tasks
        self._model = None
        if X is not None and Y is not None:
            self.redefine_data(X, Y)

    def _init_wrapped_model(self, X: npt.NDArray, Y: npt.NDArray) -> None:
        # task indices
        inds = np.squeeze(X[:, -1]).astype(int)
        self.check_task_indices(inds)
        # observations list
        XX = [X[inds == index, :-1] for index in range(self.num_tasks)]
        YY = [Y[inds == index] for index in range(self.num_tasks)]
        # normalise observation mean
        self.normmean = [np.mean(Y) for Y in YY]
        # scale normalisation is not used unless ynorm is true
        self.normsd = [1] * self.num_tasks
        if self.use_norm:
            self.normsd = [np.ptp(Y) for Y in YY]
        # normalised observation list:
        YY_norm = [(Y - m) / s for Y, m, s in zip(YY, self.normmean, self.normsd)]
        # initialise model
        self._model = GPy.models.GPCoregionalizedRegression(
            XX, YY_norm, kernel=self._kernel
        )
        self._model.mixed_noise.constrain_fixed(self._noise)
        self._kernel = self._model.kern

    def get_X(self, index: int | None = None) -> npt.NDArray:
        """
        Returns observed X.
        """
        if self._model is not None:
            if index is None:
                return self._model.X
            else:
                return self._model.X[self.inds == index, :-1]
        else:
            return np.empty((0, self.dim), dtype=float)

    def get_Y(self, index: int | None = None) -> npt.NDArray:
        """
        Returns observed Y.
        """
        if self._model is not None:
            if index is None:
                Y = self._model.Y.copy()
                for index in range(self.num_tasks):
                    Y[self.inds == index] *= self.normsd[index]
                    Y[self.inds == index] += self.normmean[index]
                return Y
            else:
                Y_norm = self._model.Y[self.inds == index]
                return Y_norm * self.normsd[index] + self.normmean[index]
        else:
            return np.empty((0, 1), dtype=float)

    @property
    def X(self) -> npt.NDArray:
        return self.get_X()

    @property
    def Y(self) -> npt.NDArray:
        return self.get_Y()

    @property
    def inds(self) -> npt.NDArray:
        return self._model.X[:, -1].astype(int)

    def add_data(self, X_new: npt.ArrayLike, Y_new: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset appending.
        """
        X_new, Y_new = shape_consistent_XY(X_new, Y_new, self.dim)
        if self._model is None:
            self._init_wrapped_model(X_new, Y_new)
            return

        inds_new = X_new[:, -1].astype(int)

        # construct new datasets
        X = np.vstack([self.X, X_new])
        Y = np.vstack([self.Y, Y_new])

        inds = X[:, -1].astype(int)

        # update normalisation
        Y_norm = np.vstack([self._model.Y, np.zeros_like(Y_new)])
        for i in np.unique(inds_new):
            self.normmean[i] = np.mean(Y[inds == i])
            if self.use_norm:
                self.normsd[i] = np.ptp(Y[inds == i])
            Y_norm[inds == i] = (Y[inds == i] - self.normmean[i]) / self.normsd[i]

        # update model
        self._model.Y_metadata = {"output_index": inds}
        self._model.set_XY(X, Y_norm)

    def redefine_data(self, X: npt.ArrayLike, Y: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset overwriting.
        """
        X, Y = shape_consistent_XY(X, Y, self.dim)
        if self._model is None:
            self._init_wrapped_model(X, Y)
            return

        inds = X[:, -1].astype(int)
        self.check_task_indices(inds)

        # update normalisation
        Y_norm = np.zeros_like(Y)
        for i in range(self.num_tasks):
            self.normmean[i] = np.mean(Y[inds == i])
            if self.use_norm:
                self.normsd[i] = np.ptp(Y[inds == i])
            Y_norm[inds == i] = (Y[inds == i] - self.normmean[i]) / self.normsd[i]

        # update model
        self._model.Y_metadata = {"output_index": inds}
        self._model.set_XY(X, Y_norm)

    def get_best_xy(self, index: int | None = None) -> tuple[npt.NDArray, float]:
        """
        Returns the lowest energy acquisitions (x, y).
        """
        if index is None:
            x_best = []
            y_best = []
            for index in range(self.num_tasks):
                Y_i = self.get_Y(index)
                x_best.append(np.append(self.get_X(index)[np.argmin(Y_i)], index))
                y_best.append(np.min(Y_i))
        else:
            Y_i = self.get_Y(index)
            x_best = np.array(self.get_X(index)[np.argmin(Y_i)])
            y_best = np.min(Y_i)
        return x_best, y_best

    def check_task_indices(self, inds: npt.NDArray) -> None:
        """
        Raises an error if all tasks are not included in the index list or if
        the list includes more tasks than expected.
        """
        counts = np.bincount(inds, minlength=self.num_tasks)
        if not np.all(counts > 0):
            raise ValueError("All tasks must be represented in the dataset.")

        num_tasks = max(inds) + 1
        if num_tasks > self.num_tasks:
            raise ValueError(
                f"Received a dataset with {num_tasks} tasks. "
                f"Expected {self.num_tasks} tasks."
            )

    def extend_input(self, x: npt.ArrayLike, index: ArrayLike1D) -> npt.NDArray:
        """
        Returns x extended with task index.
        """
        x = np.atleast_2d(x)
        inds = np.full((len(x), 1), np.array(index).reshape(-1, 1))
        x = np.hstack((x, inds))
        return x

    def predict(
        self,
        x: npt.ArrayLike,
        index: ArrayLike1D | None = None,
        noise: bool = True,
        norm: bool = False,
    ):
        """
        Returns model prediction mean and variance at point x, with or without
        model variance (noise) and normalisation (norm).

        Task index can be included in the input x or provided with index.
        """
        # extend x with task index if needed
        x = np.atleast_2d(x)
        if index is not None:
            x = self.extend_input(x, index)
        # build metadata
        inds = x[:, -1].astype(int)
        meta = {"output_index": inds}
        # predict output
        m, v = self._model.predict(x, Y_metadata=meta, include_likelihood=noise)
        v = np.clip(v, 1e-12, np.inf)
        if norm:
            return m, v
        # remove normalisation
        for i in np.unique(inds):
            m[inds == i] = m[inds == i] * self.normsd[i] + self.normmean[i]
            v[inds == i] = v[inds == i] * self.normsd[i] ** 2
        return m, v

    def predict_grads(
        self, x: npt.ArrayLike, index: ArrayLike1D | None = None, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance gradients with respect to
        input at point x, with or without normalisation (norm).

        Task index can be included in the input x or provided with index.
        """
        # extend x with task index if needed
        x = np.atleast_2d(x)
        if index is not None:
            x = self.extend_input(x, index)
        # predictive gradients
        dmdx, dvdx = self._model.predictive_gradients(np.atleast_2d(x))
        if norm:
            return dmdx, dvdx
        # remove normalisation
        inds = x[:, -1].astype(int)
        for i in np.unique(inds):
            dmdx[inds == i] *= self.normsd[i]
            dvdx[inds == i] *= self.normsd[i] ** 2
        return dmdx, dvdx

    def predict_mean_sd_grads(
        self,
        x: npt.ArrayLike,
        index: ArrayLike1D | None = None,
        noise: bool = True,
        norm: bool = True,
    ) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray, npt.NDArray]:
        """
        Returns the model prediction mean, standard deviation and their
        gradients at point x, with or without model variance (noise) and
        normalisation (norm).

        Task index can be included in the input x or provided with index.
        """
        m, v = self.predict(x, index=index, noise=noise, norm=norm)
        dmdx, dvdx = self.predict_grads(np.atleast_2d(x), index=index, norm=norm)
        dmdx = dmdx[:, :, 0]
        dsdx = dvdx / (2 * np.sqrt(v))
        return m, np.sqrt(v), dmdx, dsdx

    def predict_mean_grad(
        self, x: npt.ArrayLike, index: ArrayLike1D | None = None, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model mean and its gradient at point x, with or without
        normalisation (norm).

        Task index can be included in the input x or provided with index.
        """
        m, _ = self.predict(x, index=index, norm=norm)
        dmdx, _ = self.predict_grads(x, index=index, norm=norm)
        return m, dmdx

    def estimate_num_local_minima(self, search_bounds: ArrayLike2D) -> int:
        """
        Returns estimated number of local minima calculated based on model
        properties.
        """
        # For the ith dimension, the number of local minima along a slice
        # is approximately n(i) = boundlength(i)/(2*lengthscale(i)). Note
        # that periodic kernels operate on normalised distances: distance
        # between inputs that are period(i)/2 apart is 1. To get the total
        # number of minima for all of the search space, multiply together
        # n(i) over all i.
        numpts = 1

        # get baseline kernel parameters (exclude coregionalisation kernel)
        ks = self._model.kern.parameters[:-1]
        for bounds, kern in zip(search_bounds, ks):
            if hasattr(kern, "period"):
                bound_distance = (bounds[1] - bounds[0]) / float(kern.period)
            else:
                bound_distance = (bounds[1] - bounds[0]) / 2
            numpts *= max(1, bound_distance / float(kern.lengthscale))
        return int(numpts)

    def predict_task_covariance(self, x: npt.ArrayLike) -> npt.NDArray:
        """
        Return predictive covariance between tasks at point x.
        """
        inds = np.arange(self.num_tasks)
        x = np.squeeze(x)[:-1]
        x_list = np.vstack([self.extend_input(x, i) for i in inds])
        meta = {"output_index": inds.astype(int)}
        _, cov = self._model.predict(x_list, Y_metadata=meta, full_cov=True)
        return np.outer(self.normsd, self.normsd) * cov

    def get_all_params(self) -> dict[str, float | list]:
        """
        Returns model parameters as a dictionary with entries:
        noise, lengthscales, periods, kappa, W
        There exists a period only for those dimensions which are using a
        periodic kernel.
        """
        # likelihood params
        ll = self._model.likelihood.likelihoods_list
        noise = [float(likelihood.variance) for likelihood in ll]
        # kernel params
        lss = []
        pers = []
        # get baseline kernel parameters (exclude coregionalisation kernel)
        ks = self._model.kern.parameters[:-1]
        for kern in ks:
            lss.append(float(kern.lengthscale))
            if hasattr(kern, "period"):
                pers.append(float(kern.period))
        # coregionalisation params
        kappa = np.array(self._model.kern.parameters[-1].kappa).reshape(1, -1)
        W = np.array(self._model.kern.parameters[-1].W).reshape(1, -1)

        # the variables are returned in a dict:
        params = {}
        params["noise"] = noise
        params["lengthscales"] = lss
        params["periods"] = pers
        params["kappa"] = kappa
        params["W"] = W

        return params

    def get_task_covariance(self) -> npt.NDArray:
        """
        Returns estimated task covariance matrix.
        """
        kappa = np.array(self._model.kern.parameters[-1].kappa)
        W = np.array(self._model.kern.parameters[-1].W)
        cov = np.outer(W, W) + np.diag(kappa)
        return np.outer(self.normsd, self.normsd) * cov


class HeteroscedasticModel(STModel):
    """
    Functionality for creating, refitting and optimizing a Heteroscedastic GP model
    """

    def __init__(
        self,
        kernel,
        hsc_noise,
        X: npt.ArrayLike | None = None,
        Y: npt.ArrayLike | None = None,
        hsc_args: dict = None,
        noise_init: list = [1e-12],
        ynorm: bool = False,
    ) -> None:
        """
        Initializes the HeteroscedasticModel class.
        """
        # scale normalisation is not used unless ynorm is true:
        self.use_norm = ynorm
        self._kernel = kernel
        self._model = None
        self.normmean = 0.0
        self.normsd = 1.0
        self.hsc_noise = hsc_noise
        self.hsc_args = hsc_args
        self.noise_init = noise_init

        if X is not None and Y is not None:
            self._init_wrapped_model(X, Y)

    def _init_wrapped_model(self, X: npt.NDArray, Y: npt.NDArray) -> None:
        """
        Initializes the heteroscedastic model.
        """
        # normalise observation mean:
        self.normmean = np.mean(Y)
        # previous boss code used normsd to normalise observation variance:
        # if self.ynorm: self.normsd = np.std(Y)
        # current version normalises observation range:
        self.normsd = np.ptp(Y) if self.use_norm else 1.0
        # note that the choice betweeen variance or range normalisation needs
        # to be taken into account when we set kernel parameter priors
        # normalised data:
        Y_norm = (Y - self.normmean) / self.normsd
        # set Y_metadata
        Ny = Y.shape[0]
        Y_metadata = {"output_index": np.arange(Ny)[:, None]}
        # initalise model
        self._model = GPy.models.GPHeteroscedasticRegression(
            X, Y_norm, kernel=self._kernel, Y_metadata=Y_metadata
        )
        # for the first hyperparameter optimization the noise
        # is given pointwise by the noise_init keyword
        # if only one noise value is given, use constant noise
        if len(self.noise_init) == 1:
            noise_array = np.reshape(
                self.noise_init[0] * np.ones(X.shape[0]), (X.shape[0], -1)
            )
        else:
            noise_array = np.reshape(self.noise_init, (X.shape[0], -1))
        # set the noise parameters to the error in Y
        self._model[".*het_Gauss.variance"] = noise_array
        # fix the noise term
        self._model.het_Gauss.variance.fix()
        self._model.optimize()
        # lengthscales can be used for noise estimation
        # check that kernel lengthscales can be accessed
        lengthscale = None
        if hasattr(self._model.kern, "lengthscale"):
            lengthscale = [self._model.kern.lengthscale]
        elif hasattr(self._model.kern, "parts"):
            lengthscale = []
            for part in self._model.kern.parts:
                if hasattr(part, "lengthscale"):
                    lengthscale.append(part.lengthscale)
                else:
                    lengthscale.append(None)
                    warnings.warn(
                        "Kernel doesn't contain lengthscales in kern or kern.parts."
                    )
        else:
            warnings.warn(
                "Kernel doesn't contain lengthscales in kern or kern.parts."
            )
        # estimate noise using the user-defined function
        noise_array = self.compute_hsc_noise(X, Y, Y_norm, lengthscale)
        self._model[".*het_Gauss.variance"] = noise_array
        self._model.het_Gauss.variance.fix()
        self._kernel = self._model.kern

    def compute_hsc_noise(
        self,
        X: npt.NDArray,
        Y: npt.NDArray,
        Y_norm: npt.NDArray,
        lengthscale: npt.NDArray,
    ) -> npt.NDArray:
        """
        Returns the noise estimate for each point X using the user-defined noise function.
        """
        # if using normalization estimate errors based on normalized data
        if self.use_norm:
            noise_array = self.hsc_noise(
                self.hsc_args, Y=Y_norm, X=X, lengthscale=lengthscale, model=self
            )
        else:
            noise_array = self.hsc_noise(
                self.hsc_args, Y=Y, X=X, lengthscale=lengthscale, model=self
            )
        return noise_array

    def add_data(self, X_new: npt.ArrayLike, Y_new: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset appending.
        """
        X_new, Y_new = shape_consistent_XY(X_new, Y_new, self.dim)
        X = np.vstack([self.X, X_new])
        Y = np.vstack([self.Y, Y_new])
        self.redefine_data(X, Y)

    def redefine_data(self, X: npt.ArrayLike, Y: npt.ArrayLike) -> None:
        """
        Updates the model evidence (observations) dataset overwriting.
        """
        # update normalisation
        X, Y = shape_consistent_XY(X, Y, self.dim)
        if self._model is None:
            self._init_wrapped_model(X, Y)
        else:
            self.normmean = np.mean(Y)
            self.normsd = np.ptp(Y) if self.use_norm else 1
            Y_norm = (Y - self.normmean) / self.normsd
            # set Y_metadata
            Ny = Y.shape[0]
            Y_metadata = {"output_index": np.arange(Ny)[:, None]}
            # lengthscales can be used for noise estimation
            # check that kernel lengthscales can be accessed
            lengthscale_prev = None
            if hasattr(self._model.kern, "lengthscale"):
                lengthscale_prev = [self._model.kern.lengthscale]
            elif hasattr(self._model.kern, "parts"):
                lengthscale_prev = []
                for part in self._model.kern.parts:
                    if hasattr(part, "lengthscale"):
                        lengthscale_prev.append(part.lengthscale)
                    else:
                        lengthscale_prev.append(None)
                        warnings.warn(
                            "Kernel doesn't contain lengthscales in kern or kern.parts."
                        )
            else:
                warnings.warn(
                    "Kernel doesn't contain lengthscales in kern or kern.parts."
                )
            # estimate noise using the user-defined function
            noise_array = self.compute_hsc_noise(X, Y, Y_norm, lengthscale_prev)
            # update model by reinstantiating it
            self._model = self.set_XY(X, Y_norm, self._kernel, Y_metadata)
            # set the noise parameters to the error in Y
            self._model[".*het_Gauss.variance"] = noise_array
            # we can fix the noise term
            self._model.het_Gauss.variance.fix()

    def set_XY(self, X: npt.ArrayLike, Y_norm: npt.ArrayLike, kernel: Kern, Y_metadata: dict) -> GPy.models.GPHeteroscedasticRegression:    
        """
        Returns the reinstantiated model with new X and Y data.
        This is done by reinstantiating the model because the 'set_XY'
        method is incorrectly implemented for heterocedastic GPs in GPy.
        """
        model = GPy.models.GPHeteroscedasticRegression(
                X, Y_norm, kernel=kernel, Y_metadata=Y_metadata
            )
        return model

    def get_best_xy(self) -> tuple[npt.NDArray, float]:
        """
        Returns the lowest energy acquisition (x, y).
        """
        xbest = np.array(self.X[np.argmin(self.Y)])
        ybest = np.min(self.Y)
        return xbest, ybest

    def predict(
        self, x: npt.ArrayLike, noise: bool = False, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance at point x, with or without
        model variance (noise).
        """
        m, v = self._model.predict(
            np.atleast_2d(x),
            include_likelihood=noise,
            Y_metadata=self._model.Y_metadata,
        )
        v = np.clip(v, 1e-12, np.inf)
        if norm:
            return m, v
        else:
            return m * self.normsd + self.normmean, v * (self.normsd**2)

    def predict_grads(
        self, x: npt.ArrayLike, norm: bool = False
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Returns model prediction mean and variance gradients with respect to
        input at point x.
        """
        dmdx, dvdx = self._model.predictive_gradients(np.atleast_2d(x))
        if norm:
            return dmdx, dvdx
        else:
            return dmdx * self.normsd, dvdx * (self.normsd**2)

    def predict_mean_sd_grads(
        self, x: npt.ArrayLike, noise: bool = False, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray, npt.NDArray]:
        """
        Returns the model prediction mean, standard deviation and their
        gradients at point x, with or without model variance (noise).

        This method is a wrapper used primarily during calculations
        of acquisition functions and their derivatives.
        """
        m, v = self.predict(np.atleast_2d(x), noise=noise, norm=norm)
        dmdx, dvdx = self.predict_grads(np.atleast_2d(x), norm=norm)
        dmdx = dmdx[:, :, 0]
        dsdx = dvdx / (2 * np.sqrt(v))
        return m, np.sqrt(v), dmdx, dsdx

    def predict_mean_grad(
        self, x: npt.ArrayLike, norm: bool = True
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """Returns model mean and its gradient at point x.

        This method is a wrapper used primarily when the
        mean function is minimized in order to obtain a
        global minimum prediction.
        """
        m, _ = self.predict(np.atleast_2d(x), norm=norm)
        dmdx, _ = self.predict_grads(np.atleast_2d(x), norm=norm)
        return m, dmdx

    def estimate_num_local_minima(self, search_bounds: ArrayLike2D):
        """
        Returns estimated number of local minima within bounds, calculated
        based on model properties.
        """
        # For the ith dimension, the number of local minima along a slice
        # is approximately n(i) = boundlength(i)/(2*lengthscale(i)). Note
        # that periodic kernels operate on normalised distances: distance
        # between inputs that are period(i)/2 apart is 1. To get the total
        # number of minima for all of the search space, multiply together
        # n(i) over all i.
        numpts = 1
        ks = self._model.kern.parameters if self.dim > 1 else [self._model.kern]
        for bounds, kern in zip(search_bounds, ks):
            if hasattr(kern, "period"):
                bound_distance = (bounds[1] - bounds[0]) / float(kern.period)
            else:
                bound_distance = (bounds[1] - bounds[0]) / 2
            numpts *= max(1, bound_distance / float(kern.lengthscale))
        return int(numpts)

    # model parameters:

    def get_all_params(self) -> dict[str, float | list]:
        """
        Returns model parameters as a dictionary with entries:
        variance, noise, lengthscales, periods
        where the last three are 1D lists. There exists a period only for those
        dimensions which are using a periodic kernel.
        """
        noise_array = []
        for i in range(self._model.likelihood.variance.size):
            noise_array.append(self._model.likelihood.variance[i][0])

        sigma = float(self._model.kern.param_array[0])
        lss = []
        pers = []
        ks = self._model.kern.parameters if self.dim > 1 else [self._model.kern]
        for kern in ks:
            lss.append(float(kern.lengthscale))
            if hasattr(kern, "period"):
                pers.append(float(kern.period))

        # the variables are returned in a dict:
        params = {}
        params["noise"] = noise_array
        params["variance"] = sigma
        params["lengthscales"] = lss
        params["periods"] = pers

        return params

    def get_unfixed_params(self) -> npt.NDArray:
        """
        Returns the unfixed parameters of the model in an array.
        """
        return np.array(self._model.unfixed_param_array.copy()).astype(float)

    def sample_unfixed_params(self, num_samples: int) -> npt.NDArray:
        """
        Sample unfixed model parameters.
        """
        hmc = GPy.inference.mcmc.HMC(self._model)
        burnin = hmc.sample(int(num_samples * 0.33))
        return hmc.sample(num_samples)

    def set_unfixed_params(self, params: npt.NDArray) -> None:
        """
        Sets the unfixed parameters of the model to given values.
        """
        self._model[self._model._fixes_] = params
        self._model.parameters_changed()

    def optimize(self, restarts: int = 1) -> None:
        """
        Updates the model hyperparameters by maximizing marginal likelihood.
        """
        self._model.optimization_runs = []
        if restarts == 1:
            self._model.optimize()
        else:
            self._model.optimize_restarts(
                num_restarts=restarts, verbose=False, messages=False
            )
