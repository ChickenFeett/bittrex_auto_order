import copy
import math
import os
from utils import Utils
from configuration import LoggingModes


class OrderController:

    def __init__(self):
        pass

    # Removes any crypto orders that already has an open order
    def remove_duplicate_orders(self, pending_orders, open_orders):
        refined_orders = copy.copy(pending_orders)
        count = 1
        for holding_crypto in pending_orders:
            for order in open_orders:
                if holding_crypto.market == order.exchange:
                    Utils.log(str(count) + ". Open order already exists on " + order.exchange
                            + ".\tCancel this order if you want to renew it.", LoggingModes.INFO)
                    count = count + 1
                    refined_orders.remove(holding_crypto)
                    break
        return refined_orders

    # Removes any orders which the account currently does not have any balance for
    def remove_orders_with_no_balance(self, pending_orders, balances):
        refined_orders = copy.copy(pending_orders)
        count = 1
        for order in pending_orders:
            if "USDT" in order.market.upper():  # not processing any orders bought with USDT
                Utils.log(str(count) + ". Removing USDT order: " + order.market, LoggingModes.INFO)
                count = count + 1
                refined_orders.remove(order)
                continue

            crypto_exists_with_balance = False
            for balance in balances:
                if order.market.split('-')[1] == balance.currency:
                    crypto_exists_with_balance = True
            if not crypto_exists_with_balance:
                Utils.log(str(count) + ". Removing 0 balance crypto:" + order.market, LoggingModes.INFO)
                count = count + 1
                refined_orders.remove(order)
        return refined_orders

    def read_and_process_orders_ready_for_placing_sell_order(self, balances, open_orders):
        orders = Utils.process_orders_from_file()
        orders = self.remove_orders_with_no_balance(orders, balances)
        orders = self.remove_duplicate_orders(orders, open_orders)
        return orders

    def print_placed_order(self, r, order, high, url):
        print ("\n--------------------------------------------------------------------------------------------------"
               + "\nPlacing order on " + order.market
               + "\n\t-\tQuantity:................ " + Utils.float_to_str(
                    order.sell_quantity) + "\tof\t" + Utils.float_to_str(order.quantity)
               + "\n\t-\tSell Price:.............. " + Utils.float_to_str(order.sell_price)
               + "\n\t-\tReturn:.................. " + Utils.float_to_str(order.sell_price * order.quantity / 2)
               + "\n\t-\tCurrent Price:........... " + Utils.float_to_str(high)
               + "\n\t-\tCompletion Percentage:... " + str(round((high / order.sell_price) * 100, 2)) + "%"
               + "\n--------------------------------------------------------------------------------------------------")
        if "success" in r:
            if r['success'] or r['success'] == 'true':
                print ("                            ! ! ! ! !       SUCCESS         ! ! ! ! !                        ")
            elif 'message' in r and len(r['message']) != 0 and not str(r['message']).isspace():
                print ("                            * * * * *     F A I L E D !     ->  " + r['message'] + "         ")
            else:
                print (
                    "                            * * * * *     F A I L E D !     * * * * *                            ")
        else:
            print ("                            * * * * *     F A I L E D !     * * * * *                            ")
        print (
                    url + "\n--------------------------------------------------------------------------------------------------\n")

    @staticmethod
    def print_balance(index, balance):
        if balance is None:
            Utils.log("Could not print stats - failed to retrieve balance", LoggingModes.ERROR)
            return
        print ("\n--------------------------------------------------------------------------------------------------"
               + "\n"+str(index)+". Statistics of " + balance.currency
               + "\n\t-\tQuantity:................ " + Utils.float_to_str(balance.balance)
               + "\n\t-\tAvailable:............... " + Utils.float_to_str(balance.available)
               + "\n\t-\tPending:................. " + Utils.float_to_str(balance.pending)
               + "\n\t-\tAddress:................. " + str(balance.crypto_address)
               + "\n--------------------------------------------------------------------------------------------------")

    @staticmethod
    def print_order_stats(index, order, balance, market_summary):
        if order is None:
            Utils.log("Could not print stats - failed to retrieve order", LoggingModes.ERROR)
            return
        if balance is None:
            Utils.log("Could not print stats - failed to retrieve balance", LoggingModes.ERROR)
            return
        if market_summary is None:
            Utils.log("Could not retrieve market summary for " + order.market, LoggingModes.ERROR)
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            Utils.log("Could not retrieve high price for " + order.market, LoggingModes.ERROR)
            return
        print ("\n--------------------------------------------------------------------------------------------------"
               + "\n"+str(index)+". Statistics of " + order.market
               + "\n\t-\tQuantity:................ " + Utils.float_to_str(
                    order.sell_quantity) + "\tof\t" + Utils.float_to_str(balance.balance)
               + "\n\t-\tSell Price:.............. " + Utils.float_to_str(order.sell_price)
               + "\n\t-\tReturn:.................. " + Utils.float_to_str(
                    order.sell_price * order.quantity / 2)
               + "\n\t-\tCurrent Price:........... " + Utils.float_to_str(high)
               + "\n\t-\tCompletion Percentage:... " + str(round((high / order.sell_price) * 100, 2)) + "%"
               + "\n--------------------------------------------------------------------------------------------------")

    @staticmethod
    def print_open_order_stats(index, open_order, balance, market_summary):
        if open_order is None:
            Utils.log("Could not print stats - failed to retrieve order", LoggingModes.ERROR)
            return
        if balance is None:
            Utils.log("Could not print stats - failed to retrieve balance", LoggingModes.ERROR)
            return
        if market_summary is None:
            Utils.log("Could not retrieve market summary for " + open_order.exchange, LoggingModes.ERROR)
            return
        high = float(market_summary.high)
        if high is None or math.isnan(high) or high == 0:
            Utils.log("Could not retrieve high price for " + open_order.exchange, LoggingModes.ERROR)
            return
        print ("\n--------------------------------------------------------------------------------------------------"
               + "\n"+str(index)+". Statistics of " + open_order.exchange
               + "\n\t-\tQuantity Remaining:...... " + Utils.float_to_str(
                    open_order.quantity_remaining) + "\tof\t" + Utils.float_to_str(balance.balance)
               + "\n\t-\tSell Price:.............. " + Utils.float_to_str(open_order.limit)
               + "\n\t-\tCurrent Price:........... " + Utils.float_to_str(high)
               + "\n\t-\tReturn:.................. " + Utils.float_to_str(
                    open_order.limit * open_order.quantity_remaining / 2)
               + "\n\t-\tVolume:.................. " + Utils.float_to_str(market_summary.volume)
               + "\n\t-\tBase Volume:............. " + Utils.float_to_str(market_summary.base_volume)
               + "\n\t-\tCompletion Percentage:... " + str(round((high / open_order.limit) * 100, 2)) + "%"
               + "\n--------------------------------------------------------------------------------------------------")

    @staticmethod
    def prepare_output_file():
        filename = "temp_orders_to_be_confirmed.csv"
        folder = "output"
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(folder + "\\" + filename, 'w') as f:
            f.write("Exchange,Available Quantity,Sell Quantity,Sell Price,Return,Current Price,Completion Percentage")
        return filename

    @staticmethod
    def append_to_output_file(filename, order, balance, market_summary):
        high = None
        current_price = "unknown"
        market = "unknown"
        available_quantity = "unknown"
        sell_quantity = "unknown"
        sell_price = "unknown"
        return_price = "unknown"
        completion_percent = "unknown"
        if order is not None:
            market = order.market
            sell_quantity = Utils.float_to_str(order.sell_quantity)
            sell_price = Utils.float_to_str(order.sell_price)
            return_price = Utils.float_to_str(order.sell_price * order.quantity / 2)
        if balance is not None:
            available_quantity = Utils.float_to_str(balance.balance)
        if market_summary is not None:
            high = float(market_summary.high)
            current_price = Utils.float_to_str(high)
        if high is None or high == 1:
            current_price = "unknown"
        elif order is not None:
            completion_percent = str(round((high / order.sell_price) * 100, 2))
        with open("output\\" + filename, 'a') as f:
            f.write("\n"+market+","
                    + available_quantity+","
                    + sell_quantity+","
                    + sell_price+","
                    + return_price+","
                    + current_price+","
                    + completion_percent)
