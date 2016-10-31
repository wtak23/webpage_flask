from flask_frozen import Freezer
from app import app

from os import path
freezer = Freezer(app)
# freezer = Freezer(app,with_no_argument_rules=False, log_url_for=False)
app.config['FREEZER_DESTINATION']='mybuild'
# app.config['FREEZER_BASE_URL']= path.dirname(app.static_folder)
app.config['FREEZER_RELATIVE_URLS']= True
# print app.config['FREEZER_BASE_URL']
if __name__ == '__main__':
    freezer.freeze()
    #freezer.run(debug=True)