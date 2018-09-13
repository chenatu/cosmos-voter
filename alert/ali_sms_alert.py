# coding=utf-8
# aliyun dayu sms system. Just check personal account for now
import json
import alert
import logging
import uuid

from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider


log = logging.getLogger(__name__)

REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"
region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)


def buildAliSmsAlertFromConfig(config):
    return AliSmsAlert(config["alert"]["ali_sms_alert"]["access_key"],
                       config["alert"]["ali_sms_alert"]["access_secret"],
                       config["alert"]["ali_sms_alert"]["sign_name"].encode("utf-8"),
                       config["alert"]["ali_sms_alert"]["template_code"])


class AliSmsAlert(alert.Alert):
    def __init__(self, access_key, access_secret, sign_name, template_code):
        self.acs_client = AcsClient(access_key, access_secret, REGION)
        self.sign_name = sign_name
        self.template_code = template_code

    def doAlert(self, level, des, content):
        log.info("level - %s, des - %s, content - %s" % (level, des, content))
        self.send_sms(uuid.uuid1(), des, self.sign_name, self.template_code,
                      content)

    def send_sms(self, business_id, phone_numbers, sign_name, template_code,
                 template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)

        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)

        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)

        # 短信签名
        smsRequest.set_SignName(sign_name)
        
        # 数据提交方式
        # smsRequest.set_method(MT.POST)
        
        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)
        
        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)

        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)

        jsonResoponse = json.loads(smsResponse)
        if jsonResoponse["Message"] != "OK":
            raise Exception(smsResponse)
        return smsResponse
