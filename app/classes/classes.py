
from typing import List


class Bank:
    def __init__(self, name):
        self.name = name
        self.clients: List[Client] = []
        self.credits: List[Credit] = []

    def statistics(self):
        return {
            "bank_name": self.name,
            "total_clients": len(self.clients),
            "total_credits": len(self.credits)
            }

class Client:
    def __init__(self, name, age, client_id):
        self.name = name
        self.age = age
        self.client_id = client_id


class Credit:
    def __init__(self, credit_id, client_id, size, term, annual_rate):
        self.credit_id = credit_id
        self.client_id = client_id
        self.size = size
        self.term = term
        self.annual_rate = annual_rate
        self.monthly_payment=self.get_payment()


    def get_payment(self):
        monthly_rate = self.annual_rate / 100 / 12
        payment = (self.size * monthly_rate * (1 + monthly_rate) ** self.term) / ((1 + monthly_rate) ** self.term - 1)
        return round(payment, 2)


    @staticmethod
    def amortize(size, annual_rate, term):
        schedule = []
        monthly_rate = annual_rate / 1200  # Месячная процентная ставка
        monthly_payment = (size * monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
        remaining_principal = size  # Отдельная переменная для остатка долга

        for month in range(1, term + 1):
            interest = remaining_principal * monthly_rate
            principal = monthly_payment - interest

            # Корректировка последнего платежа
            if month == term:
                principal = remaining_principal
                monthly_payment = principal + interest

            remaining_principal -= principal

            schedule.append({
                "month": month,  # Номер текущего месяца
                "payment": round(monthly_payment, 2),
                "principal": round(principal, 2),
                "interest": round(interest, 2),
                "remaining_balance": round(remaining_principal, 2)
            })

        return schedule