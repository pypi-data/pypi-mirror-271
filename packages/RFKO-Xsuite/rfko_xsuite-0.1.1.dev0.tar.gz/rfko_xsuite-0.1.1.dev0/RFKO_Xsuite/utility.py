
import numpy as np
import os



def replace_extracted_val(monitor, delta=False, turn=None, turn_all_after=False, max_search=1e4, message=True):
    xcopy = monitor.x.copy()
    pxcopy = monitor.px.copy()
    if delta is True:
        deltacopy = monitor.delta.copy()


    if turn is not None:
        extracted_mask = xcopy[:, turn] == 0  # xcopy MUST EXISTS!
    else:  # inutile
        turn = len(xcopy[0, :]) - 1
        extracted_mask = xcopy[:, turn] == 0

    find_val = True
    search_counter = 1
    while find_val:
        if turn_all_after:  # This modifies all the values after some turn(param) to be as the last value before extraction
            xcopy[extracted_mask, turn:] = np.tile(xcopy[extracted_mask, turn - search_counter],
                                                   (len(monitor.x[0, :]) - turn, 1)).transpose()  #
            pxcopy[extracted_mask, turn:] = np.tile(pxcopy[extracted_mask, turn - search_counter],
                                                    (len(monitor.x[0, :]) - turn, 1)).transpose()
            if 'deltacopy' in locals():
                deltacopy[extracted_mask, turn:] = np.tile(deltacopy[extracted_mask, turn - search_counter],
                                                           (len(monitor.x[0, :]) - turn, 1)).transpose()
        else:
            xcopy[extracted_mask, turn] = xcopy[extracted_mask, turn - search_counter]
            pxcopy[extracted_mask, turn] = pxcopy[extracted_mask, turn - search_counter]
            if 'deltacopy' in locals():
                deltacopy[extracted_mask, turn] = deltacopy[extracted_mask, turn - search_counter]

        search_counter += 1
        extracted_mask = xcopy[:, turn] == 0
        if np.sum(extracted_mask) == 0:
            if message:
                print(f'process finished in {search_counter - 1} cycles')
            find_val = False

        if (turn - search_counter) < 0 & (turn != 0):
            if message:
                zero_first_turn = np.sum(monitor.x[:, 0] == 0)
                print(f'index exceeded ---> {zero_first_turn} particles are extracted the first turn ')
            find_val = False
            # break

        if search_counter > max_search:
            if message:
                print('maximum search iterations reached --> abort ')
            break
    if 'deltacopy' in locals():
        return xcopy, pxcopy, deltacopy
    else:
        return xcopy, pxcopy

def replace_array(arr, ind=False):
    arr_copy = arr.copy()
    index = np.where(arr == 0)[0][0]
    arr_copy[index:] = arr_copy[index - 1]
    if ind == False:
        return arr_copy
    else:
        return arr_copy, index


def replace_null(arr, ind=False):
    # WORKS WITH THE ENTIRE MATRIX
    # can return the index consistent with the particles.at_turn

    li = []
    index = np.zeros(shape=(arr.shape[0]))
    for i in range(arr.shape[0]):
        if np.sum(arr[i] == 0) != 0:
            if ind == True:
                replaced = replace_array(arr[i], ind=ind)
                index[i] = int(replaced[
                                   1])  # aggiunge alla particella numero i+1 l'indice in cui è stato trovato il primo zer, quidi in cui è stata estratta
                li.append(replaced[0])
            else:
                li.append(replace_array(arr[i]))
        else:
            li.append(arr[i])
    if ind == False:
        return np.array(li)
    else:
        return np.array(li), index



def _clean_dependencies(dependencies):
    clean_dep = []
    for x in dependencies:
        clean_dep.append(str(x)[6:].strip("']"))
    return clean_dep


def search_folder(directory, folder_name):
    """
    Search for a folder within a specified directory.

    Args:
        directory (str): The directory to search in.
        folder_name (str): The name of the folder to search for.

    Returns:
        str: The path to the found folder, or None if not found.
    """
    # Iterate through all items in the directory
    for root, dirs, files in os.walk(directory):
        # Check if the folder_name is in the list of directories
        if folder_name in dirs:
            # If found, return the full path to the folder
            return os.path.join(root, folder_name)
    # If not found, return None
    return None





def read_from_txt(filename,param,type_='float'):
    '''Search a parameters in the params file (Benchmark_dir)'''
    assert type_ in ['float','int','string']
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if param in line:
                val = line[line.index('=')+1:].strip()
                if type_=='float':
                    return float(val)
                elif type_=='string':
                    return val # already a string
                else:
                    return int(val)





