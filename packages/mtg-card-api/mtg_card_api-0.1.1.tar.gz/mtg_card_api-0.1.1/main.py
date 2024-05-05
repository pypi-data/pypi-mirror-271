from src.mtg_card_api import ScryfallAPI

api = ScryfallAPI()
res = api.get_card_by_name("Sacred Foundry")

if res.error is False:
    print(res.response)
