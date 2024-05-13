import numpy as np


mat1 = [[1],
        [2],
        [3],
        [4]]
mat2 = [[1, 2, 3, 4]]

mat3 = [1, 2, 3, 4]

mult = np.matmul(mat1, mat2)

print(mult)


print(zip(mat1, mat2))

for item in zip(mat1, mat2):
    print(item)
