#calculate the size of a folder by
#summing the size of each of its files/subfolders

#acts recursively

#converts a (probably integer) number of bytes into
# a more reasonable unit, depending on size
# and returns a human-readable string 
# supports KB, MB, GB, and TB
def getAsReasonableUnit(byteSize):

    #try each unit in descending order of size
    #when we find a unit where the value is greater than one,
    #pick that unit and return
    
    factors = (
        ("TB", 1e+12),
        ("GB", 1e+9),
        ("MB", 1e+6),
        ("KB", 1e+3)
        )

    for factorName, factor in factors:

        scaledSize = byteSize / factor

        if scaledSize >= 1:
            return "{:.2f} {}".format(scaledSize, factorName)
        
    #if size is too small even for KB, return in bytes
    return "{} bytes".format(byteSize)


#return the size of a folder in bytes
#acts "recursively" using walk 
def calcFolderSize(folderPath):
    import os

    size = 0

    for path, dirs, files in os.walk(folderPath):

        for file in files:
            filePath = os.path.join(path, file)
            size += os.path.getsize(filePath)

    return size


    
#get the results for each folder in one 'master' (top level) folder
#and list them individually

def masterFolderSize(folderPath):
    import os

    for path, dirs, files in os.walk(folderPath):
        for file in files:
            print("Scanning {}".format(file), end = " ")
            ssize = os.path.getsize(os.path.join(path, file))
            print(getAsReasonableUnit(size))

        for directory in dirs:
            print("Scanning {}:".format(directory), end = " ")
            size = calcFolderSize(os.path.join(path, directory))
            print(getAsReasonableUnit(size))
        
        break

#get the results for each folder in one 'master' (top level) folder
#and list them individually ordered by size (descending)
#returns total folder size in bytes (scanned size)
def orderedFolderSize(folderPath):
    import os

    folderSizes = []

    try:
        #weird way to do this but I don't know a better one
        for path, dirs, files in os.walk(folderPath):
    
            for file in files:
                #calc size from files
                print("Scanning {}:".format(file), end = " ")
                size = os.path.getsize(os.path.join(path, file))
                print(getAsReasonableUnit(size))
                folderSizes.append((file, size))
        
                
            for directory in dirs:
                #calc size from folders
                print("Scanning {}:".format(directory), end = " ")
                size = calcFolderSize(os.path.join(path, directory))
                print(getAsReasonableUnit(size))
                folderSizes.append((directory, size))


            #important break! 
            break
        
    except KeyboardInterrupt:
        print('\nAborted\n')

    print("Ordering Items...")
    
    folderSizes.sort(key = lambda x: x[1], reverse = True)
    totalFolderSize = sum(map(lambda x: x[1], folderSizes))

    print("Showing Ordered Results:\n#######")

    for folderName, folderSize in folderSizes:
        reasonableSize = getAsReasonableUnit(folderSize)
        print("{}: {}".format(folderName, reasonableSize))

    print("######")
    return totalFolderSize

if __name__ == '__main__':
    import sys

    #initialize targetDir
    targetDir = None

    blurb ="""Size finder

Finds the size of folders by summing the size
of each child object

Acts recursively (Run on C:/ at your own risk!!!!)
"""
    
    
    if len(sys.argv) <= 1:
        blurb +="\nPlease specify a folder (example: sizefinder.py \"c:/Progam Files\""

    else:
        targetDir = sys.argv[1]

    print(blurb)

    if targetDir != None:
        from datetime import datetime
        
        print("Scanning {}".format(targetDir))

        startTime = datetime.now()
        
        scannedSize = orderedFolderSize(targetDir)
            
        endTime = datetime.now()

        print("Started at {}".format(startTime))

        print("Scanned {} worth of files".format(getAsReasonableUnit(scannedSize)))

        print("Ended at {}".format(endTime))

        totalTime = endTime - startTime

        print("{} Elapsed".format(totalTime))

        bytesPerSecond = scannedSize/totalTime.total_seconds()

        print("Avg speed of {} per second".format(getAsReasonableUnit(bytesPerSecond)))




            
            
