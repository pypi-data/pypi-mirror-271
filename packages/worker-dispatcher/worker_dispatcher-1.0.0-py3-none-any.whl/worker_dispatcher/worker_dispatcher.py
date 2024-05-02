import multiprocessing, concurrent.futures
import time, copy, requests

# Sample callback function
def callback_sample(id: int, config=None, task=None):
    if id == 1:
        print("Runing sample task function, please customize yours according to the actual usage.")
    result = {
        'taskId': id
    }
    return result

# Sample result callback function
def result_callback_sample(id: int, config=None, result=None, log: dict=None):
    if id == 1:
        print("Runing sample result function, please customize yours according to the actual usage.")
    return result

# Default configuration
default_config = {
    'debug': False,
    'task': {
        'list': [],                     # Support list and integer. Integer represent the number of tasks to be generated.
        'callback': callback_sample,
        'config': {},
        'result_callback': False
    },
    'worker': {
        'number': multiprocessing.cpu_count(),
        'per_second': 0,                # If greater than 0, the specified number of workers run at set intervals.
        'cumulative': False,            # Cumulative mode for per_second method.
        'multiprocessing': False
    }
}

# Global variable
results = []
logs = []
result_info = {}

# Start function
def start(userConfig: dict) -> list:

    global results, logs, result_info
    results = []
    logs = []

    # Merge config with 2 level
    config = copy.deepcopy(default_config)
    for level1_key in config.keys():
        if level1_key in userConfig:
            if isinstance(config[level1_key], dict):
                config[level1_key].update(userConfig[level1_key])
            else:
                config[level1_key] = userConfig[level1_key]

    # Multi-processing handler
    use_multiprocessing = config['worker']['multiprocessing']
    if use_multiprocessing:
        in_child_process = (multiprocessing.current_process().name != 'MainProcess')
        # Return False if is in worker process to let caller handle
        if in_child_process:
            # print("Exit procedure due to the child process")
            return False
        
    # Debug mode
    if config['debug']:
        print("Configuration Dictionary:")
        print(config)

    # Callback check
    if not callable(config['task']['callback']):
        exit("Callback function is invalied")

    # Task list to queue
    task_list = []
    user_task_list = config['task']['list']
    if isinstance(user_task_list, list):
        id = 1
        for task in user_task_list:
            data = {
                'id': id,
                'task': task
            }
            task_list.append(data)
            id += 1
    elif isinstance(user_task_list, int):
        for i in range(user_task_list):
            id = i + 1
            data = {
                'id': id,
                'task': {}
            }
            task_list.append(data)

    # Worker dispatch
    worker_num = config['worker']['number']
    worker_num = worker_num if isinstance(worker_num, int) else 1
    worker_per_second = config['worker']['per_second'] if config['worker']['per_second'] else 0
    max_workers = len(task_list) if worker_per_second else worker_num
    print("Worker Dispatcher Configutation:")
    print("- Task Number: {}".format(len(task_list)))
    print("- Worker Type:", "Processing" if use_multiprocessing else "Threading")
    print("- Worker Number: {}".format(worker_num))
    print("- Worker Per Second: {}".format(worker_per_second))
    print("- Max Worker: {}".format(max_workers))
    pool_executor_class = concurrent.futures.ProcessPoolExecutor if use_multiprocessing else concurrent.futures.ThreadPoolExecutor
    result_info['started_at'] = time.time()
    print("\n--- Start to dispatch workers ---\n")

    # Pool Executor
    with pool_executor_class(max_workers=max_workers) as executor:
        pool_results = []
        per_second_count = worker_num
        # Task dispatch
        for task in task_list:
            pool_result = executor.submit(consume_task, task, config)
            pool_results.append(pool_result)
            # Worker per_second setting
            per_second_count -= 1
            if worker_per_second and per_second_count <= 0:
                if config['worker']['multiprocessing']:
                    worker_num += worker_per_second
                per_second_count = worker_num
                time.sleep(float(worker_per_second))
        timestamp_end_dispatch = time.time()
        # Get results from the async results
        for pool_result in concurrent.futures.as_completed(pool_results):
            log = pool_result.result()
            result = log['result']
            if callable(config['task']['result_callback']):
                result = config['task']['result_callback'](config=config['task']['config'], id=log['task_id'], result=log['result'], log=log)
            logs.append(log)
            results.append(result)
        # results = [result.result() for result in concurrent.futures.as_completed(pool_results)]

    result_info['ended_at'] = time.time()
    result_info['duration'] = result_info['ended_at'] - result_info['started_at']
    print("\n--- End of worker dispatch ---\n")
    print("Spend Time: {:.6f} sec".format(result_info['duration']))
    return results

