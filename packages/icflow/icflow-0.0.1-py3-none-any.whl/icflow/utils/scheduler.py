import os
import socket
import torch.distributed as dist


def run(rank, size, hostname):
    print(f"I am {rank} of {size} in {hostname}")


def init_processes(my_rank, world_size, hostname, fn, backend):

    os.environ["MASTER_ADDR"] = os.environ["SLURM_LAUNCH_NODE_IPADDR"]
    os.environ["MASTER_PORT"] = "8933"

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("my ip: ", ip_address)
    fn(my_rank, world_size, hostname)

    dist.init_process_group(
        backend, init_method="env://", rank=my_rank, world_size=world_size
    )
    print("Initialized Rank:", dist.get_rank())


if __name__ == "__main__":
    world_size = int(os.environ["SLURM_NPROCS"])
    my_rank = int(os.environ["SLURM_PROCID"])

    hostname = socket.gethostname()

    init_processes(my_rank, world_size, hostname, run, backend="nccl")
