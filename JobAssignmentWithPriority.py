def generate_worker_dict(worker_data_input):
    worker_keys = ['priorityNumber', 'prefix', 'firstName', 'lastName', 'rank', 'jobName', 'positionName', 'jobId', 'scores']
    worker_data_dict = []

    # print(worker_data_input)
    for worker in worker_data_input:
        worker_key_pair = zip(worker_keys, worker)
        worker_data_dict.append(dict(worker_key_pair))

    # print(worker_data_dict[0]['firstName'])
    return worker_data_dict

def generate_dict(key, values):
    result_dict = []

    for value in values:
        key_pair = zip(key, value)
        result_dict.append(dict(key_pair))

    return result_dict




def do_job_assignment(worker_datas, job_datas):
    assignment_result = []
    # print(job_datas)
    for worker in worker_datas:
        # print(f"worker {worker['firstName']}")
        # print(f"No.{worker['priorityNumber']} Name {worker['firstName']}")
        preferred_job = None
        for job in worker['scores']:
            job_rank = job[-1]
            job_id = job[0] 
            job_index = job_datas[job_id-1]
            # print(f"wanted job {job_id} rank {job_rank}")
            preferred_job_capacity = job_index['capacityList']
            if preferred_job_capacity[job_rank-1] > 0:
                preferred_job = job_index
                job_datas[job_id-1]['capacityList'][job_rank-1] -= 1 # reduce the capacity by 1
                assignment_result.append([worker['firstName'], preferred_job, job_rank])
                break
            else:
                print("not available")

        if preferred_job is None:
            assignment_result.append([worker['firstName'], -1])
        else:
            job_datas[worker["jobId"]-1]['capacityList'][worker['rank']-1] += 1
            # print(job_datas[worker["jobId"]-1]['capacityList'][worker['rank']-1])
        # print(" ")
    return assignment_result, job_datas


if __name__ == '__main__':
    worker_keys = ['priorityNumber', 'prefix', 'firstName', 'lastName', 'rank', 'jobName', 'positionName', 'jobId', 'scores']
    # Read worker data from file
    worker_data = [
        # PriorityNo., Prefix, Firstname, Lastname, Rank(1-8), Location, Position Name, Current job id, Appraisal Score()
        [1, "Mr.", "Mork1", "Suk", 1, "Job1", "Pos1", 1,  [
            [1 ,"job1", "pos1", 30, 2],
            [2 ,"job1", "pos1", 29, 3],
            [3 ,"job1", "pos1", 28, 4]
        ]],
        [2, "MrS.", "Sahassawat3", "Pra", 4, "Job1", "Pos2", 2,  [
            [1 ,"job1", "pos1", 19, 1],
            [2 ,"job1", "pos1", 18, 2],
            [3 ,"job1", "pos1", 17, 3]
        ]],
        [3, "Mr.", "Sahassawat", "Suk", 5, "Job2", "Pos1", 3,  [
            [1 ,"job1", "pos1", 30, 1],
            [2 ,"job1", "pos1", 29, 2],
            [3 ,"job1", "pos1", 28, 3]
        ]],
        [4, "Mr.", "Mork2", "Suk", 5, "Job2", "Pos2", 4,  [
            [1 ,"job1", "pos1", 30, 1],
            [2 ,"job1", "pos1", 29, 2],
            [3 ,"job1", "pos1", 28, 3]
        ]]
    ]

    job_keys = ['jobId', 'jobName', 'positionName', 'capacityList']
    # Read job data from file ข้อมูลอัตรากำลัง
    # job_data = [
    #     # jobId, jobName, positionName, capa[6, 5, 4, 3, 2, 1]
    #     [1, 'job1', "pos1", [0, 1, 2, 2, 0, 0]],
    #     [2, "job1", "pos2", [0, 2, 2, 2, 0, 0]],
    #     [3, "job2", "pos1", [0, 1, 2, 2, 4, 8]],
    #     [4, "job2", "pos2", [0, 2, 0, 9, 8, 7]]
    # ]
    job_data = [
        # jobId, jobName, positionName, capa[1, 2, 3, 4, 5, 6]
        [1, 'job1', "pos1", [1, 1, 1, 1, 1, 1]],
        [2, "job1", "pos2", [1, 1, 1, 1, 1, 1]],
        [3, "job2", "pos1", [1, 1, 1, 1, 1, 1]],
        [4, "job2", "pos2", [1, 1, 1, 1, 1, 1]]
    ]
    # worker_datas = generate_worker_dict(worker_data)
    worker_datas = generate_dict(worker_keys, worker_data)
    job_datas = generate_dict(job_keys, job_data)
    # print(worker_datas[0]['score'])
    # print(job_datas[0]['capacityList'])

    result, vacancy_mat = do_job_assignment(worker_datas, job_datas)
    for job in vacancy_mat:
        print(f"{job['capacityList']}")
    for worker in result:
        print(worker)
    # print(result)