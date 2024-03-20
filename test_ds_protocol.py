import ds_protocol as dsp

#test send dm
msg1 = dsp.format_json_send_dm(token="user_token", message="Hello World!", recipient="ohhimark", t="1603167689.3928561")
if msg1.strip() == '{"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}':
    print("test 1 (sending dm to user ohhimark) passed!")
    print(f"here is the formatted message: {msg1}")
else:
    print("test failed...")
    print('supposed to have: \n {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}')
    print(f"we got: {msg1}")

#test requesting for messages
msg2 = dsp.format_json_other_dm(token="user_token", option="n")
if msg2 == '{"token":"user_token", "directmessage": "new"}':
    print("test 2 (requesting unreads) passed!")
    print(f"here is the formatted message: {msg2}")
else:
    print("test failed...")
    print('supposed to have: \n {"token":"user_token", "directmessage": "new"}')
    print(f"we got: {msg2}")
msg3 = dsp.format_json_other_dm(token="user_token", option="a")
if msg3 == '{"token":"user_token", "directmessage": "all"}':
    print("test 2 (requesting all messages) passed!")
    print(f"here is the formatted message: {msg3}")
else:
    print("test failed...")
    print('supposed to have: \n {"token":"user_token", "directmessage": "all"}')
    print(f"we got: {msg3}")


#test extracting messages from server
#rec1 = dsp.extract_json('{"response": {"type": "ok", "message": "Direct message sent"}}')
#print(rec1)
rec2 = dsp.extract_json('{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}')
print(rec2)