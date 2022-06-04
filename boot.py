# This file is executed on every boot (including wake-boot from deepsleep)
import esp
from connect import *

esp.osdebug(None)

do_connect()
