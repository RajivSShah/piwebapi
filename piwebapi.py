"""
PiWebAPI

REQUIREMENTS:
Uses:
- Flask for the web application
- mpd and mpc for playing internet radio streams
-- mpd playlists must be manually configured outside this application
- YouTube playback functionality with mpsyt and mpv only works with Python3

NOTES:
- All variables are hard-coded so anybody else who want to use this
  app will have to modify the source code
"""

from flask import Flask, render_template, request
import subprocess
import alsaaudio

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('main.html')

@app.route("/radio_play_stn_1")
def radio_play_stn_1():
	subprocess.check_output(["mpc", "play", "1"])
	return render_template('main.html')

@app.route("/radio_play_stn_2")
def radio_play_stn_2():
	subprocess.check_output(["mpc", "play", "2"])
	return render_template('main.html')

@app.route("/radio_play_stn_3")
def radio_play_stn_3():
	subprocess.check_output(["mpc", "play", "3"])
	return render_template('main.html')

@app.route("/stop_radio")
def stop_radio():
	subprocess.check_output(["mpc", "stop"])
	return render_template('main.html')

@app.route("/vol_up")
def vol_up():
	m = alsaaudio.Mixer('PCM')
	current_volume = m.getvolume()
	if current_volume[0] < 95 :
#		print (current_volume[0])
		m.setvolume(current_volume[0] + 5)
	return render_template('main.html')

@app.route("/vol_down")
def vol_down():
	m = alsaaudio.Mixer('PCM')
	current_volume = m.getvolume()
	if current_volume[0] > 10 :
#		print (current_volume[0])
		m.setvolume(current_volume[0] - 5)
	return render_template('main.html')

@app.route("/play_youtube/<string:song>")
def play_youtube(song):
	try:
		playshell = \
			subprocess.Popen(["mpsyt",""] \
				,stdin=subprocess.PIPE ,stdout=subprocess.PIPE)
		playshell.stdin.write(bytes('/' + song + '\n1\n', 'utf-8'))
		playshell.stdin.flush()
		return render_template('main.html')
	except:
		return render_template('main.html')

@app.route("/stop_youtube")
def stop_youtube():
	subprocess.Popen(["/usr/bin/pkill","mpsyt"],stdin=subprocess.PIPE)
	subprocess.Popen(["/usr/bin/pkill","mpv"],stdin=subprocess.PIPE)
	return render_template('main.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=1024, debug=True)

