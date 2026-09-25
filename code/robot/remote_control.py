# Wi-Fi Remote Control: the robot makes its own Wi-Fi hotspot and serves
# a web page with driving buttons. Join the hotspot on your phone, then
# open http://192.168.4.1 in the browser.
import socket
import time
import network
from robot import Robot

HOTSPOT_NAME = "CircuitCoder-Robot"
HOTSPOT_PASSWORD = "drive-me-123"   # at least 8 characters: change it!
DEADMAN_MS = 700    # stop if no command arrives for this long

PAGE = """<!DOCTYPE html>
<html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Robot Remote</title>
<style>
body { font-family: sans-serif; background: #0e1116; color: #fff;
       text-align: center; margin: 0; padding: 20px;
       user-select: none; -webkit-user-select: none; }
.pad { display: grid; grid-template-columns: repeat(3, 90px);
       gap: 12px; justify-content: center; margin: 24px 0; }
button { height: 90px; font-size: 40px; border: 0; border-radius: 16px;
         background: #1a8fe6; color: #fff; touch-action: none; }
button:active { background: #ffd23f; color: #000; }
#stop { background: #e63946; font-size: 22px; }
input { width: 280px; }
</style></head><body>
<h2>Robot Remote</h2>
<div class="pad">
  <span></span><button data-cmd="forward">&#9650;</button><span></span>
  <button data-cmd="left">&#9664;</button>
  <button id="stop" data-cmd="stop">STOP</button>
  <button data-cmd="right">&#9654;</button>
  <span></span><button data-cmd="backward">&#9660;</button><span></span>
</div>
<p>Speed: <span id="val">70</span>%</p>
<input id="speed" type="range" min="30" max="100" value="70">
<script>
const speed = document.getElementById("speed");
speed.oninput = () => document.getElementById("val").textContent = speed.value;
let current = "stop", repeat = null;
function send(cmd) {
  fetch("/go?cmd=" + cmd + "&speed=" + speed.value).catch(() => {});
}
function press(cmd) {
  current = cmd; send(cmd);
  clearInterval(repeat);
  // keep repeating while held, so the robot knows we're still here
  repeat = setInterval(() => send(current), 200);
}
function release() {
  clearInterval(repeat); current = "stop"; send("stop");
}
document.querySelectorAll("button").forEach(b => {
  b.addEventListener("pointerdown", e => { e.preventDefault(); press(b.dataset.cmd); });
  ["pointerup", "pointercancel", "pointerleave"].forEach(ev =>
    b.addEventListener(ev, release));
});
</script>
</body></html>
"""

robot = Robot()


def start_hotspot():
    ap = network.WLAN(network.WLAN.IF_AP)
    ap.config(ssid=HOTSPOT_NAME, key=HOTSPOT_PASSWORD,
              security=network.WLAN.SEC_WPA2)
    ap.active(True)
    while not ap.active():
        time.sleep_ms(100)
    address = ap.ipconfig("addr4")[0]
    print("Join the Wi-Fi network", HOTSPOT_NAME)
    print("Then open http://" + address)


def parse_request(request):
    # "GET /go?cmd=forward&speed=70 HTTP/1.1" -> ("/go", {"cmd": "forward", "speed": "70"})
    first_line = request.split("\r\n", 1)[0]
    parts = first_line.split(" ")
    if len(parts) < 2:
        return None, {}
    path = parts[1]
    query = {}
    if "?" in path:
        path, query_string = path.split("?", 1)
        for pair in query_string.split("&"):
            if "=" in pair:
                key, value = pair.split("=", 1)
                query[key] = value
    return path, query


def run_command(cmd, speed):
    # returns True if the robot is now moving
    if cmd == "forward":
        robot.forward(speed)
    elif cmd == "backward":
        robot.backward(speed)
    elif cmd == "left":
        robot.spin_left(speed * 2 // 3)   # spins are gentler, easier to aim
    elif cmd == "right":
        robot.spin_right(speed * 2 // 3)
    else:
        robot.stop()
        return False
    return True


def send_response(client, status, content_type, body):
    client.sendall(("HTTP/1.1 " + status + "\r\n"
                    "Content-Type: " + content_type + "\r\n"
                    "Connection: close\r\n\r\n").encode())
    client.sendall(body.encode())


start_hotspot()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 80))
server.listen(2)
server.settimeout(0.05)   # don't wait forever for a visitor

moving = False
last_command = time.ticks_ms()

while True:
    # 1. Answer a web request, if one is waiting
    try:
        client, address = server.accept()
    except OSError:
        client = None   # nobody knocked: carry on

    if client:
        try:
            client.settimeout(1)
            request = client.recv(1024).decode()
            path, query = parse_request(request)
            if path == "/":
                send_response(client, "200 OK", "text/html", PAGE)
            elif path == "/go":
                try:
                    speed = max(30, min(100, int(query.get("speed", "70"))))
                except ValueError:
                    speed = 70
                moving = run_command(query.get("cmd", "stop"), speed)
                last_command = time.ticks_ms()
                send_response(client, "200 OK", "text/plain", "OK")
            else:
                send_response(client, "404 Not Found", "text/plain", "Not found")
        except (OSError, ValueError):
            pass   # the phone hung up early or sent garbage: no problem
        client.close()

    # 2. Safety: if the phone goes quiet while we're moving, stop
    if moving and time.ticks_diff(time.ticks_ms(), last_command) > DEADMAN_MS:
        robot.stop()
        moving = False
        print("No signal: stopped")
