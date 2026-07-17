"""Generate an expanded mock parts catalog (~300 parts).

Run once (or after editing) with:  uv run python data/generate_catalog.py
Writes data/parts_catalog.json. Deterministic - no randomness.
"""

import json
from pathlib import Path

OUT = Path(__file__).parent / "parts_catalog.json"

parts = []


def add(prefix, asset_type, name, number, desc, keywords, price, stock):
    parts.append(
        {
            "id": f"{prefix}-{len([p for p in parts if p['id'].startswith(prefix)]) + 1:03d}",
            "asset_type": asset_type,
            "part_name": name,
            "part_number": number,
            "description": desc,
            "keywords": keywords,
            "unit_price_usd": price,
            "in_stock": stock,
        }
    )


# ---------------- Traffic signals ----------------
for size in (200, 300):
    for color, kw in (("Red", "top light"), ("Amber", "middle light"), ("Green", "bottom light")):
        add("TS", "Traffic light", f"LED Signal Module - {color} ({size}mm)",
            f"TL-LED-{color[0]}{size}",
            f"Replacement {color.lower()} LED lamp module for {size}mm vehicular traffic signal heads. Fits polycarbonate housings.",
            ["traffic light", "signal", f"{color.lower()} light", kw, "burnt out", "dead lamp", "flickering", "LED module"],
            64.5 if size == 200 else 84.5, 10)
for size in (200, 300):
    add("TS", "Traffic light", f"Signal Visor / Hood ({size}mm)", f"TL-VIS-{size}",
        f"Black polycarbonate sun visor (tunnel hood) shielding a {size}mm signal lens. Replace after wind or impact damage.",
        ["traffic light", "visor", "hood", "cracked", "broken shade", "missing hood", "sun shield"], 14.0 + size * 0.02, 30)
    add("TS", "Traffic light", f"Signal Lens - Clear Polycarbonate ({size}mm)", f"TL-LENS-{size}",
        f"Clear replacement lens for {size}mm signal aspect. Replace crazed, yellowed, or shattered lenses.",
        ["traffic light", "lens", "cracked lens", "shattered", "cloudy", "yellowed"], 11.5, 40)
add("TS", "Traffic light", "Signal Head Mounting Bracket Kit", "TL-BRKT-U",
    "Universal aluminium bracket kit for pole- or span-wire mounting of signal heads, with stainless hardware.",
    ["traffic light", "bracket", "mounting", "loose head", "tilted signal", "hanging"], 38.0, 22)
add("TS", "Traffic light", "Signal Backplate with Retroreflective Border", "TL-BP-3S",
    "Louvered black backplate with yellow retroreflective border for 3-section signal heads. Improves visibility; replace bent or missing plates.",
    ["traffic light", "backplate", "border", "bent", "missing plate"], 46.0, 12)
add("TS", "Pedestrian crossing", "Pedestrian Push Button Assembly", "PED-PB-2",
    "Weatherproof pedestrian call button with tactile arrow plate. Replaces vandalized or unresponsive crossing buttons.",
    ["pedestrian button", "crossing", "push button", "not working", "vandalized", "stuck button"], 96.0, 14)
add("TS", "Pedestrian crossing", "Pedestrian Countdown Display Module", "PED-CD-16",
    "LED countdown and walking-man display module for pedestrian signal heads, 16-inch, with driver board.",
    ["pedestrian signal", "countdown", "walking man", "display dead", "segments out"], 168.0, 6)
add("TS", "Traffic controller", "Signal Controller Cabinet Door Lock Set", "TC-LOCK-2",
    "Tamper-resistant lock and handle set for roadside signal controller cabinets, keyed alike, with weather gasket.",
    ["controller cabinet", "lock", "broken lock", "door won't close", "pried open"], 54.0, 16)
add("TS", "Traffic controller", "Cabinet Ventilation Fan and Filter Kit", "TC-FAN-120",
    "120mm thermostat-controlled fan with washable dust filter for signal controller cabinets. Replace seized or noisy fans.",
    ["controller cabinet", "fan", "overheating", "noisy fan", "filter clogged"], 31.0, 20)

