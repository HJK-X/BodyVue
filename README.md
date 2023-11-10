# BodyVue

#### Objective:
This project creates a measurement device for estimating body fat percentage. We integrate techniques in computer vision and embedded system design via mounting a camera on a programmed rotating mechanical arm to capture data which we then send to the cloud for computing into the estimated value. 

RISKS, RESOURCES:
  - NERF is still an emerging technology with limited resources and frameworks in the application of body fat estimation. Researching and developing our application may take time and require us to remain flexible in other aspects of the project design.
  - The mechanical build could prove to be costly and/or technical. There are specific design challenges needed to develop a CPS that works within our goals within a desired budget and with limited time and access to mechanical expertise and tools. 
  - NERF is being developed at UC Berkeley and scientific advising from researchers on campus is a necessary resource.
  - Existing research as well as software for NERF, such as nerfstudio, is available
  - UC Berkeley provides a MakersSpace and wood cutting work areas making wood a viable cost-effective option

Stages:
STAGE ONE (Current): 
a. Model the CPS, the mechanical frame and the process of collecting data and transmitting it
    - May require additional research and may be updated as b is pursued
b. Research and develop the techniques for estimating body fat
c. Build
    - See materials section, see part a

MODEL:
https://cad.onshape.com/documents/1690b7961daa5385eab02831/w/c3eccbb35e9dc502be3e9784/e/fe6c83db17739d6f8b106a67?renderMode=0&uiState=6541fc8abfbc6356464c7dd8

MATERIALS:
  - Raspberry Pi 4
    https://www.canakit.com/raspberry-pi-4.html
    https://www.canakit.com/raspberry-pi-camera-module-3.html

  - Turntable
    https://www.amazon.com/Dailydanny-Aluminum-Rotating-Turntable-Dining-Table/dp/B086PMFKPL

  - Wood (platforms)

  - Caster Wheel
    https://www.amazon.com/ASHGOOB-Casters-Locking-Polyurethane-Castors/dp/B085RQFMYR

STAGE TWO:
a. Develop module for estimating body fat
b. Develop code for synchronizing CPS (highly dependent on part a):
  - Rotate arm for desired duration
  - Set up camera to capture data
  - Send data to cloud for computing
