from math import log

# 00000_3 - no words match
# 11111_3 - all words in wrong position
# 22222_3 - all words in right position (right)

def comp(word1, word2):
    final = 0
    wordsu = word2
    for i in range(5):
        final *= 3
        if word1[i] == word2[i]:
            wordsu = wordsu.replace(word1[i], "", 1)
            final += 2
        elif (word1[i] in wordsu):
            wordsu = wordsu.replace(word1[i], "", 1)
            final += 1
    return final

def best(wordl):
    arrc = [0] * 3**5
    max = (None, 0)
    wlen = len(wordl)

    for word in wordl:
        arrc = [0] * 3**5
        for wordc in wordl:
            arrc[comp(word, wordc)] += 1/wlen
        final_s = -sum([x * log(x) for x in arrc if x != 0])
        if final_s > max[1]:
            max = (word, final_s)

    return max

def conv(strr):
    if strr == "":
        return 0
    return int(strr[-1]) + conv(strr[:-1]) * 3

def filter(wordl, bes, seq):
    return [x for x in wordl if comp(bes, x) == seq]

def checkin(input):
    if len(input) != 5:
        return False
    for x in input:
        if x not in "012":

            return False
    return True

initwords = []
file = open("5lw.txt", "r")
for line in file.readlines():
    initwords.append(line.strip())

def run():
    print("input key:")
    print("0 - gray, 1 - yellow, 2 - green")
    print("e.g: 02100")
    print("================================\n")

    wordlist = initwords

    while(len(wordlist) > 0):
        bes = best(wordlist)
        if (bes[1] > 0):
            print("best word is: " + bes[0] + " (" + str(bes[1]) + " total info)")
        else:
            print("no more info to give")
            return

        inp = input().strip()
        while(not checkin(inp)):
            if inp == "":
                return
            inp = input().strip()

        wordlist = filter(wordlist, bes[0], conv(inp))
    print("no possible words")

run()
