Overview for AI agent who will write this: The text below is the scraped web text from the old site. you must review this and rebuild the whole thing. consider what images may have fitted in where and add them in. all images should be included. feel free to rework the text to be better. the current status which isnt added is that ive tuned both speakers and fully implemented the cascade system so i have a very powerful speaker system that plays down to 40Hz. My next steps when i have time are to calibrate and measure them, as well as do some aesthethic updates like vinyl wrapping or 3D printing some exterior designs and bonding them on.


Write ups pending - This one is an active WIP as of Nov 2025

Enjoyed making some speakers, wanted just a bit more oomph

Needed to be manufacturable in a small london flat with minimal tools and space - bambu a1 mini 180mm3 3d printer is the main workhorse here

I started off with a few conceptual designs. Firstly, an omnidirectional design:

ruled this out because omnidirectional speakers are great, unless you put them up against a wall. which is generally the best place to put a speaker


Next I pivoted to a a 3 way design with 3d printed shell that can be infilled with plaster of paris for mass loading. 

There is a bent bass relex port for low end extension.

with a few wire channels for routing cables



This first prototype seemed interesting enough to do the first prototype. Manufacturing was effectively 3d printing some shells, then fillin them with plaster. 



For the electronics, i decided to go with JAB5 boards, which have integrated DSP, signal processing, 4x100W channels, bluetooth and can be daisy chained for an 8x100w system. 


this design was prototyped mainly to learn some lesssons. Boy was there some!

including how much of a nightmare it is to spill plaster all over the flat...


Firstly, I 3d printed the shells and stuck them all together, with some bonding putty as a sealing agent. These were loaded under a couple of guinness cans, plates and a pot of water to set.




Though unfortunately, I did not realise that filing with liquid plaster mix from the top would be a much bigger challenge. Leading to a large and fairly unstoppable series of leaks. the below pic was taken when noticing the leak, best believe it got much much worse as the resorvoiur of plaster gradually oozed out. 



V2
New design, learning from some lessons:

Old design was designed to have continous walls, whereby it was a series of shells that were stacked ontop of eachother. But when infilling, it leaked, and it's really hard to get the right viscosity of plaster such that it sets in the walls and flows to the bottom. Too thin - its got too much water and it might leak through gaps and too thick - it doesnt flow and just blocks up the flow channels. 

additionally, the gypsum mixture thickens during pouring making the whole thing a nonlinear nightmare!

V2 will have modular shells which can be infilled seperately then stacked. If one messes up, it can just be remade instead of rebuilding the whole system

Height can be reduced by incorporating the bass reflex port as one of the walls.

Addition of angled screw mounts so proper fasteners can be used to hold everything together (the holes on the outside and internal bumps are the screw mounts, providing a clamping force between the pieces . Using epoxy was a bit expensive and not very good.






Wall Design
The walls are designed as a multilayer composite


This image shows a section view of a single speaker composite wall. 


The left side is inside the speaker, the rightside is outside the speaker.

The building process is as follows:

Shells are printed

Gypsum and PVA is mixed with water and poured into an individual shell

Allow to dry

Infilled shells are bonded together with screws and a small amount of epoxy / sealing glue depending on location

Acoustic foam liner is stuck to the inside wall

The outside of the speaker is vinyl wrapped

The speaker is stuffed with wool

Finishing can resume by sticking things to the outside of the speaker.


Boxes are held together with Stixall sealing and some screws which can hold seperate 3d printed shells together. 

Stixall provides some air barrier sealing, adhesion and gap filling, though the main air barrier is provided by the vinyl wrap.

Screws allow the whole speaker to maintain rigitidy and also help with ensuring a good adhesive cure. This means that when picking the speakers up, all of the seperate shells don't seperate from eachother (which is fairly important)

This was an observed failure mode with V1 - as the gypsum was no good in tension (surprise surprise)




Filling moulds can be a bit messy - but we got the box built!

Boxes sealed together with Stixall sealing and bonding agent with screws holding everything together (this worked really well to get a strong mechanical build and an airtight seal). 

Next is to vinyl wrap a first layer, which actually provides some functional benefits including 

a tensioned outerface (for rigidity)

an airtight seal around all of the potential gaps

As well as it covers up all of the ugly plaster fills.

Vinyl wrapping for an airtight seal around subwoofer chamber:

Key learning lesson: I will NEVER have a future in vinyl wrapping.

This vinyl wrapping is not for aesthethics (that's to come later) but to act as a robust, cheap way of achieving an airtight envelope around an otherwisae difficult to seal multi part 3D printed chamber




3d printed inserts go into the screw holes with a dot of epoxy putty to fill them in and keep everything flush



Getting an even wrap was a nightmare but i was not too precious about it being perfect - the surface i was bonding to was very imperfect and the whole thing will later get covered in some exterior design (yet to be designed - possibly fabric or 3d printed parametric arts)

First sound test


Started to program the amplifier drive units in Sigma Studio, which had a bit of a learning curve, after spending a few hours trying to get my PC to recognise the programming board (which itself required reprogramming), we got a fairly nice sounding speaker already.

current program:




Now it makes sound:




first sound test


Wrapped up and a potentiometer added for volume control

The plan was initially to have a JAB5 mounted to the back of each speaker, and linked with an I2S cable in a master-slave config. News to me was that the maximum length of these cables is about 10cm! that's no good for a stereo system. This genuinely appears like a disaster from a design perspective, and was a reall unexpected blocker. 

A bit of brainstorming later, it seems the most reasonable solution is now to keep the master - slave setup, but to have all of the processing and amplification for both speakers done on the same speaker. Effectively both JAB5's mounted to the back of one of the speakers and then passing speaker cables to the other, now passive, speaker. 




AI Generating some concepts for aesthetics / finishing

Time to start also thinking about how these things are going to look in their final form. 

AI image gen might be really useful for this, so I started with a reference image of the 2 speakers I have made and wrapped in crude vinyl wrap (which was never going to be the final form) and used Nano Banana Pro to generate a good range of potential concepts. 


Reference image: The two terrible wrapped speaker boxes.


The outputs:

AI Generated Parametric concepts




AI Generated block wrap








AI generated print designs




Building the electronics




