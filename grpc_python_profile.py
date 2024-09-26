import random
import time
import sys
from pandas import DataFrame
import matplotlib.pyplot as plt
import asyncio

from betterproto_py_client.client import (
    list_images as list_images_betterproto,
    stream_images as stream_images_betterproto,
)

from protobuf_py_client.client import (
    list_images as list_images_protobuf,
    stream_images as stream_images_protobuf,
)

from protobuf_py_grpcio_client.client import (
    list_images as list_images_protobuf_grpcio,
    stream_images as stream_images_protobuf_grpcio,
)



class GrpcOperationProfile:
    def __init__(self, op, size, constructor_params=[]):
        self.size = size
        self.test_operation = op
        self.execution_times = []
        self.constructor_params = constructor_params

    def as_tuple(self) -> tuple:
        return (
            self.size,
            self.test_operation.__module__,
            self.test_operation.__name__,
            self.execution_times,
        )

    def run(self, *args, **kwargs) -> None:
        start = time.perf_counter_ns()
        asyncio.run(self.test_operation(*self.constructor_params, *args, **kwargs))
        end = time.perf_counter_ns()
        self.execution_times.append(end - start)


def run_profiles(profiles: GrpcOperationProfile, trials: int) -> None:
    for i in range(trials):
        print(f"Trial: {i + 1}/{trials}")
        random.shuffle(profiles)
        for profile in profiles:
            profile.run()


def to_dataframe(profiles: GrpcOperationProfile):
    frame = DataFrame.from_records(
        data=map(lambda profile: profile.as_tuple(), profiles),
        columns=["arg_size", "module", "operation", "time"],
    )
    frame = frame.explode("time")
    frame["time"] = frame["time"].astype(float)
    frame["time"] /= 10**3
    return frame


def execute_profiles(seed, profiles, num_trials):
    random.seed(seed)
    run_profiles(profiles, num_trials)
    df = to_dataframe(profiles)

    # Plotting time as a function of argument size
    _, ax = plt.subplots()
    plt.title(f"GRPC Client Performance : {sys.platform}")
    ax.set_xlabel("Size of the argument")
    ax.set_ylabel("Time (microseconds)")

    grouped = df.groupby(["module", "operation"])
    for name, group in grouped:
        means = group.groupby("arg_size")["time"].mean()
        ax.plot(means, label=name)
    ax.legend()

    plt.savefig(f"_profiles/grpc_python_profile-{seed}.png")

    # Plotting fps
    _, ax = plt.subplots()
    plt.title(f"GRPC Client Performance : {sys.platform} - FPS")
    ax.set_xlabel("Module")
    ax.set_ylabel("FPS")

    grouped = df.groupby(["module"])
    for i, (name, group) in enumerate(grouped):
        means = group.groupby("arg_size")["time"].mean()
        fps = 1 / (means / 10**6)
        ax.bar(i, fps.mean(), label=name)

    # hide the x-axis ticks
    ax.set_xticks([])

    ax.legend()
    plt.savefig(f"_profiles/grpc_python_profile-fps-{seed}.png")



def unary_unary_profiles(call_numbers: list[int] = [1, 10, 100, 1000]):
    for call_number in call_numbers:
        def unary_unary_call(method):
            async def _():
                for _ in range(call_number):
                    await method()

            return _

        profiles = [
            GrpcOperationProfile(unary_unary_call(list_images_protobuf), size=call_number),
            GrpcOperationProfile(unary_unary_call(list_images_betterproto), size=call_number),
            GrpcOperationProfile(unary_unary_call(list_images_protobuf_grpcio), size=call_number),
        ]

    return profiles


def unary_stream_profiles(stream_image_names: list[list[str]]):
    profiles = []
    for image_names in stream_image_names:
        profiles.append(
            GrpcOperationProfile(stream_images_protobuf, constructor_params=[image_names], size=len(image_names))
        )
        profiles.append(
            GrpcOperationProfile(stream_images_betterproto, constructor_params=[image_names], size=len(image_names))
        )

        profiles.append(
            GrpcOperationProfile(stream_images_protobuf_grpcio, constructor_params=[image_names], size=len(image_names))
        )
    
    return profiles

if __name__ == "__main__":
    
    seed = 46

    #unary_profiles = unary_unary_profiles()

    base_image_names = ["image-0.jpg", "image-1.jpg", "image-2.jpg"]

    # smaller sub samples
    stream_image_names = [ base_image_names* i for i in range(1, 100, 5)]

    stream_profiles = unary_stream_profiles(stream_image_names)

    execute_profiles(seed, stream_profiles, 5)

    