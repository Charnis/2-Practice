J = input("j = ").strip() #Драгоценности
S = input("s = ").strip() #Камни

result = 0
for i in S:
    if i in J:
        result += 1

print(result)