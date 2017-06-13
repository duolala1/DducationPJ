
def getTopIndex(array,k):
    temp = array[:]
    temp.sort()
    length = len(array)
    top = [0]*k
    for j in range(k):
        for i in range(len(array)):
            if array[i] == temp[length-j-1]:
                top[j] = i
    return top
