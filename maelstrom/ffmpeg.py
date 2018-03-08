import subprocess


def get_duration_seconds(path):
    output = subprocess.run(['ffmpeg', '-i', path],
                            stderr=subprocess.PIPE)
    for l in output.stderr.decode().split('\n'):
        line = l.strip()
        if line.startswith('Duration: '):
            duration_str = line.split()[1][:-1]
            hours, minutes, seconds = duration_str.split(':')

            hours = int(hours)
            minutes = int(minutes)
            seconds = float(seconds)

            duration = \
                (hours * 60 * 60) + \
                (minutes * 60) + \
                (seconds)

            return duration
