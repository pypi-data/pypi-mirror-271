'''
Created on 6 Mar 2024

@author: jacklok
'''


from flask import Blueprint, render_template, request, current_app
import logging
from trexweb.conf import is_local_development
from trexweb.controllers.system.system_routes import verify_recaptcha_token
from trexmodel.utils.model.model_util import create_db_client
from trexlib.utils.string_util import is_not_empty
from trexmail.email_helper import is_valid_email 
from trexmail.conf import DEFAULT_SENDER, DEFAULT_RECIPIENT_EMAIL
from trexweb.forms.system_forms import DemoRequestForm
from trexmodel.models.datastore.system_models import DemoRequest
from trexmail.flask_mail import send_email
from trexlib.utils.log_util import get_tracelog
from flask_babel import gettext
from trexweb.libs.http import create_rest_message, StatusCode
from werkzeug.utils import redirect
from flask.helpers import url_for


presentation_bp = Blueprint('merchant_presentation_bp', __name__,
                     template_folder    = 'templates',
                     static_folder      = '/presentation/static',
                     url_prefix         = '/presentation'
                     )

logger = logging.getLogger('controller')

'''
Blueprint settings here
'''
@presentation_bp.context_processor
def merchant_presentation_bp_inject_settings():
    return dict(
                
                )

@presentation_bp.route('/')
def presentation_bp_index(): 
    return render_template("presentation/presentation_index.html")

@presentation_bp.route('/html')
def presentation_in_html(): 
    return redirect(url_for('static', filename='presentation/pv2024.html'))

@presentation_bp.route('/pdf')
def presentation_in_pdf(): 
    return redirect(url_for('static', filename='presentation/pv2024.pdf'))