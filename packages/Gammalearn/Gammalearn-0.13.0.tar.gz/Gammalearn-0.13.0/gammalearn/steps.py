import torch
from gammalearn.utils import BaseW


def get_training_step_mae(**kwargs):

    def training_step_mae(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        images = batch['image']

        if kwargs['add_pointing']:
            pointing = torch.stack((batch['dl1_params']['alt_tel'],
                                    batch['dl1_params']['az_tel']), dim=1).to(torch.float32)
            loss = module.net(images, pointing)
        else:
            loss = module.net(images)

        if module.experiment.regularization is not None:
            loss += module.experiment.regularization['function'](module.net) * module.experiment.regularization['weight']

        return None, None, {'autoencoder': loss.detach().item()}, loss

    return training_step_mae


def get_eval_step_mae(**kwargs):

    def validation_step_mae(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        images = batch['image']

        if kwargs['add_pointing']:
            pointing = torch.stack((batch['dl1_params']['alt_tel'],
                                    batch['dl1_params']['az_tel']), dim=1).to(torch.float32)
            loss = module.net(images, pointing)
        else:
            loss = module.net(images)

        return None, None, {'autoencoder': loss.detach().item()}, loss

    return validation_step_mae


def get_training_step_mt(**kwargs):

    def training_step_mt(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        outputs = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(outputs, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return outputs, labels, loss_data, loss

    return training_step_mt


def get_training_step_dann(**kwargs):

    def training_step_dann(module, batch):
        """
        The training operations for one batch
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        # Add the target domain into the output and labels
        output['domain_class'] = torch.cat([output['domain_class'], data['outputs_target']['domain_class']])
        labels['domain_class'] = torch.cat([labels['domain_class'], data['labels_target']['domain_class']])

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return output, labels, loss_data, loss

    return training_step_dann


def get_training_step_deepjdot(**kwargs):

    def training_step_deepjdot(module, batch):
        """
        The training operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        labels['deepjdot'] = data['outputs_target']['deepjdot']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return output, labels, loss_data, loss

    return training_step_deepjdot


def get_training_step_deepcoral(**kwargs):

    def training_step_deepcoral(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        labels['deepcoral'] = data['outputs_target']['deepcoral']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return output, labels, loss_data, loss

    return training_step_deepcoral


def get_training_step_mkmmd(**kwargs):

    def training_step_mkmmd(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        labels['mkmmd'] = data['outputs_target']['mkmmd']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return output, labels, loss_data, loss

    return training_step_mkmmd


def get_training_step_mt_gradient_penalty(**kwargs):

    def training_step_mt_gradient_penalty(module, batch):
        """
        The training operations for one batch for vanilla mt learning with gradient penalty
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        images = batch['image']
        labels = batch['label']
        images.requires_grad = True

        if kwargs.get('add_pointing', False):
            pointing = torch.stack((batch['dl1_params']['alt_tel'], batch['dl1_params']['az_tel']), dim=1)
            output = module.net({'data': images, 'pointing': pointing})
        else:
            output = module.net(images)

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        if module.experiment.regularization is not None:
            gradient_x = torch.autograd.grad(loss, images, retain_graph=True)[0]
            penalty = torch.mean((torch.norm(gradient_x.view(gradient_x.shape[0], -1), 2, dim=1) - 1) ** 2)
            loss += penalty * module.experiment.regularization['weight']

        return output, labels, loss_data, loss

    return training_step_mt_gradient_penalty


def get_eval_step_mt(**kwargs):

    def eval_step_mt(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        outputs = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Compute loss and quality measures
        loss, loss_data = module.experiment.LossComputing.compute_loss(outputs, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return outputs, labels, loss_data, loss

    return eval_step_mt


def get_eval_step_dann(**kwargs):

    def eval_step_dann(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        # Add the target domain into the output and labels
        output['domain_class'] = torch.cat([output['domain_class'], data['outputs_target']['domain_class']])
        labels['domain_class'] = torch.cat([labels['domain_class'], data['labels_target']['domain_class']])

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return output, labels, loss_data, loss

    return eval_step_dann


def get_eval_step_deepjdot(**kwargs):

    def eval_step_deepjdot(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        labels['deepjdot'] = data['outputs_target']['deepjdot']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return output, labels, loss_data, loss

    return eval_step_deepjdot


def get_eval_step_deepcoral(**kwargs):

    def eval_step_deepcoral(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        labels['deepcoral'] = data['outputs_target']['deepcoral']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return output, labels, loss_data, loss

    return eval_step_deepcoral


def get_eval_step_mkmmd(**kwargs):

    def eval_step_mkmmd(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data['outputs_source']
        labels = data['labels_source']
        dl1_params = data['dl1_params_source']

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        labels['domain_mask'] = torch.cat([data['labels_source']['class'], data['labels_target']['class']])

        labels['mkmmd'] = data['outputs_target']['mkmmd']

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return output, labels, loss_data, loss

    return eval_step_mkmmd


def get_test_step_mt(**kwargs):

    def test_step_mt(module, batch):
        """
        The test operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch, train=False)
        outputs = data['outputs_source']
        labels = data['labels_source']
        dl1_params = batch.get('dl1_params', None)

        return outputs, labels, dl1_params

    return test_step_mt


def save_memory(module, outputs: dict) -> dict:
    for k, v in module.experiment.targets.items():
            if k in ['deepjdot', 'deepcoral', 'mkmmd']:
                if outputs.get('outputs_source', None) is not None:
                    del outputs['outputs_source'][k]
                if outputs.get('outputs_target', None) is not None:
                    del outputs['outputs_target'][k]
    return outputs


def run_model(module, batch, train=True):
    """
    Run the model for one batch of data. 
    
    Parameters
    ----------
        module: (LightningModule) The current module.
        batch: (torch.tensor) The current batch of data.
        train: (bool) Whether the current step is a training or a test step.
    """
    module.net.train() if train else module.net.eval()
    
    forward_params = {}
    inputs_target, labels_target, outputs_target, dl1_params_target = None, None, None, None
    pointing_source, pointing_target = None, None

    if train and module.experiment.context['train'] == 'domain_adaptation':
        # Load data
        inputs_source = batch['image_source']
        inputs_target = batch['image_target']
        labels_source = batch['label_source']
        labels_target = batch.get('label_target', None)
        dl1_params_source = batch.get('dl1_params_source', None)
        dl1_params_target = batch.get('dl1_params_target', None)

        if dl1_params_source is not None:
             # Include the spurce alt/az information into the network
            alt_tel = batch['dl1_params_source']['alt_tel']
            az_tel = batch['dl1_params_source']['az_tel']
            pointing_source = torch.stack((alt_tel, az_tel), dim=1).to(torch.float32)

            # Include the target alt/az information into the network
            alt_tel = batch['dl1_params_target']['alt_tel']
            az_tel = batch['dl1_params_target']['az_tel']
            pointing_target = torch.stack((alt_tel, az_tel), dim=1).to(torch.float32)
    else:
        # Load data
        inputs_source = batch['image']
        labels_source = batch.get('label', None)
        dl1_params_source = batch.get('dl1_params', None)

        # Include the alt/az information into the network
        if dl1_params_source is not None:
            alt_tel = batch['dl1_params']['alt_tel']
            az_tel = batch['dl1_params']['az_tel']
            pointing_source = torch.stack((alt_tel, az_tel), dim=1).to(torch.float32)

    # Include gradient weighting if applied
    for _, v in module.experiment.targets.items():
        if v.get('grad_weight', None) is not None:
            if isinstance(v['grad_weight'], BaseW):
                forward_params['grad_weight'] = v['grad_weight'].get_weight(module.trainer)
            else:
                forward_params['grad_weight'] = v['grad_weight']

    # Forward pass
    forward_params['pointing'] = pointing_source
    outputs_source = module.net(inputs_source, **forward_params)
    if inputs_target is not None:
        forward_params['pointing'] = pointing_target
        outputs_target = module.net(inputs_target, **forward_params)

    output_dict = {
        'inputs_source': inputs_source,
        'inputs_target': inputs_target,
        'labels_source': labels_source,
        'labels_target': labels_target,
        'dl1_params_source': dl1_params_source,
        'dl1_params_target': dl1_params_target,
        'outputs_source': outputs_source,
        'outputs_target': outputs_target,
    }

    if module.experiment.test_dataset_parameters is not None:
        if module.experiment.test_dataset_parameters.get('memory_diet', False) and train is False:
            output_dict = save_memory(module, output_dict)

    return output_dict
