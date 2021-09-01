import numpy as np

# generates an empty matrix with adequate size for variables and constraints.
def gen_matrix(var,cons):
	#[[0]*(cons+1)]*(var + cons + 2)
    tab = np.zeros((cons+1, var+cons+2))
    print("generated")
    return tab

# checks the furthest right column for negative values ABOVE the last row. If negative values exist, another pivot is required.
def next_round_r(table):
    m = min(table[:-1,-1])
    if m>= 0:
        return False
    else:
        return True

# checks that the bottom row, excluding the final column, for negative values. If negative values exist, another pivot is required.
def next_round(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m>=0:
        return False
    else:
        return True

# Similar to next_round_r function, but returns row index of negative element in furthest right column
def find_neg_r(table):
    # lc = number of columns, lr = number of rows
    lc = len(table[0,:])
    # search every row (excluding last row) in final column for min value
    m = min(table[:-1,lc-1])
    if m<=0:
        # n = row index of m location
        n = np.where(table[:-1,lc-1] == m)[0][0]
    else:
        n = None
    return n

#returns column index of negative element in bottom row
def find_neg(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m<=0:
        # n = row index for m
        n = np.where(table[lr-1,:-1] == m)[0][0]
    else:
        n = None
    return n

# locates pivot element in tableu to remove the negative element from the furthest right column.
def loc_piv_r(table):
        total = []
        # r = row index of negative entry
        r = find_neg_r(table)
        # finds all elements in row, r, excluding final column
        row = table[r,:-1]
        # finds minimum value in row (excluding the last column)
        m = min(row)
        # c = column index for minimum entry in row
        c = np.where(row == m)[0][0]
        # all elements in column
        col = table[:-1,c]
        # need to go through this column to find smallest positive ratio
        for i, b in zip(col,table[:-1,-1]):
            # i cannot equal 0 and b/i must be positive.
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,c]
# similar process, returns a specific array element to be pivoted on.
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i,b in zip(table[:-1,n],table[:-1,-1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # placeholder for elements that did not satisfy the above requirements. Otherwise, our index number would be faulty.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,n]

# Takes string input and returns a list of numbers to be arranged in tableu
def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

# The final row of the tablue in a minimum problem is the opposite of a maximization problem so elements are multiplied by (-1)
def convert_min(table):
    table[-1,:-2] = [-1*i for i in table[-1,:-2]]
    table[-1,-1] = -1*table[-1,-1]
    return table

# generates x1,x2,...xn for the varying number of variables.
def gen_var(table):
    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

# pivots the tableau such that negative elements are purged from the last row and last column
def pivot(row,col,table):
    # number of rows
    lr = len(table[:,0])
    # number of columns
    lc = len(table[0,:])
	#t = [[0]*lr]*lc
    t = np.zeros((lr,lc))
    pr = table[row,:]
    if table[row,col]**2>0: #new
        e = 1/table[row,col]
        r = pr*e
        for i in range(len(table[:,col])):
            k = table[i,:]
            c = table[i,col]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# checks if there is room in the matrix to add another constraint
def add_cons(table):
    lr = len(table[:,0])
    # want to know IF at least 2 rows of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j**2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There are at least 2 rows with all zero elements if the following is true
    if len(empty)>1:
        return True
    else:
        return False

# adds a constraint to the matrix
def constrain(table,eq):
    if add_cons(table) == True:
        lc = len(table[0,:])
        lr = len(table[:,0])
        var = lc - lr -1
        # set up counter to iterate through the total length of rows
        j = 0
        while j < lr:
            # Iterate by row
            row_check = table[j,:]
            # total will be sum of entries in row
            total = 0
            # Find first row with all 0 entries
            for i in row_check:
                total += float(i**2)
            if total == 0:
                # We've found the first row with all zero entries
                row = row_check
                break
            j +=1

        eq = convert(eq)
        i = 0
        # iterate through all terms in the constraint function, excluding the last
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]
            i +=1
        #row[len(eq)-1] = 1
        row[-1] = eq[-1]

        # add slack variable according to location in tableau.
        row[var+j] = 1
    else:
        print('Cannot add another constraint.')

# checks to determine if an objective function can be added to the matrix
def add_obj(table):
    lr = len(table[:,0])
    # want to know IF exactly one row of all zero elements exist
    empty = []
    # iterate through each row
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use squared value so (-x) and (+x) don't cancel each other out
            total += j**2
        if total == 0:
            # append zero to list ONLY if all elements in a row are zero
            empty.append(total)
    # There is exactly one row with all zero elements if the following is true
    if len(empty)==1:
        return True
    else:
        return False

# adds the onjective functio nto the matrix.
def obj(table,eq):
    if add_obj(table)==True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:,0])
        row = table[lr-1,:]
        i = 0
    # iterate through all terms in the constraint function, excluding the last
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]*-1
            i +=1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')

