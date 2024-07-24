'''
This is the base code used to 
study branch and bound and 
solve the common job assignment problem
'''

input_data = [ # the cost matrix
#job 0, 1, 2, 3 
    [9, 2, 7, 8], # Worker 0
    [6, 4, 3, 7], # Worker 1
    [5, 8, 1, 8], # Worker 2
    [7, 6, 9, 4]  # Worker 3
]

def calculate_cost(matrix, assignment):
    bound = 0
    for i, j in enumerate(assignment):
        bound += matrix[i][j] # Add cost of assignment
    return bound

def find_least_cost(cost_matrix): # The branch and bound function
    worker_length = len(cost_matrix)

    # Initialize with positive infinity
    least_cost = float('inf') 

    # result matrix
    assignment_result = [] 

    # Initialize stack
    stack = [(0, [], list(range(worker_length)))] 
    print(stack, "\n")
    while stack:
        # cost, list of assigned worker, list of unassigned worker
        cost, assignment, unassigned = stack.pop()

        if not unassigned: # Check if all worker are assigned
            if cost < least_cost: # if the path cost is less than total cost
                least_cost = cost
                assignment_result = assignment
            continue

        # create child node for each unassigned worker
        for job in unassigned:
            new_assignment = assignment + [job] # add job to assignment
            new_unassigned = [j for j in unassigned if j != job]
            new_cost = calculate_cost(cost_matrix, new_assignment)

            if new_cost < least_cost:
                stack.append((new_cost, new_assignment, new_unassigned))        

    return least_cost, assignment_result

        
solution, assignment = find_least_cost(input_data)
print("Optimal Solution:", solution)
print("Optimal Assignment:", assignment)