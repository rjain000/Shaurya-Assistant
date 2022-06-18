import pickle

def add_pickle(variable_key, value):
    filename = "global_variables.pkl"
    global_vars= None
    with open(file=filename, mode='rb') as pkl_obj:
        pkl_obj.seek(0)
        global_vars = pickle.load(pkl_obj)
    print(global_vars)
    if variable_key not in global_vars:
        with open(file=filename, mode='wb') as pkl_obj:
            global_vars[variable_key] = value
            pickle.dump(global_vars, pkl_obj)
            print("value added...")
    else:
        print("value is already available")


def change_pickle(variable_key, value):
    filename = "global_variables.pkl"
    global_vars= None
    with open(file=filename, mode='rb') as pkl_obj:
        pkl_obj.seek(0)
        global_vars = pickle.load(pkl_obj)
    
    if variable_key in global_vars:
        with open(file=filename, mode='wb') as pkl_obj:
            global_vars[variable_key] = value
            pickle.dump(global_vars, pkl_obj)
            print("value changed...")

    else:
        print("value not available...")
        


def fetch_pickle(variable_key):
    filename = "global_variables.pkl"
    global_vars= None
    with open(file=filename, mode='rb') as pkl_obj:
        global_vars = pickle.load(pkl_obj)

    if variable_key in global_vars:
        return global_vars[variable_key]

