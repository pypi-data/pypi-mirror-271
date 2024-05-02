from vapi_python import Vapi
from vapi_python.vapi_python import create_web_call
from .qai_call import QaiCall

class VapiQai(Vapi):

    def start(self, *, assistant_id=None, assistant=None):
        # Start a new call
        if assistant_id:
            assistant = {'assistantId': assistant_id}
        elif assistant:
            assistant = {'assistant': assistant}

        call_id, web_call_url = create_web_call(
            self.api_url, self.api_key, assistant)

        if not web_call_url:
            raise Exception("Error: Unable to create call.")

        print('Joining call... ' + call_id)

        self._client = QaiCall()
        self._client.join(web_call_url)

    
    def stop(self):
        self._client.leave()
        self._client = None
