import os 
path = '/workspace/dataSet/raw/adc/changdian/alpha/labeled/2PxM'

dirs = os.listdir(path)
for dir in dirs:
    print(dir)
    new = os.path.join(path, dir)
    print(os.path.isfile(new))
        