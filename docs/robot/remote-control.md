# Wi-Fi Remote Control

<img src="../../assets/img/icons/wifi.png" alt="" class="cc-icon">

Time to take the controls! In this final robot lesson, the ESP32 creates its
**own Wi-Fi network** and hosts a tiny **web page** with driving buttons.
Connect your phone to the robot, open the page, and drive it around like a
remote-control car. No app to install, and no home Wi-Fi needed, so it works
anywhere.

<div class="cc-parts" markdown>
**You'll need:**

- [x] Your robot (the sensors can stay on; this program doesn't use them)
- [x] A phone, tablet or laptop with Wi-Fi and a web browser
- [x] `robot.py` saved on the ESP32
</div>

## How it works

### The robot is the Wi-Fi hotspot

Normally, your ESP32 **joins** a Wi-Fi network, like your phone joins your
home router. That's called **station** mode. But the ESP32 can also **be**
the network, like a phone's personal hotspot. That's **access point** mode:

```python
ap = network.WLAN(network.WLAN.IF_AP)
ap.config(ssid="CircuitCoder-Robot", key="drive-me-123",
          security=network.WLAN.SEC_WPA2)
ap.active(True)
```

Your phone connects to the network called **CircuitCoder-Robot**, and the
robot is always at the address **192.168.4.1** on its own network.

!!! note "No internet on this network"
    The robot's hotspot isn't connected to the internet. Your phone may warn
    you about that, or even try to switch back to your home Wi-Fi or mobile
    data. Tell it to **stay connected**.

### The robot is also a web server

When you type an address into a browser, it sends a **request** to a
server, a bit like a letter asking for a page. The server sends back a
**response** with the page inside. The robot runs a tiny web server that
understands two requests:

| The browser asks for | The robot sends back |
|---|---|
| `GET /` | The remote control page (HTML and a little JavaScript) |
| `GET /go?cmd=forward&speed=70` | Drives forwards at 70 %, and replies "OK" |

The bit after the `?` is called a **query string**. It's a simple way to pass
information in a web address: `cmd` says which way to go, and `speed` says how
fast.

### The buttons

The web page has five big buttons and a speed slider. While you **hold** a
button, the page sends that command every 200 ms. When you let go, it sends
`stop`.

## Safety first: the "dead man's switch"

What if your phone goes out of range, or the browser freezes, just as the
robot is driving towards the stairs? The `stop` message would never arrive.

To handle this, the robot uses a **dead man's switch** (a name that comes from
trains, where the driver has to keep holding a handle). The robot only keeps
moving while commands keep arriving. If it hears nothing for **0.7 seconds**
while moving, it stops by itself. That's why the page repeats the command
while you hold a button, instead of sending it just once.

## Code

Save this to the ESP32 as **`main.py`**. Change `HOTSPOT_PASSWORD` to your
own password (at least 8 characters) first!

```python title="remote_control.py"
--8<-- "robot/remote_control.py"
```

## Drive it!

1. Switch on the robot's battery pack and power the ESP32 from the power
   bank.
2. On your phone, open the **Wi-Fi settings** and join **CircuitCoder-Robot**,
   using the password you set.
3. Open the web browser and go to **http://192.168.4.1**
4. Hold the arrows to drive. Use the slider to change speed.

!!! tip "Can't connect?"
    - Plug the ESP32 into your computer and check the Shell. It prints the
      network name and the address to open.
    - Make sure you typed **http://**, not https://. The robot doesn't do
      encrypted connections.
    - If the page loads but the buttons do nothing, check the battery
      pack's switch.

## How the code works

### The main loop does two jobs

```python
server.settimeout(0.05)
```

`server.accept()` waits for a browser to connect. Normally it would wait
**forever**, and the robot couldn't do anything else in the meantime. With a
50 ms timeout, it gives up quickly if nobody's there, which lets the loop
check the dead man's switch too. So every time round the loop:

1. **Answer a request,** if one is waiting.
2. **Check the dead man's switch:** if the robot is moving and the last
   command was too long ago, stop.

### Reading the request

The first line of every request looks like this:

```text
GET /go?cmd=forward&speed=70 HTTP/1.1
```

`parse_request()` splits it into the **path** (`/go`) and a **dictionary** of
the query values (`{"cmd": "forward", "speed": "70"}`), using nothing more
than the string `split()` method. The speed arrives as text, so it's turned
into a number with `int()`, and clamped between 30 and 100 in case
anyone sends something silly.

### The web page lives in the program

The whole page, its HTML (layout), CSS (colours and sizes) and JavaScript
(the button behaviour), is stored in one big string called `PAGE`. You don't
need to know those languages to use it, but it's worth a look. Try changing
the button colours in the `<style>` section!

## Make it your own

- **Horn:** add a button to the page that sends `/go?cmd=horn`, and make the
  robot beep the buzzer when it gets it.
- **Distance readout:** add a `/distance` request that replies with the
  ultrasonic sensor's reading, and have the page show it, updating every
  half-second.
- **Crash protection:** combine this with the
  [Obstacle Avoider](obstacle-avoider.md) so that the robot refuses to drive
  forwards when something is too close, even if you tell it to.
- **Your home network:** instead of a hotspot, connect the robot to your home
  Wi-Fi with `wifi.connect()` (from the [Wi-Fi & APIs](../components/wifi.md)
  lesson), and drive it from any device in the house.
- **Tank steering:** replace the arrows with two sliders, one for each
  wheel, and send them straight to `robot.drive(left, right)`.

## You built a robot!

Take a moment to look at what you've made. Your robot has:

- **Actuators** (motors) that move it,
- **Sensors** (ultrasonic and infrared) that let it perceive the world,
- a **controller** (the ESP32) running code that makes decisions, and
- **communication** (Wi-Fi) so it can talk to other devices.

That's every major piece of a real robot. From here, you can add more
sensors, an arm with servos, a camera, or a completely different body.
Whatever you build next, you know how the parts fit together.
