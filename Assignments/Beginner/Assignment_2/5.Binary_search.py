def binary_search(a,key):
    n = len(a)
    low = 0
    high = n-1
    while (low<=high):
        mid = int((low+high)/2)
        if key == a[mid]:
            return mid
        elif key < a[mid]:
            high = mid -1
        else:
            low = mid+1
    return -1

array = [3,6,2,8,25,78,34,7,89,45,2,7,8]
print()
print('Element found at index ', binary_search(array,34))