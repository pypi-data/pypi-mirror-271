from histomer.data import dna_to_one_hot, one_hot_to_dna, reverse_complement_onehot

def check_one_hot_and_reverse_complement():
    sequence = "ACGTNNAC"
    rc_sequence = "GTNNACGT"
    encoded = dna_to_one_hot(sequence)
    decoded = one_hot_to_dna(encoded)
    rc = reverse_complement_onehot(encoded)
    rc_decoded = one_hot_to_dna(rc)

    print("Original:", sequence)
    print("Decoded:", decoded)
    print("Reverse complement:", rc_decoded)
    print("Is reverse complement:", rc_sequence == rc_decoded)
    assert sequence == decoded
    assert rc_sequence == rc_decoded


def is_reverse_complement(seq1, seq2):
    """
    # Example usage:
    seq1 = "AGTCN"
    seq2 = "NGACT"
    print("Sequence 1:", seq1)
    print("Sequence 2:", seq2)
    print("Is reverse complement:", is_reverse_complement(seq1, seq2))
    """
    # Define a dictionary for complementing the nucleotides, including 'N'
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
    
    # Check if the lengths are the same
    if len(seq1) != len(seq2):
        return False
    
    # Compare each character in seq1 to the complement of the corresponding character from the end of seq2
    for i in range(len(seq1)):
        # Get complement of the current character in seq2 from the opposite end
        if complement.get(seq2[-1 - i], None) != seq1[i]:
            return False

    return True


def is_reversed_profile(profile1, profile2):
    """
    # Example usage:
    profile1 = np.array([1, 2, 3, 4, 5])
    profile2 = np.array([5, 4, 3, 2, 1])
    print("Profile 1:", profile1)
    print("Profile 2:", profile2)
    print("Is reverse profile:", is_reversed_profile(profile1, profile2))
    """
    # Check if the lengths are the same
    if len(profile1) != len(profile2):
        return False
    
    return (profile1 == profile2[::-1]).all()