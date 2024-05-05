# Copyright (C) 2022 Aaron Gibson (eulersidcrisis@yahoo.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
try:
    import pkg_resources

    __version__ = pkg_resources.get_distribution("bufferq").version
except Exception:
    __version__ = "unknown"

# Bring the following imports into scope.
from bufferq.base import AbstractQueue, AsyncAbstractQueue
from bufferq.queues import Queue, PriorityQueue, LIFOQueue
from bufferq.errors import QueueError, QueueEmpty, QueueFull, QueueStopped

# Bring the following Asynchronous queues into scope as well.
from bufferq.async_queues import AsyncQueue, AsyncLIFOQueue, AsyncPriorityQueue

__all__ = [
    "QueueError",
    "QueueEmpty",
    "QueueFull",
    "QueueStopped",
    "AbstractQueue",
    "Queue",
    "PriorityQueue",
    "LIFOQueue",
    "AsyncAbstractQueue",
    "AsyncQueue",
    "AsyncLIFOQueue",
    "AsyncPriorityQueue",
]
