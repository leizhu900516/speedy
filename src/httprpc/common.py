from eventlet.green import socket
import eventlet.debug
import logging

class Message(object):
  '''A simple helper class to build POD type objects.
  
  Object attributes can be set via keyword arguments in the constructor.'''
  def __init__(self, **kw):
    for k, v in kw.iteritems():
      setattr(self, k, v)

  def __repr__(self):
    kv = [(k, getattr(self, k)) for k in self.__dict__ if k[0] != '_']
    return ','.join(['%s : %s' % (k, v) for (k, v) in kv])

def dump_eventlet():
  logging.warn('Listeners:\n %s', eventlet.debug.format_hub_listeners())
  logging.warn('Timers:\n %s', eventlet.debug.format_hub_timers())

def enable_debugging():
  eventlet.debug.hub_listener_stacks(True)
  eventlet.debug.hub_timer_stacks(True)

  import atexit
  atexit.register(dump_eventlet)

def find_open_port():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(("", 0))
  s.listen(1)
  port = s.getsockname()[1]
  s.close()
  return port

def split_addr(hostport):
  host, port = hostport.split(':')
  return host, int(port)