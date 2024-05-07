import concurrent.futures
import psutil
import time

def lightning(func, iterable, batch_size=None, verbose=False, timeout=None):
    """
    A high performance module made for batching and parallelizing CPU-bound tasks.

    Example:
        ```python
        import zyx

        def sample_function(x):
            return x * x

        data = list(range(100))
        results = zyx.lightning(sample_function, data, batch_size=10, verbose=True)
        print(results)
        ```

    Args:
        func (function): The function to be executed in parallel.
        iterable (iterable): The data to be processed.
        batch_size (int, optional): The size of each batch. Defaults to None.
        verbose (bool, optional): Whether to print the execution time and memory usage. Defaults to False.
        timeout (int, optional): The maximum number of seconds to wait for the worker threads to finish. Defaults to None.
    """
    num_workers = psutil.cpu_count(logical=False) or 4 

    def process_batch(batch):
        results = []
        for item in batch:
            result = func(item)
            results.append(result)
        return results

    results = []
    if verbose:
        start_time = time.time()
        start_memory = psutil.virtual_memory().used

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        if batch_size:
            batches = [iterable[i:i + batch_size] for i in range(0, len(iterable), batch_size)]
            future_to_batch = {executor.submit(process_batch, batch): batch for batch in batches}
        else:
            future_to_item = {executor.submit(func, item): item for item in iterable}
        for future in concurrent.futures.as_completed(future_to_batch if batch_size else future_to_item, timeout=timeout):
            try:
                batch_results = future.result()
                results.extend(batch_results)
            except Exception as exc:
                item = future_to_batch[future] if batch_size else future_to_item[future]
                print(f'Generated an exception: {exc} with item/batch: {item}')

    if verbose:
        end_time = time.time()
        end_memory = psutil.virtual_memory().used
        execution_time = end_time - start_time
        memory_used = end_memory - start_memory

        print(f"Execution Time: {execution_time:.2f} seconds")
        print(f"Memory Used: {memory_used} bytes")
        print(f"Worker Threads Used: {num_workers}")
        print(f"Available Memory: {psutil.virtual_memory().available} bytes")
        print(f"Total Memory: {psutil.virtual_memory().total} bytes")

    return results

# Example usage
if __name__ == "__main__":
    def sample_function(x):
        return x * x

    data = list(range(100))
    results = lightning(sample_function, data, batch_size=10, verbose=True)
    print(results)
