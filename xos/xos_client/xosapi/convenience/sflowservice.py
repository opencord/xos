from xosapi.orm import ORMWrapper, register_convenience_wrapper



class ORMWrapperSFlowService(ORMWrapper):

   



    sync_attributes = ("sflow_port", "sflow_api_port",)



    @property

    def sflow_port(self):

        return self.get_attribute("sflow_port", self.default_attributes["sflow_port"])



    @sflow_port.setter

    def sflow_port(self, value):

        self.set_attribute("sflow_port", value)



    @property

    def sflow_api_port(self):

        return self.get_attribute("sflow_api_port", self.default_attributes["sflow_api_port"])



    @sflow_api_port.setter

    def sflow_api_port(self, value):

        self.set_attribute("sflow_api_port", value)


    register_convenience_wrapper("SFlowService", ORMWrapperSFlowService)




