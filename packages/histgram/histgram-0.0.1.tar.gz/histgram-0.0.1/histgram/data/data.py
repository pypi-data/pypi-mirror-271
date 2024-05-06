from scipy.ndimage import gaussian_filter1d
import numpy as np
import pandas as pd
import torch
import pyBigWig
import pyfaidx
import numpy.random as random
import lightning as L

from histogram.genome import hg38

def gaussian1D_smoothing(input_array, sigma, window_size):
    truncate = (((window_size - 1) / 2) - 0.5) / sigma
    return gaussian_filter1d(input_array, sigma=sigma, truncate=truncate, axis=0) #, axis=-2) # axis=-2 is the axis for the sequence


def reverse_complement_onehot(seq_1hot):
    # rev_seq_1hot = seq_1hot[::-1, ]
    # complement_seq_1hot = rev_seq_1hot[:, ::-1]
    return seq_1hot[::-1, ::-1]


def random_reverve_complement(seqs, plus_profile, minus_profile, control_plus_profile, control_minus_profile, frac=0.5):
    '''
    Data augmentation: applies reverse complement randomly to a fraction of
    sequences and labels.
    Assumes seqs are arranged in ACGT. Then ::-1 gives TGCA which is revcomp.
    NOTE: Performs in-place modification.
    '''
    rc = np.random.rand()
    if rc<frac:
        seqs = seqs[::-1, ::-1].copy()
        plus_profile = plus_profile[::-1]
        minus_profile = minus_profile[::-1]
        control_plus_profile = control_plus_profile[::-1]
        control_minus_profile = control_minus_profile[::-1]
    return seqs, plus_profile, minus_profile, control_plus_profile, control_minus_profile


def dna_to_one_hot(sequence: str,
                   alphabet: str = 'ACGT',
                   neutral_alphabet: str = 'N',
                   neutral_value: int = 0,
                   dtype=np.float32) -> np.ndarray:
    """One-hot encode sequence."""
    def to_uint8(string):
        return np.frombuffer(string.encode('ascii'), dtype=np.uint8)
    hash_table = np.zeros((np.iinfo(np.uint8).max, len(alphabet)), dtype=dtype)
    hash_table[to_uint8(alphabet)] = np.eye(len(alphabet), dtype=dtype)
    hash_table[to_uint8(neutral_alphabet)] = neutral_value
    hash_table = hash_table.astype(dtype)
    return hash_table[to_uint8(sequence)]


def one_hot_to_dna(one_hot_matrix: np.ndarray, alphabet: str = 'ACGT') -> str:
    """Convert a one-hot encoded matrix back to a DNA sequence."""
    # Ensure the matrix is strictly one-hot; each row should sum to 1 or 0 if it is neutral (all zeros)
    if not np.all(np.sum(one_hot_matrix, axis=1) <= 1):
        raise ValueError("Each row of one_hot_matrix must be a valid one-hot vector or all zeros.")

    # Find the index of the maximum value (1) in each row, which corresponds to the character's position in the alphabet
    indices = np.argmax(one_hot_matrix, axis=1)
    
    # Map indices to corresponding characters in the alphabet
    # If a row is all zeros (neutral character), handle it by checking sum of the row
    sequence = ''.join(alphabet[idx] if np.any(row) else 'N' for row, idx in zip(one_hot_matrix, indices))

    return sequence



