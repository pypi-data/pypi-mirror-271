import logging

import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
from pytorch_lightning import LightningModule
import gammalearn.utils as utils
import ot
from typing import List, Dict


def cross_entropy_loss(output, target, weight):
    return F.cross_entropy(output, target.long(), weight)


def cross_entropy_loss_nn(output, target):
    return nn.CrossEntropyLoss(ignore_index=-1)(output, target.long())


def nll_nn(output, target):
    return nn.NLLLoss(ignore_index=-1)(output, target.long())


def angular_separation_loss(reduce='mean'):

    def loss_function(output, target):
        """
        Compute the mean angular separation loss between 2 directions
        Parameters
        ----------
        output (Tensor) : output of the net for direction regression
        target (Tensor) : labels for direction regression

        Returns
        -------
        Loss
        """
        logger = logging.getLogger('angular separation loss')
        logger.debug('output size : {}'.format(output.size()))
        if output.size() != target.size():
            logger.error('Output and target shapes must be the same but are {} and {}'.format(output.size(), target.size()))
            raise AssertionError('Output and target shapes must be the same')

        alt1 = output[:, 0]
        if alt1.data.nelement() <= 0:
            logger.error('reconstructed alt must have at least 1 element but have {}'.format(alt1.data.nelement()))
            raise AssertionError('reconstructed alt must have at least 1 element')

        if np.isnan(np.sum(alt1.data.cpu().numpy())):
            logger.error('alt1 has NaN value(s) : {}'.format(alt1.data))
            raise AssertionError('alt1 has NaN value(s)')

        logger.debug('mean on {} elements'.format(alt1.data.nelement()))

        az1 = output[:, 1]
        if np.isnan(np.sum(az1.data.cpu().numpy())):
            logger.error('az1 has NaN value(s) : {}'.format(az1.data))
            raise AssertionError('az1 has NaN value(s)')

        alt2 = target[:, 0]
        if np.isnan(np.sum(alt2.data.cpu().numpy())):
            logger.error('alt2 has NaN value(s) : {}'.format(alt2.data))
            raise AssertionError('alt2 has NaN value(s)')

        az2 = target[:, 1]
        if np.isnan(np.sum(az2.data.cpu().numpy())):
            logger.error('az2 has NaN value(s) : {}'.format(az2.data))
            raise AssertionError('az2 has NaN value(s)')

        loss_cos = (torch.mul(torch.mul(alt1.cos(), alt2.cos()), (az1 - az2).cos()) + torch.mul(alt1.sin(), alt2.sin()))

        if np.isnan(np.sum(loss_cos.data.cpu().numpy())):
            logger.error('loss_cos has NaN value(s) : {}'.format(loss_cos.data))
            raise AssertionError('loss_cos has NaN value(s)')

        # the loss_coss needs to be < 1 for the gradient not to be inf
        loss = loss_cos.clamp(min=-0.999999, max=0.999999).acos()

        if reduce == 'mean':
            loss = loss.sum() / alt1.data.nelement()
        elif reduce == 'sum':
            loss = loss.sum()

        if np.isnan(np.sum(loss.data.cpu().numpy())):
            logger.error('loss has NaN value(s) : {}'.format(loss.data))
            raise AssertionError('loss has NaN value(s)')

        return loss
    return loss_function


# From https://github.com/kornia/kornia/blob/master/kornia/losses/focal.py
def one_hot(labels, num_classes, device=None, dtype=None, eps=1e-6):
    r"""Converts an integer label 2D tensor to a one-hot 3D tensor.
    Args:
        labels (torch.Tensor) : tensor with labels of shape :math:`(N, H, W)`,
                                where N is batch siz. Each value is an integer
                                representing correct classification.
        num_classes (int): number of classes in labels.
        device (Optional[torch.device]): the desired device of returned tensor.
         Default: if None, uses the current device for the default tensor type
         (see torch.set_default_tensor_type()). device will be the CPU for CPU
         tensor types and the current CUDA device for CUDA tensor types.
        dtype (Optional[torch.dtype]): the desired data type of returned
         tensor. Default: if None, infers data type from values.
        eps
    Returns:
        torch.Tensor: the labels in one hot tensor.
    """
    if not torch.is_tensor(labels):
        raise TypeError("Input labels type is not a torch.Tensor. Got {}"
                        .format(type(labels)))
    if not len(labels.shape) == 1:
        raise ValueError("Invalid depth shape, we expect B. Got: {}"
                         .format(labels.shape))
    if not labels.dtype == torch.int64:
        raise ValueError(
            "labels must be of the same dtype torch.int64. Got: {}" .format(
                labels.dtype))
    if num_classes < 1:
        raise ValueError("The number of classes must be bigger than one."
                         " Got: {}".format(num_classes))
    batch_size = labels.shape[0]
    one_h = torch.zeros(batch_size, num_classes,
                        device=device, dtype=dtype)
    return one_h.scatter_(1, labels.unsqueeze(1), 1.0) + eps


