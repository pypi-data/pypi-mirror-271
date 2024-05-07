from rest_framework import status
from json import dumps
from authsystem.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch , call
import string
import random
from rest_framework.authtoken.models import Token
from django.test import override_settings, TestCase, tag
import io
import datetime
from utils import models as utils_models
from django.contrib.auth import authenticate
from django.utils import timezone

def gen_random_letters():
    rnd_letter = "".join(random.sample(string.ascii_letters, 5))
    return rnd_letter


def gen_random_username():
    return gen_random_letters()


def gen_random_email():
    return gen_random_letters() + "@" + gen_random_letters() + ".com"


def create_user(**kwargs):
    username = kwargs.get('username')
    if not username:
        username = gen_random_username()
        return User.objects.create(
            username=username , **kwargs
        )
    return User.objects.create(**kwargs)


def create_token(user):
    return Token.objects.create(user=user)


def create_cellphone_verify_token(**kwargs):
    return utils_models.CellphoneVerificationToken.objects.create(**kwargs)


@tag("register")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
@patch("django.contrib.auth.base_user.make_password", return_value="hash")
class Register(TestCase):
    def generate_photo_file(self):
        file = io.BytesIO()
        file.write(10 * b"b")
        file.name = "filename"
        file.seek(0)
        return file

    def setUp(self):
        self.client = APIClient()
        self.username = "1234567890"
        self.cellphone = "04214124412"
        self.fullname = "vahid asadi"
        self.avatar = self.generate_photo_file()

        self.post_data = {
            "username": self.username,
            "cellphone": self.cellphone,
            "fullname": self.fullname,
            "avatar": self.avatar
        }
        self.invalid_post_data_invalid_fields = {
            "username": self.username,
            "cellphone": "",  # wrong. should be None
            "fullname": "",  # should not be blank
        }
        self.invalid_post_data = {}

    def test_register_success(self, mock_makepass):
        response = self.client.post(
            reverse("authsystem:register"),
            data=self.post_data,
            format="multipart",
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(len(response.data),7)

        user_obj = User.objects.get(username=self.username)
        self.assertTrue(hasattr(user_obj, "auth_token"))
        self.assertEqual(str(user_obj.id), response.data["id"])
        self.assertEqual(user_obj.cellphone, response.data["cellphone"])
        self.assertEqual(user_obj.fullname, response.data["fullname"])
        self.assertEqual(user_obj.email, response.data["email"])
        self.assertTrue(user_obj.avatar.url)

    def test_register_failed_Bad_request(self, mock_makepass):
        # user exists
        pre_created_user = create_user(username=self.username)
        response = self.client.post(
            reverse("authsystem:register"),
            data=self.post_data,
            format="multipart",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue(len(response.data), 1)
        self.assertTrue("username" in response.data)
        pre_created_user.delete()

        # invalid postdata . username  , cellphone , fullname are required
        response = self.client.post(
            reverse("authsystem:register"),
            data=dumps(self.invalid_post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data), 3)
        self.assertTrue("username" in response.data)
        self.assertTrue("fullname" in response.data)
        self.assertTrue("cellphone" in response.data)


@tag("login")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
class Login(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cellphone = '09321321323'
        self.verify_token_obj = create_cellphone_verify_token(cellphone = self.cellphone)
        self.expired_verify_token = create_cellphone_verify_token(cellphone = self.cellphone)
        self.expired_verify_token.expire_date = timezone.now() - datetime.timedelta(minutes = 5)
        self.expired_verify_token.save()
        self.user_obj = create_user(cellphone = self.cellphone)
        self.post_data = {"verify_token": self.verify_token_obj.key}
        self.post_data_verify_token_not_registered = {"verify_token": "bbb"}
        self.post_data_verify_token_expired = {"verify_token": self.expired_verify_token.key}
        self.invalid_post_data = {}

    def test_login_success(self):
        response = self.client.post(
            reverse("authsystem:login"),
            data=dumps(self.post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(Token.objects.filter(user=self.user_obj).exists())
        self.assertEqual(response.data["token"], self.user_obj.auth_token.key)
        self.assertEqual(str(self.user_obj.id), response.data["id"])
        self.assertFalse(utils_models.CellphoneVerificationToken.objects.filter(id = self.verify_token_obj.id).exists())

    def test_login_failed_verify_token_expired(self):
        response = self.client.post(
            reverse("authsystem:login"),
            data=dumps(self.post_data_verify_token_expired),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_login_failed_verify_token_not_registered(self):
        response = self.client.post(
            reverse("authsystem:login"),
            data=dumps(self.post_data_verify_token_not_registered),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_login_failed_user_with_this_cellphone_not_registered(self):
        self.user_obj.delete()
        response = self.client.post(
            reverse("authsystem:login"),
            data=dumps(self.post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_login_failed_invalid_data(self):
        # invalid post data
        response = self.client.post(
            reverse("authsystem:login"),
            data=dumps(self.invalid_post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertTrue("verify_token" in response.data)


@tag("change-password")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
@patch("django.contrib.auth.base_user.make_password", return_value="hash")
class ChangePassword(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "vahid@vahid.com"
        self.old_password = "jf;lj;fajbb"
        self.new_password = "grsgregfbfs1"
        self.invalid_new_password = "111"  # pass shoudl be atleast 9 characheters
        self.user_obj = create_user(username=self.username)
        self.user_obj.set_password(self.old_password)
        self.user_obj.save()
        self.token = Token.objects.create(user=self.user_obj)

        self.patch_data = {
            "username": self.username,
            "old_password": self.old_password,
            "new_password": self.new_password,
        }

        self.patch_data_wrong_old_pass = {
            "username": self.username,
            "old_password": "ffffffffff",
            "new_password": self.new_password,
        }
        self.invalid_patch_data_empty_body = {}
        self.invalid_patch_data_invalid_new_pass = {
            "username": self.username,
            "old_password": self.old_password,
            "new_password": self.invalid_new_password,
        }
        self.invalid_patch_data_old_pass_equals_to_new_one = {
            "username": self.username,
            "old_password": self.old_password,
            "new_password": self.old_password,
        }

    def test_change_pass_success(self, mock_makepass):
        response = self.client.patch(
            reverse("authsystem:change-pass"),
            data=dumps(self.patch_data),
            content_type="application/json",
        )
        self.user_obj.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(Token.objects.filter(user=self.user_obj).exists())
        self.assertEqual(response.data["token"], self.user_obj.auth_token.key)
        self.assertRaises(Token.DoesNotExist, self.token.refresh_from_db)
        self.assertEqual(response.data["id"], str(self.user_obj.id))

    def test_change_pass_failed_invalid_data(self, mock_makepass):
        # wrong old pass
        response = self.client.patch(
            reverse("authsystem:change-pass"),
            data=dumps(self.patch_data_wrong_old_pass),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # invalid patch data. fields dropded from body
        response = self.client.patch(
            reverse("authsystem:change-pass"),
            data=dumps(self.invalid_patch_data_empty_body),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue("username" in response.data)
        self.assertTrue("old_password" in response.data)
        self.assertTrue("new_password" in response.data)
        self.assertEqual(len(response.data), 3)

        # invalid patch data. invalid new pass. pass should be at least 8 chars
        response = self.client.patch(
            reverse("authsystem:change-pass"),
            data=dumps(self.invalid_patch_data_invalid_new_pass),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue("new_password" in response.data)
        # len=1 means there is just one error for `new_password` field
        self.assertEqual(len(response.data), 1)
        # len=1 means there is one validation for `new_password` field
        self.assertEqual(len(response.data["new_password"]), 1)

        # invalid patch data. new pass should be differ than old one.
        response = self.client.patch(
            reverse("authsystem:change-pass"),
            data=dumps(self.invalid_patch_data_old_pass_equals_to_new_one),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertTrue("non_field_errors" in response.data)


@tag("user_operation")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
class UserOperationTest(TestCase):
    def create_user_with_token(self, username, **kwargs):
        user = create_user(username = username, **kwargs)
        token = create_token(user)
        return {"user": user, "token": token}

    def generate_photo_file(self):
        file = io.BytesIO()
        file.write(10 * b"b")
        file.name = "filename"
        file.seek(0)
        return file

    def setUp(self):
        self.client = APIClient()
        self.username = gen_random_username()
        self.old_email = gen_random_email()
        self.old_fullname = "vahid"
        self.old_cellphone = gen_random_letters()

        self.new_email = gen_random_email()
        self.new_fullname = "vahido"
        self.new_cellphone = gen_random_letters()
        self.avatar = self.generate_photo_file()

        self.user_data = self.create_user_with_token(
            self.username,
            cellphone=self.old_cellphone,
            fullname=self.old_fullname,
            email=self.old_email,
        )

        self.patch_data = {
            "cellphone": gen_random_letters(),
            "email": gen_random_email(),
            "fullname": self.new_fullname,
            "avatar":self.avatar
        }

        self.patch_data_with_old_values = {
            "cellphone": self.old_cellphone,
            "email": self.old_email,
            "fullname": self.old_fullname,
        }
        self.invalid_patch_data = {
            "fullname": None,
            "email": '',
            "cellphone": '',
        }

    # GET METHOD
    def test_get_profile(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user_data["token"].key
        )
        response = self.client.get(
            reverse("authsystem:user-operation"),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(6, len(response.data))
        user_fields = [
            "cellphone",
            "email",
            "fullname",
            "username",
            "id",
            "avatar"
        ]
        for field in user_fields:
            self.assertTrue(field in response.data)

    def test_get_profile_unauthorized(self):
        response = self.client.get(
            reverse("authsystem:user-operation"),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    # UPDATE METHOD
    """
    fields that could be updated is as follows:
        cellphone
        email
        fullname
    """
    def test_teacher_update_success(
        self,
    ):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user_data["token"].key
        )
        response = self.client.patch(
            reverse("authsystem:user-operation"),
            data=self.patch_data,
            format="multipart",
        )
        user = self.user_data["user"]
        user.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(6, len(response.data))
        fields = ["id", "username", "email", "cellphone", "fullname", "avatar"]
        for field in fields:
            self.assertTrue(field in response.data)

        self.assertEqual(user.cellphone,self.patch_data["cellphone"])
        self.assertEqual(user.email,self.patch_data["email"])
        self.assertEqual(user.fullname,self.patch_data["fullname"])
        self.assertTrue(user.avatar.url)

    def test_personUpdate_unauthorized(self):
        response = self.client.patch(
            reverse("authsystem:user-operation"),
            data=self.patch_data,
            format="multipart",
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_update_profile_invalid_input(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user_data["token"].key
        )
        response = self.client.patch(
            reverse("authsystem:user-operation"),
            data=dumps(self.invalid_patch_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data), 3)

    def test_update_failed_with_existing_values(self):
        existing_user = create_user(username='elcid' ,cellphone = '011111' , email = 'elcid@elcid.com')
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user_data["token"].key
        )
        response = self.client.patch(
            reverse("authsystem:user-operation"),
            data=dumps({
                'cellphone': '011111',
                'email': 'elcid@elcid.com'
            }),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data) , 2)

    # DELETE METHOD
    def test_delete_profile(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user_data["token"].key
        )
        response = self.client.delete(
            reverse("authsystem:user-operation"),
            content_type="application/json",
        )
        user = self.user_data['user']
        user.refresh_from_db()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertTrue(user.is_deleted)



@tag("forget-password")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
class ForgetPassword(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "vahid@vahid.com"
        self.cellphone = "0424324234"
        self.user_obj = create_user(username=self.username , cellphone = self.cellphone)

    @patch("utils.helpers.SendSMS")
    def test_forget_pass_success(self, mock_send_sms):
        response = self.client.get(
            reverse("authsystem:forget-pass") + f"?cellphone={self.user_obj.cellphone}",
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)
        ver_code = utils_models.VerificationToken.objects.get(owner=self.user_obj)
        mock_send_sms.assert_called_once()
        token = ver_code.key
        calls = [call(cellphone = self.user_obj.cellphone ,token=token)]
        mock_send_sms.assert_has_calls(calls)

    @patch("utils.helpers.SendSMS")
    def test_forget_pass_failed_invalid_cellphone(self, mock_send_sms):
        response = self.client.get(
            reverse("authsystem:forget-pass") + f"?cellphone=somefakecellphone",
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertFalse(utils_models.VerificationToken.objects.filter(owner=self.user_obj).exists())
        mock_send_sms.assert_not_called()

    def test_forget_pass_failed_no_cellphone_supplied(self):
        response = self.client.get(
            reverse("authsystem:forget-pass"),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('non_field_errors' in response.data)


@tag("reset-password")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
class ResetPassword(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "vahid@vahid.com"
        self.user_obj = create_user(username=self.username)
        self.ver_token_obj = utils_models.VerificationToken.objects.create(owner=self.user_obj)
        self.token_obj = Token.objects.create(user=self.user_obj)
        self.new_password = '12345678g'
        self.invalid_new_password = '78g'

        self.post_data = {
            'key': self.ver_token_obj.key ,
            "new_password": self.new_password
        }
        self.invalid_post_data = {
            'key': self.ver_token_obj.key ,
            "new_password": self.invalid_new_password
        }
        self.invalid_post_data_fake_key = {
            'key': '3802112f' ,
            "new_password": self.new_password
        }


    def test_reset_pass_success(self):
        response = self.client.post(
            reverse("authsystem:reset-pass"),
            data= dumps(self.post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 2)
        self.assertFalse(utils_models.VerificationToken.objects.filter(owner=self.user_obj).exists())
        self.assertFalse(Token.objects.filter(key = self.token_obj.key).exists())
        self.assertTrue(Token.objects.filter(user = self.user_obj).exists())
        res_fields = ['token' ,'id']
        for field in res_fields:
            self.assertTrue(field in response.data)

        self.assertTrue(authenticate(username = self.user_obj.username , password = self.new_password))


    def test_reset_pass_failed_verification_token_expired(self):
        self.ver_token_obj.expire_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=21)
        self.ver_token_obj.save()
        response = self.client.post(
            reverse("authsystem:reset-pass"),
            data= dumps(self.post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(len(response.data), 1)


    def test_reset_pass_failed_invalid_new_pass(self):
        response = self.client.post(
            reverse("authsystem:reset-pass"),
            data= dumps(self.invalid_post_data),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('new_password' in response.data)

    def test_reset_pass_failed_invalid_verification_token(self):
        response = self.client.post(
            reverse("authsystem:reset-pass"),
            data= dumps(self.invalid_post_data_fake_key),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


@tag("get-cellphone-verify-token")
@override_settings(DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage")
class GetCellphoneVerifyToken(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cellphone = "0424324234"

    @patch("utils.helpers.SendSMS")
    def test_verify_success(self, mock_send_sms):
        response = self.client.get(
            reverse("authsystem:get-cellphone-verify-token") + f"?cellphone={self.cellphone}",
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(len(response.data), 1)
        ver_code = utils_models.CellphoneVerificationToken.objects.get(cellphone = self.cellphone)
        token = ver_code.key
        self.assertTrue(token)
        calls = [call(cellphone = self.cellphone ,token=token)]
        mock_send_sms.assert_called_once()
        mock_send_sms.assert_has_calls(calls)

    def test_forget_pass_failed_no_cellphone_supplied(self):
        response = self.client.get(
            reverse("authsystem:get-cellphone-verify-token"),
            content_type="application/json",
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('non_field_errors' in response.data)
