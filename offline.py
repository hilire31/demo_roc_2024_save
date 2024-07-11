import numpy as np




def create_data_model():
    """Create the data for the example."""
    data = {}
    weights = [8,2,3,11,4,9,2,3,7,4,8,11]
    data["weights"] = weights
    data["items"] = list(range(len(weights)))
    data["bins"] = data["items"]
    data["bin_capacity"] = 12
    return data



def next_fit_offline(data):
    
    bin=[]
    bins=[]
    full_capacity=data["bin_capacity"]
    bin_capacity=full_capacity

    for i in data["items"]:
        if bin_capacity - data["weights"][i]>=0:
            bin.append(i)
            bin_capacity-=data["weights"][i]
        else:
            bins.append(bin.copy())
            bin=[i]
            bin_capacity=full_capacity-data["weights"][i]
            print("capacity = ",bin_capacity, "bin : ",bin)
    bins.append(bin.copy())


    somme=sum(data["weights"])
    nb_bins=len(bins)
    ratio = somme/nb_bins
        

    return nb_bins,bins,ratio

def next_k_fit_offline(data,k):
    K=k
    
    bins=[[] for i in data["items"]]
    full_capacity=data["bin_capacity"]
    bin_capacity=[full_capacity for i in data["items"]]
    deb=0
    for i in data["items"]:
        STO=False
        for j in range(deb,deb+K):
            if bin_capacity[j] - data["weights"][i]>=0 and not STO:
                bins[j].append(i)
                bin_capacity[j]-=data["weights"][i]
                STO=True
                break
        if not STO:
            if VERBOSE>1:print("full item ",i,"de poids ",data["weights"][i])
            bins[deb+K]=[i]
            bin_capacity[deb+K]=full_capacity-data["weights"][i]
            deb+=1
    somme=sum(data["weights"])
    nb_bins=0
    for i in bins:
        if i !=[]:
            nb_bins+=1
    ratio = somme/nb_bins
    if VERBOSE>1:print("FIN ALGO : ",__name__)
    if TEST:
        if VERBOSE>1:print("DEBUT TEST")
        for i,bin in enumerate(bins):
            s=np.sum([data["weights"][elem] for elem in bin])
            assert 0 <= s <= data["bin_capacity"]
            assert data["bin_capacity"]-s==bin_capacity[i]
        if VERBOSE>1:print("TEST OK")
            
    
    
        

    return nb_bins,bins,ratio

global VERBOSE,TEST
VERBOSE=2
TEST=True
data=create_data_model()
print(data)
nb_bins,bins,ratio=next_k_fit_offline(data,2)



def trie(data,decreasing=True):
    return data