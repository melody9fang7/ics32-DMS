import ds_protocol as dsp

#test send dm
msg1 = dsp.format_json_send_dm(token="user_token", message="Hello World!", recipient="ohhimark", t="1603167689.3928561")
assert msg1.strip() == '{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}':

#test requesting for messages
msg2 = dsp.format_json_other_dm(token="user_token", option="n")
assert msg2 == '{"token":"user_token", "directmessage": "new"}':

msg3 = dsp.format_json_other_dm(token="user_token", option="a")
assert msg3 == '{"token":"user_token", "directmessage": "all"}':


#test extracting messages from server
rec1 = dsp.extract_json('{"response": {"type": "ok", "message": "Direct message sent"}}')
print(rec1)
rec2 = dsp.extract_json('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}')
print(rec2)