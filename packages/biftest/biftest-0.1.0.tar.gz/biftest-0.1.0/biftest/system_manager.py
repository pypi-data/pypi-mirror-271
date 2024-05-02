
from biftest.request import Request
# 패키지를 만들때는 앞에 패키지명을 붙여주는게 좋음

class Grouops(Request):

    def __init__(self, url, token):
        super().__init__(url, token)

    def get_list(self, params):
        endpoint = self.url + 'groups'
        return self._get_request(endpoint, params)
        
    def regist(self, data):
        endpoint = self.url + 'groups'
        return self._post_request(endpoint, data)
    
    def put(self, inputId, data):
        endpoint = self.url + 'groups/' + inputId + '/put'
        return self._post_request(endpoint, data)
        
    def delete(self, inputId, data):
        endpoint = self.url + 'groups/' + inputId + '/delete'
        return self._post_request(endpoint, data)
    

class Users(Request):

    def __init__(self, url, token):
        super().__init__(url, token)

    def get_info(self,inputId, params):
        endpoint = self.url + 'users/'+inputId
        return self._get_request(endpoint, params)
        
    def create(self, data):
        endpoint = self.url + 'users'
        return self._post_request(endpoint, data)
    
    def put(self, inputId, data):
        endpoint = self.url + 'users/' + inputId + '/put'
        return self._post_request(endpoint, data)

    def update_account(self, inputId, data):
        endpoint = self.url + 'users/' + inputId + '/account'
        return self._post_request(endpoint, data)
    
    def update_status(self, inputId, data):
        endpoint = self.url + 'users/' + inputId + '/enabled'
        return self._post_request(endpoint, data)    
    
    def refresh_token(self, inputId, data):
        endpoint = self.url + 'users/' + inputId + '/refreshToken'
        return self._post_request(endpoint, data)    
            
    def delete(self, inputId, data):
        endpoint = self.url + 'users/' + inputId + '/delete'
        return self._post_request(endpoint, data)