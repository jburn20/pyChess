# Test case 1: word1 is smaller than word2
assert Solution.merge_alternatively("abc", "123") == ['a', '1', 'b', '2', 'c', '3']

# Test case 2: word2 is smaller than word1
assert Solution.merge_alternatively("hello", "world") == ['h', 'w', 'e', 'o', 'l', 'r', 'l', 'l', 'o', 'd']

# Test case 3: word1 and word2 have the same length
assert Solution.merge_alternatively("abc", "def") == ['a', 'd', 'b', 'e', 'c', 'f']

# Test case 4: word1 is an empty string
assert Solution.merge_alternatively("", "123") == ['1', '2', '3']

# Test case 5: word2 is an empty string
assert Solution.merge_alternatively("abc", "") == ['a', 'b', 'c']

# Test case 6: both word1 and word2 are empty strings
assert Solution.merge_alternatively("", "") == []

print("All test cases passed!")