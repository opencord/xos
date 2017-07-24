from xosapi.orm import ORMWrapper, register_convenience_wrapper

class ORMWrapperSFlowTenant(ORMWrapper):



    sync_attributes = ("listening_endpoint", )



    @property

    def listening_endpoint(self):

        return self.get_attribute("listening_endpoint", None)



    @listening_endpoint.setter

    def listening_endpoint(self, value):

        if urlparse(value).scheme != 'udp':

            raise XOSProgrammingError("SFlowTenant: Only UDP listening endpoint URLs are accepted...valid syntax is: udp://ip:port")

        self.set_attribute("listening_endpoint", value)

		

    register_convenience_wrapper("SFlowTenant", ORMWrapperSFlowTenant)


