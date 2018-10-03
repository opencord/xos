# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from prometheus_client import Counter, Histogram
import time

REQUEST_COUNT = Counter(
    'grpc_request_count', 'GRPC Request Count',
    ['app_name', 'model_name', 'endpoint', 'status']
)

# TODO (teone) add caller as label for the counter (eg: GUI, TOSCA, SYNCHRONIZER)
# TODO (teone) add user informations as label for the counter

REQUEST_LATENCY = Histogram(
    'grpc_request_latency_seconds', 'GRPC Request latency',
    ['app_name', 'model_name', 'endpoint']
)

def get_indices_for_uppercase_letter(s):
    return [i for i, c in enumerate(s) if c.isupper()]

def get_labels_from_func_name(f):
    method = f.__name__
    try:
        strip_to = get_indices_for_uppercase_letter(method)[1]
        model = method[strip_to:]
    except IndexError:
        model = method

    return [model, method]

def track_request_time(function):
    """
    This decorator register the request time of a request
    """

    def wrapper(*args, **kwargs):

        [model, method] = get_labels_from_func_name(function)

        start_time = time.time()
        res = function(*args, **kwargs)
        resp_time = time.time() - start_time
        REQUEST_LATENCY.labels('xos-core', model, method).observe(resp_time)
        return res

    return wrapper