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

        wt = start - p['at']
        tt = finish - p['at']

        total_wt += wt
        total_tt += tt

        p['wt'] = wt
        p['tt'] = tt

        gantt.append((p['id'], start, finish))
        current_time = finish

    return processes, gantt, total_wt, total_tt


n = int(input("Jumlah proses: "))
processes = []

for i in range(n):
    at = int(input(f"Arrival Time P{i+1}: "))
    bt = int(input(f"Burst Time P{i+1}: "))
    processes.append({'id': f"P{i+1}", 'at': at, 'bt': bt})


result, gantt, total_wt, total_tt = fcfs(processes)

print("\n=== GANTT CHART ===")
for g in gantt:
    print(f"| {g[0]} ({g[1]}-{g[2]}) ", end="")
print("|")

print("\n=== TABLE ===")
print("Process\tAT\tBT\tWT\tTT")
for p in result:
    print(f"{p['id']}\t{p['at']}\t{p['bt']}\t{p['wt']}\t{p['tt']}")

print("\nTotal WT:", total_wt)
print("Total TT:", total_tt)
print("Average WT:", total_wt / n)
print("Average TT:", total_tt / n)