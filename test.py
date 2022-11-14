list = [3,1,4,6,2,5]
list2 = [3,6,9]
list.sort()

print(list)
for i in list:
    for j in list2:
        if i == j:
            print("break")
            break

    print(i,j)
print("done")

class Test():
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

a = Test(2)
b = Test(1)
c = Test(3)

list3 = [a,b,c]
list3.sort(key=lambda x: x.value)
for i in list3:
    print(i.__str__(), end='')

coo = [1,3]
s = str(coo)
print(s)

inf = float('inf')
print(inf > 1000)