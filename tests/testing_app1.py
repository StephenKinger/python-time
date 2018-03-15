import time
from measure_time import measure_time
import random

class TestHello(object):
    def __init__(self):
        self.x = 0
        time.sleep(0.3)

    @measure_time()
    def test_hello_m1(self):
        r = random.randint(1,10)
        time.sleep(r/10.0)

    def test_hello_m2(self):
            time.sleep(0.1)


if __name__ == "__main__":
    test = TestHello()
    for ii in range(0,200):
        test.test_hello_m1()


