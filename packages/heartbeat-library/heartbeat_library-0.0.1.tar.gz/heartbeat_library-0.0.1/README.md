# Python Heartbeat Library

The Python Heartbeat Library is a simple utility that allows you to send regular "pulses" to a specific endpoint. These pulses serve as confirmation that your main script is functioning correctly. If the main script stops for any reason, the heartbeat will also cease, indicating that something went wrong.

# Installation

You can install the Python Heartbeat Library using pip:

pip install heartbeat

# Example

```python
===============================================================================================================================
from heartbeat import defineUrl, heartbeat

# Set the URL for sending pulses
defineUrl("https://")

# Start the heartbeat with a pulse every 10 seconds
heartbeat(interval = 600, name = 'process name', description = 'process description', additional_info = '', show_response = True)

# Your main script logic goes here...

# When your script ends or encounters an error, stop the heartbeat
killHeartbeat()
===============================================================================================================================
```

# License

This project is licensed under the MIT License - see the LICENSE file for details.
