def next_permutation(arr):
    i = len(arr) - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return False
    
    j = len(arr) - 1
    while arr[j] <= arr[i]:
        j -= 1

    arr[i], arr[j] = arr[j], arr[i]
    
    new_arr = arr[i+1:]
    arr[i+1:] = new_arr[::-1]
    return True

def gen(n):
    if n < 1:
        return []

    arr = list(range(1, n + 1))
    permutations = []

    while True:
        permutations.append(' '.join(map(str, arr)) + ' ')
        if not next_permutation(arr):
            break

    return permutations

n = int(input())
permutations = gen(n)

for p in permutations:
    print(p)
