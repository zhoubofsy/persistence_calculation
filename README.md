# 持久性
持久性是数据丢失的概率，可以用于度量一个存储系统的可靠性，俗称 “多少个9”。数据的放置(DataPlacement)决定了数据持久性，而Ceph的CRUSH MAP又决定了数据的放置，因此CRUSH MAP的设置决定了数据持久性。

# 数学模型
## 公式
`P = Pr x M / C（R，N）`

## 解释
### P
P为丢失数据的概率，持久性，可用1-P来计算。

### Pr
`Pr = P1（any） x P2（any） x P3（any）`

Pr为一年内R（ceph副本数）个OSD发生故障的概率。

* P1（any）为一年内第一个OSD发生故障的概率
硬盘在一定时间内的失败概率符合Possion（伯松）分布 `Pn（入,t）`(`入`为lamda)，由于我们不太容易直接计算任意一个OSD顺坏的概率，但可以计算出没有OSD出现故障的概率，再用1减去无OSD节点故障的概率，就得到了`P1（any）`
`入=FIT x N` ，`FIT=AFR/（24×365）`，AFR为硬盘年故障概率;
`t`为一年的小时数，24x365

* P2（any）为一个OSD恢复周期内第二个OSD发生故障的概率
`入`中的N为N-1
`t` 为一个OSD恢复周期，`OSD恢复周期 = 恢复数据量 / 恢复速度`；`恢复数据量 = 硬盘容量 x 使用率`；`恢复速度 = 每个OSD写速度 x 参与恢复的OSD数量`

* P3（any）为一个OSD恢复周期内第三个OSD发生故障的概率
`入`中的N为N-2
`t` 为一个OSD恢复周期，算法同上

### M
Copy Set个数，copy set上至少有一个PG的所有副本。
丢失数据必须是主副本数据同时丢失，数据不可恢复才算。而一个copy set，包含一个PG的所有主副本数据，所以一个copy set损坏（或丢失）导致至少一个PG的主副本数据丢失，数据不可恢复。

### C（R，N）
N为OSD数量（一个OSD对应一个硬盘），R为副本数，C（R，N）为N个OSD中任意挑选R个OSD的组合数。

## 优化
综上所述，我们能调节的参数包括：

* OSD恢复周期（recovery time）
    增加`参与恢复的OSD数量`可以缩短`OSD恢复周期`，从而降低丢失数据的概率
* copy set个数
    减少copy set个数，可以降低丢失数据的概率

以上优化需要修改Crush map

# 使用prmc计算持久性
## 获取prmc
从github上下载prmc代码
```shell
git clone https://github.com/zhoubofsy/persistence_calculation.git
```

## 配置输入参数
修改`config.py`文件中的`prmc`字典
```shell
# 算法名称
name = 'prmc'

prmc = {
# 副本数
'replica_num' : 3, 

# 集群OSD总数数量
'osd_num' : 14,

# AFR(硬盘年故障率)
'disk_afr' : 0.017,

# 磁盘平均容量（MB）
'disk_capacity' : 1000.0,

# 磁盘平均写速度（MB/s）
'disk_writerate' : 50.0,

# 磁盘使用率
'disk_usage' : 0.75,

# 一个Host中OSD的数量
'num_osd_in_host' : 4, 

# 一个副本域的host数量
'num_host_in_replic_domain' : 1,

# rack数量
'num_rack_in_root' : 4, 

# 副本域数量
'num_replic_domain_in_root' : 1
}
```
程序会根据`name`的设置，选择相关的算法，不同的算法会采用不同的配置参数，目前只支持`prmc`算法

## 执行计算
执行`main.py`进行计算持久性
```shell
./main.py
```

# 参考&鸣谢
* [打造高性能高可靠块存储系统](https://www.ustack.com/blog/build-block-storage-service/)
* [CEPH可靠性的计算方法分析](http://blog.csdn.net/xiaoquqi/article/details/43055031#0-tsina-1-70142-397232819ff9a47a7b7e80a40613cfe1)
