def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


result = factorial(0)
print(result)  # 24
