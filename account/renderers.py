from rest_framework import renderers
import json


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            # if "Given token not valid for any token type" in str(data.get("detail")):
            #     print("dmkd")
            #     print(data.get("code"))
            if data.get("code") == "token_not_valid":
                print(type(data.get("detail")))
                print(type(data.get("code")))
                response = json.dumps(
                    {'status': "error", "message": "Given token not valid for any token type"})
            else:
                response = json.dumps(
                    {'status': "error", "message": data})
        else:
            response = json.dumps(data)

        return response
