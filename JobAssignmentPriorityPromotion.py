def generate_dict(key, values):
    result_dict = []

    for value in values:
        key_pair = zip(key, value)
        result_dict.append(dict(key_pair))

    return result_dict

def do_job_assignment(worker_datas, job_datas):
    assignment_result = []
    for worker in worker_datas:
        preferred_job = None
        for job in worker['Scores']:
            job_rank = job[-1]
            job_id = job[0] 
            job_index = job_datas[job_id-1]
            preferred_job_capacity = job_index['CapacityList']
            if preferred_job_capacity[job_rank-1] > 0:
                preferred_job = job_index
                job_datas[job_id-1]['CapacityList'][job_rank-1] -= 1 # reduce the capacity by 1
                assignment_result.append([worker['PriorityNumber'], preferred_job, job_rank])
                break
            else:
                print("not available")

        if preferred_job is None:
            assignment_result.append([worker['PriorityNumber'], -1, -1])
        else:
            job_datas[worker["CurrentJobId"]-1]['CapacityList'][worker['CurrentRank']-1] += 1
    return assignment_result, job_datas


if __name__ == '__main__':
    worker_keys = ['PriorityNumber', 'CurrentRank', 'CurrentJobId', 'Scores', 'RelocType']
    worker_datas = [
        # PriorityNo, Rank, Job
        [1, 5, 1, [ # worker 1
            # JobId, Score, JobRank
            [2, 30, 5],
            [3, 29, 5],
            [4, 28, 5]
        ], 0],
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
            [2, 29, 4],
            [4, 28, 4],
            [5, 27, 4]
        ], 1]
    ]
    job_keys = ['JobId', 'JobName', 'PositionName', 'CapacityList']
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

    worker_datas = generate_dict(worker_keys, worker_datas)
    for worker in worker_datas:
        print(worker)
    sorted_data = sorted(worker_datas, key=lambda x: (-x['CurrentRank'], -x['RelocType']))
    print("\nSorted")
    for worker in sorted_data:
        print(worker)
    job_datas = generate_dict(job_keys, job_datas)
    print("")
    result, vacancy_mat = do_job_assignment(sorted_data, job_datas)
    print("")

    # print(result)
    for worker in result:
        if worker[1] != -1:
            print(f"worker {worker[0]} to jobID {worker[1]['JobId']} rank {worker[2]}")
        else:
            print(f"worker {worker[0]} to jobID same rank {worker[2]}")


    