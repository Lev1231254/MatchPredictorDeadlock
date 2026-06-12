from pathlib import Path


def find_biggest_lesser_num(arr, num):
    # arr is sorted
    if len(arr) == 0: return None
    if min(arr) > num: return None
        
    for i in range(1, len(arr)):
        if arr[i] > num:
            return i - 1
            
    return len(arr) - 1

def find_all_time_stamps():
    time_stamps = [int(f.name[7:-4]) for f in Path("data/").glob("matches*.csv")]
    time_stamps.sort()
    return time_stamps
