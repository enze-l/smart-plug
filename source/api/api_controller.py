import gc
from config.config import API_NAME


class APIController:
    def __init__(self, hardware):
        self.hardware = hardware
        self.api_cash_dict = {}
        self.__load_api(API_NAME)

    def __import_api(self, api_name):
        api = __import__("api." + api_name + ".api", globals(), locals(), [], 0)
        self.api = api.API(self.hardware)
        self.api_cash_dict[api_name] = self.api

    def __load_api(self, api_name):
        if api_name in self.api_cash_dict:
            print("api loaded from cash")
            self.api = self.api_cash_dict[api_name]
        else:
            print("api loaded from memory")
            self.__import_api(api_name)
        gc.collect()

    async def start_api(self):
        await self.api.start()

    def stop_api(self):
        self.api.stop()

    async def change_api(self, api_name):
        self.stop_api()
        self.__load_api(api_name)
        await self.start_api()