# solves maximization problem for optimal solution, returns dictionary w/ keys x1,x2...xn and max.
def maxz(table, output='summary'):
    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1,-1]
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return val

# solves minimization problems for optimal solution, returns dictionary w/ keys x1,x2...xn and min.
def minz(table, output='summary'):
    print("entered min")
    table = convert_min(table)

    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['min'] = table[-1,-1]*-1
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return val

#if __name__ == "__main__":
m = gen_matrix(50, 38)
constrain(m,'187,180,164,191,176,165,534,29,125,19,32,191,22,32,15,37,34,41,18,53,20,31,43,43,25,13,31,25,30,25,149,14,25,22,32,40,81,34,22,20,26,16,48,149,160,11,28,120,210,0,L,2200')
constrain(m,'9.04,8.23,7.25,8.37,8.06,8.38,18.29,1.1,1.87,1.8,3.02,1.42,2.2,2.6,1.36,1.12,2.82,0.93,0.88,2.89,2.2,1.83,1.61,3.38,1.28,1.5,1.43,1.92,3.27,0.98,6.36,1.13,2.58,3.09,1.83,1.1,5.42,1.39,0.91,0.86,0.99,0.68,1.18,6.36,2,2.3,0.9,4.38,8.23,0,L,30')

constrain(m,'0.32,0.3,2.7,0.32,0.3,1.67,1.55,2.5,1.61,1.1,0.46,1.77,0.5,4.4,0.78,0.22,1.7,4.74,2.63,0.99,1.88,3.26,6.76,2.2,3.2,1.18,3.83,1.91,1.85,3.53,1,1.38,2.05,1.98,2.33,4.24,5.67,4.71,3.03,2.4,4.2,1.86,7.99,1,0.66,0.2,3.8,0.87,4.46,0,L,40')

constrain(m,'0,0,0,0,0,0,0,0,3,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,L,750')

constrain(m,'0,0,0,0,0,0,0,0,17,0,0,11,0,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,L,2700')

constrain(m,'0,0,0,0,0,0,0,1,18,306,251,13,316,346,370,102,31,835,42,1,38,35,2,38,5,223,56,0,218,1,0,198,119,0,50,0,38,51,67,18,157,0,0,0,7,160,0,0,1,0,G,850.0')

constrain(m,'0.104,0.215,0.142,0.17,0.141,0.149,1.644,0.04,0.1,0.04,0.054,0.082,0.1,0.08,0.07,0.057,0.071,0.066,0.037,0.05,0.143,0.082,0.031,0.139,0.061,0.04,0.064,0.05,0.078,0.039,0.2,0.056,0.044,0.081,0.055,0.046,0.266,0.056,0.056,0.057,0.054,0.012,0.008,0.2,0.067,0.09,0.04,0.107,0.102,0,G,1.4')

constrain(m,'0.041,0.052,0.049,0.055,0.051,0.064,0.161,0.02,0.021,0.09,0.13,0.048,0.22,0.26,0.08,0.06,0.117,0.058,0.019,0.089,0.141,0.104,0.04,0.09,0.04,0.07,0.069,0.06,0.115,0.037,0.11,0.053,0.086,0.402,0.08,0.027,0.132,0.078,0.048,0.028,0.085,0.039,0.024,0.11,0.13,0.12,0.03,0.11,0.056,0,G,1.6')

constrain(m,'0.124,0.446,0.372,0.281,0.51,0.936,3.08,0.1,1.324,0.4,0.742,0.845,0.4,1,0.375,0.302,0.639,0.983,0.594,1.11,0.978,0.734,0.334,0.745,0.234,0.5,0.418,0.507,0.647,0.649,0.7,0.249,0.305,3.607,0.525,0.116,2.09,1.262,0.655,0.48,0.979,0.254,0.386,0.7,1.738,0.2,0.4,0.41,0.464,0,G,15.0')

constrain(m,'0.124,0.446,0.372,0.281,0.51,0.936,3.08,0.1,1.324,0.4,0.742,0.845,0.4,1,0.375,0.302,0.639,0.983,0.594,1.11,0.978,0.734,0.334,0.745,0.234,0.5,0.418,0.507,0.647,0.649,0.7,0.249,0.305,3.607,0.525,0.116,2.09,1.262,0.655,0.48,0.979,0.254,0.386,0.7,1.738,0.2,0.4,0.41,0.464,0,L,300')

constrain(m,'0.082,0.061,0.142,0.202,0.106,0.157,0.473,0.08,0.312,0.099,0.165,0.1,0.106,0.247,0.09,0.032,0.175,0.138,0.08,0.081,0.091,0.141,0.067,0.219,0.124,0.194,0.209,0.184,0.138,0.084,1.235,0.066,0.073,0.104,0.061,0.12,0.169,0.463,0.247,0.224,0.291,0.071,0.073,1.235,0.257,0.129,0.09,0.123,0.123,0,G,1.4')

