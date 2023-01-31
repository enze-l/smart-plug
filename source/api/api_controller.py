from config.config import API_NAME


class APIController:
    def __init__(self, hardware):
        self.hardware = hardware
        self.__import_api(API_NAME)

    def __import_api(self, api_name):
        api = __import__("api." + api_name + ".api", globals(), locals(), [], 0)
        self.api = api.API(self.hardware)

    async def start_api(self):
        await self.api.start()

    def stop_api(self):
        self.api.stop()

    async def change_api(self, api_name):
        self.stop_api()
        self.__import_api(api_name)
        await self.start_api()



