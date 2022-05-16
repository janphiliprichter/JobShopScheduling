

def makespan(all_jobs):
    """
    Get the makespan times of all jobs
    :param all_jobs: Nested list of all jobs
    :return: List of the makespan times for each job
    """
    # Empty makespans list to be filled
    makespans = [0] * len(all_jobs)

    # For every job we sum up the time of all tasks
    for job in range(len(all_jobs)):
        for task in all_jobs[job]:
            makespans[job] += task[1]

    return makespans


def release_time(jobs, machines, schedule):
    """
    For each job we calculate the current release time.
    This is the earliest time the next task of the job can be executed, given the current schedule.
    :param jobs: Int. Number of jobs
    :param machines: Int. Number of machines
    :param schedule: Nested list of the current schedule
U    :return: List of the release times
    """
    # Empty release_times list to be filled
    release_times = [0] * jobs

    # For every machine in the schedule we calculate the release time for every job
    # and update when we get a larger release time
    for i in range(machines):
        rt = 0
        for j in range(len(schedule[i])):
            job = schedule[i][j][0]
            if isinstance(job, int):
                if release_times[job] < rt + schedule[i][j][1]:
                    release_times[job] = rt + schedule[i][j][1]
            rt += schedule[i][j][1]

    return release_times


def create_schedule(machines, jobs, all_jobs):
    """
    Create a schedule for all jobs.
    :param jobs: Int. Number of jobs
    :param machines: Int. Number of machines
    :param all_jobs: Nested list of all jobs
    :return: Nested list of the schedule
    """
    # Empty schedule to be filled
    schedule = [[] for _ in range(machines)]

    # For every task that exists we successively find the next one to schedule
    for _ in range(jobs * machines):

        # Getting the release times for each job
        release_times = release_time(jobs, machines, schedule)
        # Getting the makespans for each job
        makespans = makespan(all_jobs)
        # Getting the index of the job with the maximum makespan
        max_ms_ind = makespans.index(max(makespans))
        # Getting the next task of that job
        next_task = all_jobs[max_ms_ind][0]
        # Getting the machine, that the next task has to be run on
        next_machine = next_task[0]
        # Calculating the runtime of all tasks so far on the next machine
        runtime_next_machine = sum([task[1] for task in schedule[next_machine]])

        # When the release time of the next job is larger than the current runtime of all tasks on the machine,
        # we have to pause the machine until the next task is ready to be executed
        if release_times[max_ms_ind] > runtime_next_machine:
            schedule[next_task[0]].append(("pause", release_times[max_ms_ind] - runtime_next_machine))
            schedule[next_task[0]].append((max_ms_ind, next_task[1]))
        # If not we can execute the task straight away
        else:
            schedule[next_task[0]].append((max_ms_ind, next_task[1]))
        # We delete that task from the all_jobs list to find the next task to execute
        del all_jobs[max_ms_ind][0]

    return schedule


def print_schedule(schedule):
    """
    Print out a schedule machine-wise
    :param schedule: Nested list of the schedule to print
    """
    print("Schedule:")
    for i in range(len(schedule)):
        print(f"Machine {i}: {schedule[i]}")


def print_all_jobs(all_jobs):
    """
    Print out the all_jobs list job-wise
    :param all_jobs: Nested list of all jobs
    """
    print("All Jobs:")
    for i in range(len(all_jobs)):
        print(f"Job {i}: {all_jobs[i]}")


def print_total_makespan(schedule):
    """
    Print out the total makespan
    :param schedule: Nested list of the schedule
    """
    time_per_machine = [0] * len(schedule)
    for i in range(len(schedule)):
        for j in range(len(schedule[i])):
            time = schedule[i][j][1]
            time_per_machine[i] += time
    print(f"The total makespan is: {max(time_per_machine)} time units")


