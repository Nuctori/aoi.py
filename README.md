# 简易十字链表AOI(Area Of Interest)算法实现

一个简易的aoi算法，灵感来源于 https://github.com/CandyMi/aoi-c 项目

###  用法(usage)
* 引入 

```
from aoi import Aoi, Unit
```

* 构造aoi对象
```
aoi = Aoi(x,y) 
# x y 为该aoi逻辑最大大小
``` 

* 构造unit对象
```
unit = Unit(x,y,id)
# Unit构造函数返回的是一个函数对象，需要获取unit信息只需要如下操作
x,y,id = unit()
```

* 插入
```
aoi.enter(unit)
```

* 离开

```
aoi.leave(unit)
```

* 移动

```
aoi.move(unit,x,y)
```

## 算法复杂度
* Aoi.enter O(n)
* Aoi.move O(lgn)
* Aoi.leave O(1)

适用性
十字链表主要用于优化查找的场景, 所以牺牲了插入的性能来提升查询的性能(因为敢兴趣点区域总在附近的链表上).

move阶段我们删除的时候可以直接断开链表链接, 然后根据之前的链表判断是移动点位后再次进行插入. 这会比直接aoi_enter效率要高, 因为移动一般是小范围的.

这里再介绍一种场景. 对于某个单位短时间内(1ms)对于大范围的move, 例如: Unit(500, 500) -> Unit(1, 1).

这种不属于move的范畴, 它更类似于游戏场景中的瞬移(Teleport). 使用move也许无法得到正确答案. 因为我们Aoi算法中无法判断这种情况.

并且这种情况使用move是完全没有意义的, 这时候计算出的时间复杂度大部分情况下可能还不如aoi_enter + aoi_leave, 且中间路程上的单位计算也完全没意义.

十字链表算法适用于大量(临时)Scense场景, 它将空间复杂度降低为O(1). 比传统网格类算法有空间上的优势(因为是基于Unit).

## 协议
MIT