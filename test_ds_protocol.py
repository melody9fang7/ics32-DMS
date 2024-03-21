"""
testing module for ds_protocol
"""
import ds_messenger as dsm


class TestDSMessenger:
    """
    different testing methods to test all of ds_protocol's functionalities
    """
    def test_extract_json(self):
        """
        testing extract_json's accuracy with a sample json string
        """
        json_msg = '{"response": {"type": "ok", "message": "Success"}}'
        result = dsm.dp.extract_json(json_msg)
        assert result.type == "ok"
        assert result.message == "Success"
        assert result.token == ""
        assert result.messages == []

    def test_format_json_join(self):
        """
        testing join message accuracy with sample parameters
        """
        username = "test_user"
        password = "test_password"
        result = dsm.dp.format_json_join(username, password)
        expected = '{"join": {"username": "test_user", "password": \
"test_password", "token": ""}}'
        assert result == expected

    def test_format_json_post(self):
        """
        testing post message accuracy
        """
        token = "test_token"
        postmsg = "Hello, World!"
        result = dsm.dp.format_json_post(token, postmsg)
        assert '"token": "test_token"' in result
        assert '"entry": "Hello, World!"' in result

    def test_format_json_bio(self):
        """
        testing post message accuracy
        """
        token = "test_token"
        bio = "Test bio"
        result = dsm.dp.format_json_bio(token, bio)
        assert '"token": "test_token"' in result
        assert '"entry": "Test bio"' in result

    def test_format_json_send_dm(self):
        """
        testing send message json formatting accuracy
        """
        token = "test_token"
        message = "Test message"
        recipient = "test_recipient"
        result = dsm.dp.format_json_send_dm(token, message, recipient)
        assert '"token":"test_token"' in result
        assert '"entry": "Test message"' in result
        assert '"recipient":"test_recipient"' in result

    def test_format_json_other_dm(self):
        """
        testing ability to make message to retrieve new or all messages
        """
        token = "test_token"
        result_n = dsm.dp.format_json_other_dm(token, "n")
        result_a = dsm.dp.format_json_other_dm(token, "a")
        assert '"token":"test_token"' in result_n
        assert '"token":"test_token"' in result_a
        assert '"directmessage": "new"' in result_n
        assert '"directmessage": "all"' in result_a
