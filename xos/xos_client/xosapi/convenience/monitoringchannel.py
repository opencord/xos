from xosapi.orm import ORMWrapper, register_convenience_wrapper

class ORMWrapperMonitoringChannel(ORMWrapper):





    sync_attributes = ("private_ip", "private_mac",

                       "ceilometer_ip", "ceilometer_mac",

                       "nat_ip", "nat_mac", "ceilometer_port",)





#    def save(self, *args, **kwargs):

#        if not self.creator:

#            if not getattr(self, "caller", None):

#                # caller must be set when creating a monitoring channel since it creates a slice

#                raise XOSProgrammingError("MonitoringChannel's self.caller was not set")

#            self.creator = self.caller

#            if not self.creator:

#                raise XOSProgrammingError("MonitoringChannel's self.creator was not set")

#

#        if self.pk is None:

#            #Allow only one monitoring channel per user

#            channel_count = sum ( [1 for channel in MonitoringChannel.get_tenant_objects().all() if (channel.creator == self.creator)] )

#            if channel_count > 0:

#                raise XOSValidationError("Already %s channels exist for user Can only create max 1 MonitoringChannel instance per user" % str(channel_count))

#

#        super(MonitoringChannel, self).save(*args, **kwargs)

#        model_policy_monitoring_channel(self.pk)





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



    @property

    def ceilometer_ip(self):

        return self.addresses.get("ceilometer", (None, None))[0]



    @property

    def ceilometer_mac(self):

        return self.addresses.get("ceilometer", (None, None))[1]





    @property

    def tenant_list(self):

        return self.slice_tenant_list | self.site_tenant_list



    @property

    def ceilometer_port(self):

        # TODO: Find a better logic to choose unique ceilometer port number for each instance 

        if not self.id:

            return None

        return 8888+self.id



    @property

    def ssh_proxy_tunnel(self):

        return self.get_attribute("ssh_proxy_tunnel", False)



    @ssh_proxy_tunnel.setter

    def ssh_proxy_tunnel(self, value):

        self.set_attribute("ssh_proxy_tunnel", value)



    @property

    def ssh_tunnel_port(self):

        return self.get_attribute("ssh_tunnel_port")



    @ssh_tunnel_port.setter

    def ssh_tunnel_port(self, value):

        self.set_attribute("ssh_tunnel_port", value)



    @property

    def ssh_tunnel_ip(self):

        return self.get_attribute("ssh_tunnel_ip")



    @ssh_tunnel_ip.setter

    def ssh_tunnel_ip(self, value):

        self.set_attribute("ssh_tunnel_ip", value)


    register_convenience_wrapper("MonitoringChannel", ORMWrapperMonitoringChannel)


