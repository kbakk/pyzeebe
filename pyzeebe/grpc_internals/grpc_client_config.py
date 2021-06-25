GRPC_CHANNEL_OPTIONS = {
    # https://docs.camunda.io/docs/product-manuals/zeebe/deployment-guide/operations/setting-up-a-cluster/#keep-alive-intervals
    "grpc.keepalive_time_ms": 45_000
}


def _grpc_channel_options():
    """ Channel arguments are expected as a tuple of tuples:
    https://grpc.github.io/grpc/python/glossary.html#term-channel_arguments """
    return (
        (k, v) for k, v in GRPC_CHANNEL_OPTIONS.items()
    )
