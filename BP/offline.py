import numpy as np
import random as rd
import traceback
from BP import BP_exact
def extract(fich):
    if type(fich)!=str:
        raise TypeError
    if fich[-4:]!=".txt":
        raise ValueError
    try:
        open(fich,"r")
    except Exception as e:
        print("error open : ",e)
        raise FileNotFoundError
    try:
        open(fich,"r")
    except Exception as e:
        print("error open : ",e)
        raise FileNotFoundError
    lignes=[]
    sol=None
    size=None
    with open(fich,"r") as file:
        for ligne in file:
            ligne_liste=ligne.split()
            if ligne_liste!=[]:
                lignes.append(ligne_liste)
            if len(lignes)==1 and size==None:
                size=int(lignes[-1][0])
            
            if 'solution' in ligne_liste:
                sol=ligne_liste[-1][1:-2]
                break
    sol = int(sol)
    weights=[int(lignes[i][0]) for i in range(2,size+2)]
    capacity=int(lignes[1][0])
    return weights,sol,size,capacity

def test_extract(registre_test,fich):
    if VERBOSE>1:print("DEBUT TEST extract")
    registre_test["test_extract"]={}
    
    registre_test["test_extract"]["open"]=True
    registre_test["test_extract"]["parameters"]=True
    try:
        weights,sol,size,capacity=extract(fich)
    except Exception as e:
        if e == TypeError:
            print("error extract wrong parameter")
            registre_test["test_extract"]["parameters"]=e
            return False
        if e == ValueError:
            print("wrong file extension only .txt")
            registre_test["test_extract"]["parameters"]=e
            return False
        if e==FileNotFoundError:
            registre_test["test_extract"]["open"]=False
            print("error open")
            return False
    

    registre_test["test_extract"]["length"]=True
    try:
        assert len(weights)==size
    except:
        registre_test["test_extract"]["length"]=False
        return False


    registre_test["test_extract"]["value"]=True
    try:
        for i in weights:
            if type(i)!=int:
                raise ValueError
    except:
        registre_test["test_extract"]["value"]=False
        return False
    if VERBOSE>1:print("FIN TEST extract : TEST OK")
    return True
import random
import numpy as np

def generate_weights(size, max_capacity, vmin,vmax,mean=None, std_dev=None, distribution='uniform'):
    if distribution == 'uniform':
        # Génération de poids avec une distribution uniforme
        weights = [random.randint(0, max_capacity) for _ in range(size)]
    elif distribution == 'normal':
        if vmin is None:
            vmin = 0
        if vmax is None:
            vmax = max_capacity
        if mean is None:
            mean = max_capacity / 2
        if std_dev is None:
            std_dev = max_capacity / 10  # Ajustez selon le niveau de dispersion souhaité
        weights = np.random.normal(mean, std_dev, size).tolist()
        # S'assurer que les valeurs sont dans l'intervalle [0, max_capacity]
        weights = [min(max(vmin, int(w)), vmax) for w in weights]
    else:
        raise ValueError("Distribution not supported. Use 'uniform' or 'normal'.")
    
    return weights

def stat_an(data):

    stat={"size":len(data["weights"]),"max_capacity":data["bin_capacity"],"mean":None,"std_dev":None,"vmin":None,"vmax":None}
    stat["vmax"]=max(data["weights"])
    stat["vmin"]=min(data["weights"])
    stat["std_dev"]=np.std(data["weights"])
    stat["mean"]=np.mean(data["weights"])
    return stat
    

def create_data_model(size=7,capacity=12,weights = [8,2,3,5,12,7,9]):
    """Create the data for the example."""
    if type(weights)!=list:
        raise TypeError 
    if type(size)!=int:
        raise TypeError
    if size<=0 :
        raise ValueError
    if type(capacity)!=int:
        raise TypeError
    if capacity<1:
        raise ValueError
    if size!=len(weights):
        weights=[rd.randint(0,capacity) for i in range(size)]

    if len(weights)<1:
        raise ValueError
    for i in weights:
        if type(i)!=int:
            raise TypeError
        if i<0 or i>capacity:
            raise ValueError
    
    data = {}
    
    data["weights"] = weights
    data["items"] = list(range(len(weights)))
    data["bins"] = data["items"]
    data["bin_capacity"] = capacity
    return data


