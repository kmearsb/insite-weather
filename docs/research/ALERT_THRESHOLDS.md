# Alert thresholds: research and recommendations

**Status:** Research note, Nov 19 2026. Proposes changes to PRD §6.2 and the TDD §6 rules. Nothing is changed in those documents yet.
**Scope:** (1) Weather triggers for dust, stormwater and track-out. (2) Other pollution events that weather can cause.

Every number below is marked as either **sourced** (taken from a rule, permit or study, linked at the end) or **judgment** (our proposal, to be backtested). We are not lawyers. A site's own permit and air-district rules always win over these defaults.

---

## 1. Proposed triggers at a glance

| Concern | Moderate | High | Change from PRD §6.2 |
|---|---|---|---|
| **Dust** | Sustained ≥ 15 mph **or** gusts ≥ 20 mph | Sustained ≥ 20 mph **or** gusts ≥ 25 mph | Gusts lowered by 5 mph in each tier. **RH gate removed.** |
| | Both tiers apply only if there was < 0.10 in of rain in the prior 48 h | | Dry-ground gate unchanged |
| **Stormwater** | ≥ 0.10 in forecast in 24 h, PoP ≥ 50% | ≥ 0.50 in forecast in 24 h, PoP ≥ 50% (this is exactly California's "qualifying precipitation event") | High: PoP 60% → 50%. The 6-hour intensity trigger becomes optional. |
| **Stormwater, severe** (new; needs per-site data) | — | Forecast 24-h rain ≥ the site's 2-year, 24-hour storm depth | New tier |
| **Track-out** | ≥ 0.10 in forecast during operating hours or in the 12 h before opening, PoP ≥ 50% | ≥ 0.50 in in 24 h | Adds a high tier. Closes the open question. |

Optional add-ons, all new:

- **Permit-aware inspection reminders** (§3.2).
- A **first-storm-of-the-season** note (§3.4).

**Unit values for the rule JSON (SI units):**

| Imperial | SI |
|---|---|
| 15 mph | 6.71 m/s |
| 20 mph | 8.94 m/s |
| 25 mph | 11.18 m/s |
| 0.10 in | 2.54 mm |
| 0.25 in | 6.35 mm |
| 0.50 in | 12.7 mm |
| 3.25 in of snow | 82.55 mm |

NWS gridpoint wind comes in km/h. Convert at ingest, as `insite/weather` already does.

---

## 2. Dust

### 2.1 What regulators use (sourced)

- **25 mph is the common "high wind" line.**
  - Several California air districts define high wind as instantaneous gusts above 25 mph: South Coast AQMD Rule 403 and Rule 1157 (aggregate plants), Antelope Valley Rule 403, and Mojave Desert Rule 403.
  - Maricopa County Rule 312 defines a wind event as a 60-minute average above 25 mph.
  - Utah's opacity limits stop applying above 25 mph, provided controls are in place.
- **15 mph sustained means water more.** Santa Barbara County APCD, which covers the pilot site in Santa Maria, says watering frequency should increase when sustained wind exceeds 15 mph. It also says earthmoving should be minimized above 25 mph.
- **The physics agrees.** AP-42 §13.2 says wind erosion of exposed surfaces starts at wind speeds above roughly 12 mph.
- **The National Weather Service (NWS) uses the same line for blowing dust.** Its blowing dust advisories and warnings usually need winds of 25 mph or more.

**What this gives the tiers.**

- **Sourced:**
  - Moderate, sustained 15 mph: Santa Barbara County APCD.
  - High, gusts 25 mph: the air-district rules above.
- **Judgment:**
  - Moderate, gusts 20 mph: one step below the regulators' "high wind" line.
  - High, sustained 20 mph: kept from the PRD. Sustained 20 mph almost always comes with gusts over 25 mph anyway.

### 2.2 Why drop the relative humidity (RH) gate

- **The evidence on humidity points both ways.**
  - In semi-arid field data with wind above 4 m/s, dust concentration peaked near 25% RH and fell as humidity rose (Csavina et al. 2014).
  - Other field and wind-tunnel work shows that the wind speed needed to lift dust rises and falls with RH rather than in one direction. In some tests it drops as RH climbs from about 40% to 65%.
- **Air humidity misses most site dust.** At an aggregate site, most dust comes from trucks and loaders on haul roads and stockpiles. That dust depends on the moisture of the surface (rain or watering), not of the air.
- **The gate would silence real events.** A coastal site such as Santa Maria can have windy afternoons with RH above 45%. Under the current gate it would get no alert at all on those days.
- **Recommendation:** remove RH from the trigger. Keep logging it so that calibration can test it later.

### 2.3 Dry-ground gate (judgment)

- **Keep the gate at < 0.10 in in the prior 48 h.**
  - AP-42 counts a day with ≥ 0.01 in as a "wet" day, and a peer reviewer of AP-42 noted that the effect of moisture lasts a while after rain.
  - Unpaved roads also dry quickly.
  - So 0.10 in over 48 h is a conservative point at which to stand down.
- **Make the gate use observed rain** from the nearest station, not only forecast rain.

### 2.4 Message content

- **High-tier texts should add a line about loose material**, such as "secure tarps and loose material". NWS wind advisories already tell people to secure objects outdoors.
- **This covers windblown litter and debris** (§5) without a separate concern.

---

## 3. Stormwater

### 3.1 What permits use (sourced)

| Source | Trigger | What it means for us |
|---|---|---|
| 40 CFR 122.21(g)(7)(ii) | Storm event: > 0.1 in, at least 72 h after the previous measurable event | Origin of the 0.10 in moderate tier |
| EPA 2022 Construction General Permit (CGP) | Inspect every 7 days, **or** every 14 days and within 24 h of ≥ 0.25 in of rain in 24 h, or snowmelt from ≥ 3.25 in of snow in 24 h | Post-storm reminder that uses **observed** rain |
| California 2022 CGP: qualifying precipitation event (QPE) | Starts at the first 6-hour NWS interval with PoP ≥ 50%. That block plus the next three (24 h in all) must sum to ≥ 0.5 in of rain (QPF). The event extends for each later 24 h with QPF ≥ 0.25 in. | Our **high** tier. The pre-event inspection is due within 72 h before the event (up to 120 h with an extended forecast), which matches our T−72h heads-up. There is one inspection in each 24 h during the event, and a post-event inspection within 96 h if the **on-site** gauge recorded ≥ 0.5 in. Forecasts must come from the NWS. |
| California Industrial General Permit (IGP): qualifying storm event (QSE) | Any discharge from at least one drainage area, after 48 h with no discharge. Sample 2 QSEs in July–December and 2 in January–June, within 4 h of the discharge starting during operating hours. | "Sampling crew ready" reminder when the moderate tier falls inside operating hours |
| EPA Multi-Sector General Permit (MSGP) | The 2021 permit expired on Feb 28, 2026 and was administratively continued. As of Aug 2026 its replacement had not been issued. EPA's permit only covers places where EPA issues the permits (e.g. MA, NH, NM, DC, Indian Country). States issue their own, e.g. Texas (effective Aug 14, 2026) and Idaho (effective May 2, 2026). California sites fall under the IGP. | Check each pilot site's permit. Don't hard-code EPA's terms. |
| EPA 2022 CGP §2.2.12 | A sediment basin may be sized for the runoff of the 2-year, 24-hour storm | Basis for the **severe** tier |
| EPA SPCC guidance | "Sufficient freeboard" for secondary containment means room for a 25-year, 24-hour storm (guidance, not codified) | Containment-overflow reminder (§5) |

### 3.2 Recommendation

- **Tiers.**
  - Moderate: 0.10 in in 24 h at PoP ≥ 50%.
  - High: the California QPE definition, used for every site.
  - Using one PoP value (50%) everywhere is simpler, and 50% is the only PoP figure a regulator uses.
- **Implement the QPE as 6-hour blocks, not a rolling 24-hour sum.** This lets us claim that an alert is "CGP-consistent". **TDD change:** add a `block_6h` window type to the rules engine.
- **Add a per-site "permit profile"** with these values:
  - EPA CGP
  - California CGP
  - California IGP
  - Federal or state MSGP
  - None

  The profile adds the right inspection or sampling reminder to an alert, for example:
  - "Pre-storm inspection due by Thu 3 pm"
  - "Post-storm inspection due within 24 h; 0.31 in fell at KSMX"
- **Caveat for reminders based on rain that has already fallen.** The California CGP's post-event trigger uses the **site's own gauge**. NWS station data can prompt the inspection, but the copy must not say it satisfies the permit.

### 3.3 Severe tier (judgment; needs site data)

- **Trigger:** compare the forecast 24-h rain with the site's 2-year, 24-hour depth from NOAA's precipitation frequency data (Atlas 14).
- **Message:** "Rain may exceed what your sediment basin is designed for".
- **Setup:** the depth is fetched once per site.

### 3.4 First storm of the season (judgment)

- **Why:** the first rain after a long dry period often carries the most pollution. Material builds up over the dry season and washes off in the first storms.
- **Proposal:** when the first moderate or high event follows ≥ 30 days without measurable rain, add one line to the alert: "first storm in a while — expect dirtier runoff; check BMPs first."

---

## 4. Track-out

- **Sourced.**
  - Caltrans-based guidance flags wet weather as the time when mud is most easily tracked off a site.
  - South Coast AQMD Rule 403 requires track-out to stay under 25 ft and be removed at the end of the day.
  - Wisconsin requires inspecting tracking pads within 24 h of ≥ 0.5 in of rain.
- **Proposal.**
  - Moderate: ≥ 0.10 in forecast during operating hours or in the 12 h before opening, PoP ≥ 50%.
  - High: ≥ 0.50 in in 24 h.
  - Action: sweep the exits and check the pad. Reply keyword: `SWEPT`.
  - Dry-weather track-out (dust) is already covered by the dust rule.

---

## 5. Other weather-driven pollution events

| Event | Who it matters to | Weather signal | Data | Priority |
|---|---|---|---|---|
| **Secondary containment overflow** (fuel or oil) | Any site with tanks, totes or drums (SPCC) | Heavy rain, roughly toward the 25-year, 24-hour depth, or several storms without draining. Before draining the rainwater, check it for sheen. | QPF + NOAA Atlas 14 | **Next** (add to the severe stormwater tier) |
| **Sediment basin or pond overtopping** | Construction, quarries | Forecast ≥ 2-year, 24-hour storm | QPF + Atlas 14 | **Next** (severe tier) |
| **Windblown debris, tarps, litter** | Construction, recycling, landfills | Dust high tier | `windGust` | **Pilot** (message line only) |
| **Fire risk to combustible stockpiles and hot work** (mulch, compost, green waste, wood, tires) | Recycling, compost, landfill, some quarries | NWS Red Flag Warning. Typical criteria: RH ≤ 15% with sustained wind or frequent gusts ≥ 25 mph for 3 h or more. Criteria vary by NWS office. | `hazards` (RFW), `redFlagThreatIndex` | **Next** |
| **Snowmelt runoff** | Construction (EPA CGP) | ≥ 3.25 in of snow in 24 h (the EPA CGP trigger). Thaw: temperature rising above freezing after snow. | `snowfallAmount`, `temperature` | **Later** (not a pilot region) |
| **Odor** (landfill, compost, biosolids, wastewater) | Those sectors | Calm, clear dawn and dusk; low mixing height; inversions; wind toward neighbors. Caveat: a 10-year landfill study found no link between complaints and weather alone. | `mixingHeight`, `transportWindSpeed`, `atmosphericDispersionIndex`, `windDirection` + a per-site neighbor bearing | **Later**, as a segment add-on |
| **Ozone action days** | Fleets and sites with fueling, painting, solvents | Hot, sunny, light wind. Agencies ask for voluntary steps: refuel after dusk, delay solvent and paint work, defer gas-powered equipment. | AirNow `/aq/forecast/current/` (takes lat/long). The old `/aq/forecast/latLong/` was retired Sep 30, 2026. | **Later** (voluntary; low compliance value) |
| **Tropical storms** | Gulf and Atlantic sites | Tropical-storm or hurricane wind probability. The 2021 MSGP asks for major-storm measures such as raising materials and reducing outdoor storage. | `probabilityOfTropicalStormWinds`, `probabilityOfHurricaneWinds` | **Later** (when we expand into those regions) |
| **Spray drift** (herbicide on slopes or landscaping) | Sites that spray | Wind > 10 mph, or < 3 mph (a possible inversion) | `windSpeed` | **Later**, niche |

**Not recommended:** air stagnation (PM build-up) and lightning. Air districts already forecast stagnation, and site operators can do little about it. Lightning is a safety issue, not a pollution issue.

---

## 6. Data changes

- **New NWS gridpoint layers**, needed only for the "Next" and "Later" items:
  - `hazards`
  - `redFlagThreatIndex`
  - `snowfallAmount`
  - `mixingHeight`
  - `transportWindSpeed`
  - `atmosphericDispersionIndex`
  - `probabilityOfTropicalStormWinds`
- **Possible confidence signal for dust:** the NWS also publishes `potentialOf20mphWindGusts`, `potentialOf30mphWindGusts` and similar layers.
- **Values can be null for some intervals.** Check the pilot grid cells before relying on a layer.
- **Per-site setup fields:**
  - Permit profile (§3.2)
  - 2-year and 25-year 24-hour depths (fetched once from NOAA's precipitation frequency server)
  - Optional bearing to the nearest neighbors (for odor)
- **NWS hazards as a cross-check:** if the NWS has an active Blowing Dust Advisory, Wind Advisory or High Wind Warning for the site's zone, raise a dust event to high.

## 7. To validate before the pilot

1. Backtest the dust and stormwater tiers against 2–3 years of Santa Maria (KSMX) observations. Count alerts per month per site; the target is ≤ 4 a month.
2. Confirm each pilot site's permit type and the air-district dust rule that applies.
3. Decide whether "severe" should be a third tier in the product or just a line added to a high alert.
4. Have an environmental consultant review the defaults (this is still an open question in the PRD).

---

## Sources

**Dust**

- South Coast AQMD: [Rule 403](https://www.aqmd.gov/docs/default-source/rule-book/rule-iv/rule-403.pdf), [Rule 1157](https://www.aqmd.gov/docs/default-source/rule-book/reg-xi/rule-1157.pdf), [Rule 403.1](https://www.aqmd.gov/docs/default-source/rule-book/rule-iv/rule-403-1.pdf)
- [Antelope Valley AQMD Rule 403](https://www.avaqmd.ca.gov/files/b6046ee22/AV403+2010+20+Apr+reformatted.pdf); [Mojave Desert AQMD Rule 403](https://mdaqmd.ca.gov/home/showpublisheddocument/650/636305698521900000)
- [Santa Barbara County APCD, Fugitive Dust Control Measures (2025)](https://www.ourair.org/wp-content/uploads/Attachment-A-Fugitive-Dust-Control-Measures-2025.pdf)
- [Maricopa County Rule 312](https://www.maricopa.gov/7030/Rule-312---Abrasive-Blasting); [Utah R307-309 instructions](https://documents.deq.utah.gov/legacy\compliance\air-quality\stationary-source\docs\2006\05May\FUGDUST-Ins.pdf)
- EPA AP-42: [§13.2 Fugitive dust](https://www.epa.gov/sites/default/files/2020-10/documents/13.2_fugitive_dust_sources.pdf), [§13.2.2 Unpaved roads](https://gaftp.epa.gov/ap42/ch13/s021/final/c13s02-2_sept1998.pdf), [§13.2.1 moisture decisions](https://gaftp.epa.gov/ap42/ch13/s021/related/rel03_c13s0201.pdf)
- NWS: [glossary, blowing dust](https://forecast.weather.gov/glossary.php?word=blowing), [wind products](https://weather.gov/safety/wind-ww)
- Research: [Csavina et al. 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4072227); [Ravi et al. 2005](https://digitalcommons.usu.edu/crc_research/93); [EGU 2005 wind-tunnel abstract](https://meetings.copernicus.org/www.cosis.net/abstracts/EGU05/00351/EGU05-J-00351-2.pdf)

**Stormwater**

- [40 CFR 122.21(g)(7)(ii) summary](https://ercweb.com/regulations/show/What-Qualifies-as-a-Storm-Event-for-Stormwater-Sampling)
- EPA 2022 CGP: [inspection report template](https://www.epa.gov/system/files/documents/2022-01/site-inspection-report-template.docx), [2-year, 24-hour storm](https://www.epa.gov/system/files/documents/2022-01/2022-cgp_2-year-24-hour-storm-frequencies.pdf)
- California 2022 CGP: [QPE guidance](https://waterboards.ca.gov/water_issues/programs/stormwater/construction/docs/2022-cgp-qpe.pdf)
- California IGP: [To-Do List](https://www.waterboards.ca.gov/water_issues/programs/stormwater/docs/toolbox/IGP-To-Do-List-(English).pdf), [Fact Sheet excerpt](https://www.trihydro.com/flipbooks/ca_stormwater_workshop_handouts/files/basic-html/page91.html)
- MSGP status: [Dober (Aug 2026)](https://www.dober.com/greenfloc/resources/epa-msgp-2026), [EPA No Action Assurance (Feb 2026)](https://www.epa.gov/system/files/documents/2026-03/oeca-no-action-assurance-memo-msgp.pdf), [J.J. Keller](https://www.jjkeller.com/news/article/EPA-temporarily-extends-2021-MSGP-coverage_id-c2bac09b-ebf7-4f79-ca4f-9c35b13d9835), [TCEQ 2026 MSGP](https://www.tceq.texas.gov/assistance/resources/the-advocate-1/2026-msgp-renewal), [Idaho DEQ](https://www.deq.idaho.gov/?p=83305)
- [EPA SPCC freeboard guidance](https://epa.gov/oil-spills-prevention-and-preparedness-regulations/what-are-specifications-bulk-storage-secondary)
- First flush: [Taylor & Francis overview](https://taylorandfrancis.com/knowledge/Engineering_and_technology/Civil%2c_environmental_and_geotechnical_engineering/First_flush)

**Track-out**

- [Rocklin tracking BMP flyer (Caltrans TC-1)](https://www.rocklin.ca.us/sites/main/files/file-attachments/tracking_flyer_0.pdf)
- [SCAQMD Rule 403 presentation](https://www.aqmd.gov/docs/default-source/compliance/rule-403-dust-control-forms/403-presentation.pdf)
- [Wisconsin SPS 325 tracking pads](https://docs.legis.wisconsin.gov/code/admin_code/sps/safety_and_buildings_and_environment/320_325/325_a/_1750?up=1)

**Other events**

- NWS Red Flag criteria: [Grand Junction](https://www.weather.gov/gjt/firewxcriteria), [Boulder](https://weather.gov/bou/RFW_Definitions)
- Odor: [Wake County landfill](https://www.wake.gov/news/science-smell-does-landfill-smell-more-certain-times), [FAU study](https://fau.isle.flvc.org/node/55699)
- Ozone action days: [EPA Region 3](https://archive.epa.gov/reg3artd/archive/web/html/actdays.html); [AirNow API June 2026 changes](https://docs.airnowapi.org/docs/AirNowAPIUpdates2026June.pdf)
- Major storms: [EPA 2021 MSGP presentation](https://epa.gov/sites/default/files/2021-03/documents/final_2021_msgp_presentation.pdf)
- Spray drift: [Univ. of Kentucky PSEP](https://www.uky.edu/Ag/Entomology/PSEP/65drift.html)

**Data**

- [NWS gridpoint layers](https://weather-gov.github.io/api/gridpoints)
