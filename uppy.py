from connect_base_criterion import _table_unit_, _table_coeff_


# --- получение единиц измерения параметров
def get_units_parameters(unit_of_measurement = {}, parameters = []):
    units_measurement = [unit_of_measurement.get(i) for i in parameters]
    return units_measurement

# --- получение коэффициентов из единиц измерения
def get_coeff_from_units(table_coeff = {}, units_measurement = []):
    temporary = []
    for i in units_measurement:
        if i in table_coeff:
            temporary.append(table_coeff.get(i))
    return temporary

# --- получаем из одной матрицы 4on3 -> 4 матрицы 3on3 (крч иллюзия приравнивания к нулю)
def create_3on3_matrix(matrix_a):
    sparse_matrix = []
    # в данном случае:  len(matrix_a[0]) = кол-во неизвестных; len(matrix_a) = кол-во уравнений
    for i in range(len(matrix_a[0]) * (len(matrix_a[0]) - len(matrix_a))):
        temporary = [[*matrix_a[i]] for i in range(len(matrix_a))]
        for j in temporary:
            j.pop(i)
        sparse_matrix.append(temporary)
        # print(sparse_matrix)
    return sparse_matrix

# --- поворот матриц и реверс + генерация матриц A и B для метода гауса
def preparation_matrix_gauss(source_matrix):
    B = source_matrix.pop(0) # вычленяем матрицу B
    A = list(zip(*source_matrix[::-1])) # поворачиваем матрицу по часовой
    A = list(map(list, A)) # переделываем вложенные кортежи в списки
    for i in A: # реверсим вложенные списки
        i.reverse()
    A = create_3on3_matrix(A)
    return(A, B)

# --- исследование других законов на той же базе. напимер(F= f(v, m, l, t); l = f(v, F, m, t))
def get_new_laws(parameters):
    list_of_parameters = []
    for i in range(len(parameters)):
        parameters = parameters[-1:] + parameters[:-1] 
        list_of_parameters.append(parameters)
    list_of_parameters.reverse()
    return list_of_parameters

# --- перемена местами двух строк системы
def swap_rows(A, B, row1, row2):
    A[row1], A[row2] = A[row2], A[row1]
    B[row1], B[row2] = B[row2], B[row1]

# --- деление строки системы на число
def divide_row(A, B, row, divider):
    A[row] = [a / divider for a in A[row]]
    B[row] /= divider

# --- сложение строки системы с другой строкой, умноженной на число
def combine_rows(A, B, row, source_row, weight):
    A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
    B[row] += B[source_row] * weight

# --- решение системы методом Гаусса (приведением к треугольному виду)
def gauss(A, B):
    column = 0
    while (column < len(B)):
        current_row = None
        for r in range(column, len(A)):
            if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                 current_row = r
        if current_row is None:
            return None
        if current_row != column:
            swap_rows(A, B, current_row, column)
        divide_row(A, B, column, A[column][column])
        for r in range(column + 1, len(A)):
            combine_rows(A, B, r, column, -A[r][column])
        column += 1
    X = [0 for b in B]
    for i in range(len(B) - 1, -1, -1):
        X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))

    return X

# --- получаем на входе список матриц из которого возвращаем критерии
def preparation_criterion(list_end_matrix, units_measurement):
    list_of_criterion = []
    for i in range(len(list_end_matrix)):
        sTR = ''
        # print("\nprint(list_end_matrix)1",list_end_matrix)
        list_end_matrix[i].insert(i, 0.0)
        list_end_matrix[i].insert(0, -1.0)
        # print("\nprint(list_end_matrix)2",list_end_matrix)
        for j in range(len(list_end_matrix[i])): # 0 1 2 3 4
            if list_end_matrix[i][j] != 0:
                sTR += f" * {str(units_measurement[j])}^{str(list_end_matrix[i][j])}"
        list_of_criterion.append(f'{sTR[3:]}')
    # sTR = f'{sTR[3:]}'
    
    return(list_of_criterion)

# --- просто сбор всех вышеупомянутых функций в одну
def get_init_criterion(table_coeff, table_unit, parameters):
    c= preparation_matrix_gauss(get_coeff_from_units(table_coeff, get_units_parameters(table_unit, 
    parameters)))
    list_end_matrix = []
    for i in (c[0]): list_end_matrix.append(gauss(i, (c[1]).copy()))
    # _criterion_ = preparation_criterion(list_end_matrix, get_units_parameters(table_unit, parameters))
    _criterion_ = preparation_criterion(list_end_matrix, parameters)
    # print("_criterion_\n",_criterion_)
    return _criterion_

def end_criterion(table_coeff, table_unit, parameters):
    a = []
    for i in get_new_laws(parameters):
        try:
            a.append(get_init_criterion(table_coeff,table_unit, i))
        except:
            continue

    temporary = []
    for i in a:
        for j in i:
            temporary.append(j)
    return(temporary)


# _parameters_ = ['v', 'm', 't', 'l', 'F', 'V','Pa','Hz']
_parameters_ = list(map(str, input('введи параметры (через пробел)\n').split())) # v m t l F V Pa Hz



print(
    end_criterion(_table_coeff_, _table_unit_, _parameters_)
    )



# --- вот это вот пример кода который должен выводиться
foo1 = [
    'v^-1.0 * t^-1.0 * l^1.0', 'v^-1.0 * t^-1.0 * l^1.0', 
    'v^-1.0 * m^-0.5 * F^0.5 * l^0.5', 'v^-1.0 * m^-1.0 * F^1.0 * t^1.0', 
    't^-1.0 * Hz^1.0 * v^1.0 * m^-1.0', 
    't^-1.0 * l^0.5 * v^0.5 * m^-0.5', 
    't^-1.0 * l^1.0 * Hz^-1.0', 
    't^-1.0 * l^1.0 * Hz^-1.0', 
    'l^-1.0 * v^-1.0 * m^1.0 * F^2.0', 
    'l^-1.0 * Hz^1.0 * F^1.0', 
    'l^-1.0 * Hz^1.0 * F^1.0', 
    'l^-1.0 * Hz^2.0 * v^1.0 * m^-1.0', 
    'Hz^-1.0 * F^-1.0 * t^1.0', 
    'Hz^-1.0 * F^-1.0 * t^1.0', 
    'Hz^-1.0 * v^-0.5 * m^0.5 * t^0.5', 
    'Hz^-1.0 * v^-1.0 * m^1.0 * F^1.0'
]