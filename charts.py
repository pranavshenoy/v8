
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import statistics
import glob
import sys
import random
import os
import math
from tabulate import tabulate
from scipy.stats import linregress
import pathlib
from enum import Enum
import matplotlib.colors as pltc

# class Data:
#     def __init__(self, table):
#         # self.gc_time = column(table, 4)
#         pass

MB = 1024 * 1024
colors = ["lightsteelblue", "darkviolet", "blue", "pink", "yellow", "gold", "orange", "red", "brown", "lightcoral", "lightgrey", "dimgrey", "black", "lightpink", "violet"]
symbols = ["-", ">", "<", "o", "+", "*", "1", "2", "3", "h"]
if(len(sys.argv) == 1):
    print("Pass output directory")
    exit()

input_dir = sys.argv[1]+"/"

def read_file(filename):
    data = []
    for line in open(filename):
        data.append(line.strip().split("\t"))
    return data

def column(matrix, i):
    matrix = matrix[1:]
    matrix = np.asarray(matrix, dtype=int)
    return [row[i] for row in matrix]

def cleanup():
    dirs = get_dirs()
    #cleanup all plots
    files = glob.glob(input_dir+"*.png")
    for file in files:
        os.remove(file)

    for _, dir in enumerate(dirs):
        files = glob.glob(dir+"*.png")
        for file in files:
            os.remove(file)

def get_files(dir):
    files = glob.glob(dir+"v8_young_gen_*.log")
    return files

def get_dirs():
    dirs = glob.glob(input_dir+"/*/")
    return dirs

def get_title(dir):
    path = pathlib.PurePath(dir)
    if path.name == "t":
        return "TypeScript"
    if path.name == "p":
        return "PdfJS"
    if path.name == "s":
        return "Splay"
    return path.name

# def plot_graph(x, y, xlabel, ylabel, filename, dir, title):
#     if(len(x) == 0 or len(y) == 0):
#         return
#     plt.figure()
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.title(title)
#     plt.plot(x, y, 'o')
#     plt.savefig(dir+filename+".png")
#     plt.close()

def get_intercept(a, b):
    if len(a) == 0 or len(b) == 0:
        return 
    res = linregress(a, b)
    # print(res)
    return res.intercept

# def plot_func(dir, fx, fy, x_axis_label, y_axis_label, img_name, add_intercept):
#     files = get_files(dir)
#     x = []
#     y = []
#     for file in files:
#         data = read_file(file)
#         if len(data) <= 2:
#             continue
#         x_ = fx(data)
#         y_ = fy(data)
#         x.append(x_)
#         y.append(y_)

#     #find intercept
#     # print(dir)
#     y_intercept = get_intercept(x, y)
#     if add_intercept:
#         if y_intercept:
#             x.append(0)
#             y.append(y_intercept)
#     plot_graph(x, y, x_axis_label, y_axis_label, img_name, dir, get_title(dir))
#     return y_intercept

# def plot_for_all_dir(fx, fy, x_axis_label, y_axis_label, img_name, add_intercept):
#     dirs = get_dirs()
#     y_intercepts = []
#     for _, dir in enumerate(dirs):
#         y_intercept = plot_func(dir, fx, fy, x_axis_label, y_axis_label, img_name, add_intercept)
#         y_intercepts.append([get_title(dir), y_intercept])
#     return y_intercepts

def get_mean_after_verify(col):
    if(len(set(col)) == 0):
        return 
    assert(len(set(col)) == 1)
    return mean(col)

class Column(Enum):
    GC_TIME = 11
    YG_SIZE = 7
    PROMOTED_BYTES = 9
    USED_BYTES = 5

def get_sum(col):
    s = sum(col)
    print(s)
    return s

class NamedFunction:
    def __init__(self, func, name):
        self.func = func
        self.name = name

class BenchmarkData:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

def get_benchmark_data_for(dir, benchmark_name, fx, fy):
    files = get_files(dir)
    x = []
    y = []
    for file in files:
        data = read_file(file)
        if len(data) <= 2: #first one is the header
            continue
        x_ = fx(data)
        y_ = fy(data)
        x.append(x_)
        y.append(y_)
    intercept = get_intercept(x, y)
    if intercept:
        x.append(0)
        y.append(intercept)
    bm = BenchmarkData(x, y, benchmark_name)    
    return bm

