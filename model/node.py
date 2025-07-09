from dataclasses import dataclass

@dataclass
class Node():
    product_number: int
    ricavoTot: float

    def __hash__(self):
        return hash(self.product_number)

    def __eq__(self, other):
        return self.product_number == other.product_number

    def __str__(self):
        return f"Product: {self.product_number} - ricavo totale: {self.ricavoTot}"