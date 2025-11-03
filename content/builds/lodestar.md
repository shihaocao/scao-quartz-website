---
title: "Lodestar: An Electric VTOL Rocket"
date: 2025-02-23
tags:
  - drone
  - build
  - software
---

## Lodestar: An Electric VTOL Rocket

[Back to builds](/builds/builds-landing)

<div style="display: flex; justify-content: center;">
  <img src="builds/images/lodestar/lodestar.jpg" alt="Lodestar" style="max-width: 100%;">
</div>

<div style="text-align: center; font-style: italic;">An homage to SpaceX's Starship, Lodestar is a single-point thrust vectoring VTOL drone.</div>

[**Watch it Fly!**](https://govindchari1.wixsite.com/portfolio/vtol-rocket)

I worked on this project with Govind Chari! Check out his site [here](https://govindchari1.wixsite.com/portfolio/vtol-rocket).


## 2024 Update

<div style="display: flex; align-items: flex-start;">
  <div style="flex: 1; display: flex; justify-content: center; max-width: 100%; margin: 0 5px;">
    <img src="builds/images/lodestar/vvtol_on_desk.jpeg"
         style="height: auto; vertical-align: middle;">
  </div>
  <div style="flex: 1; display: flex; justify-content: center; max-width: 100%; margin: 0 5px;">
    <img src="builds/images/lodestar/vvtol_v1_pcb_design.jpg"
         style="height: auto;">
  </div>
</div>
</div>
<div style="display: flex; align-items: flex-start;">
  <div style="flex: 1; text-align: center; font-style: italic;">Assembled board + chassis</div>
  <div style="flex: 1; text-align: center; font-style: italic;">Board in KiCAD</div>
</div>


I am also working on an updated version here, pics/documentation on [github here](https://github.com/shihaocao/vvtol)

---

## Introduction

Lodestar is a small-scale electric vertical takeoff and landing (VTOL) project that I worked on with Govind Chari over the summer of 2020. I was in Hawthorne, so I designed the craft and wrote the flight software. My partner, Govind, built and tested the vehicle and also wrote the guidance, navigation, and control (GNC) code. By the end of the summer, the vehicle could take off and land vertically. The objective was to understand the challenges of creating a vehicle that could take off and land vertically using thrust vectoring only—similar to the Falcon 9.

---

## Years Before

The first attempts at this project actually started back in 2017 before I had even met Govind. Together with Matthew Cox and Jude Bedessem, we studied how to build a similar system for the recovery of high-power rockets. While they worked on the rocketry side of the project, I led the way on the recovery side with two pathfinder vehicles for an electric motor vertical landing system.

---

## Pathfinder 1 - EDF Thrust Vectoring

<div style="display: flex; justify-content: center;">
  <img src="builds/images/lodestar/edf-vectoring.jpg" alt="EDF Thrust Vectoring" style="max-width: 100%;">
</div>

This initial pathfinder taught me how to build thrust vectoring actuators, and I was also able to test using an EDF as a main power system. I realized that the torque delivered from the motor needed significant compensation. Additionally, an EDF-sized system was too large and heavy for safe prototyping. This led me to target a lighter, smaller system for the next iteration.

---

## Pathfinder 2 - Counter Rotating Props and Active Control

<div style="display: flex; justify-content: center;">
  <img src="builds/images/lodestar/counter-rotating.jpg" alt="Counter Rotating Props" style="max-width: 100%;">
</div>

On this iteration, I tested using a commercial flight computer—the Pixhawk 4—and two counter-rotating propellers. This version also used a similar fin-based thrust vectoring system. In the picture above, you'll see it hanging from strings as a partial free-hanging system to test roll control. This prototype showed that the split prop design had a much better thrust-to-weight ratio, but the Pixhawk flight computer did not have sufficient customization for this task. I would repeat the same mechanical and electrical design, but the software and control stack would need an upgrade.

---

## Lodestar Design

Using lessons learned from my past designs, the bill of materials and overall system design (mass budget, power budget, etc.) were easy to get right on the first try. I chose to use two counter-rotating quadcopter motors to cancel torque and ensure centerline thrust. Roll control was achieved through differential thrust, while pitch and yaw were controlled through thrust vectoring vanes actuated by servos inside the thrust structure. The two motors had separate power systems, with one also powering the avionics stack.

---

## Flight Software and Ground Software

The flight software for this vehicle was derived from the flight software on PAN (my satellite team). This gave me the fine-grained control that I lacked in previous commercial flight computers. I wrote all the code to parse orientation and position data from the onboard IMU and barometer. I developed a mission manager state machine to guide the craft through sensor initialization, flight, and post-landing. To aid with initial development, I built a custom NodeJS-based web ground station. I also wrote the boilerplate code that my partner used for guidance, navigation, and control.

[**Lodestar GitHub Repository**](https://github.com/shihaocao/lodestar)

Here’s a screenshot of the ground station relaying live telemetry through the radio system:

<div style="display: flex; justify-content: center;">
  <img src="builds/images/lodestar/lodestar_gs.jpg" alt="Lodestar Groundstation" style="max-width: 100%;">
</div>

---

## Iteration

I worked with my partner to develop an iterative testing campaign to guide us to full mission success. We created a MATLAB simulation to verify simple attitude control PID loops. After building the craft, we conducted thrust testing to confirm that it had a thrust-to-weight ratio greater than one. To aid in development and diagnose flight failures, I added SD-card data logging for post-flight analysis.

---

## Roll Control

We verified the full control loop from sensors to actuators by allowing movement only in the roll axis. This confirmed that the craft could maintain a steady roll angle.

---

## Final Flights

After extensive testing and multiple complete rebuilds of the vehicle, Lodestar successfully performed a vertical takeoff and landing after the **23rd test flight**.

---

This should be Quartz-ready, keeping the same structure and readability while making it more web-friendly! Let me know if you need any tweaks! 🚀
