# Copyright (c) 2017 Thomas Chiroux
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.widget import base
import subprocess


class ConnectionStatus(base.ThreadedPollText):
    """A simple widget to display if a given Vconnection is launched or not.

    This widget uses (so: needs) network manager's nmcli tool.

    A classic (and default) use case is to check if a vpn is ON or OFF and
    display a corresponding lock icon.

    setup the 'name' option to parse the output of the nmcli command.
    """

    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 30, "Update time in seconds."),
        ("name", 'vpn', "name"),
        ("color_ok", "55cc55", "color_ok"),
        ("color_nok", "cc5555", "color_nok"),
        ("fmt_ok", "\U0001F510", "fmt_ok"),
        ("fmt_nok", "\U0001F513", "fmt_nok"),
    ]

    def __init__(self, **config):
        """Initalise VpnStatus widget."""
        base._TextBox.__init__(self, **config)
        self.add_defaults(ConnectionStatus.defaults)
        self.last_output = ''

    def poll(self):
        """Use nmcli to poll connexion status."""
        args = "nmcli c show --active"  # .split(' ')
        p1 = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True)
        p2 = subprocess.Popen(["grep", self.name],
                              stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        stdout, stderr = p2.communicate()
        if p2.returncode == 0:
            # ok we can find a connection
            self.last_output = stdout.decode('utf-8')
            self.layout.colour = "55cc55"
            return(self.fmt_ok)
        else:
            self.last_output = ''
            self.layout.colour = "cc5555"
            return(self.fmt_nok)

    def button_press(self, x, y, button):
        """handle mouse button press on the widget."""
        if button == 1 and self.last_output:  # left click
            network_name = self.last_output.split(' ')[0]
            subprocess.call(
                '/usr/bin/notify-send -u low -t 1000 -a ConnectionStatus '
                '-c info "connected to: %s"' % network_name, shell=True)
