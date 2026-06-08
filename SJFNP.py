def sjf_non_preemptive(processes):
    processes.sort(key=lambda x: (x['at'], x['bt']))
    n = len(processes)

    completed = 0
    current_time = 0
    visited = [False] * n
    gantt = []
    total_wt = 0
    total_tt = 0

    while completed < n:
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            if processes[i]['at'] <= current_time and not visited[i]:
                if processes[i]['bt'] < min_bt:
                    min_bt = processes[i]['bt']
                    idx = i

        if idx == -1:
            current_time += 1
            continue

        p = processes[idx]
        start = current_time
        finish = start + p['bt']

        wt = start - p['at']
        tt = finish - p['at']

        p['wt'] = wt
        p['tt'] = tt

        total_wt += wt
        total_tt += tt

        gantt.append((p['id'], start, finish))

        current_time = finish
        visited[idx] = True
        completed += 1

    return processes, gantt, total_wt, total_tt