
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

# class Data:
#     def __init__(self, table):
#         # self.gc_time = column(table, 4)
#         pass

MB = 1024 * 1024
colors = ["red", "blue", "orange", "green", "brown", "pink", "yellow", "black", "blue", "purple", "silver"]

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

def plot_graph(x, y, xlabel, ylabel, filename, dir, title):
    if(len(x) == 0 or len(y) == 0):
        return
    plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot(x, y, 'o')
    plt.savefig(dir+filename+".png")
    plt.close()

def get_intercept(a, b):
    if len(a) == 0 or len(b) == 0:
        return 
    res = linregress(a, b)
    # print(res)
    return res.intercept

def plot_func(dir, fx, fy, x_axis_label, y_axis_label, img_name, add_intercept):
    files = get_files(dir)
    x = []
    y = []
    for file in files:
        data = read_file(file)
        if len(data) <= 2:
            continue
        x_ = fx(data)
        y_ = fy(data)
        x.append(x_)
        y.append(y_)

    #find intercept
    # print(dir)
    y_intercept = get_intercept(x, y)
    if add_intercept:
        if y_intercept:
            x.append(0)
            y.append(y_intercept)
    plot_graph(x, y, x_axis_label, y_axis_label, img_name, dir, get_title(dir))
    return y_intercept

def plot_for_all_dir(fx, fy, x_axis_label, y_axis_label, img_name, add_intercept):
    dirs = get_dirs()
    y_intercepts = []
    for _, dir in enumerate(dirs):
        y_intercept = plot_func(dir, fx, fy, x_axis_label, y_axis_label, img_name, add_intercept)
        y_intercepts.append([get_title(dir), y_intercept])
    return y_intercepts

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


params = [
    # {
    #     "fx": lambda data : get_mean_after_verify(column(data, 7)),
    #     "fy": lambda data : sum(column(data, 9)),
    #     "x_axis_label": "Young generation size (B)",
    #     "y_axis_label": "Promoted bytes (B)",
    #     "img_name" : "promotion-bytes-yg",
    #     "add_intercept": False
    # }, 
    # {
    #     "fx": lambda data : get_mean_after_verify(column(data, 7)),
    #     "fy": lambda data : sum(column(data, 11)),
    #     "x_axis_label": "Young generation size (B)",
    #     "y_axis_label": "gc_time (ns)",
    #     "img_name" : "gc-time",
    #     "add_intercept": False
    # }, 
    # {
    #     "fx": lambda data : get_mean_after_verify(column(data, 7)),
    #     "fy": lambda data : 1/len(column(data, 11)),
    #     "x_axis_label": "Young generation size (B)",
    #     "y_axis_label": "1/frequency",
    #     "img_name" : "gc-frequency",
    #     "add_intercept": False
    # }, 
    {
        "fx": lambda data : get_mean_after_verify(column(data, 7)),
        "fy": lambda data : mean(column(data, 11)),
        "x_axis_label": "Young generation size (B)",
        "y_axis_label": "mean_gc_time (ns)",
        "img_name" : "mean-gc-time",
        "add_intercept": True
    }, 
    # {
    #     "fx": lambda data : len(column(data, 11)),
    #     "fy": lambda data : sum(column(data, 9)),
    #     "x_axis_label": "gc_frequency",
    #     "y_axis_label": "promoted bytes (B)",
    #     "img_name" : "promoted-vs-frequency",
    #     "add_intercept": False
    # }, 
    # {
    #     "fx": lambda data : sum(column(data, 9)),
    #     "fy": lambda data : sum(column(data, 11)),
    #     "x_axis_label": "total promoted bytes (B)",
    #     "y_axis_label": "time",
    #     "img_name" : "total-promoted-vs-time",
    #     "add_intercept": False
    # }, 
    # {
    #     "fx": lambda data : mean(column(data, 9)),
    #     "fy": lambda data : mean(column(data, 11)),
    #     "x_axis_label": "total promoted bytes (B)",
    #     "y_axis_label": "time",
    #     "img_name" : "mean-promoted-vs-time",
    #     "add_intercept": False
    # }, 
    {
        "fx": lambda data : mean(column(data, 7)),
        "fy": lambda data : mean(column(data, 9)),
        "x_axis_label": "mean promoted bytes (B)",
        "y_axis_label": "promoted bytes",
        "img_name" : "mean-promoted-bytes-vs-size",
        "add_intercept": True
    }, 
    {
        "fx": lambda data : sum(column(data, 9)),
        "fy": lambda data : sum(column(data, Column.PROMOTED_BYTES)/sum(column(data, Column.))),
        "x_axis_label": "total promoted bytes (B)",
        "y_axis_label": "time",
        "img_name" : "total-promoted-vs-time",
        "add_intercept": False
    }, 
]



