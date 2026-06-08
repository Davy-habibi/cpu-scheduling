def sjf_preemptive(processes):
    n = len(processes)

    remaining_bt = [p['bt'] for p in processes]
    completed = 0
    current_time = 0

    gantt = []
    last_process = None

    total_wt = 0
    total_tt = 0

    while completed < n:
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            if processes[i]['at'] <= current_time and remaining_bt[i] > 0:
                if remaining_bt[i] < min_bt:
                    min_bt = remaining_bt[i]
                    idx = i

        if idx == -1:
            current_time += 1
            continue

        if last_process != idx:
            gantt.append([processes[idx]['id'], current_time, current_time])

        gantt[-1][2] += 1

        remaining_bt[idx] -= 1
        current_time += 1
        last_process = idx

        if remaining_bt[idx] == 0:
            completed += 1
            finish = current_time

            wt = finish - processes[idx]['bt'] - processes[idx]['at']
            tt = finish - processes[idx]['at']

            processes[idx]['wt'] = wt
            processes[idx]['tt'] = tt

            total_wt += wt
            total_tt += tt

    return processes, gantt, total_wt, total_tt
