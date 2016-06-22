#!/usr/bin/evn python2.7
# coding:utf-8

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
