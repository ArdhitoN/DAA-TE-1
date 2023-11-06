def clustered_binary_insertion_sort(a_list):
    POP = 0
    for i in range(1, len(a_list)):
        COP = i
        key = a_list[COP]
        
        if key >= a_list[POP]:
            place = binary_loc_finder(a_list, POP + 1, COP - 1, key)
        else:
            place = binary_loc_finder(a_list, 0, POP - 1, key)
        
        POP = place
        place_inserter(a_list, POP, COP)
        
    return a_list

        
def binary_loc_finder(a_list, start, end, key):
    if start == end:
        if a_list[start] > key:
            return start
        
        else:
            return start + 1
        
    if start > end:
        return start

    else:
        middle = (start + end) // 2  
        if a_list[middle] < key:
            return binary_loc_finder(a_list, middle + 1, end, key)
        elif a_list[middle] > key:
            return binary_loc_finder(a_list, start, middle - 1, key)
        else:
            return middle 
        
        
def place_inserter(a_list, start, end):
    temp = a_list[end]
    for k in range(end, start, -1):
        a_list[k] = a_list[k-1]
    a_list[start] = temp



if __name__ == "__main__":
    list = [34, 8, 64, 51, 32, 21]
    clustered_binary_insertion_sort(list)
    print("Sorted list:", list)
    
