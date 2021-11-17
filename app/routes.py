import base64
from datetime import datetime as dt
from datetime import timedelta
from flask import render_template, request, url_for, make_response, redirect, flash
from io import BytesIO
from matplotlib.figure import Figure
import obspy
from os import getcwd

from app import app
from app.forms import PlotForm

def get_stream(date, length, url):
    stream = obspy.Stream()
    station_codes = ('I44H1**BDF', 'I44H2**BDF', 'I44H3**BDF', 'I44H4**BDF', )
    for station_code in station_codes:
        traces = obspy.read(f'{url}?DATREQ={station_code}+{date:%Y/%m/%d+%H:%M:%S}+{str(length)}')
        for trace in traces:
            stream.append(trace)
        # trace.filter('highpass', freq=1.0, corners=2, zerophase=True)
    return stream

def plof_figure(stream):
    buf = BytesIO()
    fig = stream.plot(color='blue')
    plt = fig.savefig(buf, format="png")
    image = base64.b64encode(buf.getbuffer()).decode("ascii")
    return image

def render_plot(form, template_context):
    return render_template('plot_and_download.html', form=form,  **template_context)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/err/')
def http_404_handler():
    return make_response("<h2>404 Error</h2>")

@app.route('/plot_and_download/', methods=['GET', 'POST'])
def plot_and_download():
    form = PlotForm(request.form)

    if form.validate_on_submit():
        date = dt.strptime(request.form.get('date')+request.form.get('time'), "%Y-%m-%d%H:%M")
        length_in_hours = request.form.get('length')
        length = round(timedelta(hours=int(request.form.get('length'))).total_seconds())
        urls = ('http://arcy.kfgs.ru:9000/', 'http://hub1.emsd.ru:9000/')
        
        if (dt.now() - date).days > 90:
            stream = get_stream(date, length, urls[0])
        else:
            stream = get_stream(date, length, urls[1])
        
        if form.plot.data:
            template_context = dict(data=plof_figure(stream),
                               date=f'{date:%Y-%m-%d}',
                               time=f'{date:%H:%M}',
                               length=length_in_hours
                               )
            return render_plot(form, template_context)

        elif form.download.data:
            buffer = BytesIO()
            stream.write(buffer, 'MSEED')
            resp = make_response(buffer.getvalue())
            resp.mimetype = 'application/octet-stream'
            resp.headers['Content-Disposition'] = f'attachment;filename={date:%Y_%m_%d_%H%M}.mseed'
            return resp

    return render_template('plot_and_download.html', form=form)

@app.route('/test/', methods=['GET', 'POST'])
def test():
    message = ''
    if  request.method == 'POST':
        print(request.form['text'])
        if request.form['submit_button'] == 'Plot':
            print('Plot')
            flash('Plot '+request.form.get('text'))
            return redirect(url_for('test', message=message))
        elif request.form['submit_button'] == 'Download':
            print('Download')
            flash('Download '+request.form.get('text'))
            return redirect(url_for('test'))
    return render_template("test.html", message=message)
