# Two Strings
# Hacker90
# 02/03/25

s1 = 'and'
s2 = 'art'

def twoStrings(s1, s2):

    # get all the substrings for string 1
    # get all the substrings for string 2

##    substrings1 = []
##    for i in range(len(s1)):
##        for j in range(i+1, len(s1)+1):
##            substrings1.append(s1[i:j])
##
##    print(substrings1)

    substrings1 = [s1[i:j] for i in range(len(s1)) for j in range(i+1, len(s1)+1)]
    print(substrings1)

##    substrings2 = []
##    for x in range(len(s2)):
##        for y in range(x+1, len(s2)+1):
##            substrings2.append(s2[x:y])
##    print(substrings2)

    substrings2 = [s2[x:y] for x in range(len(s2)) for y in range(x+1, len(s2)+1)]
    print(substrings2)

    # Best way to find common elements in two lists
    common_elements = set(substrings1).intersection(set(substrings2))
    print(common_elements)
    
    if common_elements:
        return 'YES'
    else:
        return 'NO'

twoStrings(s1, s2)
