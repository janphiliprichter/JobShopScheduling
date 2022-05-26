import time
from read_files import read_jssp
import numpy as np


def max_makespan(all_jobs):
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

    return makespans.index(max(makespans))


def earliest_release(schedule, next_job):
    """
    Create the earliest release time of the next job over all machines
    :param schedule: Nested list of the current schedule
    :param next_job: The next job that we calculate the earliest release time for
    :return: Int. earliest release time for the next job
    """
    release_times = [0] * len(schedule)

    for i in range(len(schedule)):
        for j in range(len(schedule[i])):

            if schedule[i][j][0] == next_job:
                release_times[i] = sum(x[1] for x in schedule[i][:j+1])

    return max(release_times)


def remaining_tasks(all_jobs):
    """
    Calculate the number of remaining tasks in all_jobs
    :param all_jobs: Nested list of all jobs
    :return: Int. number of remaining tasks
    """
    number_tasks = 0
    for job in all_jobs:
        number_tasks += len(job)

    return number_tasks


def schedule_jobs(machines, all_jobs, schedule=None):
    """
    Schedule the jobs in all_jobs using the greedy heuristic.
    :param machines: Int. Number of machines
    :param all_jobs: Nested list of all jobs
    :param schedule: Nested list of the current schedule (optional)
    :return: Int. number of remaining tasks
    """

    # If no schedule was given, we create an empty one to fill with the jobs
    if not schedule:
        schedule = [[] for _ in range(machines)]

    # Calculating the number of remaining tasks in all_jobs
    number_tasks = remaining_tasks(all_jobs)

    # We schedule each of the remaining jobs
    for i in range(number_tasks):

        # Find next task to be scheduled
        next_job = max_makespan(all_jobs)
        next_task = all_jobs[next_job][0]

        # Find corresponding machine
        next_machine = next_task[0]

        # Find the earliest release time of the next task
        rt_job = earliest_release(schedule, next_job)

        # Find the earliest release time for the corresponding machine
        rt_machine = sum(x[1] for x in schedule[next_machine])

        # Checking where to schedule the next task
        # If the next task is not ready when the previous tasks on the machine are done,
        # we need to insert idle time on the machine first
        if rt_job > rt_machine:
            schedule[next_machine].append((-1, (rt_job - rt_machine)))
            schedule[next_machine].append((next_job, next_task[1]))
        # If the next task is ready exactly when the previous tasks on the machine are done, we can append the next task
        elif rt_job == rt_machine:
            schedule[next_machine].append((next_job, next_task[1]))
        # If the next task is ready before the previous tasks on the machine are done, we need to check,
        # if there is idle time scheduled on the machine already long enough to insert the next task.
        else:
            found_pause = False
            rt = 0
            for j in range(len(schedule[next_machine])):
                rt += schedule[next_machine][j][1]
                # When this statement is true, there is a window of idle time long enough and late enough
                # to insert the next task. Now we have to find out how to exactly insert the next task
                if rt >= rt_job + next_task[1] and schedule[next_machine][j][0] == -1:
                    # When the next task is ready at the beginning of the idle time window we schedule
                    # the next task as early as possible
                    if rt_job <= rt - schedule[next_machine][j][1]:
                        diff = schedule[next_machine][j][1] - next_task[1]
                        schedule[next_machine][j] = (next_job, next_task[1])
                        if diff > 0:
                            # If the next task took less time than the idle time window, we fill up the remaining time
                            # with idle time again
                            schedule[next_machine].insert(j + 1, (-1, diff))
                        found_pause = True
                        break
                    else:
                        # If the next task is not ready at the beginning of the idle time window
                        # we first insert idle time until the next task is ready, and the schedule the next task
                        pt_before = rt_job - (rt - schedule[next_machine][j][1])
                        pt_after = schedule[next_machine][j][1] - pt_before - next_task[1]
                        schedule[next_machine][j] = (-1, pt_before)
                        schedule[next_machine].insert(j + 1, (next_job, next_task[1]))
                        found_pause = True
                        # If there is still time left, we have to schedule the remaining idle time after the taskt
                        if pt_after > 0:
                            schedule[next_machine].insert(j + 2, (-1, pt_after))
                        break
            # If we did not find an idle time window big enough we have to append the next task to the machine
            if not found_pause:
                schedule[next_machine].append((next_job, next_task[1]))

        # Remove the scheduled task from all_jobs
        del all_jobs[next_job][0]

    return schedule


