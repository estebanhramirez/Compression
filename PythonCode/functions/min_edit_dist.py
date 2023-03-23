import numpy as np

def min_edit_distance(source, target, ins_cost = 1, del_cost = 1, rep_cost = 2):
    '''
    Input: 
        source: a string corresponding to the string you are starting with
        target: a string corresponding to the string you want to end with
        ins_cost: an integer setting the insert cost
        del_cost: an integer setting the delete cost
        rep_cost: an integer setting the replace cost
    Output:
        D: a matrix of len(source)+1 by len(target)+1 containing minimum edit distances
        med: the minimum edit distance (med) required to convert the source string to the target
    '''
    # use deletion and insert cost as  1
    m = len(source) 
    n = len(target) 
    #initialize cost matrix with zeros and dimensions (m+1,n+1) 
    D = np.zeros((m+1, n+1), dtype=int) 
    
    ### START CODE HERE (Replace instances of 'None' with your code) ###
    
    # Fill in column 0, from row 1 to row m, both inclusive
    for row in range(1,m+1): # Replace None with the proper range
        D[row,0] = D[row-1,0]+del_cost
        
    # Fill in row 0, for all columns from 1 to n, both inclusive
    for col in range(1,n+1): # Replace None with the proper range
        D[0,col] = D[0,col-1]+ins_cost
        
    # Loop through row 1 to row m, both inclusive
    for row in range(1,m+1):

        # Loop through column 1 to column n, both inclusive
        for col in range(1,n+1):

            # Intialize r_cost to the 'replace' cost that is passed into this function
            r_cost = rep_cost

            # Check to see if source character at the previous row
            # matches the target character at the previous column, 
            if source[row-1] == target[col-1]: # Replace None with a proper comparison
                # Update the replacement cost to 0 if source and target are the same
                r_cost = 0

            # Update the cost at row, col based on previous entries in the cost matrix
            # Refer to the equation calculate for D[i,j] (the minimum of three calculated costs)
            D[row,col] = min(D[row-1, col]+del_cost, D[row,col-1]+ins_cost, D[row-1,col-1]+r_cost)

    # Set the minimum edit distance with the cost found at row m, column n 
    med = D[m,n]
    
    ### END CODE HERE ###
    return D, med

def backtrace(D):
    n, m = D.shape
    T = np.zeros((n, m), dtype=int)
    i, j = n-1, m-1
    flag = True
    path = []
    while flag:
        path.append((i, j))
        if (i - 1) < 0 or (j - 1) < 0:
            if (i - 1) < 0 and (j - 1) < 0:
                flag = False
            else:
                if (j - 1) < 0:
                    T[i, j] = -1
                    i -= 1
                elif (i - 1) < 0:
                    T[i, j] = +1
                    j -= 1
                else:
                    if D[i, j-1] <= D[i-1, j-1] and D[i, j-1] <= D[i-1, j]:
                        T[i, j] = +1
                        j -= 1
                    elif D[i-1, j] <= D[i-1, j-1] and D[i-1, j] <= D[i, j-1]:
                        T[i, j] = -1
                        i -= 1
                    elif D[i-1, j-1] <= D[i, j-1] and D[i-1, j-1] <= D[i-1, j]:
                        T[i, j] = 2
                        i -= 1
                        j -= 1
        else:
            if D[i-1, j-1] == D[i, j]:
                T[i, j] = 0
                i -= 1
                j -= 1
            else:
                if D[i, j-1] <= D[i-1, j-1] and D[i, j-1] <= D[i-1, j]:
                    T[i, j] = +1
                    j -= 1
                elif D[i-1, j] <= D[i-1, j-1] and D[i-1, j] <= D[i, j-1]:
                    T[i, j] = -1
                    i -= 1
                elif D[i-1, j-1] < D[i, j-1] and D[i-1, j-1] <= D[i-1, j]:
                    T[i, j] = 2
                    i -= 1
                    j -= 1
    return T, path[::-1]


D_matrix, min_edit_distance = min_edit_distance('abbaabb','baba', ins_cost = 1, del_cost = 1, rep_cost = 1)
print(min_edit_distance)
print(D_matrix)

T_matrix, path_vector = backtrace(D_matrix)

print(path_vector)