# ---------------- Streetlights ----------------
for watt in (60, 100, 150, 250):
    add("SL", "Streetlight", f"Cobra Head LED Luminaire {watt}W", f"SL-COB-{watt}",
        f"Complete {watt}W LED cobra-head luminaire for arm-mounted street lighting. Replaces failed or corroded fixtures.",
        ["streetlight", "street lamp", "luminaire", "not turning on", "dark street", "fixture", "corroded"],
        140.0 + watt * 0.7, 6)
add("SL", "Streetlight", "Twist-Lock Photocell Sensor", "SL-PC-TL",
    "Dusk-to-dawn photocell that twist-locks onto the top of a streetlight fixture. Replace when a light stays on all day or never switches on.",
    ["streetlight", "photocell", "sensor", "stays on during day", "won't turn on at night", "dusk to dawn", "scorched sensor"], 14.9, 45)
add("SL", "Streetlight", "Photocell Twist-Lock Receptacle", "SL-PCR-TL",
    "NEMA twist-lock receptacle base that the photocell mounts into. Replace when contacts are burnt or the sensor no longer seats.",
    ["streetlight", "receptacle", "socket", "photocell base", "burnt contacts", "loose sensor"], 9.8, 38)
add("SL", "Streetlight", "LED Driver 100W Programmable", "SL-DRV-100",
    "Constant-current programmable LED driver for cobra-head luminaires up to 100W. Replace when the lamp flickers or is dead with power present.",
    ["streetlight", "driver", "ballast", "flickering", "dead lamp", "power supply"], 42.0, 24)
add("SL", "Streetlight", "Pole Base Access Door with Lock", "SL-DOOR-P",
    "Galvanized steel access door for the wiring compartment at the base of a streetlight pole, with tamper-resistant fastener.",
    ["streetlight pole", "access door", "missing cover", "exposed wires", "base panel", "hand hole"], 32.0, 18)
add("SL", "Streetlight", "Pole Base Anchor Bolt Cover Set", "SL-ABC-4",
    "Set of four dome covers for pole base anchor bolts. Replace missing or rusted covers exposing bolt threads.",
    ["streetlight pole", "bolt cover", "anchor bolts", "rusted", "missing caps", "base"], 12.5, 50)
for length in (1.5, 2.5):
    add("SL", "Streetlight", f"Luminaire Mast Arm {length}m Galvanized", f"SL-ARM-{int(length*10)}",
        f"{length}m galvanized steel mast arm for side-of-pole luminaire mounting. Replace bent or fatigued arms.",
        ["streetlight", "mast arm", "bracket arm", "bent arm", "sagging", "outreach"], 68.0 + length * 20, 8)
add("SL", "Streetlight", "Inline Fuse Holder and 10A Fuse Kit", "SL-FUSE-10",
    "Waterproof inline fuse holder with 10A fuses for pole base wiring. Replace after fault trips or corrosion.",
    ["streetlight", "fuse", "blown fuse", "no power", "wiring", "base compartment"], 6.4, 80)

# ---------------- Piping ----------------
for dia in (50, 75, 110, 160, 200):
    add("PP", "Piping", f"PVC Coupling {dia}mm", f"PP-CPL-{dia}",
        f"Slip-fit PVC coupling for joining two {dia}mm pipe ends. Used to repair cracked or leaking sections after cutting out the damaged length.",
        ["pipe", "pvc", "leak", "crack", "coupling", "joint", "repair"], 1.6 + dia * 0.03, 100)
    add("PP", "Piping", f"PVC 90\u00b0 Elbow {dia}mm", f"PP-ELB-{dia}",
        f"90-degree PVC elbow for {dia}mm pipe runs. Replace cracked or leaking corner fittings.",
        ["pipe", "pvc", "elbow", "corner", "leak at bend", "fitting"], 1.9 + dia * 0.035, 80)
