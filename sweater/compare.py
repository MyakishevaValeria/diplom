rep = ""
def grade_wheel(a, b, c, d, e, f, g, h, i, j, k, l):
    list = [a, b, c, d, e, f, g, h, i, j, k, l]
    if all(item == 3 for item in list):
        result = 10
        rep = "456"
    elif any(item == 4 for item in list) or any(item == 2 for item in list):
        result = 3
    else:
        result = 0
    return result


def grade_spring(a, b, c, d, e, f, g, h, i, j, k, l):
    list = [a, b, c, d, e, f, g, h, i, j, k, l]
    if all(item == 68 for item in list):
        result = 10
    elif any(item == 69 for item in list) or any(item == 67 for item in list):
        result = 3
    else:
        result = 0
    return result


def grade_dvs(a, b, c, d, e):
    if a < 1250 and b == 32 and 4 < c < 7 and 8 < d < 10 and 12 < e < 12.8:
        result = 10
    elif (1250 < a < 1500 or b == 31 or b == 33 or 2.5 < c < 4 or 7 < c < 8.5
          or d == 7 or d == 11 or e == 12 or e == 12.8):
        result = 3
    else:
        result = 0
    return result

repair = ''
def grade_transmission(a, b, c):
    global repair
    if 1.20 < a < 1.25:
        result_a = 10
    elif 1.15 < a < 1.20 or 1.25 < a < 1.30:
        result_a = 3
    else:
        result_a = 0
        repair = repair + "Замените масло в двигателе"
    if 0.35 < b < 0.4:
        result_b = 10
    elif 0.3 < b < 0.35 or 0.4 < b < 0.45:
        result_b = 3
    else:
        result_b = 0
        repair = repair + "Замените охлаждающую жидкость"
    if 0.08 < c < 0.12:
        result_c = 10
    elif 0.05 < c < 0.08 or 0.12 < c < 0.15:
        result_c = 3
    else:
        result_c = 0
        repair = repair + "Проверить давление"
    result = (result_a+result_b+result_c)/3
    return result


def grade_pneumatics(a, b, c, d, e, f, g, h, i, j, k, l, m):
    if (7.2 < a < 8.2 and b < 0.2 and c == 0.2 and d == 0.2 and 13 < e < 15 and f < 0.1
            and g < 4 and 30 < h < 40 and 5.0 < i < 5.3 and 4.0 <j< 5.0 and 80 < k < 100 and l < 3 and m < 7):
        result = 10
    elif (a == 7.2 or 8.2 == a or 0.2 == b or c == 0.3 or d == 0.3 or e == 13 or f == 0.1
            or g == 4 or 30 == h or h == 40 or 5.0 == i or i == 5.3 or 4.0 == j or j == 5.0
            or 80 == k or k == 100 or l == 3 or m == 7.1 or m == 6.9):
        result = 3
    else:
        result = 0
    return result


def grade_device(a, b, c, d, e):
    list = [a, b, c, d, e]
    if all(item == 'Исправен' for item in list):
        result = 10
    else:
        result = 0
    return result


def grade_brake(a, b):
    if a == 20 and 40 < b < 70:
        result = 10
    elif a == 19 or a == 21 or 70 < b <100:
        result = 3
    else:
        result = 0
    return result


def markM(a, b, c, d, e, f, g):
    res = (a+b+c+d+e+f+g)/7
    print(res)
    return res


def repairM():
    global repair
    if repair == '':
        repair = 'реммонт не требуется'
    return repair


