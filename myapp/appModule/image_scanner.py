from flask import Blueprint,render_template

img_scan = Blueprint("scan_img",__name__)

@img_scan.route('/images-scanner',methods=['GET', 'POST'])
def images_scan():
    return render_template("image_scanner.html")

