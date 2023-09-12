#### Objective
> Maximize total worker's appraisals based on their job assignments.

$$\begin{pmatrix}
A_{11} & A_{12} & A_{13} & ... & A_{1m} \\
A_{21} & A_{22} & A_{23} & ... & A_{2m} \\
A_{31} & A_{32} & A_{33} & ... & A_{3m} \\
... & ... & ... & ... & ... \\
A_{n1} & A_{n2} & A_{n3} & ... & A_{nm} \\
\end{pmatrix}$$

Sets/Parameters | Description
-- |--
$J$ | Sets of Jobs $\{1, 2, 3, \dots, m\}$
$W$ | Sets of Workers $\{1, 2, 3, \dots, n\}$
$C_j$ | Maximum Capacity for job $j$
$Level_{i}$| Level of worker $i$
$Requirement_j$| Level requirement for Job $j$

Decision Variable | Description
--|--
$A_{ij}$ | Appraisal score of Worker $i$ when assigned to Job $j$
$x_{ij}$ | Binary equals $1$ if Worker $i$ assigned to Job $j$, $0$ otherwise

#### Objective Function
$$Maximize : \sum_{i \text{ in W}}^n \sum_{j \text{ in J}}^m (A_{ij} \cdot x_{ij})$$

#### Constraint 
1. Binary Constraint
   $$x_{ij} \in \{0,1\}, \quad \forall{i}\in W, \forall{j} \in J$$
2. Capacity Constraint (แต่ละตำแหน่งมีการระบุจำนวนในการรับ)
   $$\sum_{i \text{ in W}}^{n}x_{ij}\leq C_{j},\quad \forall{j} \in J$$
3. Requirement Matching Constraints (ในตำแหน่งชั้นเดิม หรือเลื่อนขั้น)
   $$x_{ij}\cdot(Level_i\geq Requirement_{j}) = 1, \quad \forall i \in W, \forall j \in J$$


#### Test Result 
	- Test With Random Number
	- Only one constraint(1 Worker can be assigned to only 1 job)

==Without Eliminate==

![[Pasted image 20230904190844.png]]

| Input Size (NxN) | Iterations | Combinations | Time Took (second)   |
|------------|------------|--------------|--------------|
| 1          | 2          | 1            | 0.000000    |
| 2          | 5          | 2            | 0.000000    |
| 3          | 16         | 6            | 0.000000    |
| 4          | 65         | 24           | 0.000998    |
| 5          | 326        | 120          | 0.000000    |
| 6          | 1957       | 720          | 0.002992    |
| 7          | 13700      | 5040         | 0.011483    |
| 8          | 109601     | 40320        | 0.096949    |
| 9          | 986410     | 362880       | 0.879964    |
| 10         | 9864101    | 3628800      | 9.351670    |
| 11         | 108505112  | 39916800     | 106.020846  |
|12|1302061345|479001600|1283.081852|

```
# Try add all childs instead of the lower cost one
# and count the iteration once all workers are assigned
# But this took too much time to solve the combinations is correct(equals to n!)
# this prototype compare all combination of assignmnet result then choose the one with lowest cost
def find_least_cost(cost_matrix):
    worker_length = len(cost_matrix)
    lower_bound = float('inf') # Initialize with positive infinity
    assignment_result = []
    
    iteration = 0;
    combination = 0;
  
    # Initialize unpruned_nodes for nodes explore
    unpruned_nodes = [(0, [], list(range(worker_length)))]

    while unpruned_nodes:
        # cost, list of assigned worker, list of unassigned worker
        cost, assignment, unassigned = unpruned_nodes.pop() # pop a node to explore
        iteration += 1
        if not unassigned: # Check if all worker are assigned
            combination += 1 # All workers are assigned means we finished 1 combination
            if cost < lower_bound:
                lower_bound = cost # set new cost
                assignment_result = assignment # set new assignment
            continue
            
        # create child node for each unassigned worker
        for job in unassigned:
            new_assignment = assignment + [job] # add job to assignment
            new_unassigned = [j for j in unassigned if j != job] # <- this is constraint (1 worker can assigned to 1 job)
            new_cost = calculate_cost(cost_matrix, new_assignment)
            unpruned_nodes.append((new_cost, new_assignment, new_unassigned))  
            
    print(f"{iteration} Iterations and {combination} combinations")
    return lower_bound, assignment_result

def calculate_cost(matrix, assignment):
    cost = 0
    for worker, job in enumerate(assignment):
        cost += matrix[worker][job]
    return cost
```