for inch in (1, 2, 3):
    add("PP", "Piping", f"Galvanized Steel Elbow 90\u00b0 ({inch} inch)", f"PP-ELBG-{inch}",
        f"90-degree threaded galvanized elbow for {inch}-inch steel pipe. Replace when corroded or seized.",
        ["pipe", "steel", "elbow", "rust", "corroded", "threaded fitting"], 4.2 + inch * 2.1, 60)
    add("PP", "Piping", f"Pipe Support Clamp with Rubber Liner ({inch} inch)", f"PP-CLMP-{inch}",
        f"Wall/ceiling pipe clamp with rubber insulation liner for {inch}-inch pipe. Replaces broken brackets on sagging or vibrating runs.",
        ["pipe", "clamp", "bracket", "sagging", "loose pipe", "support", "vibration"], 1.4 + inch * 0.8, 150)
add("PP", "Piping", "Repair Clamp Stainless 110mm x 200mm", "PP-RCL-110",
    "Full-circle stainless repair clamp sealing longitudinal cracks and pinholes on 110mm pipe without cutting.",
    ["pipe", "repair clamp", "pinhole", "spray leak", "burst", "emergency repair"], 24.0, 30)
add("PP", "Piping", "Gate Valve Brass 2 inch", "PP-GV-2",
    "Full-bore brass gate valve, 2-inch threaded, for isolation on distribution lines. Replace seized or weeping valves.",
    ["pipe", "valve", "gate valve", "won't close", "seized", "weeping", "shutoff"], 28.5, 25)
add("PP", "Piping", "Valve Box Cover Cast Iron", "PP-VBC-1",
    "Cast iron surface cover for buried valve access boxes. Replace cracked or missing covers in footways.",
    ["valve box", "cover", "cracked", "missing lid", "buried valve"], 19.0, 35)
add("PP", "Piping", "Pipe Insulation Sleeve 2 inch x 1m", "PP-INS-2",
    "Closed-cell foam insulation sleeve for 2-inch exposed pipework. Replace weathered, torn, or waterlogged lagging.",
    ["pipe", "insulation", "lagging", "torn foam", "frost protection", "condensation"], 3.2, 90)

# ---------------- Hydrants & water ----------------
add("HY", "Fire hydrant", "Hydrant Nozzle Cap with Chain", "HY-CAP-N",
    "Cast-iron replacement cap for hydrant side nozzle, supplied with retaining chain. Replace when missing or cross-threaded.",
    ["fire hydrant", "cap", "missing cap", "chain", "nozzle", "stolen cap"], 26.5, 22)
add("HY", "Fire hydrant", "Hydrant Pumper Cap 4.5 inch", "HY-CAP-P",
    "Large-diameter cast-iron cap for the front pumper connection with gasket and chain.",
    ["fire hydrant", "pumper cap", "front cap", "large cap", "missing"], 34.0, 15)
add("HY", "Fire hydrant", "Operating Nut and Weather Cap", "HY-NUT-P5",
    "Pentagon operating nut with weather cap for hydrant stem. Replace rounded-off or seized nuts.",
    ["fire hydrant", "operating nut", "rounded", "seized", "won't open", "stem"], 21.0, 18)
add("HY", "Fire hydrant", "Hydrant Flange Gasket and Bolt Kit", "HY-GSK-6",
    "6-inch flange gasket with stainless bolt set for hydrant base connections. Replace when the base weeps or after knock-over repairs.",
    ["fire hydrant", "gasket", "leaking base", "weeping", "knocked over", "bolts"], 17.5, 26)
add("HY", "Water meter", "Water Meter Pit Lid 300mm", "HY-MPL-300",
    "Composite lid for domestic water meter pits, 300mm, with reader aperture. Replace cracked or missing lids.",
    ["water meter", "pit lid", "cover", "cracked", "missing", "meter box"], 15.5, 40)

# ---------------- Road & drainage ----------------
for dia, load in ((450, "B125"), (600, "D400")):
    add("RD", "Road / drainage", f"Ductile Iron Manhole Cover {dia}mm {load}", f"RD-MH-{dia}",
        f"{load}-rated ductile iron manhole cover and frame, {dia}mm clear opening. Replace cracked or rocking covers.",
        ["manhole", "cover", "cracked", "rocking", "missing", "road", "clanging"], 90.0 + dia * 0.09, 8)
