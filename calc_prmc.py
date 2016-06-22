#!/usr/bin/env python2.7
# coding:utf-8

from decimal import *
import math
import common
import calc_base


# base 
class calc_prmc(calc_base.calc_base):
    # 副本数
    rep = 3

    # OSD Number
    numOfOSD = 0

    # AFR
    afr = 0.0

    # FIT
    #fit = (1.0/1200000)*100
    fit = 0.0

    # Usage
    usage = 0.0

    # Write Rate (MB/s)
    writerate = 0.0

    # Capacity (GB)
    capacity = 0.0

    # OSD number of host (osd数量)
    n_osd_in_host = 4

    # host number of replica-domain (host 数量)
    n_host_in_rd = 4

    # rack number of root (rack 数量)
    n_rack_in_root = 1

    # replica-domain number of root (副本域数量)
    n_rd_in_root = 1

    # Hours of one year
    hour_a_year = 24*365

    def __init__(self):
        self.name = 'prmc'

    def prepare(self, cfg):
        
        self.rep = cfg['replica_num']
        self.numOfOSD = cfg['osd_num']
        self.afr = cfg['disk_afr']
        self.usage = cfg['disk_usage']
        self.writerate = cfg['disk_writerate']
        self.capacity = cfg['disk_capacity']
        self.n_osd_in_host = cfg['num_osd_in_host']
        self.n_host_in_rd = cfg['num_host_in_replic_domain']
        self.n_rack_in_root = cfg['num_rack_in_root']
        self.n_rd_in_root = cfg['num_replic_domain_in_root']

        self.fit = self.afr / self.hour_a_year

        return True

    
    def possibility(self, n_osd, time):
        y = Decimal(self.fit) * Decimal((self.numOfOSD - n_osd)) * Decimal(time) * -1
        p = 1 - math.pow(math.e, y)
        print("[possibility] y:%E, p:%E" % (y, p))
        return p

    # recovery time (hour)
    def recoverytime(self, n_osd):
        rt = (self.capacity * 1024.0 * self.usage)/(self.writerate * (self.n_osd_in_host - n_osd))/3600.0
        return rt

    '''
    Pr = P1(any) * P2(any) * P3(any)
    '''
    def calc_pr(self, rep):
        if rep <=0 :
            return 1
        rt = self.recoverytime(1)
        pr = 1
        for i in range(rep):
            if i == 0 :
                # P1(any):
                p = self.possibility(0, self.hour_a_year)
            else:
                # Pn(any):
                p = self.possibility(i, rt)
            pr = pr * p

        print("rt : %f, pr : %E" % (rt, pr))
        return pr

    def calc_copyset(self, rep):
        m = 1
        for i in range(rep):
            mi = common.combination(1, self.n_osd_in_host) * common.combination(1, self.n_host_in_rd)
            m = m * mi
        m = m * common.combination(rep, self.n_rack_in_root)
        m = m * common.combination(1, self.n_rd_in_root)

        c = common.combination(rep, self.numOfOSD)

        cs = float(m) / float(c)
        
        print("m : %d, c : %d , cs : %f" % (m, c ,cs))
        return cs

    def calc(self):

        pr = self.calc_pr(self.rep)
        cs = self.calc_copyset(self.rep)

        p = 1.0 - (pr * cs)

        return p
    



#if __name__ == '__main__':
#    ref = calc_prmc()
#    p = ref.calc()
#    print("calc : %.20f(%E)" % (p, p))
