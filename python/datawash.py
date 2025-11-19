raw = ""
a = list(raw)
while(a[0] != r'.'):
    a.pop(0)
container = []
str_ = ''
for i in a:
    if i == '\t' or i == '\n':
        container.append(str_)
        str_ = '' 
    else:
        str_ += i
counter = 0
raw_ = []
for i in container:
    counter += 1
    if(counter % 7 == 0 or (counter - 1) % 7 == 0):
        raw_.append(i)
raw_.pop(0)
num = len(raw_)
cookies = {raw_[i]:raw_[i+1] for i in range(0, len(raw_), 2)}
print(cookies)