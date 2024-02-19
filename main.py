# from word_list import wordList
def editDistance(strInput, word):
    m, n = len(strInput) + 1, len(word) + 1
    dp = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            else:
                dp[i][j] = min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
                if strInput[i - 1] != word[j - 1]: dp[i][j] += 1
    return dp[-1][-1] + len({char for char in strInput} ^ {char for char in word})


def similar(strInput, word):
    distance = editDistance(strInput, word)
    return distance - 100 if strInput == word[:len(strInput)] else distance


def autoCorrect(strInput, words):
    inputs = strInput.split(" ")

    for i in range(len(inputs)):
        distances = {word: editDistance(inputs[i], word) for word in words}
        inputs[i] = min(distances.keys(), key=lambda x: distances[x])
    return inputs


def suggestion(strInput, words):
    distances = {word: similar(strInput, word) for word in words}
    suggests = sorted(distances.keys(), key= lambda x: distances[x])
    return suggests[:5] if len(words) > 4 else suggests


with open(r"20k.txt", encoding='utf-8') as file:
    wordList = [line[:-1] for line in file]


def actions(action):
    if action == "\\suggest": printSuggests()
    elif action == "\\autocorrect": printAuto()


def printAuto():
    while True:
        user = input("Input:")
        if user[0] == "\\":
            actions(user.lower())
            return
        else: print("Corrected Sentence: ", *autoCorrect(user.lower(), wordList))


def printSuggests():
    curr = ""
    while True:
        user = input("Input:")
        if user[0] == "\\":
            actions(user.lower())
            return
        if user[0] == '+': curr = user[1:]
        else: curr += user.lower()
        print(f"Current: {curr}")
        print("Suggestion: ", *suggestion(curr, wordList))


actions("\\suggest")