class HistoneDataset(torch.utils.data.Dataset):

    def __init__(self,
        region_df: pd.DataFrame, 
        plus: str, 
        minus: str, 
        ctl_plus: str = None, 
        ctl_minus: str = None, 
        genome: str = hg38.fasta,
        input_dim: int = 2114, # size of the input sequence
        output_dim = 1000, # size of the output from the bigwig file
        shift: int = 0, # shift the summit by a random amount
        reverse_compliment: bool = False, # randomly apply reverse complement
        sigma: float = 2, # smooth the signal values
        window: int = 10, # window size for smoothing
        **kwargs
    ):

        # self.region_df = pd.read_csv(region_bed, sep='\t', header=None)
        self.region_df = region_df
        self.plus = plus 
        self.minus = minus 
        self.ctl_plus = ctl_plus 
        self.ctl_minus = ctl_minus 

        self.genome = genome
        self.input_dim = input_dim

        self.bw_flank_size = output_dim // 2 # half size of the output from the bigwig file
        self.reserve_complement = reverse_compliment
        self.shift = shift
        self.sigma = sigma
        self.window = window


    def __len__(self):
            return len(self.region_df)

    def __getitem__(self, index):
        chromo, summit = self.get_loci(index) # loci = (chromo, start, end)
        # is_peak = self.region_df.iloc[index]['annotation'] == 'peak' # is_peak = True if the locus is a peak

        seq = self.get_seq(chromo, summit)
        plus, minus = self.get_bw_value(chromo, summit)
        control_plus, control_minus = self.get_ctl_value(chromo, summit)
        
        # Randomly apply reverse complement to the sequences and bw values
        if self.reserve_complement:
            print(self.reserve_complement, flush=True)
            seq, plus, minus, control_plus, control_minus = random_reverve_complement(seq, plus, minus, control_plus, control_minus)

        # control_profile = np.concatenate([control_plus, control_minus], axis=0).reshape(2, -1).astype(dtype=np.float32)

        profile = np.concatenate([plus, minus], axis=0)

        assert not np.isnan(profile).any() and np.isfinite(profile).all()
        # assert not np.isnan(control_profile).any() and np.isfinite(control_profile).all()

        return  {
            'seq': seq.T,
            'profile': profile,
            # 'control_profile': control_profile,
            # 'is_peak': is_peak,
        }

    def smooth(self, values):
        smoothed_values = gaussian1D_smoothing(values, self.sigma, self.window)
        return smoothed_values

    def get_loci(self, index):

        current_row = self.region_df.iloc[index]
        chromo, start, summit = current_row[0], current_row[1], current_row[9]
        if self.shift > 0:
            jittering = random.randint(-self.shift, self.shift)
            summit = int(start + summit + jittering)
        else:
            summit = int(start + summit)

        return chromo, summit

    def get_seq(self, chromo, new_summit): # TO DO: considering chrom_sizes
        # Get the sequence for the loci
        seq_start = new_summit - self.input_dim//2
        seq_end = new_summit + self.input_dim//2

        fseq = pyfaidx.Fasta(self.genome)[chromo][seq_start:seq_end].seq
        assert len(fseq) == self.input_dim
        seq = dna_to_one_hot(fseq)

        return seq

    def get_bw_value(self, chromo, new_summit):
        bw_start = new_summit - self.bw_flank_size
        bw_end = new_summit + self.bw_flank_size
        loci = (chromo, bw_start, bw_end)

        # Get the signal values for the loci from bigwig files
        plus = np.array(pyBigWig.open(self.plus).values(*loci))
        minus = np.array(pyBigWig.open(self.minus).values(*loci))

        # Smooth the signal values if sigma is provided
        if self.sigma != None:
            plus = self.smooth(plus)
            minus = self.smooth(minus)

        return plus, minus

    # def get_ctl_value(self, chromo, new_summit):
    #     ctl_start = new_summit - self.input_dim // 2
    #     ctl_end = new_summit + self.input_dim // 2
    #     loci = (chromo, ctl_start, ctl_end)
    #     control_plus = np.array(pyBigWig.open(self.ctl_plus).values(*loci))
    #     control_minus = np.array(pyBigWig.open(self.ctl_minus).values(*loci))

    #     if self.sigma != None:
    #         control_plus = self.smooth(control_plus)
    #         control_minus = self.smooth(control_minus)
    #     return control_plus, control_minus

    # def get_bw_count(self, plus, minus, control_plus, control_minus):
    #     # Get the count values for the loci by log summing the signal values
    #     plus_count = np.log1p(plus.sum(keepdims=False))
    #     minus_count = np.log1p(minus.sum(keepdims=False))
    #     control_plus_count = np.log1p(control_plus.sum(keepdims=False))
    #     control_minus_count = np.log1p(control_minus.sum(keepdims=False))

    #     return plus_count, minus_count, control_plus_count, control_minus_count