for size in (300, 450, 600):
    add("RD", "Road / drainage", f"Gully Drainage Grate {size}x{size}mm", f"RD-GRT-{size}",
        f"Cast iron storm drain grate for roadside gullies, {size}mm square. Replace when broken, clogged beyond cleaning, or stolen.",
        ["drain", "grate", "storm drain", "gully", "broken grate", "blocked", "stolen"], 30.0 + size * 0.06, 15)
add("RD", "Road / drainage", "Kerb Inlet Lintel Precast", "RD-KIL-900",
    "Precast concrete lintel for kerb inlet openings, 900mm. Replace spalled or collapsed inlet mouths.",
    ["kerb inlet", "lintel", "collapsed", "spalled", "drain opening"], 44.0, 10)
add("RD", "Road / drainage", "Channel Drain Grate Galvanized 1m", "RD-CHG-100",
    "Galvanized slotted grate section for 100mm linear channel drains across driveways and paths.",
    ["channel drain", "grate", "linear drain", "bent grate", "missing section"], 22.0, 28)
add("RD", "Road", "Flexible Delineator Post with Base", "RD-DEL-750",
    "750mm orange flexible delineator post with reboundable base and reflective bands. Replace snapped or faded posts.",
    ["delineator", "flexible post", "bollard", "snapped", "run over", "faded"], 18.0, 60)
add("RD", "Road", "Raised Pavement Marker Reflective (pack of 10)", "RD-RPM-10",
    "Ceramic-base reflective road studs, pack of 10, with adhesive pads. Replace missing or crushed lane markers.",
    ["road stud", "cat eye", "pavement marker", "missing", "crushed", "lane marking"], 26.0, 45)
add("RD", "Road", "Speed Hump Rubber Section with Fixings", "RD-HUMP-50",
    "500mm modular rubber speed hump section with anchor bolts and reflective inserts. Replace cracked or lifted sections.",
    ["speed hump", "speed bump", "cracked", "lifted", "loose section"], 39.0, 20)

# ---------------- Signage ----------------
for sign, code, shape in (("Stop", "STOP", "octagon"), ("Yield", "YIELD", "triangle"), ("No Entry", "NOENT", "circle")):
    add("SG", "Signage", f"Reflective Sign Panel - {sign} (750mm)", f"SG-{code}-750",
        f"High-intensity retroreflective aluminium {sign} sign panel, 750mm {shape}, pre-drilled. Replace faded, bent, or graffitied panels.",
        ["sign", f"{sign.lower()} sign", "faded", "bent", "graffiti", "panel", "reflective"], 42.0, 25)
for speed in (30, 50, 60, 80):
    add("SG", "Signage", f"Speed Limit Sign Panel {speed} km/h (600mm)", f"SG-SPD-{speed}",
        f"Retroreflective circular speed limit panel, {speed} km/h, 600mm. Replace faded or vandalized panels.",
        ["sign", "speed limit", "faded", "vandalized", "panel"], 36.0, 18)
add("SG", "Signage", "Sign Post Mounting Bracket Set", "SG-BRKT-U",
    "Pair of universal U-channel brackets with bolts for fixing sign panels to posts. Replace stripped or corroded fixings.",
    ["sign", "bracket", "loose sign", "bolts", "mounting", "stripped"], 6.9, 90)
add("SG", "Signage", "Sign Post Galvanized 76mm x 3.5m", "SG-POST-35",
    "Galvanized steel sign post, 76mm diameter, 3.5m. Replace bent or corroded posts after vehicle strikes.",
    ["sign post", "bent post", "knocked down", "vehicle strike", "leaning"], 52.0, 14)
add("SG", "Signage", "Anti-Rotation Post Clamp", "SG-ARC-76",
    "Clamp collar preventing sign panels rotating on 76mm posts. Replace when signs spin out of alignment.",
    ["sign", "rotated", "spinning sign", "clamp", "misaligned"], 8.4, 55)
