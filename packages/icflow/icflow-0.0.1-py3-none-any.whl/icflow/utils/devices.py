import os
import torch
import torch.multiprocessing as mp
import torch.distributed as dist


class ComputeDevices:
    def __init__(self) -> None:
        pass

    def log_cpu_info(self):
        num_cpus = os.cpu_count()
        print("Num cpus: " + str(num_cpus))

    def log_cuda_info(self):
        if torch.cuda.is_available():
            num_cuda_devices = torch.cuda.device_count()

            print("Supported cuda arch: " + str(torch.cuda.get_arch_list()))
            print("Num cuda devices: " + str(num_cuda_devices))
            for idx in range(num_cuda_devices):

                device_name = torch.cuda.get_device_name(idx)
                print("Querying device: " + str(idx))
                print("Name: " + device_name)

                device_props = torch.cuda.get_device_properties(idx)
                print("Propeties: " + str(device_props))

                memory_use = torch.cuda.memory_usage(idx)
                print("Memory use: " + str(memory_use))

                processor_use = torch.cuda.utilization(idx)
                print("Processor use: " + str(processor_use))

            if num_cuda_devices > 1:
                print(
                    "p2p access available: "
                    + str(torch.cuda.can_device_access_peer(0, 1))
                )
        else:
            print("Cuda not available on system")

    def log_torch_dist_info(self):
        if dist.is_available():
            print("Torch dist is available")

            if dist.is_nccl_available():
                print("Has NCCL")
                nccl_version = torch.cuda.nccl.version()
                print("Nccl version: " + str(nccl_version))
            else:
                print("NCCL Backend not found")

            if dist.is_gloo_available():
                print("Has Gloo")
            else:
                print("Gloo Backend not found")

            if dist.is_mpi_available():
                print("Has MPI")
            else:
                print("MPI Backend not found")

    def log_system_info(self):

        print("PyTorch Version: " + str(torch.__version__))

        self.log_cpu_info()

        self.log_cuda_info()

        self.log_torch_dist_info()

    def per_device_func(self, rank, world_size):
        print("Hello from rank: " + str(rank) + " of " + str(world_size))

        dist.init_process_group("nccl", rank=rank, world_size=world_size)

        print("Dist initialized ok: " + str(dist.is_initialized()))
        print("Running on backend: " + dist.get_backend())
        print("Torch Dist Rank: " + str(dist.get_rank()))
        print("Torch Dist World Size: " + str(dist.get_world_size()))

        print("Current cuda device: " + str(torch.cuda.current_device()))

        output = torch.tensor([rank]).cuda(rank)
        print("Current tensor: " + str(output))
        s = torch.cuda.Stream()

        _ = dist.all_reduce(output, async_op=True)
        with torch.cuda.stream(s):
            s.wait_stream(torch.cuda.default_stream())
            output.add_(100)
        if rank == 0:
            print("Updated tensor: " + str(output))

        self.test_p2p()
        self.test_collective()

    def launch_per_device(self):
        world_size = 2
        mp.spawn(self.per_device_func, args=(world_size,), nprocs=world_size, join=True)

    def test_p2p(self):
        rank = dist.get_rank()
        if rank == 0:
            to_send = torch.tensor([3]).cuda(rank)
            print("Sending to 1")
            dist.send(to_send, 1)
        elif rank == 1:
            to_recv = torch.tensor([0]).cuda(rank)
            sender_rank = dist.recv(to_recv, 0)  # no recv any source on nccl
            print("Recv'd " + str(to_recv) + " from " + str(sender_rank))

    def test_collective(self):
        pass


if __name__ == "__main__":

    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "29500"

    devices = ComputeDevices()

    devices.log_system_info()

    devices.launch_per_device()
