import oauth2 as oauth
import urllib
import json
import urlparse

class InstapaperAPIException(Exception):
    pass

class InvalidToken(InstapaperAPIException):
    pass
    
class InstapaperAPIError(InstapaperAPIException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        
    def __str__(self):
        return '{0} - {1}'.format(self.code, self.message)

class InstapaperAPI(object):
    def __init__(self, user, password, key, secret):
        # TODO We don't need to init with these params
        self.hostname = 'www.instapaper.com'
        self.user = user
        self.password = password
        self.key = key
        self.secret = secret
        self.oauth_token = None
        self.oauth_token_secret = None

    def _get_params(self, **kwargs):
        '''
        Return a dictionary of parameters to pass along with HTTP request.
        Only pass along the parameter if the value is not None
        '''
        
        result = {}
        
        for key in kwargs:
            if kwargs[key]:
                result[key] = kwargs[key]
                
        return result
        
    def _check_error(self, data):
        '''
        Check output to see if an API error was returned.
        
        Raise error if necessary.
        '''
        
        if data:
            for item in data:
                print item
                if item['type'] == 'error':
                    raise InstapaperAPIError(item['error_code'], item['message'])

    def _call_api(self, path, **kwargs):
        '''
        Call the Instapaper API
        '''
        result = None
        # TODO Need some more validation here
        if self.oauth_token and self.oauth_token_secret:
            consumer = oauth.Consumer(self.key, self.secret)
            client = oauth.Client(consumer, oauth.Token(self.oauth_token, self.oauth_token_secret))
            response, data = client.request('https://{0}{1}'.format(self.hostname, path), method="POST", body=urllib.urlencode(self._get_params(**kwargs)))
            if data:
                result = json.loads(data)
                self._check_error(result)
            else:
                raise InstapaperAPIError(response['status'], 'HTTP Error')
        else:
            raise InvalidToken
            
        return result



    def access_token(self):
        params = {'x_auth_username': self.user,
            'x_auth_password': self.password,
            'x_auth_mode': 'client_auth'}
        
        consumer = oauth.Consumer(self.key, self.secret)
        client = oauth.Client(consumer)
        client.add_credentials(self.user, self.password)
        client.set_signature_method = oauth.SignatureMethod_HMAC_SHA1()
        response, data = client.request('https://{0}/api/1/oauth/access_token'.format(self.hostname), method="POST",body=urllib.urlencode(params))
        
        if response:
            if response['status'] == '200':
                token = dict(urlparse.parse_qsl(data))
                self.oauth_token = token['oauth_token']
                self.oauth_token_secret = token['oauth_token_secret']

    def verify_credentials(self):
        return self._call_api('/api/1/account/verify_credentials')
    
    def bookmarks_list(self, limit=25, folder_id=None, have=None):
        return self._call_api('/api/1/bookmarks/list', limit=limit, folder_id=folder_id, have=have)
    
    def bookmarks_update_read_progress(self, bookmark_id, progress, progress_timestamp):
        return self._call_api('/api/1/bookmarks/update_read_progress', bookmark_id=bookmark_id, progress=progress, progress_timestamp=progress_timestamp)
    
    def bookmarks_add(self, url, title=None, description=None, folder_id=None, resolve_final_url=1, content=None, is_private_from_source=None):
        return self._call_api('/api/1/bookmarks/add', url=url, title=title, description=description, folder=folder_id, resolve_final_url=resolve_final_url, content=content, is_private_from_source=is_private_from_source)
    
    def bookmarks_delete(self, bookmark_id):
        return self._call_api('/api/1/bookmarks/delete', bookmark_id=bookmark_id)
    
    def bookmarks_star(self, bookmark_id):
        return self._call_api('/api/1/bookmarks/star', bookmark_id=bookmark_id)
    
    def bookmarks_unstar(self, bookmark_id):
        return self._call_api('/api/1/bookmarks/unstar', bookmark_id=bookmark_id)
    
    def bookmarks_archive(self, bookmark_id):
        return self._call_api('/api/1/bookmarks/archive', bookmark_id=bookmark_id)
    
    def bookmarks_unarchive(self, bookmark_id):
        return self._call_api('/api/1/bookmarks/unarchive', bookmark_id=bookmark_id)
    
    def bookmarks_move(self, bookmark_id, folder_id):
        return self._call_api('/api/1/bookmarks/move', bookmark_id=bookmark_id, folder_id=folder_id)
    
    def bookmarks_get_text(self, bookmark_id):
        #TODO Fix this
        #Output: HTML with an HTTP 200 OK status, not the standard API output structures, or an HTTP 400 status code and a standard error structure if anything goes wrong.
        return self._call_api('/api/1/bookmarks/get_text', bookmark_id=bookmark_id)
    
    def folders_list(self):
        return self._call_api('/api/1/folders/list')
    
    def folders_add(self, title):
        return self._call_api('/api/1/folders/add', title=title)
    
    def folders_delete(self, folder_id):
        return self._call_api('/api/1/folders/delete', folder_id=folder_id)
    
    def folders_set_order(self, order):
        # TODO fix this
        #a set of folder_id:position pairs joined by commas, where the position is a positive integer 32 bits or less
        return self._call_api('/api/1/folders/set_order', order=order)