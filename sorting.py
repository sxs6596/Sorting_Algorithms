''' WORKING '''
import tkinter as tk
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''Sorting Algorithms'''


# Merge Sort
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        left_half = arr[:mid]  # left half
        right_half = arr[mid:]  # right half

        merge_sort(left_half)  # Sorting the first half recursively.
        merge_sort(right_half)  # Sorting the second half recursively.

        i = j = k = 0  # i for left half, j for right half, k for main array

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):  # if there are any elements left in left half
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):  # if there are any elements left in right half
            arr[k] = right_half[j]
            j += 1
            k += 1


# Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr.pop()  # last element as pivot
        low = []  # left half
        high = []  # right half

        for i in arr:
            if i < pivot:
                # if element is less than pivot, append to left half
                low.append(i)
            else:
                # if element is greater than pivot, append to right half
                high.append(i)

        # recursively sort left and right halves
        return quick_sort(low) + [pivot] + quick_sort(high)


# Heap Sort
def heap_sort(arr):
    def heapify(arr, n, i):
        largest = i  # largest element
        l = 2 * i + 1  # left child
        r = 2 * i + 2  # right child

        if l < n and arr[largest] < arr[l]:  # if left child is larger than root
            largest = l

        if r < n and arr[largest] < arr[r]:  # if right child is larger than root
            largest = r

        if largest != i:  # if largest is not root
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)

    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):  # build a maxheap
        heapify(arr, n, i)  # heapify the subtree

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


# Quick Sort (Median-of-Three)
def quick_sort_median(arr):
    def median(arr):
        arr.sort()
        return arr[len(arr) // 2]  # return the middle element

    def partition(arr, low, high):  # partition the array
        mid = (low + high) // 2
        # pivot is the median of the first, middle, and last elements
        pivot = median([arr[low], arr[mid], arr[high]])

        i = low - 1  # index of smaller element

        for j in range(low, high):
            if arr[j] < pivot:  # if current element is smaller than the pivot
                i += 1
                arr[i], arr[j] = arr[j], arr[i]  # swap

        # swap with the last element
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1  # return the index of the pivot

    def quick_sort_median_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)  # partition index
            quick_sort_median_helper(arr, low, pi - 1)
            quick_sort_median_helper(arr, pi + 1, high)

    quick_sort_median_helper(arr, 0, len(arr) - 1)


# Selection Sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i  # index of minimum element
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:  # if current element is smaller than the minimum element
                min_index = j  # update the index of minimum element

        arr[i], arr[min_index] = arr[min_index], arr[i]  # swap


# Bubble Sort
def bubble_sort(arr):
    n = len(arr)

    for i in range(n - 1):  # traverse through all elements
        for j in range(n - i - 1):  # last i elements are already in place
            if arr[j] > arr[j + 1]:  # if current element is greater than the next element
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # swap


# Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]  # current element
        j = i - 1  # index of the previous element
        # if current element is smaller than the previous element
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]  # move the previous element forward
            j -= 1  # decrement the index of the previous element
        arr[j + 1] = key  # insert the current element

# generate runtimes for each sorting algorithm


def generate_runtimes(n):
    # dictionary of sorting algorithms
    sorting_algorithms = {
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
        "Quick Sort (Median-of-Three)": quick_sort_median,
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
    }
    # dictionary of running times
    times = {}

    for name, sort_fn in sorting_algorithms.items():
        arr = [random.randint(0, n) for _ in range(n)]
        start_time = time.time()
        sort_fn(arr)

        if n < 50:  # print the elements after sorting if n<20
            print(f"\n{name} ({n} elements): {arr}")

        end_time = time.time()
        running_time = end_time - start_time
        times[name] = running_time

    runtimes = pd.DataFrame.from_dict(
        times, orient='index', columns=['Running Time (s)'])
    runtimes = runtimes.sort_values("Running Time (s)")

    return runtimes  # return the runtimes dataframe


''' GROUP PLOTTING '''

# plot runtimes for each sorting algorithm


def plot_runtimes(input_size):
    root = tk.Tk()  # create a new Tkinter window
    root.title(f"Sorting Algorithm Runtimes (n = {input_size})")

    # Generate runtimes
    # generate runtimes for input_size
    runtimes = generate_runtimes(input_size)
    algorithms = runtimes.index.tolist()  # list of sorting algorithms
    # list of running times
    running_times = runtimes["Running Time (s)"].tolist()

    # Print sorting algorithm runtimes to console
    print(
        f"\nSorting Algorithms and Their Running Time Complexity (n = {input_size}):\n")
    for name, complexity in runtimes.iterrows():
        print(f"{name} - {complexity['Running Time (s)']:.6f} s")

    # Add input size and runtimes label to GUI
    input_label = tk.Label(root, text=f"Input size: {input_size}")
    input_label.pack()

    runtimes_label = tk.Label(
        root, text="Sorting Algorithms and Their Running Time Complexity:")
    runtimes_label.pack()

    runtimes_textbox = tk.Text(root, height=10, width=50)
    runtimes_textbox.pack()

    for name, complexity in runtimes.iterrows():  # add each sorting algorithm and its running time to the GUI
        runtimes_textbox.insert(
            tk.END, f"{name} - {complexity['Running Time (s)']:.6f} s\n")

    # Set colors for each bar
    colors = ['#2A9D8F', '#E9C46A', '#F4A261',
              '#E76F51', '#264653', '#7E6A9E', '#F72585']

    # create a new figure
    fig, ax = plt.subplots()
    ax.bar(algorithms, running_times, align='center', color=colors)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Running Time (s)')
    plt.title(f'Sorting Algorithm Runtimes (n = {input_size})')

    # Embed plot in Tkinter window
    # Add the plot to the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Start the event loop for the window
    root.mainloop()


'''INDIVIDUAL PLOTTING '''


# def individualPlot(input_size, running_time, algorithm_type):
#     # Create a new Toplevel window
#     plot_window = tk.Toplevel(window)
#     plot_window.title(f'{algorithm_type}') # set the title with variable algorithm_type.

#     # Create a new figure
#     fig = plt.figure(figsize=(6, 4))

#     # Scatter plot the data
#     plt.scatter(input_size, running_time)
#     plt.xlabel('Input Size')
#     plt.ylabel('Running Time')

#     # Create a FigureCanvasTkAgg widget for displaying the plot
#     canvas = FigureCanvasTkAgg(fig, master=plot_window)
#     canvas.get_tk_widget().pack()

#     # Update the canvas to draw the plot
#     canvas.draw()

# individual plotting
def individualPlot(input_size, running_time, algorithm_type):
    # Create a new Toplevel window
    plot_window = tk.Toplevel(window)
    # set the title with variable algorithm_type.
    plot_window.title(f'{algorithm_type}')

    # Create a new figure
    fig = plt.figure(figsize=(6, 4))

    # Scatter plot the data
    plt.scatter(input_size, running_time)
    plt.xlabel('Input Size')
    plt.ylabel('Running Time')

    # Create a FigureCanvasTkAgg widget for displaying the plot
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.get_tk_widget().pack()

    # Update the canvas to draw the plot
    canvas.draw()
    # add label for input size and running time
    label_text = f'Input Size: {input_size}\nRunning Time: {running_time}'
    label = tk.Label(plot_window, text=label_text)
    label.pack()

# run the algorithm for the selected algorithm type


def run_algorithm():
    input_val = (input_box.get())
    n = int(input_val)
    algorithm_type = drop_down.get()
    arr = [random.randint(0, n) for _ in range(n)]
    algorithm_functions = {
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort,
        "Heap Sort": heap_sort,
        "Quick Sort (Median-of-Three)": quick_sort_median,
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
    }
    # call function for matching algorithm index
    if algorithm_type in algorithm_functions:
        if (algorithm_type == algorithm_type):
            start_time = time.time()
            algorithm_functions[algorithm_type](arr)
            end_time = time.time()
            running_time = end_time - start_time
            individualPlot(n, running_time, algorithm_type)
            print(
                f'algorithm name :{algorithm_type} and running time is {running_time}')
        else:
            print(f'No algorithm found for index {algorithm_type}')


# Create a new Tkinter window
window = tk.Tk()

# Add a label for the input size
input_label = tk.Label(window, text="Input size:")
input_label.pack()

# Add an entry box for the input size
input_box = tk.Entry(window)
input_box.pack()

# Add a label for the type of algorithm
algorithm_label = tk.Label(window, text="Type of algorithm:")
algorithm_label.pack()

# Add a drop-down for the algorithm types
algorithms = ["Merge Sort", "Quick Sort", "Heap Sort",
              "Quick Sort (Median-of-Three)", "Selection Sort", "Bubble Sort", "Insertion Sort"]
drop_down = tk.StringVar(window)
drop_down.set(algorithms[0])  # Set the default value
drop_down_menu = tk.OptionMenu(window, drop_down, *algorithms)
drop_down_menu.pack()

# Add a "Run" button
run_button = tk.Button(window, text="Run", command=run_algorithm)
run_button.pack()

# Add a "Run All Algorithms" button
run_all_button = tk.Button(window, text="Run All Algorithms",
                           command=lambda: plot_runtimes(int(input_box.get())))
run_all_button.pack()

# Start the event loop
window.mainloop()
