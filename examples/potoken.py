from BotGuardExtension import BotGuardClient
bg_client = BotGuardClient()
program_byrecode = ''
video_id = ''
po_token = bg_client.get_bot_guard_reponse(program=program_byrecode,identifier=video_id)
print(po_token.get('po_token'))