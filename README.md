# 7841_CLI_Tool
Used for CUCM development testing on Cisco 7841 lab phones. 

This script will establish ssh connections Cisco 7841 phones.
From here, we can send key inputs to emulate in-person phone operation.
This is very hand for remote working, or general mass automation.
This is confirmed functional for 20 phones, as per my dev. enviroment.

This is not guaranteed functional for other mode types.
The 7965, for example, has a prompt of mac>, which looks like 'SEPABCABCABC123>'.
You will have to test around. I will attempt to add these models into the code myself in future updates.

Pre-requisites:
In CUCM, under the device, ensure that:
  a. SSH access is enabled
  b. a secure username and password is set under ssh credentials