constrain(m,'0.082,0.061,0.142,0.202,0.106,0.157,0.473,0.08,0.312,0.099,0.165,0.1,0.106,0.247,0.09,0.032,0.175,0.138,0.08,0.081,0.091,0.141,0.067,0.219,0.124,0.194,0.209,0.184,0.138,0.084,1.235,0.066,0.073,0.104,0.061,0.12,0.169,0.463,0.247,0.224,0.291,0.071,0.073,1.235,0.257,0.129,0.09,0.123,0.123,0,L,55')

constrain(m,'72,132,73,152,115,160,87,11,9,14,129,24,15,80,38,76,63,19,15,89,52,33,109,61,43,66,18,57,105,22,3,34,97,17,64,19,65,25,23,10,46,25,57,3,81,9,15,42,152,0,G,240.0')

constrain(m,'72,132,73,152,115,160,87,11,9,14,129,24,15,80,38,76,63,19,15,89,52,33,109,61,43,66,18,57,105,22,3,34,97,17,64,19,65,25,23,10,46,25,57,3,81,9,15,42,152,0,L,1300')

constrain(m,'0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.04,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,G,2.4')

constrain(m,'0,0,0,0.7,1.1,1.3,0.6,53,12.1,30,35.3,18.2,30,69,9.2,3.2,89.2,5.9,13.7,7.4,5.6,12.2,4.9,85,36.6,45,57,48.2,58.1,2.2,31.2,6,15,2.1,18.8,7.4,40,131.2,97,80.4,127.7,14.8,24.9,31.2,10,43,21,0,1.1,0,G,200.0')

constrain(m,'0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,L,50')

constrain(m,'1.64,1.57,0.93,1.64,0.79,0.86,0.31,0.15,0.52,1.89,2.26,0.52,1.5,0.7,0.22,0.68,0.78,0.66,0.54,0.19,1.13,0.41,0.04,0.88,0.15,0.09,0.11,0.08,0.21,0.3,0.08,0.2,0.43,0.01,0.55,0.02,0.13,2.13,0.79,0.37,1.58,0,0.01,0.08,2.07,1,0.03,0.63,1.09,0,G,7.0')

constrain(m,'1.64,1.57,0.93,1.64,0.79,0.86,0.31,0.15,0.52,1.89,2.26,0.52,1.5,0.7,0.22,0.68,0.78,0.66,0.54,0.19,1.13,0.41,0.04,0.88,0.15,0.09,0.11,0.08,0.21,0.3,0.08,0.2,0.43,0.01,0.55,0.02,0.13,2.13,0.79,0.37,1.58,0,0.01,0.08,2.07,1,0.03,0.63,1.09,0,L,800')

constrain(m,'10.9,10.7,9.5,10.9,15.5,9.2,4.3,0,4.1,830,437.1,4.5,400,541.9,126.3,207.5,101.6,13.2,7.9,14.8,41.6,43,0.2,177,76,45.5,38.2,15.5,212.7,3.5,1.7,75.2,108.6,0,207,0.4,24.8,16.2,6.5,7.4,4.9,1.3,1.3,1.7,21,250,0.1,0,11.4,0,G,75.0')

constrain(m,'84,25,16,43,26,18,255,26,5,51,232,17,117,81,36,45,47,33,10,21,24,37,16,42,40,105,45,22,92,9,181,27,160,3,72,23,25,13,9,10,7,25,56,181,12,120,30,17,46,50,L,2300')

constrain(m,'105,130,103,137,132,167,642,16,48,46,25,28,41,76,29,22,66,35,24,73,52,38,40,69,26,37,30,44,58,24,153,24,52,86,37,29,108,34,22,20,26,20,31,153,52,60,27,151,156,0,G,1000.0')

constrain(m,'105,130,103,137,132,167,642,16,48,46,25,28,41,76,29,22,66,35,24,73,52,38,40,69,26,37,30,44,58,24,153,24,52,86,37,29,108,34,22,20,26,20,31,153,52,60,27,151,156,0,L,3000')

constrain(m,'59,65,40,46,42,33,392,8,24,81,27,22,70,38,13,13,21,12,11,42,14,25,23,23,12,19,16,15,42,14,25,10,47,9,20,10,33,19,11,10,12,10,27,25,29,21,11,64,45,0,G,340.0')

constrain(m,'3.45,1.96,2.23,1.95,2.74,3.11,5.73,0.6,0.34,1.8,0.47,0.28,2.57,1.3,0.86,0.7,0.73,0.3,0.27,0.61,2.14,1.03,0.8,1.4,0.47,0.8,0.8,0.42,1.6,0.23,1.7,0.64,1.46,0.5,1.48,0.21,1.47,0.64,0.37,0.34,0.43,0.34,0.42,1.7,0.55,0.2,0.3,1.48,2.7,0,G,7.0')

