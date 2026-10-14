# Research

## My own Modding Docs

TrackTypes: `light-metro`, `heavy-metro`, `light-rail`, `commuter-rail`, `commuter-rail-diesel`

stats:

- `carsPerCarSet`: Refers to how many can be purchased at a time, it seems

### Vanilla Reference

Operating Costs - train/hr, car/hr, track/m, station/yr(k)

- `heavy-metro`: 250, 25, 360, 320
- `light-metro`: 180, 20, 280, 200
- `light-rail`: 220, 20, 280, 200

Capital Costs - car(M), track(k), station(M)

- `heavy-metro`: 2.7, 30, 60
- `light-metro`: 2.5, 30, 45
- `light-rail`: 2, 25, 40

Train cars:

- `heavy-metro`: 18.4x3.0, 240 pax, 40 seats
- `light-metro`: 19.1x2.9, 200 pax, 64 seats
- `light-rail`: 9.6x2.6, 77 pax, 25 seats

## Random notes

For legacy lines

177,000 per train is the max aim, based on scaling up (by passenger count) the NYC heavy-metro trains.
Though aiming for ~160k is probably best. Currently set to 300 + 6x25 = 164,250/hr. This may change

Track clearance is about 1.2-1.3m (though circular tunnels are wider), just gonna use the default (Singapore MRT: Design)

Actual minimum mainline curvature is 275 m (only 3 curves < 300 m); minimum in depots is 190 (Singapore MRT: Design)

hmmm... should GoA4 trains really be more expensive? the numbers don't say so (though granted they are full contract prices)

### Seats

NSEWL Stock:

- C151: 208 (34.7)
- C651: 372 (62)
- C751B: 272 (45.3)
- C151A: 296 (49.3)
- C151B: 292 (48.7)
- C151C: 280 (46.7)
- R151: 224 (37.3)

CCL/DTL Stock

- 130 (43.3) to 146 (CCL; 48.7)

NEL Stock

- 240 (40) to 296 (49.3)

### TPH

- NEL: 90 seconds (Alstom doc), same Urbalis 300 as CCL
- NSEWL: 100 seconds ([LandTransportGuru](https://landtransportguru.net/train-cbtc/))
