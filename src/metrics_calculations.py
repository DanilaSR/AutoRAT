import numpy as np
from scipy.signal import find_peaks
from scipy.signal import peak_widths
from scipy.interpolate import CubicSpline
import scipy.integrate as integrate


def irw(signal):
    """
    Вычисляет IRW (impulse response width) входного сигнала
    :param signal: массив действительных чисел, функция вида sin(x)/x
    :return: значение IRW сигнала
    """
    # Находим локальные максимумы
    peaks = find_peaks(signal)[0]
    # Мерим их ширину на высоте 1/sqrt(2)
    width = peak_widths(signal, peaks, rel_height=1 - 1 / np.sqrt(2))[0]
    # Отбираем максимальную ширину - ширину главного лепестка
    irw = np.max(width)
    return irw


def pslr(signal):
    """
    Вычисляет PSLR (Peak sidelobe ratio) входного сигнала
    :param signal: массив действительных чисел, функция вида sin(x)/x
    :return: значение PSLR сигнала
    """
    # Находим локальные максимумы
    peaks = find_peaks(signal)[0]
    # Находим глобальный максимум
    arg_max = np.argmax(signal)
    # Находим высоту главного пика
    main = signal[arg_max]
    # Находим порядковый номер глобального максимума среди локальных
    main_index = np.where(peaks == np.argmax(signal))[0][0]
    # Порядковый номер левого и правого боковых лепестков
    # Left sidelobe index, right sidelobe index
    ls_index = main_index - 1
    rs_index = main_index + 1
    # Соответствующие им высоты
    ls = signal[peaks[ls_index]]
    rs = signal[peaks[rs_index]]

    if rs > ls:
        sidelobe = rs
    else:
        sidelobe = ls

    pslr = 10 * np.log10(sidelobe ** 2 / main ** 2)
    return pslr


def islr(signal):
    """
    Вычисляет ISLR (integrated sidelobe ratio) входного сигнала
    :param signal: массив действительных чисел, функция вида sin(x)/x
    :return: значение ISLR сигнала
    """
    # Массив аргументов
    t = np.linspace(0, signal.size, signal.size)
    # Интерполяция сигнала кубическим сплайном
    cs = CubicSpline(t, signal)
    # Поиск локальных максимумов
    peaks = find_peaks(signal)[0]
    # Поиск главного максимуа
    main_index = np.where(peaks == np.argmax(signal))[0][0]

    # Поиск левой и правой границы главного лепестка. Считаем от локальных минимумов
    sec = np.linspace(peaks[main_index - 1], peaks[main_index], 100)
    ind = np.argmin(cs(sec))
    lmin = sec[ind]

    sec = np.linspace(peaks[main_index], peaks[main_index + 1], 100)
    ind = np.argmin(cs(sec))
    rmin = sec[ind]

    islr = integrator(signal, lmin, rmin)

    return islr


def cut(t, array):
    """
    Удаляет значения массива array, которые больше чем 1/sqrt(e), на уровне 2 сигма
    :param t: массив, номера элементов array
    :param array: массив действительных чисел
    :return: возвращает номера и значения отфильтрованного массива
    """

    # Отсечение происходит на уровне 1/sqrt(e)
    ymax = np.max(array)
    del_ = []
    for i in range(np.size(array)):
        if array[i] >= 0.6 * ymax:
            del_.append(i)
    array = np.delete(array, del_)
    t = np.delete(t, del_)
    return t, array


def polynom(array):
    """
    Аппроксимация функции, заданной массивом array полиномом 2-ой степени.
    :param array: массив действительных чисел
    :return: старший коэффициент
    """
    t = np.linspace(0, np.size(array), np.size(array))
    # Обрезание спектра
    res = cut(t, array)
    t = res[0]
    array = res[1]
    # Аппроксимация полиномом второй степени для определения выпуклости
    fp = np.polyfit(t, array, 2)
    return fp[0]


def rotate(point, center, theta):
    """
    Поворачивает точку point относительно точки center на угол theta
    :param point: tuple вида (x, y)
    :param center: tuple вида (x, y)
    :param theta: значение угла в радианах
    :return:
    """
    x = point[0]
    y = point[1]

    x0 = center[1]
    y0 = center[0]

    M11 = np.cos(theta)
    M12 = -np.sin(theta)
    M21 = np.sin(theta)
    M22 = np.cos(theta)

    M = np.array(([M11, M12], [M21, M22]))
    v = np.array(([x - x0], [y - y0]))

    res = np.dot(M, v) + np.array(([x0], [y0]))
    return res[0], res[1]


def integrator(signal, a, b):
    """
    Bычисляет интеграл от signal^2 в интервале от a до b
    :param signal: интерполированный массив дейтсвительных чисел
    :param a: левая граница
    :param b: правая границы
    :return: значение интеграла
    """

    sz = signal.size
    total = 0
    main = 0
    for x in range(sz):
        total += signal[x] * signal[x]
        if a <= x <= b:
            main += signal[x] * signal[x]

    return 10 * np.log10((total - main) / main)
