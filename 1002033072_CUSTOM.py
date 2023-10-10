import numpy as np

imported_module = __import__('1002033072_SW')
s = imported_module.Solution()
UTA_ID_FILE = '1002033072_S.txt'


def dump_subs_dict(subs_dict, seq1, seq2):
    offset = len(seq1) - len(seq2)
    row_offset = 0
    col_offset = 0

    if offset < 0:
        seq1 = ''.join(['-' for i in range(abs(offset))]) + seq1
        row_offset += abs(offset)
    elif offset > 0:
        seq2 = ''.join(['-' for i in range(abs(offset))]) + seq2
        col_offset += offset
    else:
        seq1 = ''.join(['-' for i in range(1)]) + seq1
        row_offset += abs(offset)
        seq2 = ''.join(['-' for i in range(1 )]) + seq2
        col_offset += offset
    
    matrix = [[-1 for i in range(len(seq1))] for j in range(len(seq2))]

    # set the rows
    for i in range(len(seq1)):
        matrix[0][i] = seq1[i]

    # set the rows
    for j in range(len(seq2)):
        matrix[j][0] = seq2[j]

    for i in range(len(seq1)):
        for j in range(len(seq2)):
            if seq1[i] != '-' and seq2[j] != '-':
                matrix[i][j] = subs_dict[seq1[i]][seq2[j]]


    with open(UTA_ID_FILE, 'w') as fp:
        fp.write(str(np.matrix(matrix)))
    

def custom_alignment(firstname, lastname, compare_str, gap):
    name = firstname + lastname
    uniq_letters = set(name)
    english_alpha = 'abcdefghijklmnopqrstuvwxyz'
    substitution_dict = {}
    match_factor = 2
    semi_match_factor = 1
    mismatch_factor = -1
    for letter in english_alpha:
        substitution_dict[letter] = {}
        for letter2 in english_alpha:
            if (letter == letter2):
                substitution_dict[letter][letter2] = match_factor
            elif (letter in uniq_letters and letter2 in uniq_letters):  # semi matches
                substitution_dict[letter][letter2] = semi_match_factor
            else:
                substitution_dict[letter][letter2] = mismatch_factor
                
    uniq_letters_str = ''.join(uniq_letters)
    dump_subs_dict(substitution_dict, uniq_letters_str, uniq_letters_str)
    return s.local_alignment(name, compare_str, substitution_dict, gap)
    
firstname = 'devi'
lastname = 'kandimalla'
compare_str = 'thequickbrownfoxjumpsoverthelazydog'
gap = -2

# TODO: verify a couple of the custom alignments
alignments = custom_alignment(firstname, lastname, compare_str, gap)

print('Alignments generated:')
print(alignments)