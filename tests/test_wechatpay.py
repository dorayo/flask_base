import unittest
from app import create_app, db
from flask import url_for



class WechatPayAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_wechat_pay(self):
        # 测试微信支付
        response = self.client.post(url_for('api.wechat_h5_pay'), json={
            'payer_client_ip': '1.2.3.4',
            'amount': '1',
            'description':'测试支付',
            'h5_info_type':'Wap'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['data']
        print("========")
        print(data)
        self.assertIsNotNone(data['url'])
  