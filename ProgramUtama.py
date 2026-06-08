from FCFS import fcfs
from SJFNP import sjf_non_preemptive
from SJFP import sjf_preemptive
from ROUNDROBIN import round_robin

def input_proses():
    n = int(input("Jumlah proses: "))
    processes = []

    for i in range(n):
        at = int(input(f"Arrival Time P{i+1}: "))
        bt = int(input(f"Burst Time P{i+1}: "))
        processes.append({'id': f"P{i+1}", 'at': at, 'bt': bt})

    return processes


def tampilkan_hasil(result, gantt, total_wt, total_tt):
    print("\n=== GANTT CHART ===")
    for g in gantt:
        print(f"| {g[0]} ({g[1]}-{g[2]}) ", end="")
    print("|")

    print("\n=== TABLE ===")
    print("Process\tAT\tBT\tWT\tTT")
    for p in result:
        print(f"{p['id']}\t{p['at']}\t{p['bt']}\t{p['wt']}\t{p['tt']}")

    n = len(result)
    print("\nTotal WT:", total_wt)
    print("Total TT:", total_tt)
    print("Average WT:", total_wt / n)
    print("Average TT:", total_tt / n)


# MAIN MENU
while True:
    print("\n=== CPU SCHEDULING SIMULATOR ===")
    print("1. FCFS")
    print("2. SJF Non-Preemptive")
    print("3. SJF Preemptive")
    print("4. Round Robin")
    print("5. Keluar")

    pilih = int(input("Pilih algoritma: "))

    if pilih == 5:
        print("Program selesai.")
        break

    processes = input_proses()

    if pilih == 1:
        result, gantt, twt, ttt = fcfs(processes)

    elif pilih == 2:
        result, gantt, twt, ttt = sjf_non_preemptive(processes)

    elif pilih == 3:
        result, gantt, twt, ttt = sjf_preemptive(processes)

    elif pilih == 4:
        quantum = int(input("Masukkan Time Quantum: "))
        result, gantt, twt, ttt = round_robin(processes, quantum)

    else:
             print("Pilihan tidak valid!")
             continue

    tampilkan_hasil(result, gantt, twt, ttt)
