# COSMOS VOTER
This project is the cosmos voting proposal monitor. It provides some naive alert and resolving strategy. Anyone can fork this project and extends the alert method and monitor strategy.

The project consists of 3 componets:
- alert: alert message through any communication channel. This project implements alert by sms service provieded by aliyun. More alert methods will be provided in later commits
- voter: basic function of query proposals and submit votes
- monitor: the core deamon monitor the votes and page the on call person. We also realize a naive strategy. The strategy will be continuously refined in later commits

How to run?

This project runs by python27. First install the requirements in requirements.txt.

If you want to use the aliyun sms service in this repo, you should first install the sms sdk in `vendor/dysms_python`.

Then set the properites in config.yaml. The meaning of the properties is just as it shows

If you want to use the aliyun sms service, set the config as shown in config.yaml

In the end, run `python main.py` and good to go!