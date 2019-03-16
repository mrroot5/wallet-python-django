class RequestTools:
    @staticmethod
    def check_if_request_user_exist(context_dict):
        request = context_dict.get("request")
        if request and hasattr(request, "user"):
            return True
        return False
