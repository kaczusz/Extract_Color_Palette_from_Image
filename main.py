from flask import Flask, url_for, render_template, send_from_directory
import datetime
from flask_wtf import FlaskForm
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, IntegerField
from get_colors import extract_colors



app = Flask(__name__)
app.secret_key = "asdasdaasdasdaqwrfnf"
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class SettingForm(FlaskForm):
    image = FileField('Select Image File:', validators=[FileRequired(), FileAllowed(photos, 'Only images are allowed')])
    num_of_colors = IntegerField('Number of colors:', default=10)
    delta = IntegerField('Tolerance (0-100):', default=12)
    submit = SubmitField('Get Palette')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route("/", methods=['POST', 'GET'])
def home():
    palette = extract_colors()
    form = SettingForm()
    year = datetime.date.today().year
    if form.validate_on_submit():
        filename = photos.save(form.image.data)
        file_url = url_for('get_file', filename=filename)
        fname = file_url[1:]
        palette = extract_colors(fname, int(form.num_of_colors.data), int(form.delta.data))
    else:
        file_url = None
    return render_template('index.html', year=year, form=form, palette=palette, file_url=file_url)


if __name__ == "__main__":
    app.run(debug=True)