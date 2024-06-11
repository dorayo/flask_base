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
        response = self.client.post(url_for('api.wechat_native_pay'), json={
            'amount': '1'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("========")
        print(data)
        self.assertIsNotNone(data)
  