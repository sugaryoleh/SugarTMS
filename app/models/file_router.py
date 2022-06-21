def route(instance, filename):
    folder = ''
    from app.models.driver.driverfile import DriverFile
    from app.models.unit.truckfile import TruckFile
    from app.models.unit.trailerfile import TrailerFile
    from app.models.load.loadfile import LoadFile
    if instance.__class__ == DriverFile:
        folder = 'drivers/{}/'.format(instance.driver.id)
    elif instance.__class__ == TruckFile:
        folder = 'trucks/{}/'.format(instance.truck.id)
    elif instance.__class__ == TrailerFile:
        folder = 'trailers/{}/'.format(instance.trailer.id)
    elif instance.__class__ == LoadFile:
        folder = 'loads/{}/'.format(instance.load.id)
    path = 'files/{}/{}'.format(folder, filename)
    return path