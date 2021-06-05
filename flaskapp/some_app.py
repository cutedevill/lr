from flask import Flask
app = Flask(__name__)

from flask import render_template, request

@app.route("/", methods = ("GET", "POST"))
def hello():
  return '<a href="load">GO TO APP</a>'

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

import defs

global p1, p2

@app.route('/load', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file1 = request.files['file1']
            file2 = request.files['file2']
            if (file1 and (file1.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__()):
                if (file2 and (file2.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__()):
                    global filename1, filename2
                    filename1 = secure_filename(file1.filename)
                    file1.save(app.config['UPLOAD_FOLDER'] + filename1)
                    filename2 = secure_filename(file2.filename)
                    file2.save(app.config['UPLOAD_FOLDER'] + filename2)
                    return render_template('main.html', image_name1 = app.config['UPLOAD_FOLDER'] + filename1, image_name2 = app.config['UPLOAD_FOLDER'] + filename2, coeff=0.5)
        except Exception:
            blend = request.form.get('coeff');
            try:
                blend = float(blend)
            except Exception:
                return render_template('main.html', image_name1 = app.config['UPLOAD_FOLDER'] + filename1, image_name2 = app.config['UPLOAD_FOLDER'] + filename2, coeff=0.5)
            img_path1 = app.config['UPLOAD_FOLDER'] + filename1;
            img_path2 = app.config['UPLOAD_FOLDER'] + filename2;

            defs.BLEND_IMAGES(app.config['UPLOAD_FOLDER'], img_path1, img_path2, blend)

            # Графики
            defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'blended.png', app.config['UPLOAD_FOLDER'] + 'blended_graph.png', 'BLENDED')
            defs.GRAPHS(app.config['UPLOAD_FOLDER'] + filename1, app.config['UPLOAD_FOLDER'] + filename1 + 'graph.png', 'FIRST IMAGE')
            defs.GRAPHS(app.config['UPLOAD_FOLDER'] + filename2, app.config['UPLOAD_FOLDER'] + filename2 + 'graph.png', 'SECOND IMAGE')

            total = '<img src="' + app.config['UPLOAD_FOLDER'] + 'blended.png" alt="">'
            total += '<h2>Graphs</h2>'
            total += '<a href="graphs">See graphs</a>'

            return render_template('main.html', image_name1 = app.config['UPLOAD_FOLDER'] + filename1, image_name2 = app.config['UPLOAD_FOLDER'] + filename2, coeff=blend) + total

    return render_template('form.html')

@app.route('/graphs')
def graph_page():
    # Графики
    defs.GRAPHS(app.config['UPLOAD_FOLDER'] + 'blended.png', app.config['UPLOAD_FOLDER'] + 'blended_graph.png', 'BLENDED')
    defs.GRAPHS(app.config['UPLOAD_FOLDER'] + filename1, app.config['UPLOAD_FOLDER'] + filename1 + 'graph.png', 'FIRST IMAGE')
    defs.GRAPHS(app.config['UPLOAD_FOLDER'] + filename2, app.config['UPLOAD_FOLDER'] + filename2 + 'graph.png', 'SECOND IMAGE')

    img_1 = app.config['UPLOAD_FOLDER'] + 'blended_graph.png'
    img_2 = app.config['UPLOAD_FOLDER'] + filename1 + 'graph.png'
    img_3 = app.config['UPLOAD_FOLDER'] + filename2 + 'graph.png'

    return render_template('graphs.html', url = 'load', img_1 = img_1, img_2 = img_2, img_3 = img_3)

from werkzeug.utils import secure_filename
import os

if __name__ == "__main__":
  app.run(debug=True)
