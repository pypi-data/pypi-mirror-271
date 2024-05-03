from enum import Enum


class OrderStatus(Enum):
    Pending = 'Pending'
    Unshipped = 'Unshipped'
    PartiallyShipped = 'PartiallyShipped'
    Shipped = 'Shipped'
    Canceled = 'Canceled'
    Unfulfillable = 'Unfulfillable'
    InvoiceUnconfirmed = 'InvoiceUnconfirmed'
    PendingAvailability = 'PendingAvailability'

def validate_order_status(status: str) -> bool:
    # a function to validate order status
    return status in OrderStatus.__members__.keys()

if __name__ == '__main__':
    print(OrderStatus.Pending)
    print(OrderStatus.Pending.value)
    print(validate_order_status('Pending'))
    print(validate_order_status('Pending1'))
    print(OrderStatus.__members__.keys())
    print(OrderStatus.__members__.values())
    print(OrderStatus.__members__.items())
