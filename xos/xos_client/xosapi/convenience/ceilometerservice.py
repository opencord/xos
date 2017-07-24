from core.models.plcorebase import *


from django.db import models

from django.core.validators import URLValidator

from core.models import Service, PlCoreBase, Slice, Instance, Tenant, TenantWithContainer, Node, Image, User, Flavor, ServiceDependency, ServiceMonitoringAgentInfo

from core.models.plcorebase import StrippedCharField

import os

from django.db import models, transaction

from django.forms.models import model_to_dict

from django.db.models import Q

from operator import itemgetter, attrgetter, methodcaller

import traceback

from xos.exceptions import *

from core.models import SlicePrivilege, SitePrivilege

from sets import Set

from urlparse import urlparse



from xosapi.orm import ORMWrapper, register_convenience_wrapper





class ORMWrapperCeilometerService(ORMWrapper):



    LOOK_FOR_IMAGES=[ "ceilometer-service-trusty-server-multi-nic",

                    ]



    sync_attributes = ("private_ip", "private_mac",

                       "nat_ip", "nat_mac", "ceilometer_enable_pub_sub")



    def get_instance(self):

        for slice in self.slices.all():

             for instance in slice.instances.all():

                 if instance.image.name in self.LOOK_FOR_IMAGES:

                     return instance

        return None



    @property

    def addresses(self):

        if (not self.id) or (not self.get_instance()):

            return {}



        addresses = {}

        for ns in self.get_instance().ports.all():

            if "private" in ns.network.name.lower():

                addresses["private"] = (ns.ip, ns.mac)

            elif ("nat" in ns.network.name.lower()) or ("management" in ns.network.name.lower()):

                addresses["nat"] = (ns.ip, ns.mac)

            #TODO: Do we need this client_access_network. Revisit in VTN context

            #elif "ceilometer_client_access" in ns.network.labels.lower():

            #    addresses["ceilometer"] = (ns.ip, ns.mac)

        return addresses



    @property

    def nat_ip(self):

        return self.addresses.get("nat", (None, None))[0]



    @property

    def nat_mac(self):

        return self.addresses.get("nat", (None, None))[1]



    @property

    def private_ip(self):

        return self.addresses.get("private", (None, None))[0]



    @property

    def private_mac(self):

        return self.addresses.get("private", (None, None))[1]



    def get_controller(self):

        if not self.slices.count:

            raise XOSConfigurationError("The service has no slices")

        cslice = self.slices.all()[0].controllerslices.all()[0]

        controller = cslice.controller

        if not controller:

            raise XOSConfigurationError("The service slice has no controller")

        return controller



    @property

    def ceilometer_pub_sub_url(self):

        if not self.get_instance():

            return self.get_attribute("ceilometer_pub_sub_url", None)

        if not self.private_ip:

            return None

        return "http://" + self.private_ip + ":4455/"



    @ceilometer_pub_sub_url.setter

    def ceilometer_pub_sub_url(self, value):

        self.set_attribute("ceilometer_pub_sub_url", value)



    @property

    def ceilometer_enable_pub_sub(self):

        return self.get_attribute("ceilometer_enable_pub_sub", False)



    @ceilometer_enable_pub_sub.setter

    def ceilometer_enable_pub_sub(self, value):

        self.set_attribute("ceilometer_enable_pub_sub", value)



    @property

    def ceilometer_auth_url(self):

        #FIXME: Crude way to determine if monitoring service is getting deployed with its own ceilometer+keystone 

        if not self.get_instance():

            return self.get_controller().auth_url

        if not self.private_ip:

            return None

        return "http://" + self.private_ip + ":5000/v2.0"



    @property

    def ceilometer_admin_user(self):

        if not self.get_instance():

            return self.get_controller().admin_user

        return 'admin'



    @property

    def ceilometer_admin_password(self):

        if not self.get_instance():

            return self.get_controller().admin_password

        return 'password'



    @property

    def ceilometer_admin_tenant(self):

        if not self.get_instance():

            return self.get_controller().admin_tenant

        return 'admin'



    @property

    def ceilometer_rabbit_compute_node(self):

        if not self.get_instance():

            return None

        return self.get_instance().node.name



    @property

    def ceilometer_rabbit_host(self):

        if not self.get_instance():

            return None

        return self.nat_ip



    @property

    def ceilometer_rabbit_user(self):

        if not self.get_instance():

            return None

        return 'openstack'



    @property

    def ceilometer_rabbit_password(self):

        if not self.get_instance():

            return None

        return 'password'



    @property

    def ceilometer_rabbit_uri(self):

        if not self.get_instance():

            return None

        if not self.private_ip:

            return None

        return 'rabbit://openstack:password@' + self.private_ip + ':5672'



    @property

    def kafka_url(self):

        if not self.get_instance():

            return None

        if not self.private_ip:

            return None

        return 'kafka://' + self.private_ip + ':9092'



    def delete(self, *args, **kwargs):

        instance = self.get_instance()

        if instance:

            instance.delete()

        super(CeilometerService, self).delete(*args, **kwargs)

		
    register_convenience_wrapper("CeilometerService", ORMWrapperCeilometerService)




