import os
from flask_restful import Resource, Api
from flask_restful_swagger import swagger
from flansible import app
from flansible import api, app, celery, playbook_root, auth
from flansible import verify_password, get_inventory_access
from ModelClasses import AnsibleCommandModel, AnsiblePlaybookModel, AnsibleRequestResultModel, AnsibleExtraArgsModel

import celery_runner

class Playbooks(Resource):
    @swagger.operation(
        notes='List ansible playbooks. Configure search root in config.ini',
        nickname='listplaybooks',
        responseMessages=[
            {
              "code": 200,
              "message": "List of playbooks"
            }
          ]
    )
    @auth.login_required
    def get(self):
        yamlfiles = []
        for root, dirs, files in os.walk(playbook_root):
            for name in files:
                if name.endswith((".yaml", ".yml")):
                    fileobj = {'name':name, 'parent':root}
                    yamlfiles.append(fileobj)
        
        returnedfiles = []
        for fileobj in yamlfiles:
            if 'group_vars' in fileobj['parent']:
                pass
            elif fileobj['parent'].endswith('handlers'):
                pass
            elif fileobj['parent'].endswith('vars'):
                pass
            else:
                returnedfiles.append(fileobj)

        return returnedfiles


api.add_resource(Playbooks, '/api/listplaybooks')