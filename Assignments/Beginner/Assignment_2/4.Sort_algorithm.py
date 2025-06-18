def switch(index1: int, index2: int, array: list) -> list:
    temp = array[index1]
    bubble = array[index2]
    array[index1] = bubble
    array[index2] = temp
    return array

def sort(arr):
    n = 0
    i = 0
    length = len(arr)
    while i != (length**2):
        for x in range((length-1)):
            try:
                try:
                    if arr[n] > arr[n+1]:
                        switch(n,(n+1),arr)
                        n+=1
                    else:
                        n+=1
                except TypeError as e:
                    output = f"Unsupported list/array item combination: {e}"
                    return output
            except IndexError:
                n=0
        i+=1
    return arr

array = [3,6,2,8,25,78,34,7,89,45,2,7,8]
print(sort(array))