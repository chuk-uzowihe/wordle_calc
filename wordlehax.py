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
    wlen = len(wordl)
    if wlen == 1:
        return (wordl[0], 0)

    arrc = [0] * 3**5
    max = (None, 0)

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

    while True:
        bes = best(wordlist)
        print("best of " + str(len(wordlist)) +  " word(s) is: " + bes[0] + " (" + str(bes[1]) + " total info)")
        if len(wordlist) == 1:
            print("done")
            return

        inp = input("choose input: ").strip()
        while not checkin(inp):
            if inp == "" or inp.lower() == "exit" or  inp.lower() == "quit" or inp.lower() == "q":
                return
            inp = input("try input again: ").strip()

        wordlist = filter(wordlist, bes[0], conv(inp))
		
        if len(wordlist) == 0:
            print("no possible words")
            return

run()
