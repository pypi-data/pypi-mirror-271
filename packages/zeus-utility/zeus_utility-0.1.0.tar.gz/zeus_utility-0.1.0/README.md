# Zeus's Utility

## Features
- [x] Parallel Execute

## Quick Usage:
### Install:
```shell
pip install zeus-utility
# or 
pip install git+https://github.com/zeuscsc/zeus_utility.git
```
### Usage
```python
from zeus_utility.parallel_executor import QueueExecutor
def print_a_plus_b(a,b):
    print(a+b)
executor=QueueExecutor(threads_count=5)
for i in range(10):
    executor.add_task(print_a_plus_b,a=i,b=i)
executor.execute()
```