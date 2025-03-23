from BotGuardExtension import BotGuardClient
bg_client = BotGuardClient()
program_byrecode = ''
bot_guard_response = bg_client.get_bot_guard_reponse(program=program_byrecode)
print(bot_guard_response.get('bot_guard_response'))