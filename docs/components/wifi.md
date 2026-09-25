# Wi-Fi & APIs

<img src="../../assets/img/icons/wifi.png" alt="" class="cc-icon">

The ESP32 has Wi-Fi built in. Once it's online, your projects can pull in
live data (weather, time, sports scores) and send messages out, like
a notification to your phone. No new parts needed!

<div class="cc-parts" markdown>
**You'll need:**

- [x] A 2.4 GHz Wi-Fi network and its password
- [x] A phone with the free **ntfy** app (for the notification example)
</div>

!!! note "2.4 GHz only"
    The ESP32 can't see 5 GHz networks. Most home routers broadcast both, so
    this is rarely a problem. School and office networks that need a login
    page after you connect won't work, though.

## Setup

### Keep your password in secrets.py

Instead of typing your Wi-Fi password into every program, keep it in one
file called `secrets.py`:

1. Open [`secrets_example.py`](https://github.com/CircuitCoder-ngh/MicroPythonStarterGuide/blob/main/code/lib/secrets_example.py)
   and copy its contents into a new file in Thonny.
2. Fill in your Wi-Fi name (`SSID`) and `PASSWORD`, keeping the quote marks.
3. Save it onto your ESP32 as `secrets.py`.

```python title="secrets.py"
--8<-- "lib/secrets_example.py"
```

!!! warning "Don't share secrets.py"
    If you post your code online or send it to a friend, leave `secrets.py`
    out. That way you never leak your password by accident.

### The wifi module

Connecting takes a few steps, so, just like `button.py`, we've wrapped them
in a module. Save
[`wifi.py`](https://github.com/CircuitCoder-ngh/MicroPythonStarterGuide/blob/main/code/lib/wifi.py)
onto your ESP32 too.

??? info "wifi.py"

    ```python title="wifi.py"
    --8<-- "lib/wifi.py"
    ```

It switches on the ESP32's **station** interface (the part that joins an
existing network, like your phone does), connects, and waits until it has
an IP address. If it hasn't connected after 20 seconds, it stops with an
error instead of waiting forever.

### Connect!

```python title="wifi_connect.py"
--8<-- "lessons/wifi_connect.py"
```

You should see something like:

```text
Connecting to MyHomeWiFi ...
Connected! IP address: 192.168.1.42
Signal strength: -58 dBm
```

Signal strength is measured in negative numbers. Closer to 0 is stronger:
−50 is excellent, and below −80 is weak.

## What's an API?

When you visit a website, the server sends back a page designed for people
to look at. An **API** (application programming interface) is a web address
built for *programs* instead. It sends back just the data, usually as
**JSON**, which looks a lot like a Python dictionary:

```json
{"current": {"temperature_2m": 18.4, "wind_speed_10m": 11.2}}
```

There are two main kinds of request:

- **GET** asks a server for data. "What's the weather?"
- **POST** sends data to a server. "Deliver this message."

MicroPython's built-in `requests` module handles both.

## GET: live weather

[Open-Meteo](https://open-meteo.com/) is a free weather API that doesn't
need an account. Change `LATITUDE` and `LONGITUDE` to your own location:
right-click a spot on Google Maps and the coordinates appear at the top of
the menu.

```python title="api_weather.py"
--8<-- "lessons/api_weather.py"
```

- `requests.get(URL)` sends the request and waits for the reply.
- `response.status_code` is `200` if everything went well. Codes in the
  400s mean something was wrong with the request (like a typo in the URL),
  and 500s mean the server had a problem.
- `response.json()` converts the JSON text into a Python dictionary, so
  `data["current"]["temperature_2m"]` digs out the temperature.
- `response.close()` frees up the memory the reply was using. The ESP32
  doesn't have much, so **always close your responses**.

!!! tip "Prefer Fahrenheit?"
    Add `&temperature_unit=fahrenheit&wind_speed_unit=mph` to the end of the
    URL. The [Open-Meteo docs](https://open-meteo.com/en/docs) list
    everything else you can ask for, from rain to UV index.

## POST: notifications on your phone

[ntfy](https://ntfy.sh/) ("notify") is a free service that pushes a
notification to your phone whenever something POSTs a message to a
**topic**. No account needed.

1. Install the **ntfy** app from your phone's app store.
2. Make up a topic name that's **long and hard to guess**, like
   `circuitcoder-alex-7f3k9q`. Topics are public: anyone who knows the name
   can read your messages, or send you some!
3. In the app, tap **+** and subscribe to your topic.
4. Put the same name in `NTFY_TOPIC` in your `secrets.py`, and save it to
   the board again.

```python title="ntfy_hello.py"
--8<-- "lessons/ntfy_hello.py"
```

Run it and your phone should buzz within a second or two. 🎉

## Getting the time

The ESP32 has a clock, but it resets to the year 2000 every time the board
restarts. The built-in `ntptime` module sets it correctly from an internet
time server:

```python title="ntp_time.py"
--8<-- "lessons/ntp_time.py"
```

The time server gives **UTC** (world time), so the code adds
`UTC_OFFSET_HOURS` from `secrets.py` to get your local time. You'll need to
change it by an hour when the clocks go forward or back. You'll use this in
the [Alarm Clock](../projects/alarm-clock.md) project.

## Challenge

Combine what you've learned: every time the button on GPIO 14 is pressed,
fetch the temperature and send it to your phone with ntfy. (No solution
this time. You've got everything you need!)

**Next up:** You've met every component. Time to build something with them:
head to the [Projects](../projects/index.md).
