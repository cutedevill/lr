# -*- coding: utf-8 -*-
print('Hello world')
from flask import Flask
app = Flask(__name__)

# decorator dlya vivoda stranitcy po umolchaniu

from flask import render_template, request
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'PLACE KEY FROM GOOGLE HERE'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'PLACE SECRET KEY FROM GOOGLE HERE'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
@app.route("/data_to")
def data_to():
  some_pars = {'user':'Ivan', 'color':'red'}
  some_str = 'Hello my dear friends!'
  some_value = 10

  return render_template('simple.html', some_str = some_str, some_value = some_value,
                          some_pars = some_pars)

@app.route("/", methods = ("GET", "POST"))
def hello():
  return "<html><title>Some title</title><body><h1>Some text<h1></body></html>"

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)

class NetForm(FlaskForm):
  openid = StringField('openid', validators = [DataRequired()])
  upload = FileField('Load image', validators = [
                      FileRequired(),
                      FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
  recaptcha = RecaptchaField()
  submit = SubmitField('send')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = 'static/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/load', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and (file.content_type.rsplit('/', 1)[1] in ALLOWED_EXTENSIONS).__bool__():
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER'] + filename)
            return render_template('main.html', image_name = app.config['UPLOAD_FOLDER'] + filename)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

from werkzeug.utils import secure_filename
import os
# import clr as neuronet

# '''@app.route("/net", methods=['GET', 'POST'])
# def net():
#   form = NetForm()
#   filename = None
#   neurodic = {}
#
#   if form.validate_on_submit():
#     filename = os.path.join('./static', secure_filename(form.upload.data.filename))
#     fcount, fimage = neuronet.read_image_files(10, './static')
#
#     decode = neuronet.getresult(fimage)
#
#     for elem in decode:
#       neurodic[elem[0][1]] = elem[0][2]
#     form.upload.data.save(filename)
#   return render_template('net.html',form = form, image_name = filename, neurodic = neurodic)
#     '''
if __name__ == "__main__":
  app.run(debug=True)
