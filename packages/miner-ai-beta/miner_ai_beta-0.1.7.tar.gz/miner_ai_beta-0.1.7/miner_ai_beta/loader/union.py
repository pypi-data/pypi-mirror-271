from tqdm import tqdm

def MergeIndexes(dbs: list):
    """
    ## Merge all indexes together (Locally)
    This function merge all indexes inside a variable for next use. \n
    - dbs: List of indexes to merge\n
    """
    final_db = dbs[0]
    end = len(dbs)
    for db in tqdm(dbs[1:end], "Merging dbs"):
        final_db.merge_from(db)
    return final_db
