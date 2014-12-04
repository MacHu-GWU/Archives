##encoding=utf8

from __future__ import print_function

class IntegerInterval(object):
    def __init__(self, lower, upper):
        self.array = [lower, upper]

    def __str__(self):
        return str( zip(self.array[::2], self.array[1::2]) )
        
    def __len__(self):
        return len(self.array)/2
    
    def index(self, x):
        ind = 1
        for i in self.array:
            if x < i:
                return ind
            else:
                ind += 1
        return ind
    
    def __add__(self, integer_interval):
        x, y = integer_interval.array
        xi, yi = self.index(x), self.index(y)
        if xi%2 == 0: # 偶数，在子区间内
            a, b = xi-2, self.array[xi-2]
        else: # 奇数，在子区间外
            a, b = xi-1, x
        if yi%2 == 0: # 偶数，在子区间内
            c, d = self.array[yi-1], yi
        else: # 奇数，在子区间外
            c, d = y, yi-1
        array = self.array[:a] + [b, c] + self.array[d:]
        
        ## 合并相邻的整数节点
        res = list()
        res.append(array[0])
        for i, j in zip(array[1:-2:2], array[2:-1:2]):
            if (j - i) > 1:
                res.append(i)
                res.append(j)
        res.append(array.pop())
        return res
                  
if __name__ == "__main__":  
    a = IntegerInterval(0, 1)
    a.array = [1, 5, 9, 13, 17, 21]
    print(a + IntegerInterval(7, 11) )  #[(1, 5), (7, 13), (17, 21)]
    print(a + IntegerInterval(11, 15) ) #[(1, 5), (9, 15), (17, 21)]
    print(a + IntegerInterval(10, 12) ) #[(1, 5), (9, 13), (17, 21)]
    print(a + IntegerInterval(7, 15) )  #[(1, 5), (7, 15), (17, 21)]
    
    b = IntegerInterval(0, 1)
    b.array = [1, 2, 9, 13, 20, 21]
    print(b + IntegerInterval(3, 8) )  #[(1, 13), (20, 21)]
    print(b + IntegerInterval(14, 19) ) #[(1, 2), (9, 21)]
