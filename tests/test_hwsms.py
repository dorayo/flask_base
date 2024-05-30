import unittest
from app import create_app, db
from flask import url_for
from app.services import hwsms_service

class HWSMSTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.redis_store = self.app.config['REDIS_STORE']
        
        # Mock hwsms_service.send_sms
        self.original_send_sms = hwsms_service.send_sms
        hwsms_service.send_sms = self.mock_send_sms

    def tearDown(self):
        self.app_context.pop()
        hwsms_service.send_sms = self.original_send_sms

    def mock_send_sms(self, mobile):
        return True, '123456'

    def test_send_sms_hw(self):
        # 测试发送短信接口
        response = self.client.post(url_for('api.send_sms_hw'), json={'mobile': '18121658742'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['data']
        self.assertEqual(data, '123456')

        # 验证短信验证码是否存储在Redis中
        stored_code = self.redis_store.get(f'sms_code:18121658742')
        self.assertIsNotNone(stored_code)
        self.assertEqual(stored_code.decode('utf-8'), '123456')

    def test_verify_code(self):
        # 先发送短信，存储验证码
        self.redis_store.setex('sms_code:18121658742', 300, '123456')
        
        # 测试验证短信接口
        response = self.client.post(url_for('api.verify_code'), json={
            'mobile': '18121658742',
            'code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['code'], 1)

        # 测试错误的验证码
        response = self.client.post(url_for('api.verify_code'), json={
            'mobile': '18121658742',
            'code': '654321'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()['code'], 1101)
        self.assertEqual(response.get_json()['detailMsg'], '验证码错误')