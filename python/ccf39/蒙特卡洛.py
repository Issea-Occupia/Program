n = int(input())
a = float(input())
incycle = 0.0
square = 0.0
for i in range(n):
    x,y = float(input()),float(input())
    if abs(x) <= a and abs(y) <= a:
        square+=1
        if x*x + y*y <= a*a:
            incycle+=1
print(0.0 if square == 0 else incycle / square)
            