def combinations_with_replacement(iterable, r):
    """
    Same function as in the itertools package.
    Only difference is, that this creates lists instead of tuples.
    """
    # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
    pool = list(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r
    yield list(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield list(pool[i] for i in indices)


def combinations(all_jobs):
    """
    Create all allowed combinations of next tasks from an all_jobs nested list
    :param all_jobs: Nested list of all jobs
    :return: Nested list of all allowed combinations of next tasks
    """
    # Get the next tasks for every job in all_jobs
    next_tasks = [[all_jobs[i][0][0], all_jobs[i][0][1], i] for i in range(len(all_jobs))]
    # Create a list of all machines needed for the next tasks
    next_machines = [task[0] for task in next_tasks]
    # Get the number of different machines used in next_tasks
    number_combs = len(set(next_machines))
    # Create all possible combinations of the next_tasks
    all_combs = list(combinations_with_replacement(next_tasks, number_combs))
    # Empty list which will be filled with the allowed combinations
    final_combs = []

    # We iterate over all combinations and remove the infeasible ones
    # E.g.: Combinations using the same machines get removed
    for comb in all_combs:
        c = []
        for task in comb:
            if task not in c:
                c.append(task)
        # We remove combinations using the same machines
        db = [e[0] for e in c]
        if len(db) == len(set(db)):
            final_combs.append(c)

    return final_combs


def rollout(instance_path):
    """
    Create and print a schedule for every allowed combination of next tasks
    :param instance_path: Instance path of the jssp file
    :return: None
    """
    # Start time of the rollout
    start_time = time.time()
    # Reading in the data from the instance_path
    _, _, all_jobs = read_jssp(instance_path)
    # List of all allowed combinations for the rollout
    final_combs = combinations(all_jobs)
    # List of schedules to be filled for every combination
    schedules = [[] for _ in final_combs]
    # List of all_jobs for every combination
    all_jobs_list = [[] for _ in final_combs]

    # For every combination we fill the schedule with the task and remove those tasks from all_jobs
    for i in range(len(final_combs)):
        _, machines, all_jobs = read_jssp(instance_path)
        schedule = [[] for _ in range(machines)]

        for task in final_combs[i]:
            schedule[task[0]].append((task[2], task[1]))
            del all_jobs[task[2]][0]
        schedules[i] = schedule
        all_jobs_list[i] = all_jobs

    makespans = []
    # For every schedule we fill the remaining tasks using the greedy heuristic
    for i in range(len(schedules)):
        print(f"Schedule {i} before greedy heuristic:")
        print_schedule(schedules[i])
        print("")
        schedules[i] = schedule_jobs(machines, all_jobs_list[i], schedule=schedules[i])
        print(f"Final schedule {i}:")
        print_schedule(schedules[i])
        print_total_makespan(schedules[i])
        makespans.append(total_makespan(schedules[i]))
        print("")

    print(f"The minimum total makespan is {min(makespans)} time units from schedule {np.argmin(makespans)}")
    print("")
    duration = time.time() - start_time
    print(f"Time for the rollout: {duration} seconds")

    return


def print_schedule(schedule):
    """
    Print out a schedule machine-wise
    :param schedule: Nested list of the schedule to print
    """
    for i in range(len(schedule)):
        print(f"Machine {i}: {schedule[i]}")


def print_all_jobs(all_jobs):
    """
    Print out the all_jobs list job-wise
    :param all_jobs: Nested list of all jobs
    """
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


def total_makespan(schedule):
    """
    Calculate the total makespan
    :param schedule: Nested list of the schedule
    :return Int. total makespan of the schedule
    """
    time_per_machine = [0] * len(schedule)
    for i in range(len(schedule)):
        for j in range(len(schedule[i])):
            time = schedule[i][j][1]
            time_per_machine[i] += time

    return max(time_per_machine)
