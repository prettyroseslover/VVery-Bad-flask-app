from flask import render_template
import subprocess

def os_page(request, app):
    hostname = request.values.get('hostname')

    if hostname is None:
        hostname = '8.8.8.8 -c 1'

    cmd = 'ping ' + hostname

    result = subprocess.check_output(cmd, shell=True)

    return render_template('os.html', result=result)
    


def os_api(request, app):
    pass