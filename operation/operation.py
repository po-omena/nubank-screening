BUY_TYPE = 'buy'
NO_TAX_OPERATION = {"tax": 0.00}
SELL_TYPE = 'sell'


class OperationHandler:
    """
    This handler class is used to go through a list of operations and execute functions based on operation type.
    It stores the net loss to be used for tax deductions as well as the tax to be payed by each of them.
    """

    def __init__(self, operation_list):
        """
        Init method for the class, it creates some key variables to be used later on
        :param operation_list: a list of operations ordered in a sequential manner
        :type operation_list: list[dict]
        """
        self._operations = operation_list
        self.average_stock_value = 0
        self.quantity = 0
        self.tax = []
        self.net_loss = 0

    def calculate_operations(self):
        """
        Loop through the list of operations initially given, determines if it's a buy or a sell operation
        and run the calculation according to it's type
        TODO: TEST
        """
        for operation in self._operations:
            if self.is_buy(operation):
                self._calculate_buy(operation)

            elif self.is_sell(operation):
                self._calculate_sell(operation)

    def _calculate_buy(self, buy_operation):
        """
        Gets as an input a buy operation and updates the class values accordingly, tax for buy operations is always 0.
        :param buy_operation: A buy operation
        :type buy_operation: dict
        """
        self.average_stock_value = self._calculate_average_stock_value(buy_operation)
        self.quantity += int(buy_operation.get('quantity'))
        self.tax.append(NO_TAX_OPERATION)

    def _calculate_sell(self, sell_operation):
        """
        This functions calculates sell operations, for this exercise I'm locking short
        selling so it is not allowed to sell more stocks than you currently own and
        the system would return an Exception. This is not set in stone and would in real life
        be discussed with the management and CS team to match
        more closely what the bank is trying to develop at the moment
        :param sell_operation: A sell operation
        :type sell_operation: dict
        """
        units = int(sell_operation.get('quantity'))
        total_value = units * sell_operation.get('unit-cost')
        tax = NO_TAX_OPERATION

        if units > self.quantity:
            raise ValueError('Quantity to be sold is higher than currently available in this wallet')

        self.quantity -= units
        loss_or_profit = self._get_net_loss_or_profit(sell_operation)

        # If the sell price is less then the current average this is a loss operation and we should record the value
        # and return the function as there is no need to calculate tax in a loss operation
        if loss_or_profit < 0:
            self.net_loss += loss_or_profit
            return
        # If the total value of the operation is more than 20000 then the tax should be calculated
        if total_value > 20000:
            tax = self._get_operation_tax(self._get_taxable_amount(loss_or_profit))
        self.tax.append(tax)

    def _get_taxable_amount(self, profit):
        """TODO DOCSTRING"""

        result = self.net_loss + profit
        # Updating the net loss value, the if covers the case when the net loss is higher than the current profit
        # for this operation so we keep the remaining balance, on other cases we use all the accumulated loss and set
        # it again to 0
        self.net_loss = self.net_loss + profit if self.net_loss + profit <= 0 else 0
        if result < 0:
            return 0
        return result

    def _get_net_loss_or_profit(self, sell_operation):
        """TODO DOCSTRING"""
        return (sell_operation.get('unit-cost') - self.average_stock_value) * sell_operation.get('quantity')

    def _get_operation_tax(self, profit):
        """TODO DOCSTRING"""
        return {'tax': profit * 0.2}

    def _calculate_average_stock_value(self, operation):
        """
        Given a buy operation as input, updates the average stock value using a weighted average of the
        newly purchased stocks and the ones already accounted for
        :param operation: A buy operation
        :type operation: dict
        :return: returns the new weighted average stock value
        :rtype: float
        """
        if self.average_stock_value == 0:
            return operation.get('unit-cost')
        return ((self.quantity * self.average_stock_value) +
                (operation.get('quantity') * operation.get('unit-cost'))) / (self.quantity + operation.get('quantity'))

    @staticmethod
    def is_buy(operation):
        """TODO: DOCSTRING AND TEST"""
        if operation.get('operation', None) == BUY_TYPE:
            return True

    @staticmethod
    def is_sell(operation):
        """TODO: DOCSTRING AND TEST"""
        if operation.get('operation', None) == SELL_TYPE:
            return True
