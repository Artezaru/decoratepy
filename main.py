from decoratepy import Timer

# Création du décorateur
timer = Timer()

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
print(ma_fonction(1,2))

timer.initialize()

print(ma_fonction2(1,2))

timer.set_deactivated()

print(ma_fonction3(1,2))

timer.set_activated()

print(ma_fonction4(1,2))






print(timer)
