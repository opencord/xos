from django.db import models
from core.models import PlCoreBase


class NetworkDevice(PlCoreBase):

    ADMINISTRATIVE_STATE = (
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
        ('syncrequested', 'SyncRequested'),
        ('syncinprogress', 'SyncInProgress')
    )

    AUTH_TYPE = (
        ('basic', 'Basic'),
        ('key', 'Key'),
        ('oauth', 'OAuth')
    )

    # Leaving out the attributes below for now - not clear we will need them
    # type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=False)
    # manufacturer = models.CharField(unique=False, verbose_name="Manufacturer", max_length=256, editable=False)
    # serialNumber = models.CharField(unique=True, verbose_name="Serial Number", max_length=256, editable=False)
    # chassisId = models.CharField(unique=False, verbose_name="Chassis ID", max_length=256, editable=False)

    restCtrlUrl = models.CharField(unique=True,
                               verbose_name="RestCtrlURL",
                               max_length=256,
                               editable=True)
    authType = models.CharField(choices=AUTH_TYPE, verbose_name='Auth Type', max_length=16, editable=True)
    username = models.CharField(verbose_name='Username', max_length=32, editable=True, blank=True)
    password = models.CharField(max_length=32, verbose_name='Password', editable=True, blank=True)
    administrativeState = models.CharField(choices=ADMINISTRATIVE_STATE,
                                           default='disabled',
                                           verbose_name="AdministrativeState",
                                           max_length=16,
                                           editable=True)
    id = models.CharField(unique=True,
                          verbose_name="Element Id",
                          primary_key=True,
                          max_length=256,
                          editable=True)

    def __init__(self, *args, **kwargs):
        super(NetworkDevice, self).__init__(*args, **kwargs)

class NetworkPort(PlCoreBase):

    element = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE)
    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    pid = models.CharField(unique=True, verbose_name="Port ID", max_length=256, editable=False)

    def __init__(self, *args, **kwargs):
        super(NetworkPort, self).__init__(*args, **kwargs)

