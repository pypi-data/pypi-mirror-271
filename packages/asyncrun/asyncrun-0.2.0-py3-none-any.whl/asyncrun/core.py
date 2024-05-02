import concurrent.futures
import tqdm
import inspect

def all(function, args, workers=8):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = []
        for call_args in args:
            sig = inspect.signature(function)
            if len(sig.parameters) == 0:
                future = executor.submit(function)
            elif isinstance(call_args, (tuple, list)):
                future = executor.submit(function, *call_args)
            else:
                future = executor.submit(function, call_args)
            futures.append(future)
        with tqdm.tqdm(total=len(futures)) as progress:
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    progress.update(1)
                except Exception as e:
                    print(f"[asyncrun error]: {e}")
                    progress.update(1)
    return results