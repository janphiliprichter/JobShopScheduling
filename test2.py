from read_files import read_jssp
from functions import schedule_jobs, combinations, rollout, print_all_jobs, print_schedule, print_total_makespan, rollout2, multistep, max_makespan
import copy

instance_path = "instances/abz6"

jobs, machines, all_jobs = read_jssp(instance_path)

print("All jobs:")
print_all_jobs(all_jobs)
print("")

schedule = schedule_jobs(machines, all_jobs)
print("Schedule without rollout:")
print_schedule(schedule)
print_total_makespan(schedule)
print("")

multistep(instance_path, machines)




