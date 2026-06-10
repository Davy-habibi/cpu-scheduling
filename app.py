from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

# ================= FCFS =================
def fcfs(processes):
    processes.sort(key=lambda x: x['at'])
    current_time = 0
    gantt = []
    total_wt = 0
    total_tt = 0

    for p in processes:
        if current_time < p['at']:
            current_time = p['at']

        start = current_time
        finish = start + p['bt']

        p['wt'] = start - p['at']
        p['tt'] = finish - p['at']

        total_wt += p['wt']
        total_tt += p['tt']

        gantt.append((p['id'], start, finish))
        current_time = finish

    return processes, gantt, total_wt, total_tt

# ================= SJF NON PREEMPTIVE =================
def sjf_np(processes):
    n = len(processes)
    completed = 0
    current_time = 0
    visited = [False]*n
    gantt = []
    total_wt = total_tt = 0

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

        p['wt'] = start - p['at']
        p['tt'] = finish - p['at']

        total_wt += p['wt']
        total_tt += p['tt']

        gantt.append((p['id'], start, finish))

        current_time = finish
        visited[idx] = True
        completed += 1

    return processes, gantt, total_wt, total_tt

# ================= SJF PREEMPTIVE =================
def sjf_p(processes):
    n = len(processes)
    remaining_bt = [p['bt'] for p in processes]
    current_time = 0
    completed = 0
    gantt = []
    last = -1
    total_wt = total_tt = 0

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

        if last != idx:
            gantt.append([processes[idx]['id'], current_time, current_time])

        gantt[-1][2] += 1
        remaining_bt[idx] -= 1
        current_time += 1
        last = idx

        if remaining_bt[idx] == 0:
            completed += 1
            finish = current_time

            processes[idx]['wt'] = finish - processes[idx]['bt'] - processes[idx]['at']
            processes[idx]['tt'] = finish - processes[idx]['at']

            total_wt += processes[idx]['wt']
            total_tt += processes[idx]['tt']

    return processes, gantt, total_wt, total_tt

# ================= ROUND ROBIN =================
def round_robin(processes, q):
    n = len(processes)
    queue = deque()
    remaining = {p['id']: p['bt'] for p in processes}
    processes.sort(key=lambda x: x['at'])

    current_time = 0
    i = 0
    gantt = []
    total_wt = total_tt = 0

    while i < n or queue:
        while i < n and processes[i]['at'] <= current_time:
            queue.append(processes[i])
            i += 1

        if not queue:
            current_time += 1
            continue

        p = queue.popleft()
        start = current_time
        exec_time = min(q, remaining[p['id']])

        current_time += exec_time
        remaining[p['id']] -= exec_time

        gantt.append((p['id'], start, current_time))

        while i < n and processes[i]['at'] <= current_time:
            queue.append(processes[i])
            i += 1

        if remaining[p['id']] > 0:
            queue.append(p)
        else:
            finish = current_time
            p['wt'] = finish - p['bt'] - p['at']
            p['tt'] = finish - p['at']

            total_wt += p['wt']
            total_tt += p['tt']

    return processes, gantt, total_wt, total_tt


# ================= MAIN ROUTE =================
@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    gantt = []
    total_wt = total_tt = 0

    if request.method == 'POST':
        n = int(request.form['n'])
        algo = request.form['algorithm']

        processes = []

        for i in range(n):
            at_input = request.form.get(f'at{i}')
            bt_input = request.form.get(f'bt{i}')

            if at_input and bt_input:
                processes.append({
                    'id': f'P{len(processes)+1}',
                    'at': int(at_input),
                    'bt': int(bt_input)
                })

        if algo == 'fcfs':
            result, gantt, total_wt, total_tt = fcfs(processes)

        elif algo == 'sjf_np':
            result, gantt, total_wt, total_tt = sjf_np(processes)

        elif algo == 'sjf_p':
            result, gantt, total_wt, total_tt = sjf_p(processes)

        elif algo == 'rr':
            q = int(request.form.get('quantum', 1))
            result, gantt, total_wt, total_tt = round_robin(processes, q)

    return render_template(
        "index.html",
        result=result,
        gantt=gantt,
        total_wt=total_wt,
        total_tt=total_tt,
    )


@app.route('/index.html', methods=['GET'])
def index_html():
    return index()

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)