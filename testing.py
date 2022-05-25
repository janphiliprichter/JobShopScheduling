from read_files import read_jssp
from functions import schedule_jobs, combinations, rollout, print_all_jobs, print_schedule, print_total_makespan


jobs, machines, all_jobs = read_jssp("instances/ft06.txt")

print("All jobs:")
print_all_jobs(all_jobs)
print("")


schedule = schedule_jobs(machines, all_jobs)
print("Schedule without rollout:")
print_schedule(schedule)
print_total_makespan(schedule)
print("")

# We need to get the data again, because all jobs is already emptied
_, _, all_jobs = read_jssp("instances/ft06.txt")
final_combs = combinations(all_jobs)
print(f"Number of starting combinations for the rollout: {len(final_combs)}")
print("")

rollout("instances/ft06.txt")
print("")
