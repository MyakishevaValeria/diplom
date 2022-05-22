def markM(a, b):
    res = (int(a)+int(b))/2
    print(res)
    return res


def markTR(x, y, z):
    if 1.20 < float(x) < 1.25 and 0.35 < float(y) < 0.4 and 0.08 < float(z) < 0.12:
        result = 10
    elif 1.19 < float(x) < 1.26 and 0.34 < float(y) < 0.41 and 0.07 < float(z) < 0.13:
        result = 3
    else:
        result = 0
    return result


def markDVS(a, b):
    if 4.0 < float(a) < 7.0 and int(b) < 8000:
        result = 10
    elif 3.0 < float(a) < 8.0 and int(b) < 9000:
        result = 3
    else:
        result = 0
    return result


def repair(a):
    if float(a) == 10.0:
        result = 'Ремонт не требуется'
    else:
        result = 'Требуется ремонт'
    return result

