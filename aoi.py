class PrevX:
    'symbol'
    pass

class NextX:
    'symbol'
    pass

class PrevY:
    'symbol'
    pass

class NextY:
    'symbol'
    pass

class DoubleLink():
    
    def __init__(self, x:int, y:int, id:int):
        self.id = id
        self.x = x
        self.y = y
        self.prevX = None
        self.nextX = None
        self.prevY = None
        self.nextY = None
    
    def Unit(self):
        return (self.id, self.x, self.y)


def Unit(x,y,int):
    link = DoubleLink(x,y,int)
    return link.Unit

class Aoi():


    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xlist = None
        self.ylist = None

    def enter(self, unit, radius=0):
        node = self._makeNode(unit)
        self._checkUnitRange(node)  
        self._NodeToX(node)
        self._NodeToY(node)
        return self._nodeRange(node,radius)


    def leave(self,unit, radius=0):
        node = self._makeNode(unit)
        self._checkUnitRange(node)  
        self._removeFromX(node)
        self._removeFromY(node)
        return self._nodeRange(node,radius)

    def move(self,unit,toX,toY,radius=0):
        node = self._makeNode(unit)
        self._checkUnitRange(node)    
        node.x = toX
        node.y = toY
        self._NodeToX(node)
        self._NodeToY(node)
        return self._nodeRange(node,radius)

    def inRange(self,unit,radius):
        node = self._makeNode(unit)
        return self._nodeRange(node,radius)

    def _checkUnitRange(self,unit):
        node = self._makeNode(unit)
        if node.x < 0 or node.x > self.x:
            raise ValueError('node is out of range')
        if node.y < 0 or node.y > self.y:
            raise ValueError('node is out of range')


    def _nodeRange(self,node,radius):
        quantity = 0
        prev = node.prevX
        next = node.nextX
        maxY = node.y + radius
        minY = node.y - radius if node.y - radius > 0 else 0
        maxX = node.x + radius
        minX = node.x - radius if node.x - radius > 0 else 0
        units = []
        while prev:
            if prev.x < minX:
                break
            if prev.y >= minY and prev.y <= maxY:
                units.append(prev.Unit)
                quantity += 1
            prev = prev.prevX
        while next:
            if next.x > maxX:
                break
            if next.y >= minY and next.y <= maxY:
                units.append(next.Unit)
                quantity += 1
            
            next = next.nextX

        return quantity,units

    @staticmethod
    def _makeNode(unit):
        if isinstance(unit,tuple):
            node = DoubleLink(unit[0],unit[1],unit[2])
        elif not isinstance(unit,DoubleLink): 
            node = unit.__self__ # 由于isinstance无法简单断言函数类型,于是使用绕过方法
        else:
            node = unit
        return node


    @staticmethod
    def _travel(StartNode,direction,cond):
        # 朝一个方向遍历,直到满足条件则返回节点引用，找不到则抛出异常并返回链表队尾
        node = StartNode
        while True:
            if not node:
                raise EOFError('No matching node in Link', prevNode)

            if cond(node):
                return node
                
            prevNode = node
            if direction is NextX:
                node = node.nextX
            elif direction is PrevX:
                node = node.prevX
            elif direction is NextY:
                node = node.nextY
            elif direction is PrevY:
                node = node.prevY

    @staticmethod
    def _insertBeforeXnode(newNode,targetNode):
            newNode.nextX = targetNode
            newNode.prevX = targetNode.prevX
            if targetNode.prevX:
                targetNode.prevX = newNode
                newNode.prevX.nextX = newNode
            else:
                targetNode.prevX = newNode

    @staticmethod
    def _insertBeforeYnode(newNode,targetNode):
        # todo 空判断
            newNode.nextY = targetNode
            newNode.prevY = targetNode.prevY
            if targetNode.prevY:
                targetNode.prevY = newNode
                newNode.prevY.nextY = newNode
            else:
                targetNode.prevY = newNode


    def _NodeToX(self,node:DoubleLink):
        def initNode(node):
            node.prevX,node.nextX = None,None

        xNode = self.xlist
        if not xNode:
            self.xlist = node
            return

        prevNode,nextNode = node.prevX,node.nextX

        if node is self.xlist:
            if node.nextX:
                self.xlist = node.nextX
                self._removeFromX(node)
        else:
            self._removeFromX(node)

        if nextNode and node.x > nextNode.x:
            try:
                target = self._travel(nextNode,NextX,lambda xNode:xNode.x > node.x)
                if target is self.xlist:
                    self.xlist = node
                initNode(node)
                self._insertBeforeXnode(node,target)
            except EOFError as e:
                tail = e.args[1]
                if tail is node:
                    return
                initNode(node)
                node.prevX = tail
                tail.nextX = node
        elif prevNode and node.x < prevNode.x:
            try:
                target = self._travel(prevNode,PrevX,lambda xNode:xNode.x < node.x)
                initNode(node)
                self._insertBeforeXnode(node,target.nextX)
            except EOFError as e:
                head = e.args[1]
                initNode(node)
                self.xlist = node
                node.nextX = head
                head.prevX = node
        else:
            try:
                target = self._travel(self.xlist,NextX,lambda xNode:xNode.x > node.x)
                if target is self.xlist:
                    self.xlist = node
                initNode(node)
                self._insertBeforeXnode(node,target)
            except EOFError as e:
                tail = e.args[1]
                if tail is node:
                    return
                initNode(node)
                node.prevX = tail
                tail.nextX = node


    def _NodeToY(self,node:DoubleLink):
        def initNode(node):
            node.prevY,node.nextY = None,None

        yNode = self.ylist
        if not yNode:
            self.ylist = node
            return

        prevNode,nextNode = node.prevY,node.nextY

        if node is self.ylist:
            if node.nextY:
                self.ylist = node.nextY
                self._removeFromY(node)
        else:
            self._removeFromY(node)

        if nextNode and node.y > nextNode.y:
            try:
                target = self._travel(nextNode,NextY,lambda yNode:yNode.y > node.y)
                if target is self.ylist:
                    self.ylist = node
                initNode(node)
                self._insertBeforeYnode(node,target)
            except EOFError as e:
                tail = e.args[1]
                if tail is node:
                    return
                initNode(node)
                node.prevY = tail
                tail.nextY = node
        elif prevNode and node.y < prevNode.y:
            try:
                target = self._travel(prevNode,PrevY,lambda yNode:yNode.y < node.y)
                initNode(node)
                self._insertBeforeYnode(node,target.nextY)
            except EOFError as e:
                head = e.args[1]
                initNode(node)
                self.ylist = node
                node.nextY = head
                head.prevY = node
        else:
            try:
                target = self._travel(self.ylist,NextY,lambda yNode:yNode.y > node.y)
                if target is self.ylist:
                    self.ylist = node
                initNode(node)
                self._insertBeforeYnode(node,target)
            except EOFError as e:
                tail = e.args[1]
                if tail is node:
                    return
                initNode(node)
                node.prevY = tail
                tail.nextY = node
                

    def _removeFromX(self,node:DoubleLink):
        if not node.prevX and not node.nextX:
            return
        prevNode = node.prevX
        nextNode = node.nextX
        if prevNode:
            prevNode.nextX = nextNode
            if nextNode:
                nextNode.prevX = prevNode
        else:
            self.xlist = nextNode
            if nextNode:
                nextNode.prevX = None


    def _removeFromY(self,node:DoubleLink):
        if not node.prevY and not node.nextY:
            return
            
        prev = node.prevY
        next = node.nextY
        if prev:
            prev.nextY = next
            if next:
                next.prevY = prev
        else:
            self.ylist = next
            if next:
                next.prevY = None





