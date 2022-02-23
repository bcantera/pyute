"""Constants used by PyUTE, inspired on mobile app requests."""

UTE_API_URL = "https://rocme.ute.com.uy/api"
APP_HEADERS = {
    "X-Client-Type": "Android",
    "Content-Type": "application/json",
    "charset": "utf-8",
    "Host": "rocme.ute.com.uy",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.8.1",
}
LOGIN_HEADERS = {
    "RefreshedNotification": "false",
    "UniqueId": "null",
}
