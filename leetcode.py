word1 = "day"
word2 = "night"
sol = []
totallen = len(word1) + len(word2)
# throwing err when going above index 0??
try:
    if min(len(word2),len(word1)) == len(word1): # if word1 is smaller
        for i in range(len(word1)):
            sol.append(word1[i])
            sol.append(word2[i])
    # ^^ appends until we hit that index error (for loop goes out of range of smallerWord(word1))
    listlength = len(sol) # length of list so far, should be equal to double the length of word1
    for i in range(listlength-len(word2)): # for i in the differrence between the lenght of list inus the word with chars remaining(8-6=2)
        sol.append(word2[len(word1)+i]) # appends everything after len(word1)=4
    if min(len(word2),len(word1)) == len(word2): ### if word2 is smaller
        for i in range(len(word2)): # for i in the range of length of smaller word
            sol.append(word1[i]) ## append 
            sol.append(word2[i])
    listlengthTwo = len(sol)
    print(listlengthTwo)
    for i in range(listlengthTwo - len(word2)):
        sol.append(word1[len(word2)+i]) ## append word1[7+0,1]
except IndexError:
    print(sol)
"""
get total length
for i in range(total length(0, 10))
    sol.append(word1[i]) appends position 0 of word1, in this case 'b'
    sol.append(word2[i]) appends position 0 of word2

resets and starts appending position 1 of word1
once i > len(word1) we only want to append word2
    if i > len(word1):
        for i in word1[i:]:
            sol.append(i)
"""