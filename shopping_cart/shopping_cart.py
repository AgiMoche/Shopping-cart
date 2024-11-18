STATUS_DELIVERED = "DELIVERED"
STATUS_OPEN = "OPEN"
STATUS_PAID = "PAID"


def get_customer_baskets(email, shopping_baskets):
    return [
        customer_basket
        for customer_basket in shopping_baskets
        if customer_basket["email"] == email
    ]


def get_all_customers(shopping_baskets):
    customer_emails = [customer_basket["email"] for customer_basket in shopping_baskets]

    return sorted(set(customer_emails))


def get_required_stock(shopping_baskets):
    items_pending_delivery = [
        (item["name"], item["quantity"])
        for basket in shopping_baskets
        for item in basket["items"]
        if basket["status"] == STATUS_PAID
    ]

    items_to_ship = []

    for item_name in set(item_name for item_name, _ in items_pending_delivery):
        item_totals_dictionary = {"name": item_name, "quantity": 0}

        for item_in_open_basket, item_quantity in items_pending_delivery:
            if item_in_open_basket == item_name:
                item_totals_dictionary["quantity"] += item_quantity

        items_to_ship.append(item_totals_dictionary)

    return items_to_ship


def get_total_spent(email, shopping_baskets):
    total_spent = 0

    for basket in get_customer_baskets(email, shopping_baskets):
        for item in basket["items"]:
            if basket["status"] == STATUS_PAID or basket["status"] == STATUS_DELIVERED:
                total_spent += item["quantity"] * item["price"]

    return total_spent


def get_top_customers(shopping_baskets):
    customers_total_spending = [
        {
            "email": customer_email,
            "total": get_total_spent(customer_email, shopping_baskets),
        }
        for customer_email in get_all_customers(shopping_baskets)
    ]

    return sorted(
        customers_total_spending,
        key=lambda spending_totals: spending_totals["total"],
        reverse=True,
    )


def get_customers_with_open_baskets(shopping_baskets):
    customers_with_open_baskets = [
        basket["email"]
        for basket in shopping_baskets
        if basket["status"] == STATUS_OPEN
    ]

    return sorted(set(customers_with_open_baskets))
