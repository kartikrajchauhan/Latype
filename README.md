# latype

latype is a custom full-size mechanical keeb built around the **Adafruit Feather nRF52840 Express**.

the idea was pretty simple at first.. keep all the keys i use and make the board myself. that became a switch matrix, a pair of gpio expanders, a tiny colour screen and an enclosure with more cutouts than i expected. KiCad handles the electronics and Fusion 360 handles the case side of things

![latype PCB preview](Images/Screenshot%202026-10-20%20133007.png)

## why i made this

i like having the numpad and the separate navigation keys so going smaller wasnt really the plan. i wanted to figure out how a whole keyboard goes together from the schematic to the thing that eventually sits on a desk

main goals :

- draw the full keyboard schematic and PCB in KiCad
- keep the function row, arrow keys and numpad
- use I2C expanders to scan the keys without running out of controller pins
- plan for wired USB and Bluetooth operation
- leave a proper spot for a 1.9-inch screen
- add a few useful status lights
- model the bottom, switch plate and top frame in Fusion
- save the source files and fabrication exports with the BOM

most of the work ends up under the keycaps where nobody sees it lol.. the switch positions decide the plate, the plate affects the case and then the connector still needs somewhere to come out. everything has to agree with everything else

## project status

the board layout and enclosure are saved along with screenshots and production exports. this is still a design/build project, with physical assembly and testing left to do

the firmware is an early draft too. it has the key mapping and some peripheral setup but the current file stops during the display code, so theres more work there before it can run as a complete keyboard

whats in this repo :

- `PCB/` - schematic, board and KiCad project
- `Images/` - screenshots from the electronics and case work
- `Firm/` - firmware draft
- `Fusion360/` - editable case design
- `3D Mod/` - assembly and printable models
- `PDF/` - exported project documents
- `production/` - board fabrication and assembly references
- `BOM/` - supplier cart screenshots
- `bom.csv` - component sourcing and listed costs

## hardware summary

| | |
|---|---|
| Project | latype |
| Layout | Full-size, 108-switch design |
| Main controller | Adafruit Feather nRF52840 Express |
| Connection plans | USB and Bluetooth LE |
| Matrix arrangement | 6 rows x 21 columns |
| Matrix expansion | Two MCP23017 I2C expanders |
| Switch diodes | 1N4148W SOD-123 |
| Screen | Waveshare 1.9-inch SPI IPS LCD, 170 x 320 |
| Status lights | Caps Lock, Num Lock and battery indications |
| Battery listed | 3.7 V 500 mAh LiPo |
| Switch choice | Akko V3 Penguin Pro silent tactile |
| Keycaps | XVX Plum Blossom 127-key Cherry-profile PBT set |
| Stabilizers | Durock V2 clear 7+1 kit with 6.25U spacebar wire |
| Design tools | KiCad and Fusion 360 |

the matrix has more electrical positions than fitted switches because wider keys leave gaps in the grid. the firmware draft marks those unused positions with `KC.NO`

## images

### PCB and switch layout

![latype switch arrangement](Images/Screenshot%202026-10-20%20132755.png)

### PCB routing and board layers

![latype component placement](Images/Screenshot%202026-10-20%20132809.png)

![latype routing overview](Images/Screenshot%202026-10-20%20132820.png)

![latype copper fill view](Images/Screenshot%202026-10-20%20132838.png)

### schematic

these show the matrix and some of the circuits around it. the expanders take care of the extra row and column lines while the Feather connects to the screen and indicators

![latype switch matrix](Images/Screenshot%202026-10-20%20131823.png)

![latype first expander](Images/Screenshot%202026-10-20%20131826.png)

![latype second expander](Images/Screenshot%202026-10-20%20131830.png)

![latype controller wiring](Images/Screenshot%202026-10-20%20131833.png)

![latype complete schematic](Images/Screenshot%202026-10-20%20131917.png)

### firmware and build screenshots

![latype firmware draft](Images/Screenshot%202026-10-20%20134050.png)

this is the source draft stage.. theres no finished hardware test shown here yet

### CAD and case

![latype enclosure assembly](Images/Screenshot%202026-10-20%20135805.png)

![latype switch plate](Images/Screenshot%202026-10-20%20135815.png)

![latype bottom shell](Images/Screenshot%202026-10-20%20135821.png)

![latype top frame](Images/Screenshot%202026-10-20%20135826.png)

![latype case overview](Images/Screenshot%202026-10-20%20135832.png)

## repo file checklist

- `PCB/Latype.kicad_pro` - main KiCad project
- `PCB/Latype.kicad_sch` - electrical schematic
- `PCB/Latype.kicad_pcb` - board layout
- `Firm/firmware.py` - current firmware draft
- `Fusion360/Latype.f3d` - editable Fusion model
- `3D Mod/Full/` - STEP assembly export
- `3D Mod/Print/Bottom.stl` - lower shell
- `3D Mod/Print/Plate.stl` - switch plate
- `3D Mod/Print/Top Plate.stl` - top piece
- `PDF/` - PDF exports
- `production/` - fabrication archive and generated board data
- `Images/` - pictures used here
- `BOM/` - sourcing screenshots
- `bom.csv` - full build shopping list

theres a generated `bom.csv` inside `production/` as well. thats board output, while the root list includes the parts being bought for the overall build

## cad

the case is in three main pieces so the switch plate, lower tray and top frame can be printed separately. `Fusion360/Latype.f3d` is the editable version and `3D Mod/Print/` has the STL exports

the plate needs to line up with the switch and stabilizer positions, and the bottom needs enough space for the parts under the board. the display opening and USB access are part of that fit too.. these are the things to check with the current PCB before committing to a full print

the STEP export is in `3D Mod/Full/`. its current filename is `Equinox V1.step`, so dont miss it when looking for the assembly

## firmware note

the draft in `Firm/firmware.py` uses KMK and two MCP23017s at addresses `0x20` and `0x21`. it already has the 6 x 21 matrix mapping, the main key layer and a second layer definition

it also starts setting up the lock LEDs, battery voltage input and ST7789 screen. the saved file currently ends inside `_setup_scene`, before the complete display setup and keyboard startup are there

so this part still needs finishing and checking against the board connections. once thats done the next job is testing the keymap, display and connection modes on hardware.. i dont have a tested flashing guide to put here yet

## bom

the full sourcing list is [`bom.csv`](bom.csv). it has the required quantities, supplier links and USD line costs, with separate purchase quantities where a shop sells a bigger pack

**listed component subtotal: $170.29**

thats the sum of the rounded line prices in the saved CSV. it leaves out PCB fabrication and case printing, plus any extra shipping, duties or checkout taxes

a few things on the list :

| Part | Purpose |
|---|---|
| Feather nRF52840 Express | Main keyboard controller |
| MCP23017 expanders | Extra inputs and outputs for the matrix |
| 1N4148W diodes | Keep matrix switch signals isolated |
| Waveshare 1.9-inch LCD | Small display for the keyboard |
| Red and green LEDs | Operating and battery indicators |
| 500 mAh LiPo | Power for wireless use |
| Akko Penguin Pro switches | Silent tactile key presses |
| Durock V2 stabilizers | Support wide keys |
| Plum Blossom keycaps | Key surfaces and legends |

