import numpy as np

fenzi = 0
fenmu = 0

# CONSTANT
IDLE = 0
SENDING = 1
WAITING = 3


class Wire():
    state = IDLE
    to_wait = 0

    def update(self):
        if self.state == SENDING:
            self.send()

    def is_busy(self):
        return self.state == SENDING

    def send(self):
        self.to_wait -= 1
        if self.to_wait == 0:
            self.state = IDLE

    def occupy(self):
        self.state = SENDING
        self.to_wait = t0 + tau

        global fenzi
        global fenmu
        fenzi += t0
        fenmu += t0 + tau


class Proxy():
    state = IDLE
    send_queue = 0
    to_wait = 0
    k = 0

    def __init__(self, wire):
        self.wire = wire

    def update(self):
        # generate dataframe all time
        self.send_by_prob()

        if self.state == SENDING:
            self.send()

        elif self.state == WAITING:
            self.wait()

    def send_by_prob(self):
        if np.random.random() > p:
            return
        self.state = SENDING
        self.send_queue += 1

    def send(self):
        if self.send_queue == 0:
            self.state = IDLE
            return

        if self.wire.is_busy():
            self.k += 1
            t = int(2 * tau * self.get_random_k(min(self.k, k)))
            global fenmu
            fenmu += t
            # print(t)
            self.set_wait(t)
            return

        self.k = 0  # clear
        self.send_queue -= 1
        self.set_wait(t0 + tau)
        self.wire.occupy()

    def get_random_k(self, k):
        end = int(pow(2, k))
        return np.random.randint(end)  # [0,end)

    def set_wait(self, time):
        self.to_wait = time
        self.state = WAITING

    def wait(self):
        self.to_wait -= 1
        if self.to_wait == 0:
            self.state = SENDING


def ces_once():
    global fenzi
    global fenmu
    fenzi = 0
    fenmu = 0

    wire = Wire()
    proxys = []
    for i in range(n):
        proxys.append(Proxy(wire))

    for step in range(100000):
        wire.update()
        for proxy in proxys:
            proxy.update()
        # if step % 1000 == 0:
        #     print(step, wire.all_time,)

    if fenmu == 0:
        return 1.0
    return round(fenzi / fenmu, 2)

def ces():
    global tau
    global p
    global t0
    global n
    global k

    tau = 3
    p = 1e-4
    t0 = 100
    n = 10
    k = 10

    print('=' * 10)
    print('tau =', tau, 'us')
    print('bernoulli p =', p, '/us', ' === ', p * 1e6, '/sec')
    print('t0 =', t0, 'us')
    print('host =', n)
    print('k =', k)
    print('=' * 10)

    # acc = 0
    # for i in range(1001):
    #     t = ces_once()
    #     print(t)
    #     acc += t
    #     if (i + 1) in [1, 10, 50, 100, 200, 500, 1000]:
    #         print(i + 1, acc / (i + 1))


    # for i in [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
    #     n = i
    #     acc = 0
    #     for _ in range(10):
    #         acc += ces_once()
    #     print(i, acc / 10)

    # for i in [10, 50, 60, 80, 100, 200, 300, 500, 1000]:
    #     t0 = i
    #     acc = 0
    #     for _ in range(10):
    #         acc += ces_once()
    #     print(i, acc / 10)

    for i in [0, 1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 100]:
        tau = i
        acc = 0
        for _ in range(10):
            acc += ces_once()
        print(i, acc / 10)

if __name__ == '__main__':
    ces()
