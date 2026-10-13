def f(*args, **kwargs):
    print("Positional: ", kwargs)


f(galleons=100, sickles=50, knuts=25)