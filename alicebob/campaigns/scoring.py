class EmailEventScore:
    OPEN = 0.3
    CLICK = 1.5
    COMPLAINT = -3.0
    HARD_BOUNCE = -2.5
    SOFT_BOUNCE = -1.0
    UNSUBSCRIBE = -1.5
    DELIVERED = 0.1
