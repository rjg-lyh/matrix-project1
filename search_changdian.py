import os
from lib.changdian import ChangdianAoiInfo
from collections import defaultdict

class Solution:
    def searchRoot(self, path: str) -> list:
        results = defaultdict(list)
        def search(path: str) -> str:
            nonlocal results
            dirs = os.listdir(path)
            if len(dirs) == 0:                         #空文件夹
                return 'empty'
            new0 = os.path.join(path, dirs[0])
            if os.path.isfile(new0):                   #判断是否叶子节点
                try:
                    aoi_info = ChangdianAoiInfo.from_path(new0)
                except Exception as e:
                    return 'bad'
                return aoi_info.product
            for dir in dirs:                            #删去异常文件
                if os.path.isfile(os.path.join(path, dir)):
                    dirs.remove(dir)
            records_product = []
            for dir in dirs:
                new = os.path.join(path, dir)
                product_name = search(new)
                records_product.append(product_name)
            if any(name == 'mix' for name in records_product):            #这一层必不能整体聚拢
                for i in range(len(dirs)):
                    if records_product[i] == 'mix' or records_product[i] == 'empty':       
                        continue
                    results[records_product[i]].append(os.path.join(path, dirs[i]))
                return 'mix'
            else:                           #判断这一层能否整体聚拢
                isSame = True
                record = 'empty'
                for i in range(len(records_product)):
                    if record == 'empty' and records_product[i] != 'empty':
                        record = records_product[i]
                    elif record != 'empty' and records_product[i] != 'empty' and records_product[i] != record:
                        isSame = False
                        break
                if isSame:         #这一层节点全都一样，可以聚合
                    return record
                else:               #这一层不能聚合，开始存入results
                    for i in range(len(dirs)):
                        if records_product[i] != 'empty':
                            results[records_product[i]].append(os.path.join(path, dirs[i]))
                    return 'mix'    
        product_name = search(path)
        if product_name != 'mix':      # 根文件夹下都是一个类型
            results[product_name] = [path]
        return results

if __name__ == "__main__":
    path = '/workspace/dataSet/raw/adc/changdian/alpha/labeled'
    #path = '/workspace/dataSet/raw/adc/changdian/alpha/labeled/1PxM/MPS-MX3067R22-M1/'
    #path = '/workspace/dataSet/raw/adc/changdian/alpha/labeled/1PxM/MPS-ST3620R11/XP2143556A/2AI0218M2/'
    #path = '/home/yuhui/Project/project1/tree'
    solution = Solution()
    results = solution.searchRoot(path)
    print(results)
    for product_name in results.keys():
        print(product_name)
        for location in results[product_name]:
            print(location)



