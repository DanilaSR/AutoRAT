import matplotlib.pyplot as plt

import metrics_calculations as calc
import numpy as np


class PointTarget:
    def __init__(self, filename):

        self.azimuth_slice = None
        self.range_slice = None
        self.data = np.load(filename)
        self.scale = 25

        self.interpolate()
        self.slice()

    def interpolate(self):
        """
        Интерполяция отклика точеченого отражателя методом добавления нулей в концы спектра
        :return: None
        """
        #Преобразование Фурье
        ft = np.fft.fft2(self.data)
        #Матрица модуля преобразования Фурье (матрица действительных чисел)
        A = np.abs(ft)
        #Суммирование строк и стобцов матрицы A
        ysum = np.zeros(A.shape[0], dtype="double")
        xsum = np.zeros(A.shape[1], dtype="double")
        for i in range(A.shape[1]):  # Суммирование столбцов
            ysum += A[:, i]
        for j in range(A.shape[0]):  # Суммирование строк
            xsum += A[j, :]
        #Определение характера выпуклости функциЙ xsum и ysum в первом приближении
        ddy = calc.polynom(ysum)
        ddx = calc.polynom(xsum)
        #Если старший коэффициент больше нуля, то в нулевом приближении функция выпукла вверх, меньше нуля - вниз.
        #Соотвественно в первом случае мы можем найти глобальный минимум, во втором - нет

        #Степень "Растяжения спектра"
        scale = self.scale
        #"Растяжение" в длину
        length = np.zeros([ft.shape[0], scale * ft.shape[1]], dtype='complex64')
        for i in range(ft.shape[0]):
            min_row = np.argmin(np.abs(ft[i, :]))
            for j in range(ft.shape[1]):
                if ddx > 0:
                    if j < min_row:
                        length[i, j] = ft[i, j]
                    else:
                        length[i, (scale - 1) * ft.shape[1] + j] = ft[i, j]
                else:
                    length[i, int(0.5 * (scale - 1) * ft.shape[1]) + j] = length[i, j]

        # "Растяжение" в ширину
        square = np.zeros([scale * ft.shape[0], length.shape[1]], dtype='complex64')
        for j in range(length.shape[1]):
            min_col = np.argmin(np.abs(length[:, j]))
            for i in range(length.shape[0]):
                if ddy > 0:
                    if i < min_col:
                        square[i, j] = length[i, j]
                    else:
                        square[(scale - 1) * ft.shape[0] + i, j] = length[i, j]
                else:
                    square[int(0.5 * (scale - 1) * ft.shape[0]) + i, j] = length[i, j]

        #Запись интерполированного спектра
        self.data = np.fft.ifft2(square)

    def slice(self):
        """
        Вычисляет проекции отклика в главных осях
        :return: None
        """
        #Координаты главных направляющих осей
        ind_row_slice = []
        #Главные оси
        row_slice = []

        #Поиск центра отклика
        maximum = np.max(self.data)
        center = (0, 0)
        for i in range(self.data.shape[0]):
            for j in range(self.data.shape[1]):
                if self.data[i, j] == maximum:
                    center = (i, j)

        col_slice = self.data[:, center[1]]

        #Записываем координаты максимумов по строкам и столбцам
        for j in range(self.data.shape[1]):
            argmax = np.argmax(np.abs(self.data[:, j]))
            ind_row_slice.append(argmax)

        for j in range(self.data.shape[1]):
            i = ind_row_slice[j]
            row_slice.append(self.data[i][j])

        self.azimuth_slice = np.array(np.abs(col_slice))
        self.range_slice = np.array(np.abs(row_slice))

    def azimuth_irw(self):
        """
        Вычисляет IRW по азимуту
        :return: разрешение в метрах
        """
        da = 50 / 200
        return da*calc.irw(self.azimuth_slice)/self.scale

    def azimuth_pslr_db(self):
        """
        Вычисляет PSLR по азимуту
        :return: PSLR
        """
        return calc.pslr(self.azimuth_slice)

    def azimuth_islr_db(self):
        """
        Вычисляет ISLR по азимуту
        :return: ISLR
        """
        return calc.islr(self.azimuth_slice)

    def range_irw(self):
        """
        Вычисляет IRW по дальности
        :return: разрешение в метрах
        """
        dr = 0.5 * 3e8 / 720e6
        return dr*calc.irw(self.range_slice)/self.scale

    def range_pslr_db(self):
        """
        Вычисляет PSLR по дальности
        :return: PSLR
        """
        return calc.pslr(self.range_slice)

    def range_islr_db(self):
        """
        Вычисляет ISLR по дальности
        :return: ISLR
        """
        return calc.islr(self.range_slice)

    def set_scale(self, scale0):
        """
        Задаёт значение Scale
        :param scale0: параметр интерполяции
        :return: None
        """

        self.scale = scale0

    def get_scale(self):
        """
        Возвращает значение Scale
        :return: Scale
        """

        return self.scale

    def show_point(self):
        """
        Выводит изображение точечного отражателя
        :return: None
        """
        plt.imshow(np.abs(self.data))
        plt.show()

    def show_slices(self):
        """
        Выводит графики сечений по азимуту и дальности
        :return:
        """

        plt.figure(figsize=(9, 18))

        plt.subplot(211)
        plt.title('Azimuth Slice')
        t1 = np.linspace(0, self.azimuth_slice.size, self.azimuth_slice.size)
        plt.plot(t1, self.azimuth_slice)

        plt.subplot(212)
        plt.title('Range Slice')
        t2 = np.linspace(0, self.range_slice.size, self.range_slice.size)
        plt.plot(t2, self.range_slice)

        plt.show()


class PointTargetScale(PointTarget):

    def __init__(self, filename, scale0):

        self.azimuth_slice = None
        self.range_slice = None
        self.data = np.load(filename)
        self.scale = scale0

        self.interpolate()
        self.slice()


