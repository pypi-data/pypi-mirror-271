import torch
import lightning as L

from histogram.model.bpnet import BPNet
from histogram.model.losses import MNLLLoss, log1pMSELoss
from histogram.performance import calculate_performance_measures

# adapt from BPNet in bpnet-lite, credit goes to Jacob Schreiber <jmschreiber91@gmail.com>
class ChromBPNet(torch.nn.Module):
    """A ChromBPNet model.

    ChromBPNet is an extension of BPNet to handle chromatin accessibility data,
    in contrast to the protein binding data that BPNet handles. The distinction
    between these data types is that an enzyme used in DNase-seq and ATAC-seq
    experiments itself has a soft sequence preference, meaning that the
    strength of the signal is driven by real biology but that the exact read
    mapping locations are driven by the soft sequence bias of the enzyme.

    ChromBPNet handles this by treating the data using two models: a bias
    model that is initially trained on background (non-peak) regions where
    the bias dominates, and an accessibility model that is subsequently trained
    using a frozen version of the bias model. The bias model learns to remove
    the enzyme bias so that the accessibility model can learn real motifs.


    Parameters
    ----------
    bias: torch.nn.Module 
        This model takes in sequence and outputs the shape one would expect in 
        ATAC-seq data due to Tn5 bias alone. This is usually a BPNet model
        from the bpnet-lite repo that has been trained on GC-matched non-peak
        regions.

    accessibility: torch.nn.Module
        This model takes in sequence and outputs the accessibility one would 
        expect due to the components of the sequence, but also takes in a cell 
        representation which modifies the parameters of the model, hence, 
        "dynamic." This model is usually a DynamicBPNet model, defined below.

    name: str
        The name to prepend when saving the file.
    """

    def __init__(self, bias, accessibility, name):
        super(ChromBPNet, self).__init__()
        for parameter in bias.parameters():
            parameter.requires_grad = False

        self.bias = bias
        self.accessibility = accessibility
        self.name = name
        self.logger = None
        self.n_control_tracks = accessibility.n_control_tracks
        self.n_outputs = 1

    def forward(self, X, X_ctl=None):
        """A forward pass through the network.

        This function is usually accessed through calling the model, e.g.
        doing `model(x)`. The method defines how inputs are transformed into
        the outputs through interactions with each of the layers.


        Parameters
        ----------
        X: torch.tensor, shape=(-1, 4, 2114)
            A one-hot encoded sequence tensor.

        X_ctl: ignore
            An ignored parameter for consistency with attribution functions.


        Returns
        -------
        y_profile: torch.tensor, shape=(-1, 1000)
            The predicted logit profile for each example. Note that this is not
            a normalized value.
        """

        acc_profile, acc_counts = self.accessibility(X)
        bias_profile, bias_counts = self.bias(X)

        y_profile = acc_profile + bias_profile
        y_counts = torch.logsumexp(torch.stack([acc_counts, bias_counts]), 
            dim=0)
        
        return y_profile, y_counts

    def get_seq_embedding(self, X, X_ctl=None):
        """A forward pass of the model.
        pass
        """
        return self.accessibility.get_seq_embedding(X)      

    @classmethod
    def from_chrombpnet(self, bias_model, accessibility_model, name):
        """Load a ChromBPNet model trained using the official repository.

        This method takes in the path to a .h5 file containing the full model,
        i.e., the bias model AND the accessibility model. If you have two
        files -- one for the bias model, and one for the accessibility model --
        load them up as separate BPNet models and create a ChromBPNet object
        afterwards.


        Parameters
        ----------
        bias model: str
            The filename of the bias model.

        accessibility_model: str
            The filename of the accessibility model.

        name: str
            The name to use when training the model and outputting to a file.
        

        Returns
        -------
        model: bpnetlite.models.ChromBPNet
            A PyTorch ChromBPNet model compatible with the bpnet-lite package.
        """

        bias = BPNet.from_chrombpnet(bias_model)
        acc = BPNet.from_chrombpnet(accessibility_model)
        return ChromBPNet(bias, acc, name)


class ChromBPNetModel(L.LightningModule):
    def __init__(self, bias, accessibility, name):
        super().__init__()
        self.model = ChromBPNet(bias, accessibility, name)

    def forward(self, x, x_ctl=None):
        return self.model(x, x_ctl)
    
    def _step(self, batch, batch_idx, mode='train'):
        x = batch['seq'] #.permute(0, 2, 1) batch_size x 4 x seq_length
        y = batch['profile']
        y_profile, y_count = self(x) # y_profile: (batch_size, 1000, 2), y_count: (batch_size, 2)

        # Calculate the profile and count losses
        profile_loss = MNLLLoss(y_profile, y).mean()
        count_loss = log1pMSELoss(y_count, y.sum(dim=-1).reshape(-1, 1)).mean()

        # Calculate performance measures
        measures = calculate_performance_measures(y_profile, 
                            y, y_count, kernel_sigma=7, 
                            kernel_width=81, measures= ['profile_pearson', 'count_pearson'])

        # Mix losses together and update the model
        loss = profile_loss + self.model.accessibility.alpha * count_loss
        log_dict = {
            # f'{mode}_loss': loss, 
            f'{mode}/profile_loss': profile_loss,
            f'{mode}/count_loss': count_loss,
            f'{mode}/profile_pearson': measures['profile_pearson'].mean(), 
            f'{mode}/count_pearson': measures['count_pearson'].mean(),
        }
        self.log(f'{mode}_loss', loss, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        self.log_dict(log_dict, on_step=False, on_epoch=True, prog_bar=False, logger=True)
        return loss

    def training_step(self, batch, batch_idx):
        return self._step(batch, batch_idx, 'train')
    
    def validation_step(self, batch, batch_idx):
        return self._step(batch, batch_idx, 'val')
    
    def test_step(self, batch, batch_idx):
        return self._step(batch, batch_idx, 'test')
    
    def predict_step(self, batch, batch_idx):
        return self._step(batch, batch_idx, 'predict')
    
    def configure_optimizers(self):
        return super().configure_optimizers()