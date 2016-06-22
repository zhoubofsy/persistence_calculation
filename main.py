#!/usr/bin/env python2.7
# coding:utf-8

import config
import calc_prmc
import calc_base

if __name__ == '__main__':

    cfg = None
    if config.name == 'prmc':
        ref = calc_prmc.calc_prmc()
        cfg = config.prmc
    else:
        ref = calc_base.calc_base()

    print("================%s calc===================" % ref.name)
    p = 0.0
    if ref.prepare(cfg):
        p = ref.calc()
    print("calc : %.20f(%E)" % (p, p))
