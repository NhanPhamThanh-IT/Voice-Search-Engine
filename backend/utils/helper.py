"""
This module provides a function to retrieve the IPv4 address of the local machine.

Function:
1. get_ipv4_address():
   - Retrieves the IPv4 address of the local machine by resolving the hostname.
   - Uses the `socket` library to get the machine's hostname and resolve it to its corresponding IP address.
   - Returns:
     - The IPv4 address of the machine as a string.

Dependencies:
- socket: For network-related functions, including retrieving the hostname and resolving it to an IP address.
"""

# Import the required libraries
import socket

# Function to retrieve the local IPv4 address of the machine
def get_ipv4_address():
    """
    Retrieves the local IPv4 address of the machine.

    The function uses the socket library to obtain the hostname of the machine
    and then resolves it to an IPv4 address.

    Returns:
        str: The local IPv4 address of the machine.
    
    Example:
        If the machine's local address is 192.168.1.100, the function will return "192.168.1.100".
    """
    hostname = socket.gethostname()
    ipv4_address = socket.gethostbyname(hostname)
    return ipv4_address
