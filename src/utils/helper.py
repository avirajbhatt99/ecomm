class Helper:
    """
    class for helper functions
    """

    @staticmethod
    def calculate_total_amount(items):
        """
        calculate total amount for cart items
        """
        return sum(item["price"] * item["quantity"] for item in items)

    @staticmethod
    def get_items_purchased_count(orders):
        """
        get item wise count for all orders
        """
        return sum(
            item["quantity"]
            for user_orders in orders.values()
            for order in user_orders
            for item in order["items"]
        )

    @staticmethod
    def get_total_amount(orders):
        """
        get total amount for all orders
        """
        return sum(
            order["total_amount"]
            for user_orders in orders.values()
            for order in user_orders
        )

    @staticmethod
    def get_discount_amount(orders):
        """
        get total discount amount for all orders
        """
        return sum(
            order["discount_applied"]
            for user_orders in orders.values()
            for order in user_orders
        )

    @staticmethod
    def get_discount_codes(discount_codes):
        """
        get list of all discount codes
        """
        return [discount_code["code"] for discount_code in discount_codes.values()]
