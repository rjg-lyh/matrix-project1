import os
from aoi_info.lib.changdian import ChangdianAoiInfo
from collections import defaultdict

class Solution:
    def searchRoot(self, path: str) -> list:
        results = defaultdict(list)
        def search(path: str) -> str:
            nonlocal results
            dirs = os.listdir(path)
            new0 = os.path.join(path, dirs[0])
            if os.path.isfile(new0):                   #判断是否叶子节点
                return dirs[0]
            records_dog = []
            for dir in dirs:
                new = os.path.join(path, dir)
                dog_name = search(new)
                records_dog.append(dog_name)
            if any(name == 'mix' for name in records_dog):            #这一层必不能整体聚拢
                for i in range(len(dirs)):
                    if records_dog[i] == 'mix':       
                        continue
                    results[records_dog[i]].append(os.path.join(path, dirs[i]))
                return 'mix'
            else:                           #判断这一层能否整体聚拢
                isSame = True
                for i in range(len(records_dog)):
                    if i != 0 and records_dog[i] != records_dog[i - 1]:
                        isSame = False
                        break
                if isSame:         #这一层节点全都一样，可以聚合
                    return records_dog[0]
                else:               #这一层不能聚合，开始存入results
                    for i in range(len(dirs)):
                        results[records_dog[i]].append(os.path.join(path, dirs[i]))
                    return 'mix'    
        dog_name = search(path)
        if dog_name != 'mix':      # 根文件夹下都是一个类型
            results[dog_name] = [path]
        return results


if __name__ == "__main__":
    path = '/home/yuhui/Project/project1/tree'
    solution = Solution()
    results = solution.searchRoot(path)
    print(results)
    for dog_name in results.keys():
        print(dog_name)
        for location in results[dog_name]:
            print(location)



