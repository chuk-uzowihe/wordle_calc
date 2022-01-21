from math import log
import numpy as np

# 00000_3 - no words match
# 11111_3 - all words in wrong position
# 22222_3 - all words in right position (right)


def w_comp(given, correct):
    values = [(2 if given[i] == correct[i] else None) for i in range(5)]
    correct_exc = [correct[i] for i in range(5) if values[i] == None]
    final = 0
    for i in range(5):
        final *= 3
        if values[i] == None:
            if given[i] in correct_exc:
                values[i] = 1
                correct_exc.remove(given[i])
            else:
                values[i] = 0
        final += values[i]
    return final

def best(words, valid):

    if len(valid) == 1:
        return (valid["word"][0], 0)

    ftot = np.sum(valid["freq"])
    normalizer = np.vectorize(lambda x: x/ftot, otypes=[float])
    normalv = normalizer(valid["freq"])
    info_comp = np.vectorize(lambda x: x * log(x) if x != 0 else 0, otypes=[float])
    max_info = -np.sum(info_comp(normalv))


    max = ("?", 0)

    for word, _ in words:
        wcf = np.vectorize(lambda w: w_comp(word, w))
        freq_counter = np.bincount(wcf(valid["word"]), weights=normalv, minlength=3**5)
        word_info = max_info * freq_counter[-1] - np.sum(info_comp(freq_counter[:-1]))
        if word_info > max[1]:
            max = (word, word_info)

    return max


def conv(strr):
    if strr == "":
        return 0
    return int(strr[-1]) + conv(strr[:-1]) * 3

def filter(wordl, bes, seq):
    w_vec = np.vectorize(lambda w: w_comp(bes, w))
    return wordl[w_vec(wordl["word"]) == seq]

def checkin(input):
    if len(input) != 5:
        return False
    for x in input:
        if x not in "012":
            return False
    return True

def run():
    print()
    print("input key:")
    print("0 - gray, 1 - yellow, 2 - green")
    print("e.g: 02100")
    print("================================\n")

    initlist = []
    with open("5lw.txt", "r") as words, open("5lwf.txt", "r") as freqs:
        for word, freq in zip(words.readlines(), freqs.readlines()):
            w = str(word.strip())
            f = float(freq.strip())
            initlist.append((w, f))
    dt = [("word", "U5"), ("freq", "float")]
    initarr = np.array(initlist, dtype=[("word", "U5"), ("freq", "float")])
    wordlist = initarr

    while True:
        bes = best(initarr, wordlist)
        print("current best word is " + bes[0] + " (" + str(bes[1]) + " total info)")

        inp = input("choose input: ").strip()
        while not checkin(inp):
            if inp == "" or inp.lower() == "exit" or  inp.lower() == "quit" or inp.lower() == "q":
                return
            inp = input("try input again: ").strip()
        if(inp == "22222"):
            print("you win!")
            return

        wordlist = filter(wordlist, bes[0], conv(inp))

        if len(wordlist) == 0:
            print("no possible words")
            return

run()
