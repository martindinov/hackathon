# Hack the brain hackathon 2015

Team : Alain, Justin, Harry, Andrew, David and Martin   
Goal : Create a centralized social platfoem for visualizing different people's brainwaves for games and other interactions   
# Hackathon TODOs

## Pre-hackathon:
1. Set up 2 (or 3, just in case) Pis with an appropriate Linux distro (like Raspbian). Make sure we have wireless cards available for all of them (I have 1-2, will check before hackathon).
2. Set up git repo clone on each Pi, as well as sshd (should be on by default) and VNC.
3. Create checklist of all cables, electronics, etc that we need and make sure we have them and we bring them to event.

## Hackathon:

The following can be done fully in parallel, I think (in brackets for who will be working on these things mostly):

1. Intercept Zigbee packets, decode and re-format (into XML or json), then send to a specifiable host/port for server processing (visualization and stuff). (Martin)

2. Basic server interface to accept XML/json data on some port as used by client. Data to be unpacked and displayed in some basic graph form in real-time or almost real-time. (Alain (+Martin?))

3. An easy to call (from Python or PHP) Python code that outputs sine oscillations from audio jack. Should be configurable regarding volume, frequency and length of sound. (David and Andrew (+ Martin?))

4. Pin control and driving basic DC circuit (Martin (+ Andrew and David?))

5. Basic receiver/client interface to control pins/DC stimulation protocol. By clicking on buttons and selecting appropriate Voltage or time values, you can start the stimulation. (Martin (+everyone else?))

6. EEG DSP stuff (filtering, band passing, etc), so we can then use processed EEG (say, alpha or beta power) as inputs to neurofeedback software module, if there's time. If not, we've created the possibility to do that (e.g. in future iterations) and we can also send filtered data over to server to be displayed as well. (Martin (+ whoever else))
