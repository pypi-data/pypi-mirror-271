import pytest

from histomer.test import check_one_hot_and_reverse_complement, is_reverse_complement, is_reversed_profile

def test_check_one_hot_and_reverse_complement():
    check_one_hot_and_reverse_complement()

def test_is_reverse_complement():
    seq1 = "AGTCN"
    seq2 = "NGACT"
    assert is_reverse_complement(seq1, seq2)

def test_is_reversed_profile():
    import numpy as np
    profile1 = np.array([1, 2, 3, 4, 5])
    profile2 = np.array([5, 4, 3, 2, 1])
    assert is_reversed_profile(profile1, profile2)

def test_dataset():
    from histomer.data import HistoneDataset
    dataset = HistoneDataset()
    assert len(dataset) > 0



if __name__ == "__main__":
    pytest.main([__file__])
    # test_check_one_hot_and_reverse_complement()
    # test_is_reverse_complement()
    # test_is_reversed_profile()