# [benchmarkdata([x], [y], "acdc"), ....]
def get_all_benchmark_data(param):
    dirs = get_dirs()
    all_benchmarks = []
    fx = param["fx"].func
    fy = param["fy"].func
    for _, dir in enumerate(dirs):
        benchmark_name = get_title(dir)
        bm_data = get_benchmark_data_for(dir, benchmark_name, fx, fy)
        all_benchmarks.append(bm_data)
    return all_benchmarks

def plot_all_benchmarks(param, benchmark_data):
    
    plt.figure()
    plt.xlabel(param["fx"].name)
    plt.ylabel(param["fy"].name)
    for i, bm_data in enumerate(benchmark_data):
        if(len(bm_data.x) == 0 or len(bm_data.y) == 0):
            continue
        plt.plot(bm_data.x, bm_data.y, 'o', markersize=6, label = bm_data.name, color= colors[i % len(colors)])

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=5, fancybox=True, shadow=False, prop={'size': 6})
    filename = param["fy"].name + param["fx"].name
    plt.savefig(input_dir+filename+".png")
    plt.close()

def get_y_intercepts(benchmarks):
    x = []
    y = []
    for bm in benchmarks:
        intercept = get_intercept(bm.x, bm.y)
        if intercept:
            x.append(bm.name)
            y.append(intercept)
    return (x, y)

def plot_y_intercepts(param, benchmarks):
    (x, y) = get_y_intercepts(benchmarks)
    print("x: "+ str(x) + " y: "+str(y) )
    plt.figure()
    plt.xlabel("benchmarks")
    plt.ylabel("y intercepts")
    plt.bar(x, y)
    plt.xticks(rotation=90, ha='right')
    filename = "y_intercept-"+param["fy"].name
    plt.title(filename)
    plt.savefig(input_dir+filename+".png")
    plt.close()


def plot_for_all_params(params):
    for param in params:
        all_benchmarks = get_all_benchmark_data(param)
        plot_all_benchmarks(param, all_benchmarks)
        if param["y_intercept"] == False:
            continue
        plot_y_intercepts(param, all_benchmarks)


YoungGenSize = NamedFunction((lambda data : get_mean_after_verify(column(data, 7))), "Young generation size (B)")
TotalPromotedBytes = NamedFunction((lambda data : sum(column(data, 9))), "Promoted bytes (B)")
MeanPromotedBytes = NamedFunction((lambda data : mean(column(data, 9))), "Promoted bytes (B)")
PromotionRate = NamedFunction((lambda data : sum(column(data, 9)) / (sum(column(data, 2)) - sum(column(data, 5)) )), "Promotion Rate")
TotalAllocatedBytes = NamedFunction((lambda data : sum(column(data, 5))), "Total Allocated bytes")
TotalTime = NamedFunction((lambda data : sum(column(data, 11))), "Time  (ns)")
MeanAllocatedBytes = NamedFunction((lambda data : mean(column(data, 5))), "Mean Allocated bytes")
AccurateAllocatedBytes = NamedFunction((lambda data : sum(column(data, 2)) - sum(column(data, 5))), "Allocated bytes")

params = [
    {
        "fx": YoungGenSize,
        "fy": PromotionRate,
        "y_intercept": True
    },
    {
        "fx": YoungGenSize,
        "fy": TotalPromotedBytes,
        "y_intercept": True
    }, 
    # {
    #     "fx": YoungGenSize,
    #     "fy": TotalTime,
    #     "y_intercept": True
    # }, 
    # {
    #     "fx": YoungGenSize,
    #     "fy": MeanPromotedBytes,
    #     "y_intercept": False
    # }, 
    # {
    #     "fx": YoungGenSize,
    #     "fy": MeanAllocatedBytes,
    #     "y_intercept": False
    # },
    {
        "fx": YoungGenSize,
        "fy": AccurateAllocatedBytes,
        "y_intercept": False
    }, 

]








# def generate_y_intercept_table(param, y_intercepts):
#     if param["add_intercept"] == False:
#         return
#     # print("Intercepts for "+param["img_name"]+"\n")
#     # only_intercepts = [row[1] for row in y_intercepts]
#     # print("Mean: "+ str(mean(only_intercepts)))
#     # print("Std Deviation: "+ str(np.std(only_intercepts)))
#     head = ["Benchmark", "y_Intercept"]
#     print(tabulate(y_intercepts, headers=head, tablefmt="grid"))

cleanup()
# for param in params:
#     y_intercepts = plot_for_all_dir(param["fx"].func, param["fy"].func, param["fx"].name, param["fy"].name, param["fx"].name + param["fy"].name, param["add_intercept"])
#     # generate_y_intercept_table(param, y_intercepts)
plot_for_all_params(params)