def focal_loss(x, target, gamma=2.0, reduction='none'):
    r"""Function that computes Focal loss.
    See :class:`~kornia.losses.FocalLoss` for details.
    """
    if not torch.is_tensor(x):
        raise TypeError("Input type is not a torch.Tensor. Got {}"
                        .format(type(x)))

    if not len(x.shape) == 2:
        raise ValueError("Invalid input shape, we expect BxC. Got: {}"
                         .format(x.shape))

    if not x.device == target.device:
        raise ValueError(
            "input and target must be in the same device. Got: {}" .format(
                x.device, target.device))

    # network outputs logsoftmax.

    # create the labels one hot tensor
    target_one_hot = one_hot(target, num_classes=x.shape[1], device=x.device, dtype=x.dtype)

    # compute the actual focal loss
    weight = torch.pow(-torch.exp(x) + 1., gamma)

    focal = - weight * x
    loss_tmp = torch.sum(target_one_hot * focal, dim=1)

    if reduction == 'none':
        loss = loss_tmp
    elif reduction == 'mean':
        loss = torch.mean(loss_tmp)
    elif reduction == 'sum':
        loss = torch.sum(loss_tmp)
    else:
        raise NotImplementedError("Invalid reduction mode: {}"
                                  .format(reduction))
    return loss


class FocalLoss(nn.Module):
    r"""Criterion that computes Focal loss.
    According to [1], the Focal loss is computed as follows:
    .. math::
        \text{FL}(p_t) = -\alpha_t (1 - p_t)^{\gamma} \, \text{log}(p_t)
    where:
       - :math:`p_t` is the model's estimated probability for each class.
    Arguments:
        alpha (float): Weighting factor :math:`\alpha \in [0, 1]`.
        gamma (float): Focusing parameter :math:`\gamma >= 0`.
        reduction (str, optional): Specifies the reduction to apply to the
         output: ‘none’ | ‘mean’ | ‘sum’. ‘none’: no reduction will be applied,
         ‘mean’: the sum of the output will be divided by the number of elements
         in the output, ‘sum’: the output will be summed. Default: ‘none’.
    Shape:
        - Input: :math:`(N, C, H, W)` where C = number of classes.
        - Target: :math:`(N, H, W)` where each value is
          :math:`0 ≤ targets[i] ≤ C−1`.
    Examples:
        >>> N = 5  # num_classes
        >>> args = {"alpha": 0.5, "gamma": 2.0, "reduction": 'mean'}
        >>> loss = FocalLoss(*args)
        >>> x = torch.randn(1, N, 3, 5, requires_grad=True)
        >>> target = torch.empty(1, 3, 5, dtype=torch.long).random_(N)
        >>> output = loss(x, target)
        >>> output.backward()
    References:
        [1] https://arxiv.org/abs/1708.02002
    """

    def __init__(self, alpha=0.5, gamma=2.0, reduction='mean') -> None:
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, x, target):
        return focal_loss(x, target.long(), self.gamma, self.reduction)


