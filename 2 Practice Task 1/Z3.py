def contain(nums):
    return len(nums) != len(set(nums))
print(contain([1,2,3,1]))
print(contain([5,5,4,1,10]))
print(contain([1,2,3]))