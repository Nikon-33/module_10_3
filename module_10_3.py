import random
from threading import Lock, Thread
from time import sleep


class Bank:
    def __init__(self):
        self.balance = 0
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            x = random.randint(50, 500)
            self.balance += x
            sleep(0.001)
            print(f'Пополнение: {x}\n Баланс: {self.balance}')
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()

    def take(self):
        for i in range(100):
            y = random.randint(50, 500)
            print(f'Запрос на {y}')
            if self.balance >= y:
                self.balance -= y
                print(f'Снятие: {y}. Баланс: {self.balance}')
                sleep(0.001)
            if self.balance < y:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()


T_bank = Bank()

t1 = Thread(target=Bank.deposit, args=(T_bank,))
t2 = Thread(target=Bank.take, args=(T_bank,))

t1.start()
t2.start()

t1.join()
t2.join()

print(f'Итоговый баланс: {T_bank.balance}')
