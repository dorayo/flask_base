import unittest
from flask import url_for
from app import create_app, db
from app.services import user_service
from app.models.user import User, Role, Permission
from tests.test_users import UserAPITestCase
from app.constants import PERMISSIONS 

class AdminAPITestCase(UserAPITestCase):
    def setUp(self):
        super().setUp()
        # 添加角色
        admin_role = Role(role_name='Admin')
        db.session.add(admin_role)
        # 数据库添加权限记录
        self.add_permissions()
        # 添加管理员账户
        admin_user = User(username='admin', email='admin@example.com', mobile='15901118000')
        admin_user.set_password('Admin123')
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()
        self.admin_user_id = admin_user.id

        # 模拟管理员登录以获取令牌
        self.admin_token = self.login_as_admin()

    def add_permissions(self):
        # 添加权限
        for permission in PERMISSIONS:
            db.session.add(Permission(**permission))
        db.session.commit()

    def login_as_admin(self):
        # 管理员登录获取令牌
        response = self.client.post(url_for('api.account_login'), json={
            'account': 'admin',
            'password': 'Admin123'
        })
        return response.json.get('data').get('token')

    def test_admin_add_user(self):
        # 管理员添加用户
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.post(url_for('admin.add_user'), headers=headers, json={
            'username': 'admin_created_user',
            'email': 'admin_created_user@example.com',
            'mobile': '18037772444',
            'password': 'AdminUser123',
            'roles': ['Admin']
        })
        self.assertEqual(response.status_code, 200)
        user = user_service.get_user_by_email('admin_created_user@example.com')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'admin_created_user')

    def test_admin_delete_user(self):
        # 管理员删除用户
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.delete(url_for('admin.delete_user', user_id=self.user_id), headers=headers)
        self.assertEqual(response.status_code, 200)
        user = user_service.get_user_by_id(self.user_id)
        self.assertEqual(user.status, 0)

    def test_admin_update_user(self):
        # 管理员更新用户信息
        headers = {
            'Authorization': f'Bearer {self.admin_token}'
        }
        response = self.client.put(url_for('admin.update_user', user_id=self.user_id), headers=headers, json={
            'username': 'updated_user',
            'email': 'updated_user@example.com',
            'status': 1
        })
        self.assertEqual(response.status_code, 200)
        user = db.session.query(User).filter_by(id=self.user_id).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'updated_user')
        self.assertEqual(user.email, 'updated_user@example.com')
        self.assertEqual(user.status, 1)

    def test_admin_add_user_role(self):
        # 管理员为用户添加角色
        headers = { 'Authorization': f'Bearer {self.admin_token}' }
        response = self.client.post(url_for('admin.add_user_role', user_id=self.user_id), headers=headers, json={ 'role_name': 'Admin' })
        self.assertEqual(response.status_code, 200)
        user = user_service.get_user_by_id(self.user_id)
        self.assertIsNotNone(user)
        self.assertTrue(user.has_role('Admin'))
       
    def test_admin_remove_user_role(self):
        # 管理员删除用户角色
        headers = { 'Authorization': f'Bearer {self.admin_token}' }
        response = self.client.delete(url_for('admin.remove_user_role', user_id=self.user_id), headers=headers, json={ 'role_name': 'User' })
        self.assertEqual(response.status_code, 200)
        user = user_service.get_user_by_id(self.user_id)
        self.assertIsNotNone(user)
        self.assertFalse(user.has_role('User')) 

    def test_admin_list_users(self):
        # 管理员获取用户列表
        headers = { 'Authorization': f'Bearer {self.admin_token}' }
        response = self.client.get(url_for('admin.list_users'), headers=headers)    
        self.assertEqual(response.status_code, 200)
        data = response.json.get('data')
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 1)

    # 其他管理功能的测试用例