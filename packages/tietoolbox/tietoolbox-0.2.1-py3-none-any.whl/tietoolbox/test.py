def fac(x):
    if x == 1:
        return 1
    else:
        print(x)
        return x * fac(x - 1)


print(fac(3))
