class Node:
    def __init__(self, level, assignment, cost, parent=None):
        self.level = level
        self.assignment = assignment
        self.cost = cost
        self.parent = parent

def branch_and_bound(cost_matrix):
    n = len(cost_matrix)
    root = Node(0, [-1] * n, 0)
    min_cost = float('inf')
    min_assignment = []

    queue = [root] # queue of nodes to explore

    while queue:
        node = queue.pop()
        print(f"pop {node.assignment} cost {node.cost}")

        if node.level == n:
            if node.cost < min_cost:
                min_cost = node.cost
                min_assignment = node.assignment

                print(f"min {min_cost} {min_assignment}")
                print("-"*20)
                print("\n")
            continue
        print(f"at level {node.level}")

        for worker in range(n):
            if worker not in node.assignment:
                new_assignment = node.assignment[:]
                new_assignment[node.level] = worker
                new_cost = node.cost + cost_matrix[node.level][worker]
                new_node = Node(node.level + 1, new_assignment, new_cost, parent=node)
                queue.append(new_node)
                print(new_node.assignment, new_node.cost)
        print("\n")

    return min_cost, min_assignment


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

a, b = branch_and_bound(input_data)
print(a, b)

