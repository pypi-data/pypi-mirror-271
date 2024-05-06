## This is needed to allow Airflow to pick up specific metadata fields it needs for certain features. We recognize it's a bit unclean to define these in multiple places, but at this point it's the only workaround if you'd like your custom conn type to show up in the Airflow UI.
def get_provider_info():
    return {
        "package-name": "airflow-provider-qlik-sense-client-managed", # Required
        "name": "Qlik Sense Client Managed Airflow Provider", # Required
        "description": 'Airflow package provider to perform actions on Qlik Sense Client Managed Server.', # Required
        "hook": [
            {
                "integration-name": "Qlik Sense Client Managed",
                "python-modules": ["airflow.providers.qlik_sense.hooks.qlik_sense_hook.QlikSenseHook", 
                "airflow.providers.qlik_sense.hooks.qlik_sense_hook_ntlm.QlikSenseHookNTLM",
                "airflow.providers.qlik_sense.hooks.qlik_sense_hook_cert.QlikSenseHookCert", 
                "airflow.providers.qlik_sense.hooks.qlik_sense_hook_jwt.QlikSenseHookJWT", 
                ]
            }
            ],
        "operators":[
                        {
                            "integration-name": "Qlik Reload App Operator",
                            "python-modules":"airflow.providers.qlik_sense.operators.reload_app_operator.QlikSenseReloadAppOperator"
                        },
                        {
                            "integration-name": "Qlik Reload Task Operator",
                            "python-modules":"airflow.providers.qlik_sense.operators.reload_app_operator.QlikSenseReloadTaskOperator"
                        }, 

        ],
        'connection-types': [
            {
                'hook-class-name': 'airflow.providers.qlik_sense.hooks.qlik_sense_hook_cert.QlikSenseHookCert',
                'connection-type': 'qlik_sense_client_managed_cert',
            },
            {
                'hook-class-name': 'airflow.providers.qlik_sense.hooks.qlik_sense_hook_jwt.QlikSenseHookJWT',
                'connection-type': 'qlik_sense_client_managed_jwt',
            },
            {
                'hook-class-name': 'airflow.providers.qlik_sense.hooks.qlik_sense_hook_ntlm.QlikSenseHookNTLM',
                'connection-type': 'qlik_sense_client_managed_ntlm',
            },
        ],
        #"extra-links": ["qlik_sense_cloud.operators.sample_operator.ExtraLink"],
        "versions": ["0.0.1"] # Required
    }