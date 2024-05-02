
from biftest.request import Request
# 패키지를 만들때는 앞에 패키지명을 붙여주는게 좋음

class Dataconnectors(Request):

    def __init__(self, url, token):
        super().__init__(url, token)

    def get_list(self, params):
        endpoint = self.url + 'dataconnectors'
        return self._get_request(endpoint, params)
        
    def create(self, data):
        endpoint = self.url + 'dataconnectors'
        return self._post_request(endpoint, data)
    
    def vaild(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/vaild'
        return self._post_request(endpoint, data)
    
    def put(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/put'
        return self._post_request(endpoint, data)
        
    def delete(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/delete'
        return self._post_request(endpoint, data)
        
    def get_permission(self, inputId, params):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission'
        return self._get_request(endpoint, params)
        
    def users_regist(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission/users'
        return self._post_request(endpoint, data)
        
    def users_put(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission/users/put'
        return self._post_request(endpoint, data)
        
    def users_delete(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission/users/delete'
        return self._post_request(endpoint, data)
        
    def groups_regist(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission/groups'
        return self._post_request(endpoint, data)
        
    def groups_put(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission/groups/put'
        return self._post_request(endpoint, data)
        
    def groups_delete(self, inputId, data):
        endpoint = self.url + 'dataconnectors/' + inputId + '/permission/groups/delete'
        return self._post_request(endpoint, data)
    

class Datasets(Request):

    def __init__(self, url, token):
        super().__init__(url, token)

    def get_list(self,connectorId, params):
        endpoint = self.url + 'dataconnectors/'+connectorId+'/datasets'
        return self._get_request(endpoint, params)
        
    def create(self, data):
        endpoint = self.url + 'datasets'
        return self._post_request(endpoint, data)
    
    def put(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/put'
        return self._post_request(endpoint, data)
    
    def table(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/table'
        return self._post_request(endpoint, data)    

    def query(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/query'
        return self._post_request(endpoint, data)    
            
    def delete(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/delete'
        return self._post_request(endpoint, data)
        
    def get_permission(self, inputId, params):
        endpoint = self.url + 'datasets/' + inputId + '/permission'
        return self._get_request(endpoint, params)
        
    def users_regist(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/permission/users'
        return self._post_request(endpoint, data)
        
    def users_put(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/permission/users/put'
        return self._post_request(endpoint, data)
        
    def users_delete(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/permission/users/delete'
        return self._post_request(endpoint, data)
        
    def groups_regist(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/permission/groups'
        return self._post_request(endpoint, data)
        
    def groups_put(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/permission/groups/put'
        return self._post_request(endpoint, data)
        
    def groups_delete(self, inputId, data):
        endpoint = self.url + 'datasets/' + inputId + '/permission/groups/delete'
        return self._post_request(endpoint, data)