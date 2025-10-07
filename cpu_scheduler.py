import copy
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

# ---------- Scheduling Algorithms ----------

def fcfs(proc):
    proc.sort(key=lambda x: x[1])
    time = 0
    gantt = []
    for p in proc:
        if time < p[1]:
            time = p[1]
        start = time
        time += p[2]
        completion = time
        turnaround = completion - p[1]
        waiting = turnaround - p[2]
        gantt.append((p[0], start, completion))
        p.extend([completion, turnaround, waiting])
    return gantt, proc

def sjf(proc):
    proc.sort(key=lambda x: (x[1], x[2]))
    time = 0
    completed = []
    gantt = []
    while proc:
        available = [p for p in proc if p[1] <= time]
        if not available:
            time += 1
            continue
        p = min(available, key=lambda x: x[2])
        proc.remove(p)
        start = time
        time += p[2]
        completion = time
        turnaround = completion - p[1]
        waiting = turnaround - p[2]
        gantt.append((p[0], start, completion))
        p.extend([completion, turnaround, waiting])
        completed.append(p)
    return gantt, completed

def priority_scheduling(proc):
    proc.sort(key=lambda x: (x[1], x[3]))
    time = 0
    completed = []
    gantt = []
    while proc:
        available = [p for p in proc if p[1] <= time]
        if not available:
            time += 1
            continue
        p = min(available, key=lambda x: x[3])
        proc.remove(p)
        start = time
        time += p[2]
        completion = time
        turnaround = completion - p[1]
        waiting = turnaround - p[2]
        gantt.append((p[0], start, completion))
        p.extend([completion, turnaround, waiting])
        completed.append(p)
    return gantt, completed

def round_robin(proc, quantum=2):
    proc.sort(key=lambda x: x[1])
    time = 0
    queue = proc.copy()
    remaining = {p[0]: p[2] for p in proc}
    gantt = []
    completed = []

    while queue:
        p = queue.pop(0)
        pid, arrival, burst, priority = p[:4]
        if time < arrival:
            time = arrival
        run = min(quantum, remaining[pid])
        start = time
        time += run
        remaining[pid] -= run
        gantt.append((pid, start, time))

        if remaining[pid] > 0:
            queue.append(p)
        else:
            completion = time
            turnaround = completion - arrival
            waiting = turnaround - burst
            p.extend([completion, turnaround, waiting])
            completed.append(p)
    return gantt, completed

# ---------- Smarter Algorithm Suggestion ----------

def suggest_algorithm(processes):
    bursts = [p[2] for p in processes]
    arrivals = [p[1] for p in processes]
    priorities = [p[3] for p in processes]

    burst_max = max(bursts)
    burst_min = min(bursts)
    priority_range = max(priorities) - min(priorities)
    arrival_range = max(arrivals) - min(arrivals)

    # Decision rules based on OS scheduling theory
    if priority_range >= 2:
        return "Priority", "⚡ Significant priority differences detected — Priority Scheduling will handle urgency best."
    elif burst_max > 2 * burst_min:
        return "SJF", "📊 Some processes are much shorter — SJF will reduce average waiting time."
    elif arrival_range > (burst_max + burst_min):
        return "FCFS", "📈 Processes arrive far apart — FCFS is simplest and avoids starvation."
    elif all(b < 6 for b in bursts):
        return "Round Robin", "🌀 All processes are short — Round Robin ensures responsive time-sharing."
    else:
        return "SJF", "📊 Balanced workload — SJF generally gives the best turnaround time."

# ---------- Results Display ----------

def plot_gantt_chart(gantt, title):
    fig, ax = plt.subplots(figsize=(8, 2))
    colors = {}
    color_index = 0

    for (pid, start, end) in gantt:
        if pid not in colors:
            colors[pid] = plt.cm.tab20(color_index)
            color_index += 1
        ax.barh(0, end - start, left=start, height=0.4, color=colors[pid])
        ax.text((start + end) / 2, 0, pid, ha='center', va='center', color='white', fontsize=9)

    ax.set_xlabel("Time")
    ax.set_ylabel("CPU")
    ax.set_title(title + " - Gantt Chart")
    ax.set_yticks([])
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# ---------- GUI Logic ----------

