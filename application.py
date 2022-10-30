import os
from flask import Flask, flash, request, redirect, render_template,url_for, send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
from record_linkage import record_linkage_func
import remove_files



app=Flask(__name__,static_url_path='/static')
app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path=os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'input')
STATIC_FOLDER = os.path.join(path, 'templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER
# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        remove_files.remove_input()
        remove_files.remove_output()
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')

        if len(files)!=2:
            flash('Please Upload Two Files')
            return redirect('/')
        list_df=[]
        for file in files:

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                save_location = (os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
                df=pd.read_csv(save_location)
                list_df.append(df)
            else:
                 flash('Please upload files again - not of correct CSV format')   
                 return redirect('/')
        Flag,output=record_linkage_func(list_df)
        for f in os.path.dirname('input'):
            os.remove(f)
        if Flag==0:
            flash("Columns missing From File 1  " +output[0]+ "    Columns missing From File 2  "+output[1])
            return redirect('/')
        else:    
            return redirect(url_for('download'))

@app.route('/download')
def download():
    return render_template('download.html', files=os.listdir('output'))
    
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('output', filename)
if __name__ == "__main__":
    app.run(host='0.0.0.0')