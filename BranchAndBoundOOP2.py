class Node:
    def __init__(self, assignment, cost, level, parent=None):
        self.assignment = assignment
        self.cost = cost
        self.parent = parent
        self.level = level

def branch_and_bound(cost_matrix):
    worker_length = len(cost_matrix)
    job_length = len(cost_matrix[worker_length - 1])
    print(f"size {worker_length}x{job_length}")

    optimal_cost = float('inf')
    assigned = []

    root = Node([-1]*worker_length, 0, 0)
    queue = [root]

    while queue:
        node = queue.pop()
        for job in range(job_length):
            new_assignment = node.assignment[:]
            new_assignment[node.level] = job
            cost = cost_matrix[node.level][job]
            print(f"assigned job {job} to worker {node.level}, cost {cost}")
input_data = [
#job 0, 1, 2, 3 
    [9, 2, 7, 8], # Worker 0
    [6, 4, 3, 7], # Worker 1
    [5, 8, 1, 8], # Worker 2
    [7, 6, 9, 4]  # Worker 3
]

# the result should be 
# worker 0, 1, 2, 3
#       [1, 0, 2, 3] jobs
# optimal cost = 13

branch_and_bound(input_data)