class LossComputing:
    def __init__(self, targets, conditional=False, gamma_class=None, path_distrib_weights: str=None):
        self.targets = targets.copy()

        self.conditional = conditional
        if self.conditional:
            assert 'class' in self.targets, 'The conditional loss is defined based on particle type'
            assert gamma_class is not None, 'To mask loss, one must provide the class of gamma'

        self.gamma_class = gamma_class
        self.out_of_balancing = _OutOfBalancing(targets)

        if path_distrib_weights is not None:
            self.distrib_weights = utils.DistributionW(path_distrib_weights)
        else:
            self.distrib_weights = None

    def regularization(self, loss: dict, module: LightningModule) -> dict:
        if module.experiment.regularization is not None:
            loss += module.experiment.regularization['function'](module.net) * module.experiment.regularization['weight']
        return loss

    def compute_loss(self, output, labels, module: LightningModule = None):
        loss = {}
        loss_data = {}

        if self.conditional:
            loss_mask = labels.get('class')
            loss_mask = loss_mask == self.gamma_class

        # 'targets' and 'output' must contain the same keys, but 'labels' may contain more elements, such as a domain
        # key referring to whether it belongs to the source and target datasets. Thus, we need to check if targets and
        # output keys are subset of the labels keys.
        assert (self.targets.keys() == output.keys()) and set(output.keys()).issubset(set(labels.keys())), \
            'All targets must have output and label but targets: {} \n outputs: {} ' \
            '\n labels: {}'.format(self.targets.keys(), output.keys(), labels.keys())

        for k, v in self.targets.items():
            out = output[k]
            lab = labels[k]

            # Check dimensions
            if k in ['energy', 'direction', 'impact']:
                assert out.ndim == lab.ndim, 'output and label must have same number of dimensions for correct ' \
                                             'loss computation but are {} and {}'.format(out.ndim, lab.ndim)
                out_shape = self.targets[k].get('output_shape')
                lab_shape = self.targets[k].get('label_shape', out_shape)

                assert out.shape[-1] == out_shape, \
                    '{} output shape does not match settings, got {} instead of {}'.format(k, out.shape[-1], out_shape)
                assert lab.shape[-1] == lab_shape, \
                    '{} output shape does not match settings, got {} instead of {}'.format(k, lab.shape[-1], lab_shape)
                
            # Compute class masked loss for domain adaptation
            if isinstance(v['loss'], _DomainConditionalLoss):
                if v['loss'].domain_conditional:  
                    v['loss'].set_mask(labels['domain_mask']) 

            # Get loss
            loss_k = v['loss'](out, lab)

            # Apply weights based on distribution
            if self.distrib_weights is not None:
                if k in ['energy']:
                    loss_k = self.distrib_weights.apply(loss_k, labels['energy'])

            # Compute class masked loss
            if k in ['energy', 'direction', 'impact']:
                if self.conditional:
                    loss_mask = loss_mask.to(out.device)
                    assert loss_k.shape[0] == loss_mask.shape[0], 'loss should not be reduced for mask on particle type' \
                                                                'but got {} and {}'.format(loss_k.shape, loss_mask.shape)
                    if loss_k.dim() > 1:
                        cond = [loss_mask.unsqueeze(1) for _ in range(loss_k.shape[1])]
                        cond = torch.cat(cond, dim=1)
                    else:
                        cond = loss_mask
                    assert loss_k.shape == cond.shape, \
                        'loss and mask must have the same shape but are {} and {}'.format(loss_k.shape, cond.shape)
                    loss_k = (loss_k * cond).sum() / cond.sum() if cond.sum() > 0 else \
                        torch.tensor(0., device=loss_k.device)

            if k in ['autoencoder']:
                loss_k = torch.mean(loss_k, dim=tuple(torch.arange(loss_k.dim())[1:]))
                loss_data[k] = loss_k.mean()
                loss[k] = loss_k.mean()
            else:
                loss_data[k] = loss_k.mean().detach().item()
                loss[k] = loss_k.mean()

        # Hand-designed loss weight. Requires to be out of the loss balancing scope.
        if len(self.out_of_balancing.targets) > 0:
            loss = self.out_of_balancing(loss, module)

        return loss, loss_data
    

class MovingAverageMetric:
    """
    Compute the moving average of a metric.
    """
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.average = None
        self.values = []

    def update(self, value: torch.Tensor) -> None:
        """
        Update the moving average.
        """
        if self.average is None:
            self.average = value
            self.values = [self.average] * self.window_size
        else:
            self.values.append(value)
            self.values.pop(0)
            self.average = torch.stack(self.values).mean(dim=0)


class GradientToolBox:
    """
    This class gathers some functions to calculate the gradients on a specified set of weights.
    Inspired from https://github.com/median-research-group/LibMTL/blob/main/LibMTL/weighting/abstract_weighting.py
    """
    def __init__(self, targets: Dict[str, Dict], layer: str = None) -> None:
        self.targets = targets.copy()
        self.num_targets = len(self.targets)
        self.layer = layer
        self.parameters = None
    
    def get_parameters(self):
        """
        Returns the parameters.
        """
        return self.parameters
    
    def set_parameters(self, module: nn.Module):
        """
        Set the parameters.
        """
        assert self.layer is not None, 'The layer must be specified.'
        model = module.net if isinstance(module, LightningModule) else module
        parameters = [(n, p) for n, p in model.named_parameters() if self.layer in n]
        assert parameters, 'No parameters found for layer {}.'.format(self.layer)

        _, self.parameters = parameters[-1] 

    def initialize_gradients(self):
        return torch.zeros(self.num_targets, 1)
    
    def compute_gradients(self, loss: Dict[str, torch.Tensor]) -> torch.Tensor:
        """
        Compute the gradients on the set shared weights.
        """
        assert self.get_parameters() is not None, 'The parameters must be set before computing the gradients.'
        gradients = []
        for k in self.targets.keys():
            gradients.append(torch.autograd.grad(outputs=loss[k], 
                                                 inputs=self.get_parameters(), 
                                                 retain_graph=True, # Allows to use .backward() multiple times
                                                 create_graph=True, # Allows to compute the gradients of the gradnorm weights
                                                 allow_unused=True, # Allows to compute the gradients in the multi-task scenario
                                                )[0].flatten())
        return torch.stack(gradients)


