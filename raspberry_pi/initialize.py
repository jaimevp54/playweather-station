from .sensors import CO, DHT22, lluvia, viento
from threading import Thread

import time


#
# def f1(data_collector):
#     print('running f1')
#     for i in range(10):
#         print("guarde - f1" + str(i))
#         time.sleep(1)
#         data_collector['f1_' + str(i)] = "f1" + str(i)
#
#
# def f2(data_collector):
#     print('running f2')
#     for i in range(10):
#         print("guarde - f2" + str(i))
#         time.sleep(2)
#         data_collector['f2_' + str(i)] = "f2" + str(i)
#

def initialize(*sensor_initializers):
    lectura = {}
    threads = {}
    for initializer in sensor_initializers:
        threads[initializer.__name__] = Thread(target=initializer, args=(lectura,))
        threads[initializer.__name__].start()

    while (True):
        time.sleep(5)
        print("\n\n\n*********")
        print("acumulado")
        for l in lectura:
            print(l, lectura[l])
        lectura.clear()
        print("*********\n\n\n")


initialize(
    CO.run,
    DHT22.run,
    lluvia.run,
    viento.run
)
