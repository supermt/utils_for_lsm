
from db_bench_runner import reset_CPUs
from db_bench_runner import restrict_cpus
from db_bench_runner import initial_cgroup

initial_cgroup()
restrict_cpus(10)
reset_CPUs()