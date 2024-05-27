import unittest
from flask import url_for
from app import create_app, db
from app.services import user_service
from app.models.user import User, Role

class UserAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client(use_cookies=True)

        self.add_test_datas()

        # 登录并获取令牌
        self.login_and_get_token()

    def add_test_datas(self):
        # 添加角色
        user_role = Role(role_name='User')
        db.session.add(user_role)

       # 添加测试用户
        user = User(username='dorayo', email='youzj@163.com', mobile='15901117209')
        user.set_password('Xx123abc')
        user.roles.append(user_role) 
        db.session.add(user)

        db.session.commit()

        self.user_id = user.id 

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_and_get_token(self):
        # 模拟登录以获取令牌
        response = self.client.post(url_for('api.account_login'), json={
            'account': 'dorayo',
            'password': 'Xx123abc'
        })
        self.token = response.json.get('data').get('token')

    def test_register_user(self):
        # 测试注册用户
        response = self.client.post(url_for('api.register'), json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'mobile': '18037772361',
            'password': 'Newpass123',
            'code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        user = user_service.get_user_by_email('newuser@example.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'newuser')

    def test_get_user(self):
        # 使用获取到的令牌来测试获取单个用户信息
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = self.client.get(url_for('api.get_user', user_id=self.user_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.json['data'])
        self.assertEqual(response.json['data']['username'], 'dorayo')

    def test_update_user(self):
        # 测试更新用户信息
        # 使用获取到的令牌来测试获取单个用户信息
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        new_username = 'updatedUser'
        response = self.client.put(url_for('api.update_user', user_id=self.user_id), headers=headers, json={
            'username': new_username
        })
        self.assertEqual(response.status_code, 200)
        user = db.session.query(User).filter_by(id=self.user_id).first()
        self.assertEqual(user.username, new_username)

    def test_mobile_login(self):
        # 测试手机验证码登录
        response = self.client.post(url_for('api.mobile_login'), json={
            'mobile': '15901117209',
            'code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['data']
        self.assertIsNotNone(data['token'])

    def test_account_login(self):
        # 测试账号密码登录
        response = self.client.post(url_for('api.account_login'), json={
            'account': 'dorayo',
            'password': 'Xx123abc'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()['data']
        self.assertIsNotNone(data['token'])