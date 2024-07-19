class Solution:
    @staticmethod
    def merge_alternatively(word1, word2):
        sol = []
        totallen = len(word1) + len(word2)
        try:
            if min(len(word2), len(word1)) == len(word1):  # if word1 is smaller
                for i in range(len(word1)):
                    sol.append(word1[i])
                    sol.append(word2[i])
            listlength = len(sol)  # length of list so far, should be equal to double the length of word1
            for i in range(listlength - len(word2)):  # for i in the difference between the length of list minus the word with chars remaining (8-6=2)
                sol.append(word2[len(word1) + i])  # appends everything after len(word1)=4
            if min(len(word2), len(word1)) == len(word2):  # if word2 is smaller
                for i in range(len(word2)):  # for i in the range of length of smaller word
                    sol.append(word1[i])  # append
                    sol.append(word2[i])
            listlengthTwo = len(sol)
            for i in range(listlengthTwo - len(word2)):
                sol.append(word1[len(word2) + i])  # append word1[7+0,1]
            return sol
        except IndexError:
            return sol
mysol = Solution.merge_alternatively("goadig","dinglon")
print(mysol)
result = ''.join(mysol)
print(result)