def traversal_logic(directory_index):
    files = []
    
    for key in directory_index:
        print(key)
    return files


if __name__ == "__main__":
    traversal_logic(
        {
            "size":["400mb","800mb","1200mb","1600mb","2000mb","unlimited"],
            "media":["StorageMaterial.NVMeSSD"],
            "cpu":["1CPU","2CPU","3CPU","4CPU","8CPU","12CPU"],
            "batch_size":["16MB","32MB","64MB","128MB"]
        }
    )