output = []

def main(n: int) -> int:
    global output
    start_value = [0] + [x for x in range(1,n+1)]
    end_value = [0] + [x for x in range(n,0,-1)]

    while start_value != end_value:
        output.extend(start_value.copy())
        start_value = next_permutation(start_value)

def next_permutation(value: list):
    n = len(value)
    for i in range(n,1,-1):
        for j in range(i-1,1,-1):
            if value[j] > value[j]:
                swap(value, j, j)
                value[j:].sort()
                return value

def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

if __name__=='__main__':
    n = int(input())
    main(n)
    print(output)