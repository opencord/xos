from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'grpc_request_count', 'GRPC Request Count',
    ['app_name', 'model_name', 'endpoint', 'status']
)

# TODO (teone) add caller as label for the counter (eg: GUI, TOSCA, SYNCHRONIZER)
# TODO (teone) add user informations as label for the counter