import numpy as np

class assignment1():

    def __init__(self):
        arr1 = self.pt1()
        arr2 = self.pt2(arr1)
        arr3 = self.pt3()

        bothEven = np.vectorize(lambda x,y: x % 2 == 0 and y % 2 == 0)
        arr4 = bothEven(arr2, arr3)
        #print(pt4)

        arr5 = np.sum(arr2 % 2 == 0)
        #print(pt5)

        arr6 = arr3 ** .5
        #print(pt6)

        arr7 = self.pt7(arr1)
        #print(arr7)

        arr8 = self.pt8(arr1)
        #print(arr8)

        arr9 = self.pt9()
        #print(arr9)

        arr10 = np.apply_along_axis(lambda arr: np.sum(arr)/10.0, 1, arr1)
        #print(arr10)



    """
    return a 10x10 array that contains the multiplication table
    """
    def pt1(self):
        arr1 = np.arange(1,11)
        arr2 = np.resize(arr1, (10,1))
        return arr1*arr2

    """
    Write code that selects the 4x4 array that is in the middle inside the result of pt1
    """
    def pt2(self, pt1Arr):
        return pt1Arr[3:7, 3:7]

    """
    Create a 4x4 array that contains the numbers from 1 to 16
    """
    def pt3(self):
        return np.resize(np.arange(1,17), (4,4))

    """
    Create a new 4x4 array that has value of true if both values 
    in the two arrays are even and false otherwise
    """
    def pt4(self):
        pass

    """
    returns the number of even numbers in the array from Q2
    """
    def pt5(self):
        pass

    """returns the square root of the numbers in the array from Q3"""
    def pt6(self):
        pass

    """
    Write code that returns the array from Q1, where the numbers on the diagonal are incremented by 1
    """
    def pt7(self, pt1):
        diagonals = np.zeros((10, 10))
        np.fill_diagonal(diagonals, 1)
        return pt1+diagonals

    """
    Write code that shows the array from Q1 in reverse order
    """
    def pt8(self, pt1):
        return np.fliplr(np.flipud(pt1))

    """
    Write code that creates a 10x10 array of random float numbers between 0.0 inclusive and 10.0 exclusive. 
    The numbers should appear in the array sorted in ascending order
    """
    def pt9(self):
        return np.resize(np.sort(np.random.rand(100))*10, (10,10))
    
    """
    Write code that creates one-dimensional array of 10 elements. 
    The ith element should be the average of the numbers in the ith row of the array from Q1
    """
    def pt10(self):
        pass
    

test = assignment1()