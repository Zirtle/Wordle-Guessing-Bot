#!/usr/bin/env python
# coding: utf-8

# In[1]:


words = open('valid-wordle-words.txt', 'r').read()

words = words.split('\n')

words = words[:-1]
words[-1]


# In[ ]:


from collections import Counter

yellows = []
greens = []
blacks = []

while True:
    # Recompute character frequencies after filtering
    chars = [0] * 26
    for word in words:
        for c in word:
            chars[ord(c) - ord('a')] += 1

    # Guess the word based on most frequent letters
    letters = 5
    guess_words = []
    while True:
        scored = list(enumerate(chars))
        top = sorted(scored, key=lambda x: x[1], reverse=True)[:letters]
        top_letters = [chr(i + ord('a')) for i, _ in top]

        for word in words:
            score = sum(word.count(c) for c in top_letters)
            if score >= 5:
                guess_words.append((word, len(set(word))))

        if len(guess_words) >= 1:
            break
        else:
            letters += 1

    guess_word = max(guess_words, key=lambda x:x[1])[0]
    print(f"Guess: {guess_word}")

    # Get feedback input (e.g. "gybbb")
    inp = input("Enter colors: ").strip().lower()
    if len(inp) != 5:
        print("Input must be 5 characters long.")
        continue

    for i, c in enumerate(inp):
        if c == 'g':
            if (i, guess_word[i]) not in greens:
                greens.append((i, guess_word[i]))
        elif c == 'y':
            if (i, guess_word[i]) not in yellows:
                yellows.append((i, guess_word[i]))
        elif c == 'b':
            blacks.append(guess_word[i])

    # === Green filtering ===
    words_new = []
    for word in words:
        if all(word[i] == c for i, c in greens):
            words_new.append(word)
    words = words_new
    print(f"After green filter: {len(words)}")

    # === Yellow filtering ===
    words_new = []
    for word in words:
        valid = True
        for i, c in yellows:
            if c not in word or word[i] == c:
                valid = False
                break
        if valid:
            words_new.append(word)
    words = words_new
    print(f"After yellow filter: {len(words)}")

    # === Black filtering with count checks ===
    allowed_counts = Counter(c for _, c in greens + yellows)
    words_new = []
    for word in words:
        wc = Counter(word)
        if any(wc[c] > allowed_counts.get(c, 0) for c in blacks):
            continue
        words_new.append(word)
    words = words_new
    print(f"After black filter: {len(words)}")

    # Check if one solution remains
    if len(words) == 1:
        print(f"The word is: {words[0]}")
        break
    elif len(words) == 0:
        print("No valid words left. Check your inputs.")
        break


# In[ ]:




