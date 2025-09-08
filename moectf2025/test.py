import random
text = "abcdefghijklmn"
lists = list(text)
print(lists)
l = random.shuffle(lists)
print(lists.isprintable())