def test_create_data_model(registre_test,size,capacity=None,weights=None):
    SIZE=size
    if capacity==None:
        capacity=rd.randint(10,20)

    registre_test["test_create_data_model"]={}
    if VERBOSE>=1:print("DEBUT TEST test_create_data_model")
    registre_test["test_create_data_model"]["init"]=True
    try:
        if weights==None:
            data=create_data_model(SIZE,capacity)
        else:
            data=create_data_model(SIZE,capacity,weights)
    except Exception as e:
        if VERBOSE>=0:print("error test_create_data_model init")
        registre_test["test_create_data_model"]["init"]=e
        return False
    

    registre_test["test_create_data_model"]["size_not_null"]=True
    try:
        assert data!=None
        
    except:
        if VERBOSE>=0:print("error test_create_data_model : size_not_null")
        registre_test["test_create_data_model"]["size_not_null"]=False
        return False
    assert type(data)


    registre_test["test_create_data_model"]["type_data_return"]=True
    try:
        assert type(data)==dict
    except:
        if VERBOSE>=0:print("error test_create_data_model : type_data_return")
        registre_test["test_create_data_model"]["type_data_return"]=False
        return False


    test_create_data_model_fin=True
    for i in registre_test["test_create_data_model"]:
        if registre_test["test_create_data_model"][i]!=True:
            test_create_data_model_fin=False
    if test_create_data_model_fin:
        if VERBOSE>=1:print("FIN TEST test_create_data_model : TEST OK")
        return True
    else:
        if VERBOSE>=0:print("error test_create_data_model")
        return False
    
    

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
    bins.append(bin.copy())


    somme=sum(data["weights"])
    nb_bins=len(bins)
    ratio = somme/nb_bins
        

    return nb_bins,bins,ratio

def next_k_fit_offline(data,k):
    K=k
    if VERBOSE>1:print("DEBUT ALGO : next_k_fit_offline")
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
            bins[deb+K]=[i]
            bin_capacity[deb+K]=full_capacity-data["weights"][i]
            deb+=1
    somme=sum(data["weights"])
    cnt=0
    for i in bin_capacity:
        cnt+=50-i
    nb_bins=0
    for i in bins:
        if i !=[]:
            nb_bins+=1
    ratio = somme/nb_bins
    if VERBOSE>1:print("FIN ALGO : next_k_fit_offline")
        

    return nb_bins,bins,ratio,bin_capacity

    

def test_next_k_fit_offline(registre_test,k=2,data=[]):
    if data==[]:
        data=create_data_model(rd.randint(10,20))
    K=k
    

    if VERBOSE>=1:print("DEBUT TEST test_next_k_fit_offline")
    registre_test["test_next_k_fit_offline"]={}

    registre_test["test_next_k_fit_offline"]["init"]=True
    try:
        nb_bins,bins,ratio,bin_capacity=next_k_fit_offline(data,K)
    except Exception as e:
        if VERBOSE>=0:print("error test_next_k_fit_offline init")
        registre_test["test_next_k_fit_offline"]["init"]=e
        return False
    

    registre_test["test_next_k_fit_offline"]["sum(weight)<capacity"]=True
    registre_test["test_next_k_fit_offline"]["correct remaining capacity"]=True
    S=0
    for i,bin in enumerate(bins):
        s=np.sum([data["weights"][elem] for elem in bin])
        S+=s
        try:
            assert 0 <= s <= data["bin_capacity"]
        except:
            registre_test["test_next_k_fit_offline"]["sum(weight)<capacity"]=False
        try:
            assert data["bin_capacity"]-s==bin_capacity[i]
        except:
            registre_test["test_next_k_fit_offline"]["correct remaining capacity"]=False

    registre_test["test_next_k_fit_offline"]["all packed"]=True
    try:
        assert S==sum(data["weights"])
    except:
        registre_test["test_next_k_fit_offline"]["all packed"]=False


    test_next_k_fit_offline_fin=True
    for i in registre_test["test_next_k_fit_offline"]:
        if registre_test["test_next_k_fit_offline"][i]!=True:
            test_next_k_fit_offline_fin=False
    if test_next_k_fit_offline_fin:
        if VERBOSE>=1:print("FIN TEST test_next_k_fit_offline : TEST OK")
        return True
    else:
        if VERBOSE>=0:print("error test_next_k_fit_offline")
        return False


def fonction_tri(data,decreasing=True):
    weights=data["weights"]
    indices_tries = sorted(range(len(weights)), key=lambda k: weights[k],reverse=decreasing)
    liste_triee = sorted(weights,reverse=decreasing)
    data["items"]=indices_tries
    data["weights"]=liste_triee
    return data

