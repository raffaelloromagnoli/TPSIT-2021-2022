l=[n*n for n in range(1,11) if n%2==0] #list comprehension

print(l)
size=4
matrice=[[(m,n) for n in  range(0,size)] for m in range(0, size)]

print(matrice)