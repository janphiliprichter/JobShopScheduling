def read_jssp(filename):
    """
    Read in all information from a jssp-instance
    :param filename: Path to the jssp-instance file
    :return jobs, machines, all_jobs
    """
    skip_lines = 4
    jobs = None
    machines = None
    all_jobs = []

    with open(filename) as f:
        for e, l in enumerate(f):
            if e == skip_lines:
                line = l.split()
                jobs = int(line[0])
                machines = int(line[1])

            if e > skip_lines:
                line = l.split()
                s = []
                job = []
                for n in line:
                    s.append(int(n))
                    if len(s) == 2:
                        s = tuple(
                            s)
                        job.append(s)
                        s = []
                all_jobs.append(job)

    return jobs, machines, all_jobs