def generate_y_intercept_table(param, y_intercepts):
    if param["add_intercept"] == False:
        return
    # print("Intercepts for "+param["img_name"]+"\n")
    # only_intercepts = [row[1] for row in y_intercepts]
    # print("Mean: "+ str(mean(only_intercepts)))
    # print("Std Deviation: "+ str(np.std(only_intercepts)))
    head = ["Benchmark", "y_Intercept"]
    print(tabulate(y_intercepts, headers=head, tablefmt="grid"))

cleanup()
for param in params:
    y_intercepts = plot_for_all_dir(param["fx"], param["fy"], param["x_axis_label"], param["y_axis_label"], param["img_name"], param["add_intercept"])
    # generate_y_intercept_table(param, y_intercepts)





# first_half = lambda data : data[0: int(len(data)/2)]
# second_half = lambda data : data[ int(len(data)/2): ]

# params = [
    
#     {
#         "fx": lambda data : get_mean_after_verify(column(data, Column.YG_SIZE.value)),
#         "fy": lambda data : mean(column(data, Column.USED_BYTES.value)),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "mean_used_bytes (B)",
#         "img_name" : "mean-used_bytes",
#         "add_intercept": True
#     },
#     {
#         "fx": lambda data : get_mean_after_verify(second_half(column(data, Column.YG_SIZE.value))),
#         "fy": lambda data : mean(second_half(column(data, Column.GC_TIME.value)) ),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "mean_gc_time (ns)",
#         "img_name" : "mean-gc-time_second_half",
#         "add_intercept": True
#     }, 
#     {
#  "fx": lambda data : get_mean_after_verify(first_half(column(data, Column.YG_SIZE.value))),
#         "fy": lambda data : mean(first_half(column(data, Column.GC_TIME.value)) ),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "mean_gc_time (ns)",
#         "img_name" : "mean-gc-time_first_half",
#         "add_intercept": True
#     }, 
#     {
#         "fx": lambda data : get_mean_after_verify(column(data, Column.YG_SIZE.value)),
#         "fy": lambda data : mean(column(data, Column.GC_TIME.value )),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "mean_gc_time (ns)",
#         "img_name" : "mean-gc-time_full_data",
#         "add_intercept": True
#     }, 
#     {
#         "fx": lambda data : get_mean_after_verify(first_half(column(data, Column.YG_SIZE.value))),
#         "fy": lambda data : mean(first_half(column(data, Column.PROMOTED_BYTES.value))),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "promoted bytes",
#         "img_name" : "mean-promoted-bytes-vs-size-first_half",
#         "add_intercept": True
#     }, 
#     {
#         "fx": lambda data : get_mean_after_verify(second_half(column(data, Column.YG_SIZE.value))),
#         "fy": lambda data : mean(second_half(column(data, Column.PROMOTED_BYTES.value))),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "promoted bytes",
#         "img_name" : "mean-promoted-bytes-vs-size-second_half",
#         "add_intercept": True
#     }, 
#     {
#         "fx": lambda data : get_mean_after_verify(column(data, Column.YG_SIZE.value)),
#         "fy": lambda data : mean(column(data, Column.PROMOTED_BYTES.value)),
#         "x_axis_label": "Young generation size (B)",
#         "y_axis_label": "promoted bytes",
#         "img_name" : "mean-promoted-bytes-vs-size-full_data",
#         "add_intercept": True
#     }, 
# ]


# def generate_y_intercept_table(param, y_intercepts):
#     if param["add_intercept"] == False:
#         return
#     # print("Intercepts for "+param["img_name"]+"\n")
#     # only_intercepts = [row[1] for row in y_intercepts]
#     # print("Mean: "+ str(mean(only_intercepts)))
#     # print("Std Deviation: "+ str(np.std(only_intercepts)))
#     head = ["Benchmark", "y_Intercept"]
#     print(tabulate(y_intercepts, headers=head, tablefmt="grid"))

# cleanup()
# for param in params:
#     y_intercepts = plot_for_all_dir(param["fx"], param["fy"], param["x_axis_label"], param["y_axis_label"], param["img_name"], param["add_intercept"])
#     # generate_y_intercept_table(param, y_intercepts)
