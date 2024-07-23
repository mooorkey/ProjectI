empty_positions = [2, 2, 2, 2]

cost_matrix = [
    [9, 2, 7, 8],  # Worker 0
    [6, 4, 3, 7],  # Worker 1
    [5, 8, 1, 8],  # Worker 2
    [7, 6, 9, 4]   # Worker 3
]

assignment = []
for worker_index, worker_scores in enumerate(cost_matrix):
    print(f"worker index{worker_index}, {worker_scores}")
    worker_priority = worker_index
    preferred_job = None

    for job_index, score in enumerate(worker_scores):
        print(f"job index {job_index}, {score}")
        if empty_positions[job_index] > 0:
            if preferred_job is None or score > worker_scores[preferred_job]:
                preferred_job = job_index
        
    if preferred_job is not None:
        assignment.append(preferred_job)
    else:
        assignment.append(-1)
    print(f"worker {worker_index} preferred job{preferred_job}\n")

print(assignment)