add("SG", "Street nameplate", "Street Nameplate Blank with Rails", "SG-SNP-900",
    "900mm aluminium street nameplate blank with mounting rails, ready for vinyl lettering. Replace cracked or illegible plates.",
    ["street name", "nameplate", "illegible", "cracked", "faded lettering"], 29.0, 20)

# ---------------- Street furniture ----------------
for length in (1200, 1500, 1800):
    add("PF", "Street furniture", f"Hardwood Bench Slat {length}mm", f"PF-SLAT-{length//100}",
        f"Pre-drilled treated hardwood slat, {length}mm, for standard park bench frames. Replace split, rotten, or vandalized slats.",
        ["bench", "slat", "broken plank", "park bench", "wood", "split", "rotten"], 12.0 + length * 0.006, 40)
add("PF", "Street furniture", "Bench Slat Fixing Kit Stainless", "PF-FIX-B",
    "Stainless coach bolts, washers, and cap nuts for fixing bench slats to cast frames.",
    ["bench", "bolts", "loose slat", "fixings", "rusted bolts"], 5.5, 70)
add("PF", "Street furniture", "Litter Bin Liner Galvanized 90L", "PF-BIN-90",
    "Galvanized steel inner liner for 90L street litter bins. Replace burnt, holed, or corroded liners.",
    ["litter bin", "trash can", "liner", "burnt", "holed", "corroded"], 33.0, 24)
add("PF", "Street furniture", "Litter Bin Door Hinge and Lock Kit", "PF-BINLK",
    "Hinge pair with triangular-key lock for pedestal litter bin doors. Replace when doors hang or won't latch.",
    ["litter bin", "door", "hinge", "won't close", "lock", "hanging door"], 12.0, 30)
add("PF", "Street furniture", "Steel Bollard Removable with Ground Sleeve", "PF-BOL-RM",
    "Removable 90mm steel bollard with lockable ground sleeve. Replace bent or sheared bollards after impacts.",
    ["bollard", "bent", "hit by car", "sheared", "removable post"], 88.0, 12)
add("PF", "Street furniture", "Cycle Stand Sheffield Galvanized", "PF-CYC-SH",
    "Galvanized Sheffield-pattern cycle stand with root-fix legs. Replace bent or corroded stands.",
    ["bike rack", "cycle stand", "bent", "corroded", "loose"], 46.0, 16)
add("PF", "Bus stop", "Bus Shelter Glazing Panel Toughened 1100x1400", "PF-BSG-11",
    "Toughened safety glass panel for bus shelter side bays, 1100x1400mm, with edge gaskets. Replace shattered or cracked panels.",
    ["bus shelter", "glass", "shattered", "cracked panel", "smashed", "glazing"], 74.0, 10)
add("PF", "Bus stop", "Bus Stop Flag Sign Double-Sided", "PF-BSF-DS",
    "Double-sided bus stop flag sign with pole clamp band. Replace faded or broken flags.",
    ["bus stop", "flag", "sign", "faded", "broken"], 27.0, 18)

# ---------------- Fencing & barriers ----------------
add("FB", "Fencing", "Chain-Link Fence Mesh Roll 1.8m x 15m", "FB-CLM-18",
    "Galvanized chain-link mesh roll for repairing cut or rusted fence sections, 1.8m high.",
    ["fence", "chain link", "cut fence", "hole in fence", "rusted mesh"], 96.0, 8)
add("FB", "Fencing", "Fence Line Post Galvanized 2.4m", "FB-LP-24",
    "Galvanized intermediate line post for 1.8m chain-link fencing, with cap.",
    ["fence", "post", "leaning post", "bent", "broken post"], 21.0, 30)
add("FB", "Fencing", "Gate Hinge Set Heavy Duty Adjustable", "FB-GH-HD",
    "Adjustable heavy-duty hinge pair for swing gates up to 75kg. Replace sagging or seized hinges.",
    ["gate", "hinge", "sagging gate", "won't swing", "seized", "dragging"], 18.5, 26)
