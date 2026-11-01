# Links health check

Checked: 2026-10-31T16:52:46.467756+00:00

25 Links page destinations tested with GET requests and redirects followed. 18 returned HTTP 200; 7 need review. Failing original URLs were retried once. No HTTP 404 responses were observed.

| Link | Result | HTTPS alternative |
| --- | --- | --- |
| [Penn State eWall](http://mp1.met.psu.edu/~fxg1/ewall.html) | Connection failed — curl: (28) Failed to connect to mp1.met.psu.edu port 80 after 2714 ms: Connection timed out | Connection failed |
| [College of DuPage SatRad page](http://weather.cod.edu/satrad/) | 200 | 200 |
| [NWS Aviation Weather Center](http://aviationweather.gov) | 200 | 200 |
| [One-Stop MOS](http://www.nws.noaa.gov/mdl/synop/products/bullform.all.php) | 403 | 403 |
| [PivotalWeather Model Data](https://pivotalweather.com) | 405 | Already HTTPS |
| [Tropical Tidbits Model Data](http://www.tropicaltidbits.com/analysis/models/) | 200 | 200 |
| [TwisterData](http://www.twisterdata.com/) | 200 | 200 |
| [NOAA Space Weather Prediction Center](http://www.swpc.noaa.gov/) | 301 — curl: (6) Could not resolve host: www.www.swpc.noaa.gov | 200 |
| [SpaceWeatherLive Help Page](https://www.spaceweatherlive.com/en/help/) | 200 | Already HTTPS |
| [Breathe Cams [Pittsburgh, PA]](http://breatheproject.org/learn/breathe-cam/) | 403 | 403 |
| [Prudential Center Webcams [Boston, MA]](http://bluehill.org/observatory/webcams/prudential-webcams/) | 200 | 200 |
| [More Boston webcams [Boston, MA]](http://thebostonwebcam.com/) | 406 | 406 |
| [Alexandria Marina [Alexandria, VA]](http://apps.alexandriava.gov/MarinaCam/) | 200 | 200 |
| [Denver Air Quality [Denver, CO]](https://www.colorado.gov/airquality/live_image.aspx) | 200 | Already HTTPS |
| [Bryant's Weather Wall](http://stormsellweather.com/weatherwall/themapwall.html) | 200 | 200 |
| [Penn State Campus Weather Service](http://www.campusweatherservice.com) | 200 | 200 |
| [SunsetWx](https://sunsetwx.com) | 200 | Already HTTPS |
| [IEMBot Web Monitor](https://weather.im/iembot/) | 200 | Already HTTPS |
| [Mount Washington Observatory](https://www.mountwashington.org/) | 200 | Already HTTPS |
| [NWS Local Snow Reports Map](https://www.weather.gov/source/crh/snowmap.html) | 200 | Already HTTPS |
| [MODIS Imagery - NASA Worldview](https://worldview.earthdata.nasa.gov/) | 200 | Already HTTPS |
| [AARoads](https://www.aaroads.com/) | 403 | Already HTTPS |
| [Pennsylvania Highways](http://www.pahighways.com/) | 200 | 200 |
| [3-digit interstates @ kurumi.com](http://www.kurumi.com/roads/3di/index.html) | 200 | 200 |
| [Roads to the Future](http://roadstothefuture.com/main.html) | 200 | 200 |

The NOAA SWPC HTTP URL redirects to an invalid `www.www.swpc.noaa.gov` hostname; its HTTPS alternative responds successfully.

403/405/406 responses can indicate access or automation restrictions rather than dead websites. A separate web retrieval could read the Breathe Cam and Boston Webcam pages; verify blocked destinations in a normal browser before removing them. Penn State eWall timed out over both HTTP and HTTPS.

Raw observations, redirect destinations, and retry results are recorded in `links-health.json`. No site URLs were changed.
