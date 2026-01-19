import pandas as pd
import glob
import os
from multiprocessing import Pool, cpu_count

BUCKETS = [
    'bucket_1','bucket_2','bucket_3','bucket_4','bucket_5',
    'bucket_6','bucket_7','bucket_8','bucket_9',
    'bucket_a','bucket_b','bucket_c','bucket_d','bucket_e','bucket_f'
]

BASE_GLOB = "/datadrive/jupyter/RPSGDirectory/FeatherRepo_R1/*"
COLUMNS = ['R1_s']
POOL_SIZE = min(30, cpu_count())

def read_feather_count(path):
    try:
        return pd.read_feather(path, columns=COLUMNS).shape[0]
    except Exception:
        return 0


def get_base_paths():
    parent = None
    child = None

    for p in glob.glob(BASE_GLOB):
        if os.path.basename(p).startswith("RPSGCIHBase"):
            parent = os.path.join(p, "Buckets")
        else:
            child = os.path.join(p, "Buckets")

    return parent, child


def get_file_names(base_path):
    return {os.path.basename(f) for f in glob.glob(f"{base_path}/*/100/*")}


def build_paths(base_path, file_name):
    paths = []
    for bucket in BUCKETS:
        paths.extend(glob.glob(os.path.join(base_path, bucket, "*", file_name)))
    return paths


parent_base, child_base = get_base_paths()

info = {parent_base: get_file_names(parent_base),child_base: get_file_names(child_base)}

results = []

with Pool(POOL_SIZE) as pool:
    for base_path, files in info.items():
        print(f"\nProcessing: {base_path}")

        for file in files:
            print(f"  File: {file}")

            paths = build_paths(base_path, file)
            if not paths:
                continue

            row_counts = pool.map(read_feather_count, paths)
            results.append({
                "File_Name": file,
                "Row_Count": sum(row_counts)
            })

info_data = pd.DataFrame(results)
print("\nFinal Output:")