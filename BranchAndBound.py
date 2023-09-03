# 4x4 matrix
input_data = [
#job 0, 1, 2, 3 
    [9, 2, 7, 8], # Worker 0
    [6, 4, 3, 7], # Worker 1
    [5, 8, 1, 8], # Worker 2
    [7, 6, 9, 4]  # Worker 3
]

def find_least_cost(matrix):
    worker_legnth = len(matrix)
    least_cost = float('inf') # Initialize with positive infinity
    assigned_worker = -1
    assigned_job = -1

    for worker in range(worker_legnth):
        job = matrix[worker].index(min(matrix[worker]))  # Find the index of the minimum value in the worker's row
        cost = matrix[worker][job]

        if cost < least_cost:
            least_cost = cost
            assigned_worker = worker
            assigned_job = job
    return least_cost, assigned_worker, assigned_job

cost, worker, job = find_least_cost(input_data)
print(f"Assigned Worker {worker} to job {job} with cost {cost} ")