class HistoneDataModule(L.LightningDataModule):
    def __init__(
            self, 
            peak_bed,
            plus,
            minus,
            ctl_plus,
            ctl_minus,
            genome,
            chrom_sizes: dict = hg38.chrom_sizes,
            input_dim: int = 2114,
            output_dim: int = 1000,
            shift: int = 0,
            reverse_complement: bool = False, # randomly apply reverse complement
            sigma: float = 2, # smooth the signal values
            window: int = 10, # window size for smoothing
            train_split: list = ["chr2", "chr4", "chr5", "chr7", "chr10", "chr11", "chr12", "chr13", "chr14",
                            "chr15", "chr16", "chr17", "chr18", "chr19", "chr21", "chr22", "chrX"],
            val_split: list= ['chr8', 'chr9', 'chr20'],
            test_split: list= ['chr1', 'chr3', 'chr6'],
            batch_size: int = 64,
            num_workers: int = 8, 
        ):
        
        super().__init__()
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.args = (plus, minus, ctl_plus, ctl_minus, genome, input_dim, output_dim)
        self.region_df = load_region_df(peak_bed, chrom_sizes=chrom_sizes, input_dim=input_dim, shift=shift)
        self.train_df = self.region_df[self.region_df[0].isin(train_split)]
        self.val_df = self.region_df[self.region_df[0].isin(val_split)]
        self.test_df = self.region_df[self.region_df[0].isin(test_split)]
        self.shift = shift
        

    def setup(self, stage=None):
        
        if stage == 'fit':
            self.train_dataset = HistoneDataset(self.train_df, *self.args, shift=self.shift)
            self.val_dataset = HistoneDataset(self.val_df, *self.args, shift=self.shift)
        else:
            self.train_dataset = HistoneDataset(self.train_df, *self.args, shift=0, reverse_compliment=False)
            self.val_dataset = HistoneDataset(self.val_df, *self.args, shift=0, reverse_compliment=False)
            self.dataset = HistoneDataset(self.region_df, *self.args, shift=0, reverse_compliment=False)

        print(f"Training set size: {len(self.train_dataset)}", flush=True)
        print(f"Validation set size: {len(self.val_dataset)}", flush=True)

        if stage == 'test':
            self.test_dataset = HistoneDataset(self.test_df, *self.args, shift=0, reverse_compliment=False)
        
            print(f"Test set size: {len(self.test_dataset)}", flush=True)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=self.num_workers)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)
    
    def test_dataloader(self):
        return torch.utils.data.DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)
    
    def total_dataloader(self):
        return torch.utils.data.DataLoader(self.dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)


def get_chrom_sizes(chrom_size_file):
    chrom_sizes=open(chrom_size_file,'r').readlines()
    chrom_size_dict = {}
    for row in chrom_sizes:
        row = row.strip()
        chrom,size = row.split("\t")
        chrom_size_dict[chrom] = int(size)

    return chrom_size_dict


def load_region_df(peak_bed, chrom_sizes, input_dim=71000, shift=1000):
    """
    Filters regions in the DataFrame that exceed defined chromosome sizes.

    Parameters:
    - df (pd.DataFrame): DataFrame with columns 'chr', 'start', and 'end'.
    - chrom_sizes (dict): Dictionary with chromosome names as keys and sizes as values.

    Returns:
    - pd.DataFrame: Filtered DataFrame where no region exceeds the chromosome boundaries.
    """
    # Apply filter to check each row
    # Assume column0 is chr, column 9 is the summit
    df = pd.read_csv(peak_bed, sep='\t', header=None)
    flank_length = input_dim // 2 + shift
    filtered_df = df[df.apply(lambda row: row.iloc[9] + row.iloc[1] -  flank_length > 0 
                              and row.iloc[9] + row.iloc[1] + flank_length <= int(chrom_sizes.get(row.iloc[0], float('inf'))), axis=1)]
    return filtered_df
