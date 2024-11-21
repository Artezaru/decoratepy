from decoratepy import TimerCounterLogger

# Création du décorateur
timer = TimerCounterLogger()

@timer
def ma_fonction(x, y):
    return x * y

@timer
def ma_fonction2(x, y):
    return x * y

@timer
def ma_fonction3(x, y):
    return x * y

@timer
def ma_fonction4(x, y):
    return x * y


# Appel d'une méthode
ma_fonction(1,2)

timer.initialize()

for k in range(10000):
    ma_fonction2(1,2)

timer.set_deactivated()

ma_fonction3(1,2)

timer.set_activated()

ma_fonction4(1,2)
print(timer.__help__)
print(timer)
