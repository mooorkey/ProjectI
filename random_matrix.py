import random
import time
def rnd_mat(n):
    matrix = []
    random.seed(time.time())
    row = []
    for i in range(n):
        for j in range(n):
            row.append(random.randrange(0, n))
        matrix.append(row)
        row = []
            
    return matrix

if __name__ == "__main__":
    mat = rnd_mat(10)
    print(f"NxN = {len(mat)}x{len(mat[0])}")
    print(mat)