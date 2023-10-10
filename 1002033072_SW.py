class Solution:
    def local_alignment(self, sequence_A: str, sequence_B:str, substitution: dict, gap: int) -> [tuple]:
        num_cols = len(sequence_B) + 1
        num_rows = len(sequence_A) + 1
        matrix = [[0 for i in range(num_cols)] for j in range(num_rows)]
        
        directions = self.calc_directions(matrix, gap, num_rows, num_cols, sequence_A, sequence_B, substitution, is_local=True)
        print('Local Alignment matrix is: ')
        for row in matrix:
            print(row)
            
        print('\nDirections are :')
        for row in directions:
            print(row)        # now traceback, by starting the bottom right of the matrix
        
        print('\n')
        paths_traced = self.local_traceback_helper(directions, matrix)
        all_alignments = []
        for path_list in paths_traced:
            calculated_alignment = self.calc_alignment(path_list[-1::-1], sequence_A, sequence_B, True)
            if calculated_alignment != []:
                for entry in calculated_alignment:
                    all_alignments.append(entry)
                    
        # print('Paths are:')
        # print(paths_traced)
        
        return all_alignments
    
    def traceback(self, directions, matrix, i, j, path_traced, is_local=False):
        current_element = matrix[i][j]
        # print('Current traceback: ' + str(path_traced))
        
        if i == j and i == 0 and not is_local:
            path_traced.append((0, 0))
            return path_traced
        
        # assumes there's only one valid direction??
        for direction in directions[i][j]:
            # print('Current direction: ' + str(direction))
            path_traced.append((i, j))
            # print('Current path_traced: ' + str(path_traced))
            if direction == 'diag':
                return self.traceback(directions, matrix, i - 1, j - 1, path_traced)
            if direction == 'left':
                return self.traceback(directions, matrix, i, j - 1, path_traced)
            elif direction == 'top':
                return self.traceback(directions, matrix, i - 1, j, path_traced)
        
        return path_traced
    
    def find_max_index_and_val(self, matrix):
        # returns a tuple with i, j & max_val
        current_max = -999999  # arbitraty value
        max_i, max_j = -1, -1
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] > current_max:
                    max_i, max_j = i, j
                    current_max = matrix[i][j]
                    
        return max_i, max_j, current_max
    
    def is_matrix_zeros(self, matrix):
        current_sum = 0
        for row in matrix:
            current_sum += sum(row)
        
        if current_sum == 0:
            return True
        return False
    
    def set_max_path_to_zeros(self, matrix, path_traced):
        for entry in path_traced:
            # print('Setting entry to 0: ' + str(entry))
            matrix[entry[0]][entry[1]] = 0
    
    def local_traceback_helper(self, directions, matrix):
        all_paths = []
        i, j, max_val = self.find_max_index_and_val(matrix)
        while (not self.is_matrix_zeros(matrix)):
            # print('Helper tracing path for max_val: ' + str(max_val))
            path_traced = self.traceback(directions, matrix, i, j, [])
            self.set_max_path_to_zeros(matrix, path_traced)
            all_paths.append(path_traced)
            i, j, max_val = self.find_max_index_and_val(matrix)
            
            
        return all_paths
    
    def fill_gap_values(self, matrix, num_rows, num_cols, gap):
        # fill the first row & first column with the gap values
        curr_gap = 0
        for j in range(num_cols):
            matrix[0][j] = curr_gap
            curr_gap += gap
            
        curr_gap = 0
        for i in range(num_rows):
            matrix[i][0] = curr_gap
            curr_gap += gap
            
    def calc_directions(self, matrix, gap, num_rows, num_cols, sequence_A, sequence_B, substitution, is_local=False):
        directions = [[[] for i in range(num_cols)] for j in range(num_rows)]
        # now navigate the matrix & perform the global alignment
        for i in range(1, num_rows):
            for j in range(1, num_cols):
                left_val = matrix[i][j - 1] + gap
                top_val = matrix[i - 1][j] + gap
                diag_val = matrix[i - 1][j - 1] + substitution[sequence_A[i - 1]][sequence_B[j - 1]]
                if (is_local):
                    left_val, top_val, diag_val = max(left_val, 0), max(top_val, 0), max(diag_val, 0)
                max_val = max(left_val, top_val, diag_val)
                matrix[i][j] = max_val
                
                # check if this simplification works
                if (is_local and max_val == 0):
                    continue
                
                if (left_val == max_val):
                    directions[i][j].append('left')
                if (top_val == max_val):
                    directions[i][j].append('top')
                if (diag_val == max_val):
                    directions[i][j].append('diag')
                    
        return directions
    
    def calc_alignment(self, path_traced, sequence_A, sequence_B, is_local=False):
        alignment_seq_a = ''
        alignment_seq_b = ''
        first_time_local = True
        
        # TODO: error handling
        for i in range(1, len(path_traced)):
            previous_path = path_traced[i-1]
            current_path = path_traced[i]
            if (is_local and first_time_local):
                alignment_seq_a += sequence_A[previous_path[0] - 1]
                alignment_seq_b += sequence_B[previous_path[1] - 1]
                first_time_local = False
            
            # print('Previous path: ' + str(previous_path))
            # print('Current path: ' + str(current_path))
            # current_path direction was top
            if (current_path[0] - previous_path[0] == 1 and current_path[1] == previous_path[1]):
                alignment_seq_a += sequence_A[current_path[0] - 1]
                alignment_seq_b += '-'
                
            elif (current_path[1] - previous_path[1] == 1 and current_path[0] == previous_path[0]):
                alignment_seq_a += '-'
                alignment_seq_b += sequence_B[current_path[1] - 1]
                
            elif (current_path[0] - previous_path[0] == 1 and current_path[1] - previous_path[1] == 1):
                alignment_seq_a += sequence_A[current_path[0] - 1]
                alignment_seq_b += sequence_B[current_path[1] - 1]
             
        if (alignment_seq_a == alignment_seq_b and alignment_seq_a == ''):
            return []
        return [(alignment_seq_a, alignment_seq_b)]
