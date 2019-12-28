from TBApi.TBApi import TBApi, TradeRestricted, OrderAttributes, UserInfo
from TBApi.TBApiErrors import TBApiErrors
from Common.Common import *

import http.client
import hashlib
import urllib
import json
import hmac
import time
import copy


class TBExmo(TBApi):
    """Класс взаимодествия с биржей Exmo"""

    # Размер коммиссии взимаемый биржей Exmo с кажой совершённой сделки.
    __commission = 0.002
    # Публичный ключ биржевого аккаунта Exmo
    __exmoPublicKey = bytes("", encoding='utf-8')
    # Приватный ключ биржевого аккаунта Exmo
    __exmoSecretKey = bytes("", encoding='utf-8')

    def __init__(self):
        def initialTradeRestricted():
            """Первичное создание словаря ограничений на торговые операции"""
            tradeRestricteds = self.__query(apiMethod="pair_settings")
            for tradePair in tradeRestricteds.keys():
                dictKeysRename(tradeRestricteds[tradePair],
                               ['min_quantity', 'max_quantity', 'min_amount', 'max_amount', 'min_price', 'max_price'],
                               TradeRestricted.RESTRICTEDS)
                for restrictedName in tradeRestricteds[tradePair]:
                    tradeRestricteds[tradePair][restrictedName] = float(
                        tradeRestricteds[tradePair][restrictedName])
            return tradeRestricteds

        def initialUserInfo():
            """Первичная инициализация идентифицирующей информации о пользователе на бирже"""
            userInfo = self.__query(apiMethod="user_info")
            dictKeysRemove(userInfo, ['balances', 'reserved'])
            dictKeysRename(userInfo, ['uid', 'server_date'], [UserInfo.ID, UserInfo.DATE])
            return userInfo

        TBApi.__init__(self, "api.exmo.com", "v1", self.__exmoPublicKey, self.__exmoSecretKey, self.__commission)
        # перивичная инициализация списка доступных валютных пар.
        self.__avalibleCurrencyPair = list(self.__query(apiMethod="ticker").keys())
        # перивичная инициализация списка доступных валют.
        self.__avalibleCurrency = self.__query(apiMethod="currency")
        # первичная инициализция списка словаря ограничений на реализацию торгов.
        self.__tradeRestricteds = initialTradeRestricted()
        # первичная инициализация информации о пользователе на бирже.
        self.__userInfo = initialUserInfo()
        return

    def getAvalibleCurrency(self):
        """Возвращает список валют представлнных на бирже Exmo"""
        return copy.deepcopy(self.__avalibleCurrency)

    def getAvalibleCurrencyPair(self):
        """Возвращает список валютных пар представленных на бирже Exmo"""
        return copy.deepcopy(self.__avalibleCurrencyPair)

    def getTradeRestricted(self, *, pair=None, restricted=None):
        """Возвращает ограничения накладываемые биржей Exmo на торговлю (на процесс осуществления ордеров)"""
        if pair and not self.__isExistancePairCurrency(pair):
            return TBApiErrors.UNEXISTANCE_CURRENCY_PAIR
        if restricted and not TradeRestricted.check(restricted):
            return TBApiErrors.UNEXISTANCE_TRADE_RESTRICTED
        resultRestricted = copy.deepcopy(self.__tradeRestricteds)
        # применение выборки на валютные пары
        if pair:
            if ismassive(pair):
                dictKeysRemove(resultRestricted, [availablePair for availablePair in self.__avalibleCurrencyPair if availablePair not in pair])
            else:
                resultRestricted = {pair: resultRestricted[pair]}
        # применение выборки на парметры ограничений валютных пар
        if restricted:
            if ismassive(restricted):
                for tradePair in resultRestricted.keys():
                    dictKeysRemove(resultRestricted[tradePair], [availableRestricted for availableRestricted in TradeRestricted.RESTRICTEDS if availableRestricted not in restricted])
            else:
                for tradePair in resultRestricted.keys():
                    resultRestricted[tradePair] = resultRestricted[tradePair][restricted]
        # формирование корректного ответа
        if pair and not ismassive(pair):
            resultRestricted = resultRestricted[pair]
        return resultRestricted

    def getUserInformation(self):
        """Возвращает информацию об аккаунте пользователя на бирже Exmo"""
        return copy.deepcopy(self.__userInfo)

    def getUserBalance(self, *, balance=None, reserve=None):
        """Возвращает информацию об активном (доступном) и зарезервированном (в ордерах) балансе пользователя"""
        if (balance and not self.__isExistanceCurrency(balance) and balance) or (reserve is not True and not self.__isExistanceCurrency(reserve) and reserve):
            if not ((balance is True and reserve is None) or (reserve is True and balance is None)):
                return TBApiErrors.UNEXISTANCE_CURRENCY
        userBalance = self.__query(apiMethod="user_info")
        dictKeysRemove(userBalance, ['uid', 'server_date'])
        dictKeysRename(userBalance, ['balances', 'reserved'], [UserInfo.BALANCE, UserInfo.RESERVE])
        dictValuesToFloat(userBalance[UserInfo.BALANCE])
        dictValuesToFloat(userBalance[UserInfo.RESERVE])
        # параметры зыпроса отсутствуют
        if not balance and not reserve:
            dictKeysRemove(userBalance[UserInfo.BALANCE], [currency for currency in userBalance[UserInfo.BALANCE].keys() if userBalance[UserInfo.BALANCE][currency] == 0.0])
            dictKeysRemove(userBalance[UserInfo.RESERVE], [currency for currency in userBalance[UserInfo.RESERVE].keys() if userBalance[UserInfo.RESERVE][currency] == 0.0])
        # параметры запроса заданы только на balance
        elif balance and not reserve:
            if balance is True:
                userBalance = dictKeysRemove(userBalance[UserInfo.BALANCE], [currency for currency in userBalance[UserInfo.BALANCE].keys() if userBalance[UserInfo.BALANCE][currency] == 0.0])
            elif ismassive(balance):
                userBalance = dictKeysRemove(userBalance[UserInfo.BALANCE], [currency for currency in userBalance[UserInfo.BALANCE].keys() if currency not in balance])
            else:
                userBalance = userBalance[UserInfo.BALANCE][balance]
        # параметры запроса заданы только на reserve
        elif reserve and not balance:
            if reserve is True:
                userBalance = dictKeysRemove(userBalance[UserInfo.RESERVE], [currency for currency in userBalance[UserInfo.RESERVE].keys() if userBalance[UserInfo.RESERVE][currency] == 0.0])
            elif ismassive(reserve):
                userBalance = dictKeysRemove(userBalance[UserInfo.RESERVE], [currency for currency in userBalance[UserInfo.RESERVE].keys() if currency not in reserve])
            else:
                userBalance = userBalance[UserInfo.RESERVE][reserve]
        # параметры запроса заданы для обоих входных переменных
        else:
            if ismassive(balance) and ismassive(reserve):
                dictKeysRemove(userBalance[UserInfo.BALANCE], [currency for currency in userBalance[UserInfo.BALANCE].keys() if currency not in balance])
                dictKeysRemove(userBalance[UserInfo.RESERVE], [currency for currency in userBalance[UserInfo.RESERVE].keys() if currency not in reserve])
            else:
                userBalance = [userBalance[UserInfo.BALANCE][balance], userBalance[UserInfo.RESERVE][reserve]]
        return userBalance

    def getCurrencyCountInAccess(self, currency):
        """Возвращает количество указанной валюты на аккаунте пользователя на текущий момент, которая находится в непосредственном доступе"""
        if not self.__isExistanceCurrency(currency):
            return TBApiErrors.UNEXISTANCE_CURRENCY
        return float(self.__query(apiMethod="user_info")['balances'][currency])

    def getCurrencyCountInOrder(self, currency):
        """Возвращает количество указанной валюты на аккаунте пользователя на текущий момент, которая задействована в активных ордерах"""
        if not self.__isExistanceCurrency(currency):
            return TBApiErrors.UNEXISTANCE_CURRENCY
        return float(self.__query(apiMethod="user_info")['reserved'][currency])

    def getOpenOrders(self, id=None, *, pair=None, type=None, attributes=None):
        """Возвращает информацию об открытых ордерах пользователя на бирже Exmo"""
        return self.__queryByOrdersAndFormatResponse(apiMethod="user_open_orders", id=id, pair=pair, type=type, attributes=attributes)

    def getClosedOrders(self, id=None, *, pair=None, type=None, attributes=None, offset=0, limit=100):
        """Возвращет информацию о закрытых (завершённых) ордерах пользователя на бирже Exmo"""
        return self.__queryByOrdersAndFormatResponse(apiMethod="user_trades", params={"offset": offset, "limit": limit}, id=id, pair=pair, type=type, attributes=attributes, offset=offset, limit=limit)

    def getDiscardOrders(self, id=None, *, pair=None, type=None, attributes=None, offset=0, limit=100):
        """Возвращет инфомацию об отменённых ордерах пользователя на бирже Exmo"""
        return self.__queryByOrdersAndFormatResponse(apiMethod="user_cancelled_orders", params={"offset": offset, "limit": limit}, id=id, pair=pair, type=type, attributes=attributes, offset=offset, limit=limit)

    def getCurrentBuyPrice(self, pair=None):
        """Возвращает текущую цену покупки (актуальную по биржевому курсу) валютной пары на бирже Exmo"""
        # Замечание: на Exmo какая-то странная интерпретация понятия sell и buy, поэтому, при получении
        # текущей цены покупки, необходимо обращаться к полу sell_price, а при получении текущей цены
        # продажи - обращаться к полю buy_price.
        if pair and not self.__isExistancePairCurrency(pair):
            return TBApiErrors.UNEXISTANCE_CURRENCY_PAIR
        if pair:
            return float(self.__query(apiMethod="ticker")[pair]["sell_price"])
        else:
            return {key: float(self.__lastIterableQuery[key]["sell_price"]) for key in
                    self.__iterableQuery(apiMethod="ticker").keys()}

    def getCurrentSellPrice(self, pair=None):
        """Возвращает текущую цену продажи (актуальную по биржевому курсу) валютной пары на бирже Exmo"""
        # Замечание: на Exmo какая-то странная интерпретация понятия sell и buy, поэтому, при получении
        # текущей цены покупки, необходимо обращаться к полу sell_price, а при получении текущей цены
        # продажи - обращаться к полю buy_price.
        if pair and not self.__isExistancePairCurrency(pair):
            return TBApiErrors.UNEXISTANCE_CURRENCY_PAIR
        if pair:
            return float(self.__query(apiMethod="ticker")[pair]["buy_price"])
        else:
            return {key: float(self.__lastIterableQuery[key]["buy_price"]) for key in
                    self.__iterableQuery(apiMethod="ticker").keys()}

    def createBuyOrder(self, pair, quantity, price=None, *, isEmergency=False, isTest=False):
        """Создаёт ордер на покупку от аккаунта текущего пользователя на бирже Exmo"""
        if not price:
            price = self.getCurrentBuyPrice(pair)
        if isEmergency is False:
            responceOrderRequest = self.__checkOrderRequest(pair, quantity, price)
            if responceOrderRequest[0] is False:
                return responceOrderRequest[1]
            if not self.__isAnoughtCurrencyValue(RPair(pair), quantity * price):
                return TBApiErrors.NOT_ANOUGHT_CURRENCY_FOR_BUY
            # позволяет сделать ставку на покупку цена которой не превышает рыночную более чем на 0.001
            currentPrice = self.getCurrentBuyPrice(pair)
            if price > currentPrice and (1 - currentPrice / price) > 0.001:
                return TBApiErrors.PURCHASE_PRICE_MORE_THAN_MARKET
        if isTest is True:
            return TBApiErrors.CREATE_TEST_ORDER
        return int(self.__query(apiMethod="order_create", params={'pair' : pair, 'quantity' : quantity, 'price' : price, 'type' : 'buy'})['order_id'])

    def createSellOrder(self, pair, quantity, price=None, *, isEmergency=False, isTest=False):
        """Создаёт ордер на продажу от аккаунта текущего пользователя на бирже Exmo"""
        if not price:
            price = self.getCurrentSellPrice(pair)
        if isEmergency is False:
            responceOrderRequest = self.__checkOrderRequest(pair, quantity, price)
            if responceOrderRequest[0] is False:
                return responceOrderRequest[1]
            if not self.__isAnoughtCurrencyValue(LPair(pair), quantity):
                return TBApiErrors.NOT_ANOUGHT_CURRENCY_FOR_SALE
            # позволяет сделать ставку на продажу цена не меньше рыночной более чем на 0.001
            currentPrice = self.getCurrentSellPrice(pair)
            if price < currentPrice and (1 - price / currentPrice) > 0.001:
                return TBApiErrors.SELLING_PRICE_LESS_THAN_MARKET
        if isTest is True:
            return TBApiErrors.CREATE_TEST_ORDER
        return int(self.__query(apiMethod="order_create", params={'pair' : pair, 'quantity' : quantity, 'price' : price, 'type' : 'sell'})['order_id'])

    def cancelOrderById(self, id):
        """Отменяет ордер (перемещает активный ордер в список отменённых ордеров) пользователя на бирже Exmo"""
        if self.getOpenOrders(id) == TBApiErrors.UNEXISTANCE_ORDER_ID:
            return TBApiErrors.UNEXISTANCE_ORDER_ID
        return bool(self.__query(apiMethod='order_cancel', params={'order_id ' : id})['result'])

    def __query(self, *, apiMethod, params={}):
        """
        Выполняет GET/POST запросы к Exmo и возаращет ответ.
        @apiMethod имя метода API Exmo биржы.
        @params параметрны педоваемые в метод
        @return результат запроса в виде json-форматированной строки
        """

        def computeHash(data):
            """
            Вычисляет хэш-значение приватного ключа биожевого аккаута, подмешивая в итоговое значение передаваемые данные (data).
            @data данные, подмешиваемые в итоговое значение хэша от приватного ключа.
            @return вычисленный хэш.
            """
            key = self.secretKey
            hash = hmac.new(key=self.secretKey, digestmod=hashlib.sha512)
            hash.update(data.encode('utf-8'))
            return hash.hexdigest()

        params['nonce'] = int(round(time.time() * 1000))
        params = urllib.parse.urlencode(params)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",  # тип подписываемых данных
            "Key": self.publicKey,  # публичный ключ для проверки подписи
            "Sign": computeHash(params)}  # подписанные данные
        # подключение и запрос данных.
        conn = http.client.HTTPSConnection(self.url)
        conn.request("POST", "/" + self.apiVersion + "/" + apiMethod, params, headers)
        response = conn.getresponse().read()
        conn.close()
        # обработка запроса
        result = json.loads(response.decode('utf-8'))
        if 'error' not in result:
            return result
        elif 'error' in result and result['error'] == '':
            return result
        return None

    def __iterableQuery(self, *, apiMethod, params={}):
        """Выполняет запрос __quety и сохраняет резултат в переменной __lastIterableQuery"""
        self.__lastIterableQuery = self.__query(apiMethod=apiMethod, params=params)
        return self.__lastIterableQuery

    def __queryByOrdersAndFormatResponse(self, *, apiMethod, params={}, id=None, pair=None, type=None, attributes=None, offset=0, limit=100):
        """Выполняет запрос __quety по следующим api: user_open_orders, user_trades, user_cancelled_orders и возвращает по ним форматированный ответ"""
        avalibleQuerry = ['user_open_orders', 'user_trades', 'user_cancelled_orders']
        if apiMethod not in avalibleQuerry:
            return None
        # проверяет первичные ограничения на запрос, прежде чем его выполнить
        if pair and not self.__isExistancePairCurrency(pair):
            return TBApiErrors.UNEXISTANCE_CURRENCY_PAIR
        if type and not OrderAttributes.DealType.check(type):
            return TBApiErrors.UNEXISTANCE_TYPE_ORDER_TO
        if attributes:
            if not OrderAttributes.check(attributes):
                return TBApiErrors.UNEXISTANCE_ORDER_ATTRIBUTE
            # только в ответе по запросу 'user_trades' в атрибутах ордера присутствует поле 'ID_TRADE'
            if apiMethod == 'user_trades':
                if ismassive(attributes):
                    if OrderAttributes.ID_TRADE in attributes:
                        return TBApiErrors.UNEXISTANCE_ORDER_ATTRIBUTE
                else:
                    if OrderAttributes.ID_TRADE == attributes:
                        return TBApiErrors.UNEXISTANCE_ORDER_ATTRIBUTE
        # выполняет запрос
        userOrders = self.__query(apiMethod=apiMethod, params=params)
        # для 'user_cancelled_orders' существутю особые условия первичного форматирования, т.к. ответ с биржи Exmo в этом случае отличен от остальных
        if apiMethod == 'user_cancelled_orders':
            userCanceledOrders = {}
            for orders in userOrders:
                userCanceledOrders[orders['pair']] = []
            for orders in userOrders:
                userCanceledOrders[orders['pair']].append(orders)
            userOrders = userCanceledOrders
        # общая часть ответа на запрос для всех трёх из возможных запросов
        for currencyPair in userOrders.keys():
            for order in userOrders[currencyPair]:
                dictKeysRemove(order, 'pair')
                dictKeysRename(order, ['order_id', 'order_type', 'price', 'quantity', 'amount'], [OrderAttributes.ID_ORDER, OrderAttributes.TYPE, OrderAttributes.PRICE, OrderAttributes.QUANTITY, OrderAttributes.AMOUNT])
                if order[OrderAttributes.TYPE] == 'buy':
                    order[OrderAttributes.TYPE] = OrderAttributes.DealType.BUY_ORDER
                elif order[OrderAttributes.TYPE] == 'sell':
                    order[OrderAttributes.TYPE] = OrderAttributes.DealType.SELL_ORDER
                else:
                    return TBApiErrors.UNEXISTANCE_TYPE_ORDER_FROM
        # часть ответа на запрос, уникальная для каждого из трёх запросов
        if apiMethod == 'user_open_orders':
            for currencyPair in userOrders.keys():
                for order in userOrders[currencyPair]:
                    dictKeysRename(order, 'created', OrderAttributes.TIME)
        elif apiMethod == 'user_trades':
            for currencyPair in userOrders.keys():
                for order in userOrders[currencyPair]:
                    dictKeysRename(order, ['trade_id', 'date'], [OrderAttributes.ID_TRADE, OrderAttributes.TIME])
        elif apiMethod == 'user_cancelled_orders':
            for currencyPair in userOrders.keys():
                for order in userOrders[currencyPair]:
                    dictKeysRename(order, 'date', OrderAttributes.TIME)
        # формирование ответа согласно запросу пользователя, основанному на заданных ограничениях
        if id:
            for orderCurrencyPair in userOrders:
                for order in userOrders[orderCurrencyPair]:
                    if order[OrderAttributes.ID_ORDER] == id:
                        if attributes:
                            if ismassive(attributes):
                                return dictKeysRemove(order, [notAvaliableAttribute for notAvaliableAttribute in order.keys() if notAvaliableAttribute not in attributes])
                            else:
                                return order[attributes]
                        else:
                            return order
            return TBApiErrors.UNEXISTANCE_ORDER_ID
        else:
            if pair:
                if ismassive(pair):
                    userOrders = dictKeysRemove(userOrders, [notAvaliablePair for notAvaliablePair in userOrders.keys() if notAvaliablePair not in pair])
                else:
                    userOrders = dictKeysRemove(userOrders, [notAvaliablePair for notAvaliablePair in userOrders.keys() if notAvaliablePair != pair])
            if type:
                if ismassive(type):
                    for ordersCurrencyPair in userOrders.keys():
                        userOrders[ordersCurrencyPair] = [order for order in userOrders[ordersCurrencyPair] if order[OrderAttributes.TYPE] in type]
                else:
                    for ordersCurrencyPair in userOrders.keys():
                        userOrders[ordersCurrencyPair] = [order for order in userOrders[ordersCurrencyPair] if order[OrderAttributes.TYPE] == type]
            if attributes:
                if ismassive(attributes):
                    for ordersCurrencyPair in userOrders.keys():
                        userOrders[ordersCurrencyPair] = [dictKeysRemove(order, [notAvaliableAttributes for notAvaliableAttributes in order.keys() if notAvaliableAttributes not in attributes]) for order in userOrders[ordersCurrencyPair]]
                else:
                    for ordersCurrencyPair in userOrders.keys():
                        userOrders[ordersCurrencyPair] = [order[attributes] for order in userOrders[ordersCurrencyPair]]
        if pair and not ismassive(pair):
            userOrders = userOrders[pair]
        return userOrders

    def __isExistanceCurrency(self, currencys):
        """
        Проверяет, присутствует ли валюта в списке доступных валют на бирже Exmo.
        Замечание: может принимать на вход, как одну валюту для проверки, так и список валют.
        @param currencys валюта наличие которой необходимо проверить.
        @ return true - если валюта присутствует; false -.в противном случае.
        """
        if isinstance(currencys, str):
            return currencys in self.__avalibleCurrency
        elif ismassive(currencys):
            for currency in currencys:
                if currency not in self.__avalibleCurrency:
                    return False
            return True
        return False

    def __isExistancePairCurrency(self, pairs):
        """
        Проверяет, присутствует ли валютная пара в списке доступных для торговли пар на бирже Exmo.
        Замечание: может принимать на вход, как одну валютную пару для проверки, так и список валютных пар.
        @param pairs валютная пара доступность которой необходимо проверить.
        @return true - если пара присутствует; false - в противном случае.
        """
        if isinstance(pairs, str):
            return pairs in self.__avalibleCurrencyPair
        elif ismassive(pairs):
            for pair in pairs:
                if pair not in self.__avalibleCurrencyPair:
                    return False
            return True
        return False

    def __isAnoughtCurrencyValue(self, currency, value):
        """
        Проверяет, находится ли на аккаунте пользователя указанная валюта в достаточном количестве на бирже Exmo.
        @param currency имя валюты.
        @param value необходимое количество.
        @return true - если необходимое количество имеется; false - в противном случае.
        """
        return self.getCurrencyCountInAccess(currency) >= value

    def __checkOrderRequest(self, pair, quantity, price):
        """
        Проверяет возможность создания ордера на бирже Exmo, согласно основным ограниченим создания ордера.
        @param pair валютная пара создаваемого ордера.
        @param quantity количество валюты, которое необходимо задействовать в ордере.
        @param price цена за единицу валюты создаваемого ордера.
        @return
            (True, None) - в случае, если ордер может быть создан.
            (False, код_ошибки) - в противном случае.
        """
        tradeRestricted = self.getTradeRestricted(pair=pair)
        if not self.__isExistancePairCurrency(pair):
            return (False, TBApiErrors.UNEXISTANCE_CURRENCY_PAIR)
        if quantity < tradeRestricted[TradeRestricted.MIN_QUANTITY]:
            return (False, TBApiErrors.UNAVALIBLE_MIN_QUANTITY_FOR_ORDER)
        if quantity > tradeRestricted[TradeRestricted.MAX_QUANTITY]:
            return (False, TBApiErrors.UNAVALIBLE_MAX_QUANTITY_FOR_ORDER)
        if price < tradeRestricted[TradeRestricted.MIN_PRICE]:
            return (False, TBApiErrors.UNAVALIBLE_MIN_PRICE_FOR_ORDER)
        if price > tradeRestricted[TradeRestricted.MAX_PRICE]:
            return (False, TBApiErrors.UNAVALIBLE_MAX_PRICE_FOR_ORDER)
        if (quantity * price) < tradeRestricted[TradeRestricted.MIN_AMOUNT]:
            return (False, TBApiErrors.UNAVALIBLE_MIN_AMOUNT_FOR_ORDER)
        if (quantity * price) > tradeRestricted[TradeRestricted.MAX_AMOUNT]:
            return (False, TBApiErrors.UNAVALIBLE_MAX_AMOUNT_FOR_ORDER)
        return (True, None)