==With Eliminate==

![[Pasted image 20230904162853.png]]

| Input Size (NxN) | Iterations | Combinations | Time Took (second)   |
|------------|------------|--------------|--------------|
| 1          | 2          | 1            | 0.000000    |
| 2          | 4          | 1            | 0.000000    |
| 3          | 13         | 3            | 0.000000    |
| 4          | 34         | 4            | 0.000000    |
| 5          | 60         | 4            | 0.000000    |
| 6          | 213        | 5            | 0.000000    |
| 7          | 355        | 8            | 0.001283    |
| 8          | 1116       | 19           | 0.002992    |
| 9          | 2385       | 8            | 0.011504    |
| 10         | 8198       | 25           | 0.033809    |
| 11         | 30658      | 33           | 0.123173    |
| 12         | 153001     | 35           | 0.664277    |
| 13         | 237374     | 32           | 1.237870    |
| 14         | 284596     | 43           | 1.654840    |
| 15         | 316656     | 32           | 2.160102    |
| 16         | 2458795    | 37           | 17.174433   |
| 17         | 40794489   | 103          | 269.800765  |

```
# Added combinations and iterations
# Once all worker are assigned and unassigned list is empty then this means we get a combination
# Cut the unfinished one with more cost

def find_least_cost(cost_matrix):
    worker_length = len(cost_matrix)
    lower_bound = float('inf') # Initialize with positive infinity
    assignment_result = []
    
    iteration = 0;
    combination = 0;
    
    # Initialize unpruned_nodes for nodes explore
    unpruned_nodes = [(0, [], list(range(worker_length)))]
    
    while unpruned_nodes:
        # cost, list of assigned worker, list of unassigned worker
        cost, assignment, unassigned = unpruned_nodes.pop() # pop a node to explore
        iteration += 1
        if not unassigned: # Check if all worker are assigned
            combination += 1 # All workers are assigned means we finished 1 combination
            if cost < lower_bound:
                lower_bound = cost # set new cost
                assignment_result = assignment # set new assignment
            continue
            
        # create child node for each unassigned worker
        for job in unassigned:
            new_assignment = assignment + [job] # add job to assignment
            new_unassigned = [j for j in unassigned if j != job] # <- this is constraint (1 worker can assigned to 1 job)
            new_cost = calculate_cost(cost_matrix, new_assignment)
            if new_cost < lower_bound:
                unpruned_nodes.append((new_cost, new_assignment, new_unassigned))  
    print(f"{iteration} Iterations though {combination} combinations")
    return lower_bound, assignment_result

def calculate_cost(matrix, assignment):
    cost = 0
    for worker, job in enumerate(assignment):
        cost += matrix[worker][job]
    return cost
```



#### Constraint (Code)
##### Capacity Constraint 
```
# Capacity Constraint for job
def is_capacity_satisfied(assignment, job, capacity_matrix):
    # How many worker have been assigned to this job
    job_count = assignment.count(job)
    return job_count <= capacity_matrix[job]
```

![[Pasted image 20230904180443.png]]

##### Requirement Matching Constraints
```
def is_requirement_matched(assignment, worker_level_matrix, job_requirement_matrix):
    for worker, job in enumerate(assignment):
        # if the worker has skill less than the requirement then it's false
        if worker_level_matrix[worker] < job_requirement_matrix[job]:
            return False
    return True
```

![[Pasted image 20230904180508.png]]

