from abc import ABC, abstractclassmethod
from Common.Common import *

class TradeRestricted:
    """Коды ограничений, наклыдываемых на осуществеление (реализацию) ордеров на бирже"""
    MIN_QUANTITY = 'MIN_QUANTITY' # минимально количесто валюты которое можно задействовать в ордере.
    MAX_QUANTITY = 'MAX_QUANTITY' # максимальное количество валюты которое можно задействовать в ордере.
    MIN_AMOUNT   = 'MIN_AMOUNT'   # минимально возможная итоговая стоимость ордера.
    MAX_AMOUNT   = 'MAX_AMOUNT'   # максимально возможная итоговая стоимость ордера.
    MIN_PRICE    = 'MIN_PRICE'    # минимальная цена которую можно выставить за валюту в ордере.
    MAX_PRICE    = 'MAX_PRICE'    # максимальная цена которую можно выставить за валюту в ордере.

    RESTRICTEDS  = [MIN_QUANTITY, MAX_QUANTITY, MIN_AMOUNT, MAX_AMOUNT, MIN_PRICE, MAX_PRICE]
    @classmethod
    def check(cls, restricteds):
        """
        Проверяет, присутствует ли ограничение в списке возможных ограничений на ордер.
        Замечание: может принимать на вход, как одно ограничение для проверки, так и список ограничений.
        :param restricteds: ограничения которые необходимо проверить.
        :return: true - все указанные ограничения присутствуют в списке возможных ограничений; false - в противном случае.
        """
        if not restricteds:
            return False
        elif ismassive(restricteds) and len(restricteds) > 0:
            for restricted in restricteds:
                if restricted not in cls.RESTRICTEDS:
                    return False
            return True
        elif restricteds in cls.RESTRICTEDS:
            return True
        return False


class OrderAttributes:
    """Атртибуты торгового ордера"""
    ID_ORDER    = 'ID_ORDER'    # идентификатор ордера на бирже.
    ID_TRADE    = 'ID_TRADE'    # идентификатрр сделки по ордеру (операции купли продажи связанной с ордером).
    TIME        = 'TIME'        # дата и время создания ордера/отмены ордера/завершения ордера (в зависимости от типа запроса).
    TYPE        = 'TYPE'        # тип ордера (buy, sell).
    PAIR        = 'PAIR'        # валютная пара фигурующая в ордере.
    PRICE       = 'PRICE'       # цена за единицу валюты фигурирующей в ордере.
    QUANTITY    = 'QUANTITY'    # количество валюты фигурирующей в ордере.
    AMOUNT      = 'AMOUNT'      # итоговая ценность (стоимость) ордера.

    """Возможные типы ордерат (типы сделок по ордеру)"""
    BUY_ORDER = 'BUY_ORDER'  # покупающий ордер.
    SELL_ORDER = 'SELL_ORDER'  # продающий ордер.

    class DealType:
        """Возможные типы ордерат (типы сделок по ордеру)"""
        BUY_ORDER = 'BUY_ORDER'  # покупающий ордер.
        SELL_ORDER = 'SELL_ORDER'  # продающий ордер.

        TYPES = [BUY_ORDER, SELL_ORDER]
        @classmethod
        def check(cls, types):
            """
            Проверяет, присутствует ли тип сделки по ордеру, среди существующих типов сделок.
            Замечание: может принимать на вход, как один тип сделки для проверки, так и список типов сделок.
            :param types: типы сделок по ордеру, возможность существования которых необходимо проверить.
            :return: true - если все указанные типы сделок существуют, как возможные; false - в противном случае.
            """
            if ismassive(types):
                for type in types:
                    if type not in cls.TYPES:
                        return False
                return True
            elif types in cls.TYPES:
                return True
            return False

    ATTRIBUTES = [ID_ORDER, ID_TRADE, TIME, TYPE, PAIR, PRICE, QUANTITY, AMOUNT, DealType.BUY_ORDER, DealType.SELL_ORDER]
    @classmethod
    def check(cls, arrtibutes):
        """
        Проверяет, присутствуют ли атрибуты ордера, среди существующих атрибутов ордера.
        Замечание: может принимать как один атрибут для проверки, так и список атрибутов.
        :param arrtibutes: атрибуты ордера, возможность существования которых необходимо проверить.
        :return: true - если все указанные атрибуты ордера существуют, как возможные; false - в противном случае.
        """
        if ismassive(arrtibutes):
            for arrtibute in arrtibutes:
                if arrtibute not in cls.ATTRIBUTES:
                    return False
            return True
        elif arrtibutes in cls.ATTRIBUTES:
            return True
        return False