def test_fonction_tri(registre_test,data=[]):
        if data==[]:
            data=create_data_model(rd.randint(5,15))

        if VERBOSE>=1:print("DEBUT TEST fonction_tri_decreasing")
        registre_test["fonction_tri_decreasing"]={}
        #if VERBOSE>1:print(data)


        registre_test["fonction_tri_decreasing"]["init"]=True
        try:
            data_sorted_decreasing=fonction_tri(data.copy(),decreasing=True)
        except Exception as e:
            if VERBOSE>=0:print("error fonction_tri_decreasing init")
            registre_test["fonction_tri_decreasing"]["init"]=e
            return False
        registre_test["fonction_tri_decreasing"]["init"]=True
        #if VERBOSE>1:print(data_sorted_decreasing)


        registre_test["fonction_tri_decreasing"]["ordre"]=True
        try:
            for i in range(len(data_sorted_decreasing["weights"])-1):
                assert data_sorted_decreasing["weights"][i]>=data_sorted_decreasing["weights"][i+1]
        except:
            if VERBOSE>=0:print("error fonction_tri_decreasing")
            registre_test["fonction_tri_decreasing"]["ordre"]=False


        registre_test["fonction_tri_decreasing"]["indices"]=True
        try:
            for indice_unsorted,indice_sorted in enumerate(data_sorted_decreasing["items"]):
                assert data_sorted_decreasing["weights"][indice_unsorted]==data["weights"][indice_sorted]
        except:
            registre_test["fonction_tri_decreasing"]["indices"]=False
            

        
        test_fonction_tri_decreasing=True
        for i in registre_test["fonction_tri_decreasing"]:
            if registre_test["fonction_tri_decreasing"][i]!=True:
                test_fonction_tri_decreasing=False
        if test_fonction_tri_decreasing:
            if VERBOSE>=1:print("FIN TEST fonction_tri_decreasing : TEST OK")
            return True
        else:
            if VERBOSE>=0:print("error fonction_tri_decreasing")
            return False

global VERBOSE,TEST
VERBOSE=1
TEST=True

def main():
    
    

    if TEST:
        registre_test={}
        k=3
        size=30
        max_capacity=12
        #weights=[rd.randint(0,max_capacity) for i in range(size)]
        weights=generate_weights(size, max_capacity,0+1,max_capacity-1, mean=None, std_dev=3, distribution='uniform')
        print("weights : ",weights)
        try:
            registre_test["test1"]={}
            assert test_create_data_model(registre_test["test1"],max_capacity)
            data=create_data_model(size,max_capacity,[7, 1, 4, 4, 11, 5, 12, 6, 10, 4, 7, 10, 7, 4, 9, 8, 0, 9, 4, 11, 9, 3, 8, 12, 10, 5, 1, 5, 5, 4])
            assert test_fonction_tri(registre_test["test1"],data)
            data_sorted=fonction_tri(data.copy())
            assert test_next_k_fit_offline(registre_test["test1"],k,data_sorted)
            
            #print("exact_nb_bins = ",exact_nb_bins, "and approx1 = ",nb_bins_next_fit,"and approx2 = ",nb_bins_next_k_fit)
            nb_bins_next_k_fit,bins,ratio,bin_capacity=next_k_fit_offline(data_sorted,k)

            print(bins)
            print("approx2 = ",nb_bins_next_k_fit)
            print("weights : ",data["weights"])
            '''
            exact_nb_bins,tps,bin_items,EMPTY=BP_exact(data_sorted)
            print("sans upper bound : exact_nb_bins = ",exact_nb_bins,"en ",tps,"milliseconds")
            print("bin_items",bin_items)
            print(EMPTY)
            

            exact_nb_bins,tps,bin_items,EMPTY=BP_exact(data_sorted,nb_bins_next_k_fit)
            print("avec upper bound : exact_nb_bins = ",exact_nb_bins,"en ",tps,"milliseconds")
            print("bin_items",bin_items)
            print(EMPTY)'''

            
            registre_test["test2"]={}
            assert test_extract(registre_test["test2"],r"BP\data\BPP_50_50_0.1_0.7_0_Results_BLV.txt")
            weights_extracted,solution,size,capacity=extract(r"BP\data\BPP_50_50_0.1_0.7_0_Results_BLV.txt")
            assert test_create_data_model(registre_test["test2"],size,capacity,weights_extracted)
            data_extracted=create_data_model(size,capacity,weights_extracted)
            
            assert test_next_k_fit_offline(registre_test["test2"],k,data_extracted)
            nb_bins,bins,ratio,bin_capacity=next_k_fit_offline(data_extracted,k)
            #exact_nb_bins,tps=BP_exact(data_extracted,nb_bins)
            #print("exact_nb_bins : ",exact_nb_bins,"en ",tps," millisecondes")

            
            
            
        except Exception as e:
            print("\n**********\nfin registre : ",registre_test)
            print("erreur fin : ",e)
            print(traceback.format_exc())
            return
        
        if VERBOSE>0:print("\n**********\nfin registre : ",registre_test)
        print("\nTESTS FULL OK")
    else:
        data=create_data_model()
    #nb_bins,bins,ratio=next_k_fit_offline(data,2)
if __name__=="__main__":
    main()
    
        
        
        
        
        
    