def create_process_fields():
    for widget in process_frame.winfo_children():
        widget.destroy()

    try:
        n = int(num_processes_entry.get())
    except:
        messagebox.showerror("Error", "Enter a valid number of processes.")
        return

    # Create header row
    headers = ["PID", "Arrival Time", "Burst Time", "Priority"]
    for col, text in enumerate(headers):
        tk.Label(process_frame, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=10, pady=5)

    global entries
    entries = []
    for i in range(n):
        pid_label = tk.Label(process_frame, text=f"P{i+1}", font=("Arial", 10))
        pid_label.grid(row=i+1, column=0, padx=10, pady=5)

        arrival_entry = tk.Entry(process_frame, width=10)
        burst_entry = tk.Entry(process_frame, width=10)
        priority_entry = tk.Entry(process_frame, width=10)

        arrival_entry.insert(0, "0")
        burst_entry.insert(0, "1")
        priority_entry.insert(0, "1")

        arrival_entry.grid(row=i+1, column=1, padx=10, pady=5)
        burst_entry.grid(row=i+1, column=2, padx=10, pady=5)
        priority_entry.grid(row=i+1, column=3, padx=10, pady=5)
        entries.append((f"P{i+1}", arrival_entry, burst_entry, priority_entry))

def get_process_data():
    processes = []
    for pid, arrival_entry, burst_entry, priority_entry in entries:
        arrival = int(arrival_entry.get())
        burst = int(burst_entry.get())
        priority = int(priority_entry.get())
        processes.append([pid, arrival, burst, priority])
    return processes

def run_simulation():
    try:
        processes = get_process_data()

        algo = algo_var.get()
        if algo == "":
            messagebox.showerror("Error", "Please select a scheduling algorithm.")
            return

        try:
            quantum = int(quantum_entry.get())
            if quantum <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Please enter a positive integer time quantum.")
            return

        if algo == "FCFS":
            gantt, results = fcfs(copy.deepcopy(processes))
        elif algo == "SJF":
            gantt, results = sjf(copy.deepcopy(processes))
        elif algo == "Priority":
            gantt, results = priority_scheduling(copy.deepcopy(processes))
        elif algo == "Round Robin":
            gantt, results = round_robin(copy.deepcopy(processes), quantum=quantum)

        show_results(results, gantt, algo)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def suggest_best_algorithm():
    try:
        processes = get_process_data()
        suggestion, reason = suggest_algorithm(processes)
        suggestion_label.config(text=f"📊 Suggested Algorithm: {suggestion}\n💡 Reason: {reason}")
    except Exception as e:
        messagebox.showerror("Error", f"Unable to suggest algorithm: {e}")

def show_results(results, gantt, algo):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"=== {algo} Results ===\n")
    result_text.insert(tk.END, "PID\tArrival\tBurst\tCompletion\tTAT\tWT\n")

    total_wt = total_tat = 0
    for p in results:
        result_text.insert(tk.END, f"{p[0]}\t{p[1]}\t{p[2]}\t{p[4]}\t{p[5]}\t{p[6]}\n")
        total_wt += p[6]
        total_tat += p[5]

    n = len(results)
    result_text.insert(tk.END, f"\nAverage Waiting Time: {total_wt / n:.2f}")
    result_text.insert(tk.END, f"\nAverage Turnaround Time: {total_tat / n:.2f}")

    plot_gantt_chart(gantt, algo)

# ---------- GUI Setup ----------

root = tk.Tk()
root.title("CPU Scheduling Simulator (GUI)")
root.geometry("720x700")

tk.Label(root, text="CPU Scheduling Simulator", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Number of Processes:").pack()
num_processes_entry = tk.Entry(root, width=10)
num_processes_entry.pack()

tk.Button(root, text="Create Process Fields", command=create_process_fields).pack(pady=5)

process_frame = tk.Frame(root)
process_frame.pack(pady=5)

# Suggestion Button
tk.Button(root, text="Suggest Best Algorithm", command=suggest_best_algorithm, bg="orange").pack(pady=8)
suggestion_label = tk.Label(root, text="", font=("Arial", 11), fg="green", wraplength=650, justify="left")
suggestion_label.pack()

# Algorithm selection
tk.Label(root, text="Choose Scheduling Algorithm:").pack()
algo_var = tk.StringVar()
algo_dropdown = ttk.Combobox(root, textvariable=algo_var, values=["FCFS", "SJF", "Priority", "Round Robin"])
algo_dropdown.pack()

# Time Quantum (always visible)
tk.Label(root, text="Time Quantum (Only used for Round Robin):").pack(pady=5)
quantum_entry = tk.Entry(root)
quantum_entry.insert(0, "2")
quantum_entry.pack()

tk.Button(root, text="Run Simulation", command=run_simulation, bg="lightblue").pack(pady=15)

result_text = tk.Text(root, height=15, width=80, font=("Courier", 10))
result_text.pack(pady=5)

root.mainloop()
