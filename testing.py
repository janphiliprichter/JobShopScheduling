from read_files import read_jssp
from functions import create_schedule, makespan, print_schedule, print_all_jobs, print_total_makespan

# Reading in the instance file
jobs, machines, all_jobs = read_jssp("ft06.txt")

# Printing information about the instance
print("")
print("Number of jobs: ", jobs)
print("Number of machines: ", machines)
print("")

# Getting and printing the makespans for the jobs
makespans = makespan(all_jobs)
print("Job makespans:")
print(makespans)
print("")

# Printing the jobs of the instance
print_all_jobs(all_jobs)
print("")

# Creating the schedule for the jobs
schedule = create_schedule(machines, jobs, all_jobs)

# Printing the schedule
print_schedule(schedule)
print("")

# Printing the total makespan
print_total_makespan(schedule)
print("")


