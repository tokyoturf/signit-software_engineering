import h5py

with h5py.File('models/model.h5', 'r') as f:
    print(list(f.keys()))