add("FB", "Fencing", "Gate Drop Bolt and Keeper", "FB-DB-450",
    "450mm drop bolt with ground keeper for double gates. Replace bent bolts or missing keepers.",
    ["gate", "drop bolt", "won't lock", "bent bolt", "keeper"], 13.0, 34)
add("FB", "Guardrail", "W-Beam Guardrail Panel 3.2m Galvanized", "FB-WB-32",
    "Standard 3.2m galvanized W-beam guardrail panel with splice hardware. Replace impact-damaged sections.",
    ["guardrail", "crash barrier", "dented", "impact damage", "w-beam"], 118.0, 6)
add("FB", "Guardrail", "Guardrail Post and Blockout Set", "FB-GP-SET",
    "Galvanized guardrail post with composite blockout and bolts. Replace posts bent in collisions.",
    ["guardrail", "post", "bent post", "collision", "blockout"], 64.0, 10)

# ---------------- Electrical / comms street assets ----------------
add("EL", "Feeder pillar", "Feeder Pillar Door with Lock GRP", "EL-FPD-1",
    "GRP replacement door with tri-head lock for roadside electrical feeder pillars. Replace vandalized or corroded doors.",
    ["feeder pillar", "electrical box", "door", "vandalized", "open cabinet", "exposed"], 89.0, 8)
add("EL", "Feeder pillar", "DIN Rail MCB 16A Type C", "EL-MCB-16",
    "16A Type C miniature circuit breaker for feeder pillar distribution. Replace tripped-and-failed or heat-damaged breakers.",
    ["breaker", "mcb", "tripped", "no power", "feeder pillar", "burnt"], 7.9, 60)
add("EL", "CCTV", "CCTV Camera Dome Cover Polycarbonate", "EL-CAM-DC",
    "Clear polycarbonate dome for street CCTV cameras. Replace scratched, crazed, or spray-painted domes.",
    ["cctv", "camera", "dome", "scratched", "spray painted", "cloudy"], 24.0, 14)
add("EL", "EV charging", "EV Charge Point Cable Holster", "EL-EVH-T2",
    "Replacement Type 2 cable holster/dock for public EV charge points. Replace cracked or torn-off holsters.",
    ["ev charger", "holster", "cable dock", "cracked", "torn off", "hanging cable"], 19.5, 22)
add("EL", "EV charging", "EV Charge Point RFID Front Panel", "EL-EVP-RF",
    "Front fascia panel with RFID window for kerbside EV charge points. Replace vandalized or delaminated panels.",
    ["ev charger", "front panel", "screen", "vandalized", "delaminated"], 57.0, 9)

# ---------------- Additional piping variants ----------------
for dia in (50, 75, 110, 160, 200):
    add("PP", "Piping", f"PVC Equal Tee {dia}mm", f"PP-TEE-{dia}",
        f"Equal tee junction for {dia}mm PVC pipe branches. Replace cracked or leaking branch fittings.",
        ["pipe", "pvc", "tee", "junction", "branch", "leak"], 2.4 + dia * 0.04, 60)
    add("PP", "Piping", f"PVC End Cap {dia}mm", f"PP-CAP-{dia}",
        f"Push-fit end cap sealing {dia}mm PVC pipe terminations. Replace missing or split caps.",
        ["pipe", "pvc", "end cap", "open pipe", "missing cap", "split"], 1.1 + dia * 0.02, 90)
for pair in ((75, 50), (110, 75), (160, 110), (200, 160)):
    add("PP", "Piping", f"PVC Reducer {pair[0]}mm to {pair[1]}mm", f"PP-RED-{pair[0]}{pair[1]}",
        f"Concentric reducer joining {pair[0]}mm to {pair[1]}mm PVC pipe. Replace cracked transitions.",
        ["pipe", "pvc", "reducer", "transition", "crack", "different sizes"], 2.9, 40)

# ---------------- Streetlight column variants ----------------
for height in (5, 6, 8, 10):
    add("SL", "Streetlight", f"Steel Lighting Column {height}m Galvanized", f"SL-COL-{height}",
        f"Galvanized tapered steel lighting column, {height}m, with base flange and access door aperture. Replace corroded or vehicle-struck columns.",
        ["streetlight pole", "column", "leaning", "corroded base", "knocked down", "vehicle strike"],
        260.0 + height * 45, 3)

