
def ismassive(massive):
    """
    Проверяет, принадлежит ли переданный объект типу данных list или tuple (т.к. они являются массивами).
    @param massive объект для проверки.
    @return true если проверка пройдена успешно; false - в противном случае.
    """
    return isinstance(massive, list) or isinstance(massive, tuple)

def LPair(pair):
    """
    Возвращает левую часть валютной пары.
    @pair валютная пара.
    @return левая часть валютной пары.
    Например:
        'BTC_USD' => 'BTC'
    """
    return str(pair).split('_')[0]

def RPair(pair):
    """
    Возвращает правую часть валютной пары.
    @pair валютная пара.
    @return правая часть валютной пары.
    Например:
        'BTC_USD' => 'USD'
    """
    return str(pair).split('_')[1]

def dictKeysRename(targetDict, currentNames, futureNames):
    """
    Изменяет имена ключей в словаре.
    @param targetDict целевой словарь для замены ключей.
    @param currentNames текущие имена ключей для замены.
    @param futureNames новые имена для изменяемых ключей.
    @return ссылка на переданный словарь в случае упеха; None - в противном случае.
    """
    try:
        targetDict[futureNames] = targetDict.pop(currentNames)
    except:
        try:
            for i, currentName in enumerate(currentNames):
                targetDict[futureNames[i]] = targetDict.pop(currentName)
        except:
            return None
    return targetDict

def dictKeysRemove(targetDict, removeNames):
    """
    Удаляет ключи в словаре.
    :param targetDict: целевой словарь для удаления ключей.
    :param removeNames: имена ключей которые необходимо удалить.
    :return: ссылка на переданный словарь в случае успеха; None - в противном случае.
    """
    try:
        targetDict.pop(removeNames)
    except:
        try:
            for i, removeName in enumerate(removeNames):
                targetDict.pop(removeName)
        except:
            return None
    return targetDict

def dictValuesToFloat(targetDict):
    """
    Преобразует все значения по всем ключам переданного словаря из типа str в тип float.
    :param targetDict: целевой словарь для приведения типов значений ключей.
    :return: ссылка на переданный словарь в случае успеха; None - в простивном случае.
    """
    try:
        for keys in targetDict:
            targetDict[keys] = float(targetDict[keys])
    except:
        return None
    return targetDict
