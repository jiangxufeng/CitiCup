# -*-coding:utf-8
from aliyunsdkcore.client import AcsClient
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
import uuid


REGION = "cn-hangzhou"
ACCESS_KEY_ID = "LTAI7Z5sljxhRYsc"
ACCESS_KEY_SECRET = "F1ZFrtKqhEU1XIPAZGxNsA8vHCDFAW"
acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)


def send_sms(business_id, phonenumber, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    smsRequest.set_TemplateCode(template_code)

    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    smsRequest.set_OutId(business_id)
    smsRequest.set_SignName(sign_name)
    smsRequest.set_PhoneNumbers(phonenumber)
    smsResponse = acs_client.do_action_with_exception(smsRequest)
    return smsResponse


if __name__ == '__main__':
    __business_id = uuid.uuid1()
    print(__business_id)
    params = "{\"code\":\"874818\",\"prodect\":\"用户注册\"}"
    print(send_sms(__business_id, "**********", "**********", "SMS_107095085", params))