constrain(m,'3.45,1.96,2.23,1.95,2.74,3.11,5.73,0.6,0.34,1.8,0.47,0.28,2.57,1.3,0.86,0.7,0.73,0.3,0.27,0.61,2.14,1.03,0.8,1.4,0.47,0.8,0.8,0.42,1.6,0.23,1.7,0.64,1.46,0.5,1.48,0.21,1.47,0.64,0.37,0.34,0.43,0.34,0.42,1.7,0.55,0.2,0.3,1.48,2.7,0,L,50')

constrain(m,'1.28,1.04,0.88,0.91,1,1.18,4.34,0.06,0.28,0.36,0.21,0.36,0.38,0.23,0.18,0.67,0.41,0.24,0.17,0.4,0.54,0.24,0.35,0.42,0.18,0.19,0.22,0.27,0.56,0.16,1.16,0.16,0.47,0.52,0.39,0.17,1.24,0.2,0.17,0.13,0.25,0.28,0.83,1.16,0.64,0.11,0.27,1.09,1.42,0,G,12.0')

constrain(m,'1.28,1.04,0.88,0.91,1,1.18,4.34,0.06,0.28,0.36,0.21,0.36,0.38,0.23,0.18,0.67,0.41,0.24,0.17,0.4,0.54,0.24,0.35,0.42,0.18,0.19,0.22,0.27,0.56,0.16,1.16,0.16,0.47,0.52,0.39,0.17,1.24,0.2,0.17,0.13,0.25,0.28,0.83,1.16,0.64,0.11,0.27,1.09,1.42,0,L,40')


constrain(m,'0.267,0.194,0.218,0.204,0.225,0.233,1.22,0.037,0.204,0.179,0.046,0.104,0.191,0.17,0.029,0.084,0.049,0.045,0.059,0.127,0.189,0.069,0.075,0.07,0.019,0.021,0.017,0.039,0.157,0.081,0.299,0.027,0.076,0.318,0.083,0.039,0.176,0.088,0.049,0.066,0.017,0.05,0.058,0.299,0.19,0.077,0.085,0.191,0.327,0,G,0.9')

constrain(m,'0.267,0.194,0.218,0.204,0.225,0.233,1.22,0.037,0.204,0.179,0.046,0.104,0.191,0.17,0.029,0.084,0.049,0.045,0.059,0.127,0.189,0.069,0.075,0.07,0.019,0.021,0.017,0.039,0.157,0.081,0.299,0.027,0.076,0.318,0.083,0.039,0.176,0.088,0.049,0.066,0.017,0.05,0.058,0.299,0.19,0.077,0.085,0.191,0.327,0,L,10')

constrain(m,'1.2,1.1,4.2,5.8,1.1,2.6,25.4,0.4,0.3,0.9,1.3,0.7,0.9,0.9,0.6,0.2,2.5,0.1,0,0.2,2.3,0.6,0.7,1.6,0.3,0.5,0.6,0.6,0.9,0.3,14.2,0.4,0.3,9.3,0.6,0.5,1.8,0.4,0,0,0.1,0.6,2.8,14.2,0.4,0.9,0.7,2.8,3.4,0,G,30.0')

constrain(m,'1.2,1.1,4.2,5.8,1.1,2.6,25.4,0.4,0.3,0.9,1.3,0.7,0.9,0.9,0.6,0.2,2.5,0.1,0,0.2,2.3,0.6,0.7,1.6,0.3,0.5,0.6,0.6,0.9,0.3,14.2,0.4,0.3,9.3,0.6,0.5,1.8,0.4,0,0,0.1,0.6,2.8,14.2,0.4,0.9,0.7,2.8,3.4,0,L,280')

constrain(m,'521,330,472,405,375,343,813,138,372,379,213,282,762,606,194,238,316,320,237,286,202,211,325,389,170,252,243,299,296,229,401,168,369,318,276,146,244,285,188,175,211,233,246,401,485,330,191,171,270,2,G,2500.0')


constrain(m,'521,330,472,405,375,343,813,138,372,379,213,282,762,606,194,238,316,320,237,286,202,211,325,389,170,252,243,299,296,229,401,168,369,318,276,146,244,285,188,175,211,233,246,401,485,330,191,171,270,2,L,2800')

constrain(m,'221,217,218,217,218,218,30,2,167,213,17,146,226,14,28,140,33,69,5,60,2,6,78,25,18,65,27,30,3,2,17,19,27,5,16,4,5,6,3,3,4,39,420,17,7,41,67,163,222,38700,G,600.0')

constrain(m,'0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,L,0')

constrain(m,'0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,L,0')

constrain(m,'0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,L,0')
obj(m, '1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0')
print(minz(m))