class UserInfo:
    """Ключи доступа к структуре идентифицирующей пользователя на бирже пользователя"""
    ID          = "ID"          # идентификатор пользователя на бирже
    DATE        = "DATE"        # дата получения информации о пользователе (дата запроса на биржу).
    BALANCE     = "BALANCE"     # баланс пользователя (представляе из себя словарь типа: {'BTC' : 100})
    RESERVE     = "RESERVE"     # баланс пользователя находящийся в резерве (т.е. участвующий в активных ордерах)

    INFOS = [ID, DATE, BALANCE, RESERVE]
    @classmethod
    def check(cls, infos):
        """
        Проверяет, присутствует ли ключ информации о пользователе среди ключей доступа информации о пользователе.
        Замечание: может принимать на вход, как один ключ для проверки, так и список ключей.
        @param infos ключ который необходимо проверить.
        @return true - если ключ присутствует в списке ключей доступа к информации о пользователе; false - в противном случае.
        """
        if not infos:
            return False
        elif ismassive(infos) and len(infos) > 0:
            for info in infos:
                if info not in cls.INFOS:
                    return False
            return True
        elif infos in cls.INFOS:
            return True
        return False


class TBApi(ABC):
    """Интерфейсный класс, предоставляющий набор метдов для взнаимодейтвия с API биржи"""

    def __init__(self, url, apiVersion, publicKey, secretKey, commission):
        self.__url = url                # доменное имя биржи
        self.__apiVersion = apiVersion  # версия используемого биржевого API
        self.__publicKey = publicKey    # публичный ключ торгового биожевого аккаунта
        self.__secretKey = secretKey    # секретный ключ торгового биржевого аккаунта
        self.__commission = commission  # коммиссия взимаемая биржей с каждой совершённой сделки.
        return

    @property
    def url(self):
        """Возвращает доменное имя биржи"""
        return self.__url

    @property
    def apiVersion(self):
        """Возвращает версию используемого биржевого API"""
        return self.__apiVersion

    @property
    def publicKey(self):
        """Возвращает публичный ключ используемого биржевого API"""
        return self.__publicKey

    @property
    def secretKey(self):
        """Возвращает секретный ключ испльзуемого биржевого API"""
        return self.__secretKey

    @property
    def commission(self):
        """Возвращает размер коммиссии взимаемый биржей с каждой сделки"""
        return self.__commission

    @abstractclassmethod
    def getAvalibleCurrency(self):
        """
        Возвращает список валют представлнных на бирже.
        @return Например:
        ["BTC", "ETH", "USD", "RUB"]
        В случае невозможности получить данные возвращает None.
        """
        raise NotImplemented

    @abstractclassmethod
    def getAvalibleCurrencyPair(self):
        """
        Возвращает список валютных пар представленных на бирже.
        @return Например:
        ["BTC_USD", "BTC_EUR", "USD_RUB", "BTC_ETH"]
        В случае невозможности получить данные возвращает None.
        """
        raise NotImplemented

    @abstractclassmethod
    def getTradeRestricted(self,*, pair=None, restricted=None):
        """
        Возвращает ограничения накладываемые биржей на торговлю (на процесс осуществления ордеров).
        @param pair валютная пара, ограничения по которой необходимо получить.
        @param restricted интересуемые ограничения.
        @return
        1. {'p' : {'r' : num, 'r' : num, ...}, ...}                                     - если никаких ограничений не задано.
        2. {'p' : {'r' : num, 'r' : num}, ...}                                          - если заданы ограничения только на restricted.
        3. {'p' : num, 'p' : num, ...}                                                  - если задано только единичное ограничение на restricted.
        4. {'p' : {'r' : num, 'r' : num, ...}, 'p' : {'r' : num, 'r' : num, ...}}       - если заданы ограничения только на pair.
        5. {'p' : {'r' : num, 'r' : num}, 'p' : {'r' : num, 'r' : num}}                 - если задыны ограничения на pair и на restricted.
        6. {'p' : num, 'p' : num, ...}                                                  - если заданы ограничения на pair и единичное ограничение на restricted.
        7. {'r' : num, 'r' : num, ...}                                                  - если задано только единичное ограничение на pair.
        8. {'r' : num, 'r' : num}                                                       - если задано единичное ограничение на pair и ограничения на restricted.
        9. num                                                                          - если заданы единичные ограничения на pair и на restricted.
        либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY_PAIR
            UNEXISTANCE_TRADE_RESTRICTED
        """
        raise NotImplemented

    @abstractclassmethod
    def getUserInformation(self):
        """
        Возвращает информацию об аккаунте пользователя на бирже.
        :return:
        {
            "ID": 10542,                - идентификатор пользователя на бирже.
            "DATE": 1435518576,         - серверное время и дана получения информации о пользователе.
        }
        В случае невозможности получить данные возвращает None.
        """
        raise NotImplemented

    @abstractclassmethod
    def getUserBalance(self,*, balance=None, reserve=None):
        """
        Возвращает информацию об активном (доступном) и зарезервированном (в ордерах) балансе пользователя.
        Замечание: вариатны ответа помеченные как [1] возвращают только тот баланс пользователя, который не равен нулю.
        :param balance: запрос на акстивный баланс пользователя.
        :param reserve: запрос на зарезервированный баланс пользователя.
        :return:
        1. {'BALANCE' : {'' : num, '' : num, ...}, 'RESERVE' : {'' : num, '' : num, ...}}   - [1] если никаких ограничений не задано.
        2. {'BALANCE' : {'' : num, '' : num}, 'RESERVE' : {'' : num, '' : num}}             - если заданы множественные ограничения на balance и reserve.
        3. {'' : num, '' : num, ...}                                                        - [1] если balance равно True, a reserve равно None.
        4. {'' : num, '' : num, ...}                                                        - [1] если reserve равно True, a balance равно None.
        5. {'' : num, '' : num}                                                             - если задано множественное ограничение на balance, a reserve None.
        6. {'' : num, '' : num}                                                             - если задано множественное ограничение на reserve, a balance None.
        7. [num, num]                                                                       - если заданы единственные ограничения на reverce и balance.
        8. num                                                                              - если задано единственно ограничение на balance, а reserve равно None.
        9. num                                                                              - если задано единственно ограничение на reserve, а balance равно None.
        либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY
        """
        raise NotImplemented

    @abstractclassmethod
    def getCurrencyCountInAccess(self, currency):
        """
        Возвращает количество указанной валюты на аккаунте пользователя на текущий момент, которая находится в непосредственном доступе.
        @param currency аббревиатура интересуемой валюты.
        @return количество непосредственно доступной валюты в случае успеха, либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY
        """
        raise NotImplemented

    @abstractclassmethod
    def getCurrencyCountInOrder(self, currency):
        """
        Возвращает количество указанной валюты на аккаунте пользователя на текущий момент, которая задействована в активных ордерах.
        @param currency аббревиатура интересуемой валюты.
        @return количество задействованной в ордерах валюты в случае успеха, либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY
        """
        raise NotImplemented

    @abstractclassmethod
    def getOpenOrders(self, id=None, *, pair=None, type=None, attributes=None):
        """
        Возвращает информацию по открытым ордерам пользователя.
        Замечание:
            1. Если указан парметр id, то параметры pair и type игрорируются.
            2. Если не указан парметр id, то параметры pair и type не игнорируются, а так же любой запрос будет включать как минимум идентификаторы ордеров.
        :param id: идентификатор итересуемого ордера.
        :param pair: валютная пара интересуемых ордеров.
        :param type: тип онтересуемый ордеров.
        :param attributes: интересуемые атрибуты в каждом ордере.
        :return:
        1. все атрибуты конкретного ордера          - если id не равно None.
        2. указанные атрибуты конкретного ордера    - если id и attributes не равно None; если указан только один атрибут, то выводится только его значение.
        3. если pair не равен None                  - из итоговой выборки возвращаются только те валютные пары, которые указаны в pair.
        3. если type не равен None                  - из итоговой выборки возвращаются только те ордера, тип которых соотвествуюет указанному.
        4. если attributes не навен None            - ордера из итоговой выборки, имеют только перечисленные отрибуты; если указан только один атрибут, то выводится только его значение.
        Например:
        {
            "BTC_USD": [                        - валютная пара.
                {
                    "ID_ORDER": "14",           - идентификатор ордера.
                    "TIME": "1435517311",       - дата и время создания ордера.
                    "TYPE": "BUY" или "SELL",   - тип ордера.
                    "PRICE": "100",             - цена покупки/продажи валюты.
                    "QUANTITY": "2",            - количество покупаемой/продаваемой валюты.
                    "AMOUNT": "200"             - стоимость покупаемой/продаваемой валюты (без учёта коммиссии).
                }
            ]
        }
        либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY_PAIR
            UNEXISTANCE_TYPE_ORDER_TO
            UNEXISTANCE_ORDER_ATTRIBUTE
            UNEXISTANCE_TYPE_ORDER_FROM
            UNEXISTANCE_ORDER_ID
        """
        raise NotImplemented

    @abstractclassmethod
    def getClosedOrders(self, id=None, *, pair=None, type=None, attributes=None, offset=0, limit=100):
        """
        Возвращает информацию о закрытых ордерах пользователя.
        Замечание:
            1. Если указан параметр id, то параметры pair и type игнорируются.
            2. Если не указан параметр id, то параметры pair и type не игрорируются, а так же любой запрос будет включать как минимум идентификаторы ордеров.
        :param id: идентификатор интересуемого ордера.
        :param pair: валютная пара интересуемых ордеров.
        :param type: тип интересуемых ордеров.
        :param attributes: интересуемые атрибуты в кадом ордере.
        :param offset: указывает, какое смещение (в прошлое) относительно последнего ордера необходимо использовать в запросе.
        :param limit: указывает, общее количество ордеров, получаемых в результате выполнения запроса.
        :return:
        1. все атрибуты конкретного ордера          - если id не равно None.
        2. указанные атрибуты конкретного ордера    - если id и attributes не равно None; если указан только один атрибут, то выводится только его значение.
        3. если pair не равен None                  - из итоговой выборки возвращаются только те валютные пары, которые указаны в pair.
        3. если type не равен None                  - из итоговой выборки возвращаются только те ордера, тип которых соотвествуюет указанному.
        4. если attributes не навен None            - ордера из итоговой выборки, имеют только перечисленные отрибуты; если указан только один атрибут, то выводится только его значение.
        Например:
        {
            "BTC_USD": [                        - валютная пара.
                {
                    "ID_ORDER": 7,              - идентификатор ордера.
                    "ID_TRADE": 3,              - идентификатор сделки.
                    "TIME": 1435488248,         - дата и время закрытия (заверешния) ордера.
                    "TYPE": "BUY" или "SELL",   - тип ордера.
                    "PRICE": 150,               - цена по которой была куплена/продана валюта.
                    "QUANTITY": 2,              - количество купленной/проданной валюты.
                    "AMOUNT": 300               - стоимость купленной/проданной валюты (без учтёта коммиссии).
                }
            ]
        }
        либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY_PAIR
            UNEXISTANCE_TYPE_ORDER_TO
            UNEXISTANCE_ORDER_ATTRIBUTE
            UNEXISTANCE_TYPE_ORDER_FROM
            UNEXISTANCE_ORDER_ID
        """
        raise NotImplemented

    @abstractclassmethod
    def getDiscardOrders(self, id=None, *, pair=None, type=None, attributes=None, offset=0, limit=100):
        """
        Возвращает информацию об отменённых ордерах пользователя.
        Замечание:
            1. Если указан параметр id, то параметры pair и type игнорируются.
            2. Если не указан параметр id, то параметры pair и type не игрорируются, а так же любой запрос будет включать как минимум идентификаторы ордеров.
        :param id: идентификатор интересуемого ордера.
        :param pair: валютная пара интересуемых ордеров.
        :param type: тип интересуемых ордеров.
        :param attributes: интересуемые атрибуты в кадом ордере.
        :param offset: указывает, какое смещение (в прошлое) относительно последнего ордера необходимо использовать в запросе.
        :param limit: указывает, общее количество ордеров, получаемых в результате выполнения запроса.
        :return:
        1. все атрибуты конкретного ордера          - если id не равно None.
        2. указанные атрибуты конкретного ордера    - если id и attributes не равно None; если указан только один атрибут, то выводится только его значение.
        3. если pair не равен None                  - из итоговой выборки возвращаются только те валютные пары, которые указаны в pair.
        3. если type не равен None                  - из итоговой выборки возвращаются только те ордера, тип которых соотвествуюет указанному.
        4. если attributes не навен None            - ордера из итоговой выборки, имеют только перечисленные отрибуты; если указан только один атрибут, то выводится только его значение.
        Например:
        {
            "BTC_USD": [
                {
                    "ID_ORDER": 15,             - идентификатор ордера.
                    "TIME": 1435519742,         - дата и время отмены ордера.
                    "TYPE": "BUY" или "SELL",   - тип ордера.
                    "PRICE": 100,               - цена по которой должна была быть куплена/продана валюта.
                    "QUANTITY": 3,              - количество валюты которая должна была быть куплена/продана.
                    "AMOUNT": 300               - стоимость валюты которая длжна была быть продана/куплена.
                }
            ]
        }
        либо один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY_PAIR
            UNEXISTANCE_TYPE_ORDER_TO
            UNEXISTANCE_ORDER_ATTRIBUTE
            UNEXISTANCE_TYPE_ORDER_FROM
            UNEXISTANCE_ORDER_ID
        """
        raise NotImplemented

    @abstractclassmethod
    def getCurrentBuyPrice(self, pair=None):
        """
        Возвращает текущую цену покупки (актуальную по биржевому курсу) валютной пары.
        @return
        1. Если указан параметр pair - текущую цену покупки указанной валютной пары.
        2. Если параметр pair не указан, возвращает массив соответствия валютных пар и актуальной цены.
            Например:
            {"BTC_USD" : 100, "BTC_EUR" : 70, "USD_RUB" : 70}
        3. Один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY_PAIR
        """
        raise NotImplemented

    @abstractclassmethod
    def getCurrentSellPrice(sefl, pair=None):
        """
        Возвращает текущую цену продажи (актуальную по биржевому курсу) валютной пары.
        @return
        1. Если указан параметр pair - текущую цену продажи указанной валютной пары.
        2. Если параметр pair не указан, возвращает массив соответствия валютных пар и актуальной цены.
            Например:
            {"BTC_USD" : 95, "BTC_EUR" : 69, "USD_RUB" : 68}
        3. Один из следующих кодов ошибки:
            UNEXISTANCE_CURRENCY_PAIR
        """
        raise NotImplemented

    @abstractclassmethod
    def createBuyOrder(self, pair, quantity, price=None, *, isEmergency=False, isTest=False):
        """
        Создаёт оредер на покупку.
        Замечание: если цена за единицу покупаемой валюты не указана, то ордер будет создан на основании текущй рыночной цены.
        :param pair: валютная пара создаваемого ордера.
        :param quantity: количество покупаемой валюты.
        :param price: цена за единицу покупаемой валюты.
        :param isEmergency флаг, отменяющий какие-либо проверки создаваемого ордера.
        :param isTest флаг, запрещающий фактическое создание ордера на бирже, если взведён.
        :return: идентификатор созданного ордера в случае успеха, либо один из возможных кодов ошибки.
        Возможные коды ошибок:
            NOT_ANOUGHT_CURRENCY_FOR_BUY
            UNEXISTANCE_CURRENCY_PAIR
            UNAVALIBLE_MIN_QUANTITY_FOR_ORDER
            UNAVALIBLE_MAX_QUANTITY_FOR_ORDER
            UNAVALIBLE_MIN_PRICE_FOR_ORDER
            UNAVALIBLE_MAX_PRICE_FOR_ORDER
            UNAVALIBLE_MIN_AMOUNT_FOR_ORDER
            UNAVALIBLE_MAX_AMOUNT_FOR_ORDER
            PURCHASE_PRICE_MORE_THAN_MARKET
            CREATE_TEST_ORDER
        """
        raise NotImplemented

    @abstractclassmethod
    def createSellOrder(self, pair, quantity, price=None, *, isEmergency=False, isTest=False):
        """
        Создаёт ордер на продажу.
        Замечание: если цена за единицу продаваемой валюты не указана, то ордер будет создан на основании текущей рыночной цены.
        :param pair используемая валютная пара (например, BTC_USD - означает, что продаём биткоины за доллары)
        :param quantity количество валюты которое хотим продать.
        :param price цена за единицу продаваемой валюты.
        :param isEmergency флаг, отменяющий какие-либо проверки создаваемого ордера.
        :param isTest флаг, запрещающий фактическое создание ордера на бирже, если взведён.
        :return: идентификатор созданного на продажу ордера в случае успеха, либо один из следующих кодов ошибки:
            NOT_ANOUGHT_CURRENCY_FOR_SALE
            UNEXISTANCE_CURRENCY_PAIR
            UNAVALIBLE_MIN_QUANTITY_FOR_ORDER
            UNAVALIBLE_MAX_QUANTITY_FOR_ORDER
            UNAVALIBLE_MIN_PRICE_FOR_ORDER
            UNAVALIBLE_MAX_PRICE_FOR_ORDER
            UNAVALIBLE_MIN_AMOUNT_FOR_ORDER
            UNAVALIBLE_MAX_AMOUNT_FOR_ORDER
            SELLING_PRICE_LESS_THAN_MARKET
            CREATE_TEST_ORDER
        """
        raise NotImplemented

    @abstractclassmethod
    def cancelOrderById(self, id):
        """
        Отменяет ордер (перемещает активный ордер в список отменённых ордеров).
        @param id идентификатор отменяемого ордера.
        @return true - если оредр был успешно отменён; false - в противном случае.
        либо один из следующих кодов ошибок:
            UNEXISTANCE_ORDER_ID
        """
        raise NotImplemented

