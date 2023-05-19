import random
import time
import matplotlib.pyplot as plt
#from memory_profiler import memory_usage
import tracemalloc


def generate_tasks(num_tasks, max_duration, max_due_date):
    tasks = []
    for i in range(num_tasks):
        duration = random.randint(1, max_duration)
        due_date = random.randint(duration, max_due_date)
        tasks.append([i, duration, due_date, 0])
    return tasks

def edd_schedule(tasks):
    # Sort the tasks in non-ascending order of due date
    tasks.sort(key=lambda x: x[2], reverse=True)
    schedule = []
    time = 0
    for task in tasks:
        task_id, duration, due_date, remaining = task
        if time + duration <= due_date:
            # Schedule the task
            schedule.append(task)
            time += duration

    for task in schedule:
      print("Executing Task ", task[0], ": ")
      duration = task[1]
      while duration != 0:
        print("*", end = "")
        duration -= 1
      print()  


    return schedule

def edf_schedule_with_preemptions(tasks):
  tasks.sort(key=lambda x: x[2]) # sort tasks based on due date
  schedule = []
  time = 0
  counter = 0
  cpu_counter = 0
  task_preempt_at = random.randint(5, cpu_counter+15)
  print("Next task at:",task_preempt_at)
  #new_task = tasks[0]
  new_task_id = len(tasks) - 1

  while bool(tasks):
    task_id, duration, due_date, remaining_time = tasks[0]
    tasks.pop(0)
    print("Executing Task ", task_id,": ", end='')
    remaining_time = duration
    while remaining_time > 0:

      if(cpu_counter == task_preempt_at):
        task_preempt_at = random.randint(cpu_counter+3, cpu_counter + 30) 
        #print("Next Task Preempt at:", task_preempt_at)
        new_task = generate_tasks(1, 5, cpu_counter+20)[0]
        new_task_id += 1
        if new_task[2] < cpu_counter:
          print("N\u00b0", end = "")
        elif bool(tasks) and (new_task[2] < due_date):
          print("N+")
          tasks.insert(0,[task_id, remaining_time, due_date, 0])
          remaining_time = new_task[1]
          due_date = new_task[2]
          print("Executing Task ", new_task_id,": ", end='')
          #tasks.pop(0)
        else:
          print("N", end="")
          tasks.append([new_task_id,new_task[1], new_task[2],0 ])
          tasks.sort(key=lambda x: x[2])

      remaining_time -= 1
      cpu_counter += 1
      print('*', end='')
    print()
    #counter += 1

def test_scheduling_algorithms(tasks):
    #tasks = generate_tasks(num_tasks, 20,25)
    
    
    tracemalloc.start()
    start = time.perf_counter()
    edd_schedule(tasks)
    edd_time = round((time.perf_counter() - start) * 1000, 2)
    current, peak = tracemalloc.get_traced_memory()
    edd_memory = peak - current
    tracemalloc.stop()
    
    tracemalloc.start()
    start = time.perf_counter()
    edf_schedule_with_preemptions(tasks)
    edf_time = round((time.perf_counter() - start) * 1000, 2)
    current, peak = tracemalloc.get_traced_memory()
    edf_memory = (peak - current) / 1024
    print("Memory consumed by", tasks, "tasks (in KBs):" ,edf_memory)
    print("Time (in ms):", edf_time)
    tracemalloc.stop()

    #edd_memory = memory_usage((edd_schedule, (tasks,)))[0]
    #edf_memory = memory_usage((edf_schedule_with_preemptions, (tasks,)))[0]

    return  edd_time, edf_time, edd_memory, edf_memory
  

def plot_results(edd_time, edf_time,edd_memory, edf_memory):

    
    # plotting the line 1 points
    plt.plot(num_tasks, edd_time, label = "EDD")
    
    # line 2 points
    # plotting the line 2 points
    plt.plot(num_tasks, edf_time, label = "EDF")
   
    #plt.plot(edd_times, label='EDD')
    #plt.plot(edf_times, label='EDF')
    plt.xlabel('No of tasks')
    plt.ylabel('Time')
    plt.legend()
    plt.show()
  
    # plotting the line 1 points
    plt.plot(num_tasks, edd_memory, label = "EDD")
    
    # line 2 points
    # plotting the line 2 points
    plt.plot(num_tasks, edf_memory, label = "EDF")
   
    #plt.plot(edd_times, label='EDD')
    #plt.plot(edf_times, label='EDF')
    plt.xlabel('No of tasks')
    plt.ylabel('Memory')
    plt.legend()
    plt.show()



num_tasks = list(range(100, 1001, 100))
edd_times = []
edf_times = []
edd_memory_consumption = []
edf_memory_consumption = []

tasks = generate_tasks(100,8,200)
'''
print("ID                Duration              Deadline")
for i in tasks:
  print(i[0],"\t\t\t", i[1],"\t\t\t", i[2])

for n in range(5,101,10):
  print("Schedule for ", n, "tasks:")
  sub_tasks = tasks[0:n]
  #print(sub_tasks)
  edf_schedule_with_preemptions(sub_tasks)
'''

for n in range(100,1001,100):
  sub_tasks = tasks[0:n]
  print("Schedule for ", n, "tasks:")
  edd_time, edf_time, edd_memory, edf_memory= test_scheduling_algorithms(sub_tasks)
  edd_times.append(edd_time)
  edf_times.append(edf_time)
  edd_memory_consumption.append(edd_memory)
  edf_memory_consumption.append(edf_memory)


#print(edf_times)
#print(edf_memory)
# Plot the results
plot_results(edd_times, edf_times,edd_memory_consumption, edf_memory_consumption)
