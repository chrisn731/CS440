import ctypes
import sys

def print_carray(arr):
    l = [x for x in arr.contents]
    for elm in l:
        print(elm)

lib = ctypes.cdll.LoadLibrary("./filter.so")
file = ctypes.c_char_p(bytes(sys.argv[1], encoding='utf-8'))
lib.load_world.restype = ctypes.c_uint
size = lib.load_world(file)

lib.filter_step.restype = ctypes.POINTER(ctypes.c_double * size)

actions = "RDLDDDLRUDDDUDRRRRLLULLLRDRDLUDDRLLDLDRLUUDULRRUUDDUDLDUDRRRDRLLRDLRRRRULRULLRUUULULDDUUDDULLDRRURDD"
sensor_reading = "NNTTNNNTTHHTTHTNNNTHTNNTNTTNNTTTTTTNTNTNTNTHHNNTHHNNNHTHNTNNTTNNNTHTNTNTHNNNTTTTNTNHNTNNTHTTHNNNTHHH"

if len(actions) != len(sensor_reading):
    print("Actions and sensor readings should be the same length!!!")
    exit(1)

start = None
for i in range(100):
    sensor = ctypes.c_char(bytes(sensor_reading[i], encoding='utf-8'))
    action = ctypes.c_char(bytes(actions[i], encoding='utf-8'))
    ret = lib.filter_step(sensor, action, start)
    start = ret

# Uncomment for output
#print_carray(start)
