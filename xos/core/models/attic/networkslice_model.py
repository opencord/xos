class Meta:
    unique_together = ('network', 'controller')

def tologdict(self):
    from core.models.controllernetwork import ControllerNetwork
    d=super(ControllerNetwork,self).tologdict()
    try:
        d['network_name']=self.network.name
        d['controller_name']=self.controller.name
    except:
        pass
    return d

@staticmethod
def select_by_user(user):
    from core.models.controllernetwork import ControllerNetwork
    if user.is_admin:
        qs = ControllerNetwork.objects.all()
    else:
        slices = Slice.select_by_user(user)
        networks = Network.objects.filter(owner__in=slices)
        qs = ControllerNetwork.objects.filter(network__in=networks)
    return qs

