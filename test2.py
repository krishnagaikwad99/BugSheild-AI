
def calculate_total(price, quantity):
    if quantity > 0:
        return price * quantity
    return 0

for i in range(3):
    print(i)

print(calculate_total(100, 2))
