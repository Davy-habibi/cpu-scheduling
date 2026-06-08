from collections import deque

def round_robin(processes, quantum):
    n = len(processes)

    queue = deque()
    current_time = 0
    remaining_bt = {p['id']: p['bt'] for p in processes}

    gantt = []
    total_wt = 0
    total_tt = 0

    processes.sort(key=lambda x: x['at'])
    i = 0

    while i < n or queue:
        while i < n and processes[i]['at'] <= current_time:
            queue.append(processes[i])
            i += 1

        if not queue:
            current_time += 1
            continue

        p = queue.popleft()

        start = current_time
        exec_time = min(quantum, remaining_bt[p['id']])
        current_time += exec_time
        remaining_bt[p['id']] -= exec_time

        gantt.append((p['id'], start, current_time))

        while i < n and processes[i]['at'] <= current_time:
            queue.append(processes[i])
            i += 1

        if remaining_bt[p['id']] > 0:
            queue.append(p)
        else:
            finish = current_time
            wt = finish - p['bt'] - p['at']
            tt = finish - p['at']

            p['wt'] = wt
            p['tt'] = tt

            total_wt += wt
            total_tt += tt

    return processes, gantt, total_wt, total_tt