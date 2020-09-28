#!/usr/bin/python

# Usage:
# python BinaryIndel.py aligned_file.faa name_of_outputfile

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

# The input file will be parsed through, for each ID, a list will be filled
# with 1's or 0's depending on the content in the line. 1 correspond to
# a gap (-) and 0 correspond to everything else. The list will after parsing
# be added to another list, so we end up with a list of lists, or matrix.

IDlist = []
matrix = []
index = 0
with open(infile,'r') as I1:
	for line in I1:
		if line.startswith('>'):
			line = line.split()
			IDlist.append(line[0])
			if index > 0:
				matrix.append(seqlist)
			seqlist = []
		else:
			line = line.rstrip()
			for char in line:
				if char == '-':
					seqlist.append(1)
				else:
					seqlist.append(0)
		index += 1
	matrix.append(seqlist)

# Edge trimming
# Check the maximum number of gaps in beginning and end, and trim all sequences correspondingly


# All the lists will be gone through, checked for gaps in the beginning
# and end. The maxium number of consecutive gaps in either end will be the
# number of removed nucleotides in the ends respectively.
maxgapindex = 0
maxendindex = 0
for L in matrix:
	gapindex = 0
#Checking beginning of all sequences to retrieve the max gap
	if L[0]==1:
		gapindex += 1
		for i in range(1,len(L)):
			if L[i] == 1:
				gapindex += 1
			else:
				if gapindex > maxgapindex:
					maxgapindex = gapindex
				break
	gapindex = 0
#Checking end of all sequences to retrieve max gap
        if L[-1] == 1:
                gapindex += 1
                for i in range(2,len(L)):
                        if L[-i] == 1:
                                gapindex += 1
                        else:
                                if gapindex > maxendindex:
                                        maxendindex = gapindex
				break

for i in range(len(matrix)):
	matrix[i] = matrix[i][maxgapindex:-maxendindex]


# Gap collapse

# This will add consecutive gaps together
# each "column" of the matrix will be added with the previous,
# if the sum of each row is either 0 or 2 (meaning that it was
# either two consecutive 0's or two consecutive 1's) in all of
# the rows, then one of the rows will be removed.
index = 1
for i in range(1,len(matrix[0])):
	for j in range(len(matrix)):
		if matrix[j][index]+matrix[j][index-1] == 0 or matrix[j][index]+matrix[j][index-1] == 2:
			collapse = True
		else:
			collapse = False
			break
	if collapse == True:
		for j in range(len(matrix)):
			del matrix[j][index]
		index = index-1
	index +=1

#Remove ambiguos overlap

# The previous step collapsed consecutive patterns, if there
# still exists two consecutive 1's, it must mean that there
# is an overlap, so the next step will calculate the sum
# for two consecutive elements in each row at a time, and
# if the sum is above 1, it means that it has been an overlap
# and both those columns will be removed. To not exclude
# double overlapping, the indexes are saved to later remove
# the columns.


indexlist = set()
for i in range(1,len(matrix[0])):
	for j in range(len(matrix)):
		if matrix[j][i]+matrix[j][i-1] > 1:
			indexlist.add(i-1)
			indexlist.add(i)


indexlist = list(indexlist)
indexlist.sort(reverse=True)
for k in indexlist:
	for j in range(len(matrix)):
		del matrix[j][k]

#Remove columns that are the same
# Following step will sum the columns, if the column is either 0 or
# the same as the number of rows, the column elements are identical
# and the column will be removed.
index = 0
for i in range(len(matrix[0])):
	count = 0
	for j in range(len(matrix)):
		count += matrix[j][index]
	if count == 0 or count == len(matrix):
		for k in range(len(matrix)):
			del matrix[k][index]
		index = index -1
	index += 1

with open(outfile, 'w') as O1:
	for i in range(len(matrix)):
		O1.write('{}\n{}\n'.format(IDlist[i],"".join(map(str,matrix[i]))))

