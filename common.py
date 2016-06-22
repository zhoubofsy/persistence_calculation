#!/usr/bin/env python2.7
# coding:utf-8



#
# 计算阶乘方法
#
def factorial(n, s = 1):
    if n <= 1 or n < s :
        return 1
    return reduce(lambda x,y:x*y, range(s,n+1))

#
# 计算组合方法
#
def combination(up,down):
    if up > down:
        return -1

    result = factorial(down) / (factorial(up) * factorial(down - up))
    return result


if __name__ == '__main__':
    # test factorial
    ret = factorial(3)
    print("factorial(3) = %d" % ret)

    # test combination
    ret = combination(3,5)
    print("combination(3,5) = %d" % ret)

