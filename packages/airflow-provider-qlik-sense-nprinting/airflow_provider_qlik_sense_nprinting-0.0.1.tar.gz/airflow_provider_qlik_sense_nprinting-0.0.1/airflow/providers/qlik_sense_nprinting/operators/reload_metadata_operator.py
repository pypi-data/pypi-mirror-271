from typing import Any, Callable, Dict, Optional
import time

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.models.connection import Connection
from airflow.providers.qlik_sense_nprinting.hooks.qlik_nprinting_hook_ntlm import QlikNPrintingHookNTLM


class QlikNPrintingReloadMetaDataOperator(BaseOperator):
    """
    Trigger a reload of metadata task of the app id passed in params.

    :conn_id: connection to run the operator with it
    :appId: str
    
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = ['connectionId']

    #template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#00873d'

    @apply_defaults
    def __init__(self, *, connectionId: str = None, conn_id: str = 'qlik_conn_sample', waitUntilFinished: bool = True, **kwargs: Any,) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.conn_type = Connection(conn_id=self.conn_id).conn_type
        self.connectionId = connectionId
        self.waitUntilFinished = waitUntilFinished
    
    def execute(self, context: Dict[str, Any]) -> Any:

        self.log.info("Initiating NTLM Hook")
        hook = QlikNPrintingHookNTLM(conn_id=self.conn_id)

        self.log.info("Call HTTP method to reload metadata from connection {}".format(self.connectionId))

        response = hook.reload_metadata(self.connectionId)

        idExecution = None
        self.log.info('Status Code Return {}'.format(response.status_code))
        self.log.info('Answer Return {}'.format(response.text))
        if response.status_code in range(200,300):
            body = response.json()
            idExecution = body['data']['id'] # Adding Execution Id
        elif response.status_code == 403:
            raise ValueError("Error API: Authentification to triggered the metadata reload failed. Please check credentials in connection {}".format(self.conn_id))
        else:
            raise ValueError("Error API when triggering the new metadata reloading {connectionId}".format(connectionId=self.connectionId))
        
        if self.waitUntilFinished:
            self.log.info('Synchronous mode activated waiting the ending of the execution {}'.format(idExecution))
            self.log.info('Heartbeat of the execution of reload metadata {} will start in 15s'.format(idExecution))
            time.sleep(15)
            flag=True
            while flag:
                ans = hook.check_status_reload_metedata(taskId=self.connectionId, id=idExecution)
                self.log.info('Reload Metadata Task status: {}'.format(ans.text))
                if ans.status_code == 200:
                    body = ans.json()
                    progressStatus = body['data']['progress']
                    reloadStatus = body['data']['status']
                    if progressStatus == 1.0:
                        flag=False
                        if reloadStatus.lower() == 'failed': 
                            raise ValueError('Error API: Reload MetaData Task Run has failed. Please check logs to get more informations')
                else:
                    raise ValueError("API Error return")

        return response.text