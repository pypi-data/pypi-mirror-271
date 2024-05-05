import scipy.stats
def do_ws(arr):
    nrow = arr.shape[0]
    dists = np.zeros(nrow-1)
    for i in range(nrow-1):
        dists[i] = scipy.stats.wasserstein_distance(arr[i],arr[i+1])
    return dists
        
