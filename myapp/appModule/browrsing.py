from flask import Blueprint, render_template


browse = Blueprint('browser',__name__)

@browse.route('/browse',methods=['get', 'post'])
def show_content():
    return render_template('browsing.html')