class NetworkEdgePort(PlCoreBase):

    element = models.ForeignKey(NetworkDevice, on_delete=models.CASCADE)
    id = models.AutoField(verbose_name="id", primary_key=True, editable=False)
    pid = models.CharField(unique=True, verbose_name="Port ID", max_length=256, editable=False)
    bwpCfgCbs = models.IntegerField(verbose_name="Committed Burst Size", editable=False, blank=True)
    bwpCfgEbs = models.IntegerField(verbose_name="Excess Burst Size", editable=False, blank=True)
    bwpCfgCir = models.IntegerField(verbose_name="Committed Information Rate", editable=False, blank=True)
    bwpCfgEir = models.IntegerField(verbose_name="Excess Information Rate", editable=False, blank=True)
    name = models.CharField(verbose_name="Name", max_length=256, editable=True, blank=True)
    location = models.CharField(verbose_name="Location", max_length=256, editable=True, blank=True)
    latlng = models.CharField(verbose_name="Latitude/Longitude", max_length=50, editable=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(NetworkEdgePort, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.latlng:
            try:
                latlng_value = getattr(self, 'latlng').strip()
                if (latlng_value.startswith('[') and latlng_value.endswith(']') and latlng_value.index(',') > 0):
                    lat = latlng_value[1: latlng_value.index(',')].strip()
                    lng = latlng_value[latlng_value.index(',') + 1: len(latlng_value) - 1].strip()

                    #If lat and lng are not floats, the code below should result in an error.
                    lat_validation = float(lat)
                    lng_validation = float(lng)
                else:
                    raise ValueError("The lat/lng value is not formatted correctly.")
            except:
                raise ValueError("The lat/lng value is not formatted correctly.")

        super(NetworkEdgePort, self).save(*args, **kwargs)

class NetworkPointToPointConnection(PlCoreBase):

    TYPE = (
        ('direct', 'Direct'),
        ('indirect', 'Indirect'),
        ('edge', 'Edge'),
        ('tunnel', 'Tunnel'),
        ('optical', 'Optical'),
        ('virtual', 'Virtual'),
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVESTATE = (
        ('disabled', 'Disabled'),
        ('activationrequested', 'ActivationRequested'),
        ('enabled', 'Enabled'),
        ('invalid', 'Invalid'),
        ('deactivationrequested', 'DeactivationRequested')
    )

    id = models.AutoField(verbose_name="PointToPointConnectionId",
                          primary_key=True,
                          editable=False)


    sid = models.CharField(unique=True, verbose_name="Service ID", max_length=256, editable=True)
    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=False)
    src = models.ForeignKey(NetworkPort,
                            related_name='PointToPointSrc',
                            verbose_name="Source",
                            editable=False,
                            on_delete=models.CASCADE)
    dest = models.ForeignKey(NetworkPort,
                             related_name='PointToPointDst',
                             verbose_name="Destination",
                             editable=False,
                             on_delete=models.CASCADE)
    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256, editable=False)
    adminstate = models.CharField(choices=ADMINISTRATIVESTATE, verbose_name="AdministrativeState", max_length=256, editable=True)


    def __init__(self, *args, **kwargs):
        super(NetworkPointToPointConnection, self).__init__(*args, **kwargs)

class NetworkEdgeToEdgePointConnection(PlCoreBase):

    TYPE = (
        ('direct', 'Direct'),
        ('tunnel', 'Tunnel'),
        ('optical', 'Optical'),
        ('virtual', 'Virtual'),
        ('Point_To_Point', 'Point To Point')
    )

    OPERATIONALSTATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    ADMINISTRATIVESTATE = (
        ('disabled', 'Disabled'),
        ('activationrequested', 'ActivationRequested'),
        ('enabled', 'Enabled'),
        ('invalid', 'Invalid'),
        ('deactivationrequested', 'DeactivationRequested')
    )

    id = models.AutoField(verbose_name="EdgePointToEdgePointConnectivityId",
                          primary_key=True,
                          editable=False)
    sid = models.CharField(unique=True, verbose_name="Service ID", max_length=256, editable=True)
    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=True)
    uni1 = models.ForeignKey(NetworkEdgePort,
                            related_name='EdgePointToEdgePointSrc',
                            verbose_name="UNI 1",
                            editable=True,
                            on_delete=models.CASCADE)
    uni2 = models.ForeignKey(NetworkEdgePort,
                             related_name='EdgePointToEdgePointDst',
                             verbose_name="UNI 2",
                             editable=True,
                             on_delete=models.CASCADE)
    operstate = models.CharField(choices=OPERATIONALSTATE, verbose_name="OperationalState", max_length=256, editable=True)
    adminstate = models.CharField(choices=ADMINISTRATIVESTATE, verbose_name="AdministrativeState", max_length=256, editable=True)


    def __init__(self, *args, **kwargs):
        super(NetworkEdgeToEdgePointConnection, self).__init__(*args, **kwargs)


class NetworkMultipointConnection(PlCoreBase):

    TYPE = (
        ('vlan', 'VLAN'),
        ('ip', 'IP'),
        ('ethernet', 'Ethernet'),
    )

    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    type = models.CharField(choices=TYPE, verbose_name="Type", max_length=256, editable=False)
    eps = models.ManyToManyField(NetworkPort,
                                 related_name='eps',
                                 verbose_name="Endpoints",
                                 editable=False)
    state = models.CharField(choices=STATE, verbose_name="State", max_length=256, editable=False)

    def __init__(self, *args, **kwargs):
        super(NetworkMultipointConnection, self).__init__(*args, **kwargs)

class NetworkInterLink(PlCoreBase):

    DISCOVERY = (
        ('auto', 'Automatic Discovery'),
        ('manual', 'Manual Discovery'),
    )

    STATE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    src = models.ForeignKey(NetworkPort,
                            related_name='InterLinkSrc',
                            verbose_name="Source",
                            editable=False,
                            on_delete=models.CASCADE)
    dest = models.ForeignKey(NetworkPort,
                             related_name='InterLinkDst',
                             verbose_name="Destination",
                             editable=False,
                             on_delete=models.CASCADE)
    state = models.CharField(choices=STATE, verbose_name="State", max_length=256, editable=False)
    discovery = models.CharField(choices=STATE, verbose_name="State", max_length=256, editable=False)

    def __init__(self, *args, **kwargs):
        super(NetworkInterLink, self).__init__(*args, **kwargs)