# ---------------- Additional sign speeds & panels ----------------
for speed in (40, 70, 100, 120):
    add("SG", "Signage", f"Speed Limit Sign Panel {speed} km/h (600mm)", f"SG-SPD-{speed}",
        f"Retroreflective circular speed limit panel, {speed} km/h, 600mm. Replace faded or vandalized panels.",
        ["sign", "speed limit", "faded", "vandalized", "panel"], 36.0, 18)
for name, code in (("Pedestrian Crossing Ahead", "PEDX"), ("School Zone", "SCHL"), ("Give Way to Oncoming", "GWO"), ("No Parking", "NOPK")):
    add("SG", "Signage", f"Warning Sign Panel - {name} (600mm)", f"SG-{code}-600",
        f"Retroreflective aluminium warning panel: {name}, 600mm. Replace faded, bent, or missing panels.",
        ["sign", name.lower(), "warning", "faded", "bent", "missing"], 38.0, 15)

# ---------------- Additional drainage & road ----------------
for dia in (110, 160, 225, 300):
    add("RD", "Road / drainage", f"Drainage Pipe Section Twin-Wall {dia}mm x 3m", f"RD-TWP-{dia}",
        f"Twin-wall HDPE drainage pipe section, {dia}mm x 3m, with coupler. Replace crushed or root-blocked runs.",
        ["drain", "drainage pipe", "crushed", "blocked", "root ingress", "culvert"], 12.0 + dia * 0.08, 20)
add("RD", "Road / drainage", "Gully Pot Precast Concrete 450mm", "RD-GPOT-450",
    "Precast concrete gully pot with trapped outlet, 450mm, for roadside drainage. Replace cracked or collapsed pots.",
    ["gully", "gully pot", "cracked", "collapsed", "sinkhole at drain"], 58.0, 8)
add("RD", "Road", "Kerbstone Precast HB2 915mm", "RD-KERB-HB2",
    "Standard precast concrete half-battered kerbstone, 915mm. Replace cracked, spalled, or displaced kerbs.",
    ["kerb", "curb", "cracked", "spalled", "displaced", "broken edge"], 9.5, 120)
add("RD", "Road", "Tactile Paving Slab Blister Red 400mm", "RD-TAC-400",
    "Red blister tactile paving slab, 400x400mm, for crossing points. Replace cracked or lifted slabs.",
    ["tactile paving", "blister slab", "cracked", "lifted", "trip hazard", "crossing"], 7.8, 100)

# ---------------- Additional street furniture ----------------
add("PF", "Street furniture", "Bench Cast End Frame", "PF-FRM-CE",
    "Cast aluminium bench end frame, pre-drilled for standard slats. Replace cracked or vandalized frames.",
    ["bench", "frame", "cracked", "end support", "cast"], 61.0, 8)
add("PF", "Street furniture", "Picnic Table Top Recycled Plastic 1800mm", "PF-PIC-18",
    "Recycled plastic plank table top set for 1800mm picnic units. Replace split or burnt tops.",
    ["picnic table", "table top", "split", "burnt", "vandalized"], 84.0, 6)
add("PF", "Playground", "Swing Seat with Chains Heavy Duty", "PF-SWG-HD",
    "Rubber safety swing seat with galvanized chain set and shackles. Replace cracked seats or worn chains.",
    ["swing", "playground", "seat", "cracked", "worn chain", "broken swing"], 42.0, 12)
add("PF", "Playground", "Safety Surface Tile Rubber 500mm", "PF-SST-500",
    "Impact-absorbing rubber safety tile, 500x500mm, for playground surfacing. Replace lifted, torn, or missing tiles.",
    ["playground", "rubber tile", "safety surface", "lifted", "torn", "missing tile"], 11.0, 80)


OUT.write_text(json.dumps(parts, indent=2), encoding="utf-8")
print(f"Wrote {len(parts)} parts to {OUT}")
