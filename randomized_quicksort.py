import random
def randomized_quicksort(a_list, p, r):
    if p < r:
        q = randomized_partition(a_list, p, r)
        randomized_quicksort(a_list, p, q - 1)
        randomized_quicksort(a_list, q + 1, r)
        
def randomized_partition(a_list, p, r):
    x = random.randint(p, r)
    a_list[x], a_list[r] = a_list[r], a_list[x]

    return partition(a_list, p, r)

def partition(a_list, p, r):
    x = a_list[r]
    i = p - 1
    for j in range(p, r):
        if a_list[j] <= x:
            i += 1
            a_list[i], a_list[j] = a_list[j], a_list[i]

    a_list[i + 1], a_list[r] = a_list[r], a_list[i + 1]
    
    return i + 1
    

if __name__ == "__main__":
    list = [10, 7, 8, 9, 1, 5]
    randomized_quicksort(list, 0, len(list) - 1)
    print("Sorted list:", list)