# Worker function
def consume_task(data, config) -> dict:
    started_at = time.time()
    return_value = config['task']['callback'](config=config['task']['config'], id=data['id'], task=data['task'])
    ended_at = time.time()
    duration = ended_at - started_at
    log = {
        'task_id': data['id'],
        'started_at': started_at,
        'ended_at': ended_at,
        'duration': duration,
        'result': return_value
    }
    return log

# TPS report
def get_tps(logs: dict=None, debug: bool=False, peak_duration: float=0) -> dict:
    logs = logs if logs else get_logs()
    if not isinstance(logs, list):
        return False
    started_at = 0
    ended_at = 0
    total_count = len(logs)
    invalid_count = 0
    success_count = 0
    success_logs = []
    duration_sum = 0
    duration_max = 0
    # Data processing
    for log in logs:
        if not all(key in log for key in ('started_at', 'ended_at', 'result')):
            invalid_count += 1
            continue
        started_at = log['started_at'] if log['started_at'] < started_at or started_at == 0 else started_at
        ended_at = log['ended_at'] if log['ended_at'] > ended_at else ended_at
        duration = log['duration'] if 'duration' in log else log['ended_at'] - log['started_at']
        duration_sum += duration
        duration_max = duration if duration > duration_max else duration_max
        result = log['result']
        if (isinstance(result, requests.Response) and result.status_code != 200) or not result:
            continue
        success_count += 1
        success_logs.append(log)
    
    valid_count = total_count - invalid_count
    duration = ended_at - started_at
    tps = success_count / duration if success_count else 0

    # Peak TPS
    duration_avg = duration_sum / valid_count if duration_sum else 0
    peak_duration = peak_duration if peak_duration else duration_avg * 3
    # peak_duration = duration_max
    peak_tps_data = {}
    peak_success_count = 0
    peak_ended_at = ended_at
    peak_started_at = peak_ended_at
    if debug:
        print("Peak - vaild count:{}, duration/interval:{}".format(valid_count, peak_duration));
    while peak_started_at > started_at:
        current_success_count = 0
        peak_ended_at = peak_started_at
        peak_started_at -= peak_duration
        if peak_started_at <= started_at:
            peak_started_at = started_at
            peak_duration = peak_ended_at - peak_started_at
        for log in success_logs:
            if log['started_at'] < peak_started_at or log['ended_at'] > peak_ended_at:
                continue
            current_success_count += 1
        if debug:
            print("Each Peak - count:{}, start:{}, end:{}".format(current_success_count, peak_started_at, peak_ended_at))
        if current_success_count and current_success_count > peak_success_count:
            peak_success_count = current_success_count
            peak_tps = peak_success_count / peak_duration
            if debug:
                print(" - peak_tps:{}, tps:{}".format(peak_tps, tps))
            if peak_tps > tps:
                peak_tps_data = {
                    'tps': "{:.{}f}".format(peak_tps, 2),
                    'started_at': peak_started_at,
                    'ended_at': peak_ended_at,
                    'duration': peak_duration,
                    'count': {
                        'success': peak_success_count
                    }
                }

    result = {
        'tps': "{:.{}f}".format(tps, 2),
        'started_at': started_at,
        'ended_at': ended_at,
        'duration': duration,
        'count': {
            'success': success_count,
            'invalidity': invalid_count,
            'total': total_count
        },
        'peak': peak_tps_data
    }
    return result

def get_results() -> list:
    return results

def get_logs() -> list:
    return logs

def get_result_info() -> dict:
    return result_info

def get_duration() -> float:
    return result_info['started_at'] if 'started_at' in result_info else None