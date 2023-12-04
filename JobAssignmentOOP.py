import copy
class Worker:
    def __init__(self, prioritynumber, currentrank, currentjobid, scores, reloctype) -> None:
        self.prioritynumber = prioritynumber
        self.currentrank = currentrank
        self.currentjob = currentjobid
        self.scores = scores # appraisals score for each job
        self.reloctype = reloctype # if relocate => 0, if promotion => 1 

class Job: 
    def __init__(self, jobid, jobname, positionname, capacitylist) -> None:
        self.jobid = jobid
        self.name = jobname
        self.position = positionname
        self.capacitylist = capacitylist
    
    def getcap(self, rank):
        return self.capacitylist[rank-1]


def bnb_wc(worker_list, job_list):
    upper_bound = -1
    assignment_result = []

    iteration = 0
    combination = 0

    unpruned_nodes = [(0, [], worker_list, job_list)]
    job_remains = []

    while unpruned_nodes:

        cost, assignment, workers, jobs = unpruned_nodes.pop()
        iteration += 1
        if len(workers) == 0: # all worker are assigned then we can check the score/cost to set result and bound
            combination += 1
            if cost > upper_bound:
                assignment_result = assignment
                upper_bound = cost
                job_remains = jobs
        else:
            for worker_job in workers[0].scores:
                jobs_copy = copy.deepcopy(jobs)
                preferred_job = jobs_copy[worker_job[0] - 1]
                current_worker = workers[0]
                if preferred_job.getcap(worker_job[-1]) > 0: # check capacity constraint
                    new_assignment = assignment + [worker_job]
                    new_cost = cost + worker_job[1]
                    jobs_copy[worker_job[0] - 1].capacitylist[worker_job[-1]-1] -= 1
                elif jobs_copy[current_worker.currentjob - 1].getcap(current_worker.currentrank) > 0: # check if worker can fit their old job or not 
                    # print('Can fit old job')
                    new_assignment = assignment + [[current_worker.currentjob, current_worker.scores[-1][1] - 1, current_worker.currentrank]]
                    new_cost = cost + current_worker.scores[-1][1] - 1
                    jobs_copy[current_worker.currentjob - 1].capacitylist[current_worker.currentrank - 1] -= 1
                else: # if worker can't fit neither preferred job or their old job then do not add new node to explore
                    # print('Cannot fit any job')
                    continue # no need to explore more deep
                new_worker_list = workers[1:]
                # print(new_assignment)
                unpruned_nodes.append((new_cost, new_assignment, new_worker_list, jobs_copy))
    return assignment_result, upper_bound, combination, iteration, job_remains


# Worker Datas And Job DatasÍ
worker_datas = [
        # PriorityNo, Rank, Job
        [1, 5, 1, [ # worker 1
            # JobId, Score, JobRank
            [2, 30, 5],
            [3, 29, 5],
            [4, 28, 5]
        ], 0], # Relocation Type 1 -> Promotion, 0 -> Relocation
        [2, 5, 1, [ # worker 2
            # JobId, Score, JobRank
            [2, 30, 6],
            [3, 29, 6],
            [4, 28, 6]
        ], 1],
        [3, 5, 1, [ # worker 3
            # JobId, Score, JobRank
            [2, 30, 6],
            [3, 29, 6],
            [4, 28, 6]
        ], 0],
        [4, 4, 3, [ # worker 4
            # JobId, Score, JobRank
            [1, 30, 4],
            [2, 29, 4],
            [4, 28, 4],
            [5, 27, 4]
        ], 0],
        [5, 4, 2, [ # worker 5
            # JobId, Score, JobRank
            [1, 30, 4],
            [3, 29, 4],
            [4, 28, 4],
            [5, 27, 4]
        ], 1]
    ]

job_datas = [
    [1, "Job1", "Pos1", [1, 1, 1, 1, 1, 1]],
    [2, "Job2", "Pos2", [0, 1, 1, 0, 1, 1]],
    [3, "Job3", "Pos3", [1, 0, 1, 1, 0, 1]],
    [4, "Job4", "Pos4", [1, 1, 0, 1, 1, 0]],
    [5, "Job5", "Pos5", [0, 1, 0, 1, 1, 0]],
    [6, "Job6", "Pos6", [1, 1, 1, 0, 0, 1]],
    [7, "Job7", "Pos7", [0, 0, 1, 1, 1, 0]],
    [8, "Job8", "Pos8", [1, 1, 0, 0, 1, 1]],
    [9, "Job9", "Pos9", [1, 1, 1, 1, 0, 0]],
    [10, "Job10", "Pos10", [0, 1, 1, 0, 0, 1]],
    [11, "Job11", "Pos11", [1, 0, 1, 0, 1, 1]]
]

worker_lists = []
job_lists = []
for worker in worker_datas:
    new_worker = Worker(worker[0], worker[1], worker[2], worker[3], worker[4])
    worker_lists.append(new_worker)

for job in job_datas:
    new_job = Job(job[0], job[1], job[2], job[3])
    job_lists.append(new_job)

# Test Clearing slot
copy_of_job_lists = job_lists
for job in copy_of_job_lists:
    job.capacitylist = [0]*6 # Fill 0 in capacitylist
    # job.capacitylist = [5]*6 # Fill 0 in capacitylist
    print(f"{job.name} capacity {job.capacitylist}")

for worker in worker_lists:
    worker_currentjob = copy_of_job_lists[worker.currentjob-1] # get worker current job
    worker_currentjob.capacitylist[worker.currentrank-1] += 1 # +1 for worker current job

print("\nClearing slot\n")

for job in copy_of_job_lists:
    print(f"{job.name} capacity {job.capacitylist}")

result, score, combination, iteration, remaining_jobs = bnb_wc(worker_lists, copy_of_job_lists)
print(f"iteration {iteration} combination {combination}. result {result} score {score}")
for job in remaining_jobs:
    print(job.capacitylist)