#-----测试内容-----
'''
from random import randint


def isSorted(xlist,ylist):
    count = 0
    tmpX = -1
    tmpY = -1
    nodeX = xlist
    nodeY = ylist

    

    node = nodeX
    while node is not None:
        assert node.x >= tmpX
        tmpX = node.x
        node = node.nextX
        count += 1

    node = nodeY
    while node is not None:
        assert node.y >= tmpY
        tmpX = node.y
        node = node.nextY
        count += 1

    return count


for i in range(100000):
    a = Aoi(100,100)

    xlist = [42,21,76,99,88,43,61,31,14,2]
    
    for i in range(10):
        x = randint(1,100)
        u = Unit(x,randint(1,100),randint(1,100))
        # print(x)
        a.ener(u)
    ''
    for i in range(10):
        x = xlist[i]
        u = Unit(x,randint(1,100),randint(1,100))
        print(x)
        a.enter(u)
        ''
    assert isSorted(a.xlist,a.ylist) == 20
    # print('----------------')
    b = Aoi()
    for i in range(10):
        u = Unit(i,i,i)
        b.enter(u)


    xlist = [48,85,12,30,10,13,62,39,65,66]
    assert isSorted(b.xlist,b.ylist) == 20
    node = b.xlist
    
    for i in range(10):
        next = node.nextX
        x = randint(1,100)
        b.move(node,x,randint(1,100))
        # print(x)
        node = next
        x = set()
    ''
    for i in range(10):
        next = node.nextX
        x = xlist[i]
        if x == 48:
            x
        b.move(node,x,randint(1,100))
        print(x)
        node = next
        x = set()
    ''
    # print('----------------')
    y = set()
    nodeX = b.xlist
    nodeY = b.ylist
    for i in range(10):
        x.add(nodeX)
        y.add(nodeY)
        try:
            nodeX = nodeX.nextX
            nodeY = nodeY.nextY
        except:
            pass

    c = x - y
    if c:
        c

    assert isSorted(b.xlist,b.ylist) == 20

    node = a.xlist
    assert isSorted(a.xlist,a.ylist) == 20
    for i in range(10):
        next = node.nextX
        x = randint(1,100)
        a.move(node,x,randint(1,100))
        # print(x)
        node = next
 
    x = set()
    y = set()
    nodeX = a.xlist
    nodeY = a.ylist
    for i in range(10):
        x.add(nodeX)
        y.add(nodeY)
        try:
            nodeX = nodeX.nextX
            nodeY = nodeY.nextY
        except:
            pass

    c = x - y
    if c:
        c
    # print(isSorted(a.xlist,a.ylist))
    assert isSorted(a.xlist,a.ylist) == 20

    d = Aoi()
    t = None
    for i in range(10):

        u = Unit(i,i,i)
        d.enter(u)
        if i == 5:
            t = u

'''