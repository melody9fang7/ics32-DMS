import ds_messenger as dsm


d = dsm.DirectMessenger()

d.dsuserver = "168.235.86.101"
d.username = "march13"
d.password = "march13"

d.send("hey there!", "phoebebridgers")
print(dsm.DirectMessenger.gettoken(d))
print(dsm.DirectMessenger.retrieve_all(d))