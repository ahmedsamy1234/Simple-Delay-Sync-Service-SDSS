# Simple-Delay-Sync-Service-SDSS

## Intro 🚪
Now That you understand how to use sockets, let's get a little bit deeper on how they work, we'll know how the kernel network stack deals with packets since we'll be rolling our own network stack to process ethernet (L2) packets.
Manipulating packets at this level is essential when building VPNs, virtualization technologies or implementing networking stacks for small embedded devices that can't support an operating system; Think about connected sensors, IoT devices and also devices in cars and so on.
This is totally invisible to us in university since our eco system isn't enough developed yet, but things change fast and you should either be ready or drive that change. 

## Objective 🔍
* Know the difference between a network interface and a socket
* Know the difference between TUN & TAP
* Make a new internet device using Linux's system interface
* Simulate some layers in the kernel's network stack
* Get more familiar with the networking tools in Linux

## Requirements
### Operating System: Linux
You're required to implement a network stack, starting from a TAP device then build support for ARP, ICMP and UDP protocols.
By the end of this project, you should be able to bind a UDP socket to the IP of the device you allocated (from another program) and send UDP packets using that socket normally. Then, using the TAP Fd (file descriptor) you have you'll be able to craft a reply and send it to the poor socket that doesn't know what's happening on the other side. This image will help illustrate the final output.

<p align="center">
  <img src="https://github.com/OmarReda/Simple-Delay-Sync-Service-SDSS/blob/main/Diagram.png" width="600">
</p>


## Testing your code
You'll incrementally test the code depending on the layer you're implementing. Wireshark will still be useful.
After you've finished implementing the UDP layer, you'll test it as in the provided image.

## Resources
* TUN/TAP tutorial <a href="https://web.archive.org/web/20200422190936/https://hechao.li/2018/05/21/Tun-Tap-Interface/" target="blank">here</a> (must read)
* Another TUN/TAP tutorial <a href="https://web.archive.org/web/20200422190936/https://hechao.li/2018/05/21/Tun-Tap-Interface/" target="blank">here</a> 
* Building a TCP/IP stack <a href="https://web.archive.org/web/20200422190936/https://hechao.li/2018/05/21/Tun-Tap-Interface/" target="blank">here</a> (must read)
* TAP lab <a href="https://hechao.li/2018/06/08/TAP-Interface-Lab/" target="blank">here</a>

## RFCs
* IP RFC <a href="https://tools.ietf.org/html/rfc791" target="blank">here</a>
* UDP RFC <a href="https://tools.ietf.org/html/rfc768" target="blank">here</a>
