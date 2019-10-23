from aoi import Aoi, Unit

def makeAoiList(aoi:Aoi):
    aoiList = [[ 0 for _ in range(aoi.x)] for _ in range(aoi.y)]
    node = aoi.xlist
    while node:
        aoiList[node.x][node.y] = node.id
        node = node.nextX
    return aoiList
    

def testEnter(aoi):
    x = 5
    y = 5
    id = 1
    u1 = Unit(x,y,id) # 创建一个x为5,y为5 id是1的单元
    aoi.enter(u1) # 将单元插入到aoi里面 
    AoiList = makeAoiList(aoi)
    assert AoiList[x][y] == id
    for row in AoiList:
        print(row) # 打印
    print('--------------------------------------')

def testMove(aoi):
    u2 = Unit(1,1,2)
    aoi.enter(u2)
    AoiList = makeAoiList(aoi)
    assert AoiList[1][1] == 2
    aoi.move(u2,2,2)
    AoiList = makeAoiList(aoi)
    assert AoiList[2][2] == 2
    for row in AoiList:
        print(row) # 打印
    print('--------------------------------------')

def testLeave(aoi):
    u3 = Unit(10,10,3)
    aoi.enter(u3)
    AoiList = makeAoiList(aoi)
    assert AoiList[10][10] == 3
    aoi.leave(u3)
    AoiList = makeAoiList(aoi)
    assert AoiList[10][10] == 0

def testFineArea(aoi):
    u4 = Unit(15,15,4)
    u5 = Unit(16,16,5)
    u6 = Unit(14,14,6)
    # aoi中任何公开方法都会返回radius参数指定范围内节点数量以及具体的unit
    aoi.enter(u4)
    num,units = aoi.enter(u5,1)
    assert units[0] == u4
    aoi.enter(u6)
    num,units = aoi.inRange(u4,2) # 也可以使用inRange方法直接返回参数节点附近的节点
    assert num == 2
    uTemp = Unit(15,15,9999)
    aoi.enter(uTemp)
    num,units = aoi.inRange(uTemp,2) # 可以通过创建临时节点的方式获取范围内的节点
    aoi.leave(uTemp)
    assert num == 3


if __name__ == "__main__":
    '''
    本aoi算法支持unit重叠坐标，但难以通过print体现
    '''
    aoi = Aoi(20,20) # 创建一个大小是20*20的aoi
    
    testEnter(aoi)
    testMove(aoi)
    testLeave(aoi)
    testFineArea(aoi)