import traceback

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
    with open(fich,"r") as file:
        for ligne in file:
            ligne_liste=ligne.split()
            if len(ligne_liste)==1:
                lignes.append(ligne_liste)
    lignes=[int(lignes[i][0]) for i in range(2,122)]
    print(lignes)
    return lignes,120,150

def test_extract(registre_test,fich):
    registre_test["test_extract"]={}
    
    registre_test["test_extract"]["open"]=True
    registre_test["test_extract"]["parameters"]=True
    try:
        weights,size,capacity=extract(fich)
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
        else:
            print("other error")
            return False
    

    registre_test["test_extract"]["length"]=True
    print("len = ",len(weights))
    try:
        assert len(weights)==size
    except:
        registre_test["test_extract"]["length"]=False
        return False
    return True
    
registre_test={}
#assert test_extract(registre_test,r"BP\data\binpack1.txt")
data_extracted,solution,capacity=extract(r"BP\data\binpack1.txt")
print(data_extracted)