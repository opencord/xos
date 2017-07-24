from header import *

from service_header import *

from core.models.service import Service

from monitoringpublisher_decl import MonitoringPublisher_decl


class MonitoringPublisher(MonitoringPublisher_decl):
    class Meta:
        app_label = "monitoring"
        proxy = True

    KIND = CEILOMETER_PUBLISH_TENANT_KIND

    default_attributes = {}
    def __init__(self, *args, **kwargs):
        ceilometer_services = CeilometerService.get_service_objects().all()
        if ceilometer_services:
            self._meta.get_field("provider_service").default = ceilometer_services[0].id
        super(MonitoringPublisher, self).__init__(*args, **kwargs)

    def can_update(self, user):
        #Allow creation of this model instances for non-admin users also
        return True

    @property
    def creator(self):
        from core.models import User
        if getattr(self, "cached_creator", None):
            return self.cached_creator
        creator_id=self.get_attribute("creator_id")
        if not creator_id:
            return None
        users=User.objects.filter(id=creator_id)
        if not users:
            return None
        user=users[0]
        self.cached_creator = users[0]
        return user

    @creator.setter
    def creator(self, value):
        if value:
            value = value.id
        if (value != self.get_attribute("creator_id", None)):
            self.cached_creator=None
        self.set_attribute("creator_id", value)