class MultiLossBalancing(nn.Module):
    """
    Generic function for loss balancing.

    Parameters
    ----------
    targets: (dict) The loss dictionary defining for every objective of the experiment the loss function

    Returns
    -------
    """
    def __init__(self, targets: Dict[str, Dict], balancing: bool = True, requires_gradients: bool = False, layer: str = None):
        super().__init__()
        if requires_gradients: assert layer is not None, 'If requires_gradients is True, the layer must be specified.'
        self.targets = targets.copy()
        self.weights = None
        self.weights_dict = {}  # To log using callbacks
        self.gradient = None
        self.gradients_dict = {}  # To log using callbacks
        self.requires_gradients = requires_gradients  # Whether to compute the gradients
        self.device = None
        self.layer = layer
        self.gtb = GradientToolBox(self.targets, layer) if self.requires_gradients else None
        
        for k, v in targets.items():
            if balancing:  # For automatic weighting strategy
                if not v.get('mt_balancing', False):  # Only keep targets with parameter 'mt_balancing' set to True
                    self.targets.pop(k)  # Discard it
                else:
                    pass  # Keep it
            else:  # For manual weighting strategy
                if v.get('mt_balancing', False):  # Only keep targets with parameter 'mt_balancing' set to False
                    self.targets.pop(k)  # Discard it
                else:
                    pass  # Keep it

    def _set_device(self, loss: Dict[str, torch.Tensor]) -> None:
        if self.device is None:
            self.device = next(iter(loss.values())).device

    def _set_layer(self, module: LightningModule) -> None:
        """
        Set the layer of the network from the given name.
        """
        if self.gtb is not None:
            self.gtb.set_parameters(module)

    def _setup(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        """
        Optional and method-dependent.
        """
        pass

    def _i(self, module: LightningModule) -> int:
        """
        The current iteration.
        """
        return module.trainer.fit_loop.total_batch_idx
    
    def _is_first_iter(self, module: LightningModule) -> bool:
        """
        Whether it is the first iteration of the training.
        """
        return self._i(module) == 0
    
    def _is_training(self, loss: Dict[str, torch.Tensor]) -> bool:
        """
        Whether it is the training or the validation mode. During validation, the requires_grad attribute is set to False.
        """
        return all([loss_k.requires_grad for loss_k in loss.values()])
    
    def _weights_fetch(self, module: LightningModule) -> torch.Tensor:
        """
        Fetch the weights defined by the user.
        """
        weights = torch.Tensor(torch.ones(len(self.targets)))
        for i, v in enumerate(self.targets.values()):
            if v.get('loss_weight', None) is not None:  
                if isinstance(v['loss_weight'], utils.BaseW):  
                    weights[i] = v['loss_weight'].get_weight(module.trainer)
                else:
                    weights[i] = v['loss_weight']
        return weights
    
    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule = None) -> None:
        """
        Mandatory and method-dependent.
        """
        return NotImplementedError
    
    def _weights_apply(self, loss: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        weighted_loss = loss.copy()

        for i, k in enumerate(self.targets.keys()):
            weighted_loss[k] = self.weights[i] * loss[k]

        return weighted_loss
    
    def _weights_update(self) -> None:
        for i, k in enumerate(self.targets.keys()):
            self.weights_dict[k] = self.weights[i].clone().detach()

    def _gradients_compute(self, loss: Dict[str, torch.Tensor]) -> None:
        if self._is_training(loss):
            self.gradients = self.gtb.compute_gradients(loss).to(self.device)
        else:
            self.gradients = self.gtb.initialize_gradients().to(self.device)

    def _gradients_update(self) -> None:
        for i, k in enumerate(self.targets.keys()):
            self.gradients_dict[k] = self.gradients[i].clone().detach()

    def forward(self, loss: Dict[str, torch.Tensor], module: LightningModule = None) -> dict:
        self._set_device(loss)
        self._set_layer(module)
        self._setup(loss, module)

        if self.requires_gradients:
            self._gradients_compute(loss)
            self._gradients_update()

        self._weights_compute(loss, module)
        self._weights_update()
        
        return self._weights_apply(loss)
    

class GradNorm(MultiLossBalancing):
    """
    From the article GradNorm: Gradient Normalization for Adaptive Loss Balancing in Deep Multitask Networks (
    https://arxiv.org/abs/1711.02257). The method consists in computing the gradients of the loss with respect to the
    shared weights and then compute the norm of the gradients. The weights are then updated according to the norm of
    the gradients.
    Inspired from https://github.com/NVIDIA/modulus-sym/blob/main/modulus/sym/loss/aggregator.py#L111.
    """
    def __init__(self, targets: Dict[str, Dict], alpha: float = 1.0, layer: nn.Module = None, 
                 requires_gradients: bool = True):
        super().__init__(targets=targets, balancing=True, requires_gradients=requires_gradients, layer=layer)
        assert alpha > 0, "Parameter alpha of GradNorm must be strictly positive"
        self.alpha = alpha
        self.weights = nn.Parameter(torch.zeros(len(self.targets)))  # exp(0) = 1
        self.L_grad = torch.tensor(0., requires_grad=True)

        self.tracker_g = None  # Gradient norms
        self.tracker_r = None  # Relative inverse training rate
        self.tracker_k = None  # The constant of the L_grad objective function
        self.tracker_l = None  # The relative loss
        self.tracker_l0 = None  # The initial loss
        self.tracker_lgrad = None  # The L_grad objective function
    
    def _setup(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        if self._is_first_iter(module) and self._is_training(loss):  
            self.l0 = torch.stack([loss[k].clone().detach() for k in loss.keys()]).to(self.device)

    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        if self._is_training(loss):
            self._weights_normalize()
            weights_exp = self._t(self.weights)

            # Compute the norm of the gradient of each task wrt to the last shared layer
            G = torch.mul(weights_exp.view(-1, 1), self.gradients.detach()).norm(dim=1, p=2)

            # Compute the relative inverse training rate
            loss_ratio = torch.div(torch.Tensor(list(loss.values())).to(self.device), self.l0)
            r = torch.div(loss_ratio, loss_ratio.mean()) 

            # Compute the gradient gradients
            constant = torch.mul(G.mean(), torch.pow(r, self.alpha)).detach()
            L_grad = torch.sub(G, constant).norm(p=1)
            self.L_grad = L_grad

            # Track the values
            self.tracker_g = {k: G[i].detach() for i, k in enumerate(loss.keys())}
            self.tracker_r = {k: r[i].detach() for i, k in enumerate(loss.keys())}
            self.tracker_k = {k: constant[i].detach() for i, k in enumerate(loss.keys())}
            self.tracker_l = {k: loss_ratio[i].detach() for i, k in enumerate(loss.keys())}
            self.tracker_l0 = {k: self.l0[i].detach() for i, k in enumerate(loss.keys())}
            self.tracker_lgrad = L_grad.detach()

    def _t(self, weight: torch.Tensor) -> torch.Tensor:
        """
        Exponantial transformation of the weights using w_i = exp(w_i) to ensure the weights are positive.
        """
        return torch.exp(weight)
    
    def _weights_normalize(self) -> None:
        """
        Normalize the weights using c*exp(x) = exp(log(c)+x).
        """
        with torch.no_grad():
            c = torch.div(len(self.targets), self._t(self.weights).sum())
            for i in range(len(self.targets)):
                self.weights[i] = self.weights[i].clone() + torch.log(c).detach()
    
    def _weights_apply(self, loss: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        weighted_loss = loss.copy()

        for i, k in enumerate(self.targets.keys()):
            weighted_loss[k] = self._t(self.weights[i]) * loss[k]

        weighted_loss['gradnorm'] = self.L_grad

        return weighted_loss


class UncertaintyWeighting(MultiLossBalancing):
    r"""
    Create the function to compute the loss in case of multi regression experiment with homoscedastic uncertainty
    loss balancing. See the paper https://arxiv.org/abs/1705.07115.
    In the paper the total loss is defined as:
    .. math::
        \text{L}(W,\sigma_1,\sigma_2,...,\sigma_i) = \sum_i \frac{1}{2\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2

    but in https://github.com/yaringal/multi-task-learning-example/blob/master/multi-task-learning-example.ipynb as:
    .. math::
        \text{L}(W,\sigma_1,\sigma_2,...,\sigma_i) = \sum_i \frac{1}{\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2 -1

    should not make a big difference. However, we introduce log_var_coefficients and penalty to let the user choose:
    .. math::
        \text{L} = \sum_i \frac{1}{\{log_var_coefficients}\sigma_i}^2 \text{L}_i + \text{log}\sigma_i^2 -\text{penalty}

    Parameters
    ----------
    targets (dict): The loss dictionary defining for every objective of the experiment the loss function and its
    initial log_var

    Returns
    -------
    The function to compute the loss
    """
    def __init__(self, targets: Dict[str, Dict], log_var_coefficients: list = None, penalty: int = 0, 
                 requires_gradients: bool = False, layer: str = None):
        super().__init__(targets=targets, balancing=True, requires_gradients=requires_gradients, layer=layer)
        self.weights = torch.Tensor(torch.ones(len(self.targets)))
        self.log_vars = nn.Parameter(torch.ones(len(self.targets)), requires_grad=True)
        self.penalty = penalty

        if log_var_coefficients is None:
            # If the log var coefficients have not been initialized in the experiment setting file, initialize them to 1
            self.log_var_coefficients = torch.ones(self.log_vars.shape)
        else:
            self.log_var_coefficients = torch.tensor(log_var_coefficients)
        assert len(self.log_vars) == len(self.log_var_coefficients), \
            'The number of log variance coefficients must be equal to the number of log variances.'
        
    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        for i in range(len(self.targets)):
            self.weights[i] = (torch.exp(-self.log_vars[i]) * self.log_var_coefficients[i]).to(self.device)
    
    def _weights_apply(self, loss: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        weighted_loss = loss.copy()

        for i, k in enumerate(self.targets.keys()):
            weighted_loss[k] = (torch.exp(-self.log_vars[i]) * self.log_var_coefficients[i]) * loss[k] + self.log_vars[i] - self.penalty

        return weighted_loss


class RandomLossWeighting(MultiLossBalancing):
    """
    From the article Reasonable Effectiveness of Random Weighting: A Litmus Test for Multi-Task Learning (
    https://arxiv.org/abs/2111.10603). The method consists in assigning a random weight to each task drawn from a
    normal distribution. The random weight is recomputed at each iteration.
    Implementation inspired from https://github.com/median-research-group/LibMTL/blob/main/LibMTL/weighting/RLW.py
    """
    def __init__(self, targets: Dict[str, Dict], requires_gradients: bool = False, layer: str = None):
        super().__init__(targets=targets, balancing=True, requires_gradients=requires_gradients, layer=layer)

    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        self.weights = F.softmax(torch.randn(len(self.targets)), dim=-1).to(self.device)


class EqualWeighting(MultiLossBalancing):
    """
    Assigned the same weight to all the losses.
    """
    def __init__(self, targets: Dict[str, Dict], requires_gradients: bool = False, layer: str = None):
        super().__init__(targets=targets, balancing=True, requires_gradients=requires_gradients, layer=layer)
        self.weights = torch.Tensor([1. / len(self.targets)] * len(self.targets))

    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        pass
    

class ManualWeighting(MultiLossBalancing):
    """
    Manual weighting of the loss. These hyperparameters must be defined in the targets dictionary of the experiment setting file.
    This class allows to compute gradients on the weights in the manual weighting scenario and can be used by the user.
    """
    def __init__(self, targets: Dict[str, Dict], requires_gradients: bool = False, layer: str = None) -> None:
        super().__init__(targets=targets, balancing=True, requires_gradients=requires_gradients, layer=layer)
        self.weights = torch.Tensor([1.] * len(self.targets))  # Equal 1. by default

    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        self.weights = self._weights_fetch(module)


class _OutOfBalancing(MultiLossBalancing):
    """
    Manual weighting of the loss when mt_balancing is set to False. These hyperparameters must be defined in the targets dictionary 
    of the experiment setting file. This class is used in the LossComputing class to handle the weights that are out of the loss
    balancing scope. This class must not be used directly by the user.
    """
    def __init__(self, targets: Dict[str, Dict], requires_gradients: bool = False, layer: str = None) -> None:
        super().__init__(targets=targets, balancing=False, requires_gradients=requires_gradients, layer=layer)
        self.weights = torch.Tensor([1.] * len(self.targets))  # Equal 1. by default

    def _weights_compute(self, loss: Dict[str, torch.Tensor], module: LightningModule) -> None:
        self.weights = self._weights_fetch(module)


class _DomainConditionalLoss(nn.Module):
    """
    This class is used to define the conditional loss. The loss is weighted by a mask that is set to 1 if the label
    belongs to the domain class of interest, 0 otherwise. 
    """
    def __init__(self, training_class: list = None):
        super().__init__()
        self.loss_domain_mask = None

        if training_class is not None:
            assert isinstance(training_class, list), 'training class parameter must be of type list, got {} ' \
                                                  'instead'.format(type(training_class))
            for c in training_class:
                assert isinstance(c, int), '{} must be of type int, got {} instead'.format(c, type(c))
            self.training_class = training_class
            self.domain_conditional = True
        else:
            self.training_class = None
            self.domain_conditional = False

    def set_mask(self, labels: torch.Tensor) -> None:
        """
        Update the domain loss mask.

        Parameters
        ----------
        labels: (torch.Tensor) The ground truth class labels.
        """
        self.loss_domain_mask = torch.Tensor([1 if x in self.training_class else 0 for x in labels])
        self.bs = int(self.loss_domain_mask.shape[0] / 2)

    def get_source_mask_idx(self) -> torch.Tensor:
        return self.loss_domain_mask[:self.bs].nonzero()
    
    def get_source_mask(self) -> torch.Tensor:
        mask = torch.zeros(self.bs)
        mask[self.get_source_mask_idx()] = 1
        return mask
    
    def get_target_mask_idx(self) -> torch.Tensor:
        return self.loss_domain_mask[self.bs:].nonzero()
    
    def get_target_mask(self) -> torch.Tensor:
        mask = torch.zeros(self.bs)
        mask[self.get_target_mask_idx()] = 1
        return mask


class DANNLoss(_DomainConditionalLoss):
    """
    Implementation of the Domain Adversarial Neural Networl (DANN) loss.
    From the DANN article https://arxiv.org/abs/1505.07818.

    Parameters
    ----------
    training_class: (dict) The dict of all the classes that trigger the training of the domain classifier. If set to
    None, no domain conditional is applied. In the LST dataset, MC labels are processed using the particle dictionary
    defined in the experiment settings, however the real labels remain the same.
    gamma: (int) If gamma is not None, the weight associated to the loss is computed according to the lambda_p strategy.
    """
    def __init__(self, training_class: list = None):
        super().__init__(training_class=training_class)
        self.criterion = torch.nn.CrossEntropyLoss(reduction='none')

    def forward(self, output: torch.Tensor, labels: torch.Tensor):
        """
        DANN loss function.

        Parameters
        ----------
        output: (torch.Tensor) The model's output.
        labels: (torch.Tensor) The ground truth domain labels.
        """
        loss = self.criterion(output, labels)
        if self.loss_domain_mask is not None and self.domain_conditional:
            # mask = self.loss_domain_mask.to(output.device)
            mask = torch.cat([self.get_source_mask(), self.get_source_mask()]).to(output.device)
            loss = (loss * mask).sum() / mask.sum() if mask.sum() > 0 else torch.tensor(0., device=loss.device)

        return loss


class DeepJDOTLoss(_DomainConditionalLoss):
    """
    Implementation of the Wasserstein loss using the Optimal Transport theory.
    From the DeepJDOT article https://arxiv.org/abs/1803.10081.
    """

    def __init__(self, training_class: list = None):
        super().__init__(training_class=training_class)

    def forward(self, xs: torch.Tensor, xt: torch.Tensor):
        xs = xs.view(xs.shape[0], -1)
        xt = xt.view(xt.shape[0], -1)

        if self.loss_domain_mask is not None and self.domain_conditional:
            # Square arrays are mandatory for the OT computation
            xs = xs[self.get_source_mask_idx()].flatten(start_dim=1)
            xt = xt[self.get_target_mask_idx()][:xs.shape[0]].flatten(start_dim=1)

        if xs.shape[0] > 0:
            cost = torch.cdist(xs, xt, p=2) ** 2  # ||g(x_i^s) - g(x_j^t)||²
            gamma = torch.tensor(ot.emd(ot.unif(xs.shape[0]),
                                        ot.unif(xt.shape[0]),
                                        cost.detach().cpu().numpy()),
                                dtype=torch.float32).to(cost.device)

            loss = (gamma * cost).sum()
        else:
            loss = torch.tensor(0., device=xs.device)

        return loss


class DeepCORALLoss(_DomainConditionalLoss):
    """
    Implementation of the CORAL loss.
    From the DeepCORAL article https://arxiv.org/abs/1607.01719.

    Parameters
    ----------
    """

    def __init__(self, training_class: list = None):
        super().__init__(training_class=training_class)
    
    def forward(self, xs: torch.Tensor, xt: torch.Tensor) -> torch.Tensor:
        xs = xs.flatten(start_dim=1)  # Source features of size [ns, d]
        xt = xt.flatten(start_dim=1)  # Target features of size [nt, d]

        if self.loss_domain_mask is not None and self.domain_conditional:
            xs = xs[self.get_source_mask_idx()].flatten(start_dim=1)
            xt = xt[self.get_target_mask_idx()].flatten(start_dim=1)

        if xs.shape[0] > 1 and xt.shape[0] > 1:  # cov() needs at least 2 elements in the batch
            mean = (xs.mean(0) - xt.mean(0)).pow(2).mean()
            cov = (xs.T.cov() - xt.T.cov()).pow(2).mean()
            loss = mean + cov
        else:
            loss = torch.tensor(0., device=xs.device)

        return loss


class GaussianKernel(nn.Module):
    """
    Gaussian kernel matrix.
    This implementation is inspired from
    https://github.com/thuml/Transfer-Learning-Library/blob/0fdc06ca87c71fbf784d58e7388cf03a3f13bf00/tllib/modules/kernels.py

    Parameters
    ----------
    alpha: (float) magnitude of the variance of the Gaussian
    """
    def __init__(self, alpha: torch.float32):
        super().__init__()
        self.alpha = alpha

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """
        Parameters
        ----------
        x: (torch.Tensor) the first input feature vector of size (batch_size, feature_size).
        y: (torch.Tensor) the second input feature vector of size (batch_size, feature_size).

        Returns
        -------
        The kernel value of size (batch_size, batch_size).
        """
        l2_dist = torch.cdist(x, y)
        sigma_square = self.alpha * torch.mean(l2_dist.detach())

        return torch.exp(-l2_dist / (2. * sigma_square))


class MKMMDLoss(_DomainConditionalLoss):
    """
    Implementation of the Multiple Kernel Mean Maximum Discrepancy loss.
    This implementation is inspired from
    https://github.com/thuml/Transfer-Learning-Library/blob/0fdc06ca87c71fbf784d58e7388cf03a3f13bf00/tllib/alignment/dan.py

    Parameters
    ----------
    kernels: (list(GaussianKernel)) The list of kernels to apply. Currently, only Gaussian kernels are implemented. If
    kernels is None, then it is instantiated as GaussianKernel(alpha=2**k) for k in range(-3, 2).
    """
    def __init__(self, kernels: List[GaussianKernel] = None, training_class: list = None,):
        super().__init__(training_class=training_class)
        if kernels is None:
            self.kernels = [GaussianKernel(alpha=2**k) for k in range(-3, 2)]
        else:
            self.kernels = kernels

    def forward(self, xs: torch.Tensor, xt: torch.Tensor) -> torch.Tensor:
        xs = xs.flatten(start_dim=1)  # Source features of size (batch_size, d)
        xt = xt.flatten(start_dim=1)  # Target features of size (batch_size, d)

        if self.loss_domain_mask is not None and self.domain_conditional:
            xs = xs[self.get_source_mask_idx()].flatten(start_dim=1)
            xt = xt[self.get_target_mask_idx()][:xs.shape[0]].flatten(start_dim=1)

        if xs.shape[0] > 1:
            batch_size = xs.shape[0]

            kernel_matrix = []
            for kernel in self.kernels:
                kxx = kernel(xs, xs)  # k(xi, xj)
                kyy = kernel(xt, xt)  # k(yi, yj)
                kxy = kernel(xs, xt)  # k(xi, yj)

                # According to "A Kernel Two-Sample Test" by A. Gretton, the unbiased estimator of MMD is computed as:
                hzz = kxx + kyy - 2. * kxy  # h(zi,zj) := k(xi, xj) + k(yi, yj) − k(xi, yj) − k(xj, yi)
                kernel_matrix.append(hzz)

            # Add up the contribution of each kernel
            kernel_matrix = sum(kernel_matrix)

            # Compute the loss
            loss = torch.sqrt(kernel_matrix.sum() / (batch_size * (batch_size - 1.)))
        else:
            loss = torch.tensor(0., device=xs.device)

        return loss
