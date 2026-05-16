
# nim c -d:release -r exam.nim

import std/[
  os, unicode, math, sequtils, random, 
  strformat, algorithm, json, parseopt, sets]
import sdl2, sdl2/audio, sdl2/ttf
import chamberEngine

var gLoggingEnabled = false

template log(args: varargs[untyped]) =
  if gLoggingEnabled:
    echo args


const WindowWidth = 800
const WindowHeight = 600

# ==========================================
# TYPES & STATE
# ==========================================
type
  IntPoint = tuple[lon, lat: int]
  IntEdge = tuple[p1, p2: IntPoint]
  GeoPoint = tuple[lon, lat: float]
  GeoPath = seq[GeoPoint]
  City = tuple[name: string, lon, lat: float]

  ExamState = object
    window: WindowPtr
    renderer: RendererPtr
    font, smallFont, noteFont, hintFont: FontPtr
    worldMap: seq[GeoPath]
    tourRoute: seq[City]
    tourIndex: int
    startLon, startLat: float
    targetLon, targetLat: float
    travelProgress: float
    arrivalFlashTimer: int
    lastTargetLon, lastTargetLat: float

    # Audio
    device: AudioDeviceID
    want, have: AudioSpec
    
    # Data
    allCountries: seq[string]
    numberOfAlternatives: int
    
    # Logic & State
    running: bool
    delayMs: int
    showSpeedMenu: bool
    activeBpmIdx: int
    menuHoverTimer: int
    bpmHoverTimer: int
    lastTargetBpmIdx: int
    optionsText: seq[string]
    targetCountry: string
    targetRuneSeq: seq[Rune]
    playCount: int
    hintTimer: int
    questionStartTime: uint32
    showCurrentHint: bool

    audioIdx: int
    pauseTimer: int
    questionAnswered: bool
    targetAlpha: float
    safeToHover: bool
    isHoveringCorrect: bool
    
    # Input
    mouseX, mouseY: cint
    isDragging: bool
    lastMouseX, lastMouseY: cint

const EuropeanCapitals: array[42, City] = [
  ("Tirana", 19.8189, 41.3275), ("Andorra la Vella", 1.5218, 42.5063),
  ("Vienna", 16.3738, 48.2082), ("Minsk", 27.5667, 53.9000),
  ("Brussels", 4.3517, 50.8503), ("Sarajevo", 18.4131, 43.8563),
  ("Sofia", 23.3219, 42.6977), ("Zagreb", 15.9819, 45.8150),
  ("Prague", 14.4378, 50.0755), ("Copenhagen", 12.5683, 55.6761),
  ("Tallinn", 24.7536, 59.4370), ("Helsinki", 24.9384, 60.1699),
  ("Paris", 2.3522, 48.8566), ("Berlin", 13.4050, 52.5200),
  ("Athens", 23.7275, 37.9838), ("Budapest", 19.0402, 47.4979),
  ("Reykjavik", -21.9426, 64.1466), ("Dublin", -6.2603, 53.3498),
  ("Rome", 12.4964, 41.9028), ("Riga", 24.1052, 56.9496),
  ("Vaduz", 9.5209, 47.1410), ("Vilnius", 25.2797, 54.6872),
  ("Luxembourg", 6.1319, 49.6116), ("Valletta", 14.5141, 35.8997),
  ("Chisinau", 28.8638, 47.0105), ("Monaco", 7.4246, 43.7384),
  ("Podgorica", 19.2636, 42.4411), ("Amsterdam", 4.9041, 52.3676),
  ("Skopje", 21.4316, 42.0000), ("Oslo", 10.7522, 59.9139),
  ("Warsaw", 21.0122, 52.2297), ("Lisbon", -9.1393, 38.7223),
  ("Bucharest", 26.1025, 44.4268),
  ("San Marino", 12.4515, 43.9424), ("Belgrade", 20.4489, 44.8125),
  ("Bratislava", 17.1077, 48.1486), ("Ljubljana", 14.5058, 46.0569),
  ("Madrid", -3.7038, 40.4168), ("Stockholm", 18.0686, 59.3293),
  ("Bern", 7.4474, 46.9480), ("Kyiv", 30.5234, 50.4501),
  ("London", -0.1276, 51.5072)
]


# Helper to convert degrees to radians
proc degToRad(deg: float): float = deg * PI / 180.0

proc toIntPoint(lon, lat: float): IntPoint =
  # Multiply by 1000 to keep 3 decimal places of precision, which is 
  # perfect for matching identical borders without floating-point errors.
  result = (int(round(lon * 1000.0)), int(round(lat * 1000.0)))

proc makeEdge(lon1, lat1, lon2, lat2: float): IntEdge =
  let p1 = toIntPoint(lon1, lat1)
  let p2 = toIntPoint(lon2, lat2)
  # Always order the coordinates from smallest to largest.
  # This guarantees the border is treated as the same edge regardless of direction!
  if p1.lon < p2.lon or (p1.lon == p2.lon and p1.lat < p2.lat):
    result = (p1, p2)
  else:
    result = (p2, p1)


proc loadGeoJSON*(filename: string): seq[GeoPath] =
  result = @[]
  log "Loading detailed map data from ", filename, "..."
  
  if not fileExists(filename):
    quit("Error: Could not find map file " & filename)

  let root = parseFile(filename)
  if root.kind != JObject or not root.hasKey("features"): 
    quit("Error: Invalid GeoJSON format.")
    
  var seenEdges = initHashSet[IntEdge]()
  var duplicateCount = 0

  # --- FIX: Changed 'proc' to 'template' ---
  template processRing(ring: JsonNode) =
    for i in 0 ..< ring.elems.len - 1:
      let lon1 = ring.elems[i][0].getFloat()
      let lat1 = ring.elems[i][1].getFloat()
      let lon2 = ring.elems[i+1][0].getFloat()
      let lat2 = ring.elems[i+1][1].getFloat()
      
      let edge = makeEdge(lon1, lat1, lon2, lat2)
      
      if not seenEdges.contains(edge):
        seenEdges.incl(edge)
        result.add(@[(lon: lon1, lat: lat1), (lon: lon2, lat: lat2)])
      else:
        inc duplicateCount
  # -----------------------------------------

  for feature in root["features"].elems:
    if not feature.hasKey("geometry") or feature["geometry"].kind == JNull: continue
    
    let geom = feature["geometry"]
    let geomType = geom["type"].getStr()

    if geomType == "Polygon":
      for ring in geom["coordinates"].elems:
        processRing(ring)
        
    elif geomType == "MultiPolygon":
      for poly in geom["coordinates"].elems:
        for ring in poly.elems:
          processRing(ring)
          
  log "Loaded ", result.len, " unique line segments. Removed ", duplicateCount, " overlapping borders."





# ==========================================
# HELPER FUNCTIONS
# ==========================================
proc drawCircle(renderer: RendererPtr, x0, y0, radius: cint) =
  var x: cint = radius - 1
  var y: cint = 0
  var dx: cint = 1
  var dy: cint = 1
  var err: cint = dx - (radius shl 1)

  while x >= y:
    renderer.drawPoint(x0 + x, y0 + y)
    renderer.drawPoint(x0 + y, y0 + x)
    renderer.drawPoint(x0 - y, y0 + x)
    renderer.drawPoint(x0 - x, y0 + y)
    renderer.drawPoint(x0 - x, y0 - y)
    renderer.drawPoint(x0 - y, y0 - x)
    renderer.drawPoint(x0 + y, y0 - x)
    renderer.drawPoint(x0 + x, y0 - y)

    if err <= 0:
      inc y; err += dy; dy += 2
    if err > 0:
      dec x; dx += 2; err += dx - (radius shl 1)


proc playBling(app: var ExamState) =
  let sampleRate = 44100.0
  
  # 1. Generate 250ms of silence for the pauses
  let silenceSamples = int((250.0 / 1000.0) * sampleRate)
  var silence = newSeq[int16](silenceSamples) # Defaults to zeroes
  
  # Queue pause BEFORE the sound
  discard queueAudio(app.device, addr silence[0], uint32(silence.len * sizeof(int16)))

  # 2. Synthesize the 400ms Bling (Emulating chamberEngine's ",")
  let durationMs = 400.0 
  let numSamples = int((durationMs / 1000.0) * sampleRate)
  var buffer = newSeq[int16](numSamples)

  let freq = 2093.00 # The exact C7 pitch from the engine

  for i in 0 ..< numSamples:
    let t = float(i) / sampleRate
    
    # A slightly sharper exponential decay (-8.0) to emulate the crisp "strike" of wfBling
    let envelope = exp(-8.0 * t) 
    
    # Generate the pure sine wave
    let wave = sin(2.0 * PI * freq * t)
    
    # Apply the envelope and scale it to 16-bit audio range
    let sample = wave * envelope * 12000.0
    buffer[i] = int16(sample)

  # Queue the synthesized bling
  if buffer.len > 0:
    discard queueAudio(app.device, addr buffer[0], uint32(buffer.len * sizeof(int16)))
    
  # 3. Queue pause AFTER the sound
  discard queueAudio(app.device, addr silence[0], uint32(silence.len * sizeof(int16)))


# ==========================================
# INITIALIZATION & DATA LOADING
# ==========================================
proc initExamState(): ExamState =
  result = ExamState(running: true, delayMs: 150, activeBpmIdx: 8)
  
  if sdl2.init(INIT_VIDEO or INIT_AUDIO or INIT_EVENTS) != SdlSuccess: quit("Failed to init SDL.")
  if ttfInit() != SdlSuccess: quit("Failed to init TTF.")
  
  result.window = createWindow("Country Music Exam", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WindowWidth, WindowHeight, SDL_WINDOW_SHOWN)
  result.renderer = createRenderer(result.window, -1, Renderer_Accelerated)
  discard result.renderer.setDrawBlendMode(BlendMode_Blend)

  result.font = openFont("fonts/DejaVuSans.ttf", 24)
  if result.font == nil: quit("Failed to load fonts/DejaVuSans.ttf")
  
  result.smallFont = openFont("fonts/DejaVuSans.ttf", 16)
  result.hintFont = openFont("fonts/DejaVuSans.ttf", 8)
  if result.hintFont == nil: quit("Failed to load fonts/DejaVuSans.ttf at size 8")
  result.noteFont = openFont("fonts/NotoMusic-Regular.ttf", 100)
  if result.noteFont == nil: quit("Failed to load fonts/NotoMusic-Regular.ttf")

  result.want.freq = 44100
  result.want.format = AUDIO_S16
  result.want.channels = 1
  result.want.samples = 1024
  result.want.callback = nil 
  
  result.device = openAudioDevice(nil, 0, addr result.want, addr result.have, 0)
  if result.device == 0: quit("Failed to open audio device.")
  pauseAudioDevice(result.device, 0)
  result.worldMap = loadGeoJSON("data/ne_110m_admin_0_countries.geojson.geojson") 
  result.startLon = -3.7 
  result.startLat = 40.4
  
  # Set up the Grand Tour
  result.tourRoute = @EuropeanCapitals # Convert constant array to dynamic sequence
  result.tourRoute.shuffle()           # Randomize the order!
  result.tourIndex = 0                 # Start at the beginning
  
  # Start at city 0, target city 1
  result.startLon = result.tourRoute[0].lon
  result.startLat = result.tourRoute[0].lat
  result.targetLon = result.tourRoute[1].lon
  result.targetLat = result.tourRoute[1].lat
  
  result.travelProgress = 0.0

proc loadCountries(app: var ExamState, filename: string) =
  try:
    for line in lines(filename):
      if line.strip().len > 0: 
        app.allCountries.add(line.strip())
  except IOError:
    quit("Error: Could not read " & filename)
    
  app.numberOfAlternatives = 10
  if app.allCountries.len < app.numberOfAlternatives:
    app.numberOfAlternatives = app.allCountries.len
    if app.numberOfAlternatives == 0: quit("Error: File is empty.")



proc loadNextQuestion(app: var ExamState) =
  var shuffled = app.allCountries
  shuffled.shuffle()
  
  var subset = shuffled[0 ..< app.numberOfAlternatives]
  
  # Local capture of the font pointer to satisfy memory safety
  let f = app.font 

  subset.sort(proc (x, y: string): int =
    var wX, hX, wY, hY: cint
    # Use 'f' instead of 'app.font'
    discard f.sizeText(x.cstring, addr wX, addr hX)
    discard f.sizeText(y.cstring, addr wY, addr hY)
    return cmp(wX, wY)
  )

  var contoured: seq[string] = newSeq[string](subset.len)
  var head = 0
  var tail = subset.len - 1
  
  # Distribute from the end of the sorted list (longest) inward
  for i in countdown(subset.len - 1, 0):
    if i mod 2 == 0:
      contoured[head] = subset[i]
      inc head
    else:
      contoured[tail] = subset[i]
      dec tail
      
  app.optionsText = contoured
  app.targetCountry = app.optionsText[rand(app.numberOfAlternatives - 1)]
  app.showSpeedMenu = false
  app.menuHoverTimer = 0
  app.bpmHoverTimer = 0
  app.lastTargetBpmIdx = -1
  log "\nSelected Country: ", app.targetCountry
  app.targetRuneSeq = toSeq(app.targetCountry.runes)

  var fullNoteString = ""
  for r in app.targetRuneSeq:
    let charStr = $r
    if charStr != " ": # Skip spaces
      let (_, _, staffStep, noteName) = getAudioSpec(charStr)
      fullNoteString &= fmt"[{charStr}->Step:{staffStep}({noteName})] "
      
  log fullNoteString 
  app.questionStartTime = getTicks()
  app.showCurrentHint = false

  app.audioIdx = 0
  app.pauseTimer = 0
  app.questionAnswered = false
  app.targetAlpha = 1.0
  app.safeToHover = false
  app.isHoveringCorrect = false
  
  closeAudioDevice(app.device)
  app.device = openAudioDevice(nil, 0, addr app.want, addr app.have, 0)
  pauseAudioDevice(app.device, 0)
  playBling(app)

# ==========================================
# UPDATE LOGIC
# ==========================================

proc handleEvents(app: var ExamState) =
  var event = defaultEvent
  while pollEvent(event):
    if event.kind == QuitEvent: 
      app.running = false
    elif event.kind == KeyDown:
      let sym = event.evKeyboard.keysym.sym
      if sym == K_ESCAPE or sym == K_q: app.running = false
      elif sym == K_s: 
        app.showSpeedMenu = not app.showSpeedMenu
        # Reset hover tracking timers whenever manual toggle happens
        app.menuHoverTimer = 0
        app.bpmHoverTimer = 0
        app.lastTargetBpmIdx = -1

    elif event.kind == MouseButtonDown:
      if event.evMouseButton.button == ButtonLeft:
        app.isDragging = true
        app.lastMouseX = event.evMouseButton.x
        app.lastMouseY = event.evMouseButton.y
        
    elif event.kind == MouseButtonUp:
      if event.evMouseButton.button == ButtonLeft:
        app.isDragging = false

    elif event.kind == MouseMotion:
      app.mouseX = event.evMouseMotion.x
      app.mouseY = event.evMouseMotion.y
      
      # --- Automated Hover Trigger Area ---
      # Activates if the mouse enters a 50-pixel vertical band at the bottom of the window
      if app.mouseY >= (WindowHeight - 50):
        if not app.showSpeedMenu:
          app.menuHoverTimer += 16
          if app.menuHoverTimer >= 400: # Requires 400ms of continuous hover
            app.showSpeedMenu = true
      else:
        if app.showSpeedMenu and app.menuHoverTimer > 0:
          app.showSpeedMenu = false
        app.menuHoverTimer = 0
        app.bpmHoverTimer = 0
        app.lastTargetBpmIdx = -1
      # ------------------------------------------
      
      if app.isDragging:
        let dx = float(app.mouseX - app.lastMouseX)
        let dy = float(app.mouseY - app.lastMouseY)
        
        app.startLon -= dx * 0.4
        app.startLat += dy * 0.4
        app.startLat = clamp(app.startLat, -89.0, 89.0)
        
        app.targetLon = app.startLon
        app.targetLat = app.startLat
        app.travelProgress = 0.0
        
        app.lastMouseX = app.mouseX
        app.lastMouseY = app.mouseY





proc updateAudioAndTimers(app: var ExamState) =
  let fadeSpeed = 0.008
  let recoverSpeed = 0.04 
  if app.arrivalFlashTimer > 0:
    app.arrivalFlashTimer -= 16
  # --- PROGRESSIVE FADE LOGIC ---
  if not app.questionAnswered:
    # Require moving the mouse out of the target area once before arming the fade
    if not app.isHoveringCorrect and not app.safeToHover: 
      app.safeToHover = true

    if app.isHoveringCorrect and app.safeToHover:
      app.targetAlpha -= fadeSpeed
      if app.targetAlpha <= 0.0:
        app.targetAlpha = 0.0
        app.questionAnswered = true  # Lock in the answer
        app.safeToHover = false
    else:
      # Recover visibility smoothly if the mouse leaves the target
      if app.targetAlpha < 1.0: 
        app.targetAlpha = min(1.0, app.targetAlpha + recoverSpeed)
  if app.questionAnswered:
    app.targetAlpha = 0.0
  # --- EXISTING AUDIO TIMERS ---
  if app.pauseTimer > 0:
    app.pauseTimer -= 16 
    if app.pauseTimer <= 0 and app.questionAnswered:
      app.loadNextQuestion() 
  elif getQueuedAudioSize(app.device) < 4000:
    if app.audioIdx < app.targetRuneSeq.len:
      let charStr = $app.targetRuneSeq[app.audioIdx]
      discard getAudioSpec(charStr)
      let elapsedMs = float(getTicks() - app.questionStartTime)
      var chance = 0.0
      
      # Give them 4 seconds of peace, then start scaling the probability.
      # Over the next 30 seconds, it scales from 0% to 100% chance.
      if elapsedMs > 4000.0:
        chance = (elapsedMs - 4000.0) / 30000.0 
        
      app.showCurrentHint = rand(1.0) < chance 
      playTone(app.device, charStr, app.delayMs)
      inc app.audioIdx
    else:
      if app.questionAnswered: 
        app.pauseTimer = 1500 
      else:
        app.pauseTimer = 1000 
        app.audioIdx = 0
        inc app.playCount
 

proc fillCircle(renderer: RendererPtr, x0, y0, radius: cint, r, g, b, a: uint8) =
  discard renderer.setDrawColor(r, g, b, a)
  var x: cint = radius - 1
  var y: cint = 0
  var dx: cint = 1
  var dy: cint = 1
  var err: cint = dx - (radius shl 1)

  while x >= y:
    # Draw horizontal lines to fill the circle solid
    discard renderer.drawLine(x0 - x, y0 + y, x0 + x, y0 + y)
    discard renderer.drawLine(x0 - x, y0 - y, x0 + x, y0 - y)
    discard renderer.drawLine(x0 - y, y0 + x, x0 + y, y0 + x)
    discard renderer.drawLine(x0 - y, y0 - x, x0 + y, y0 - x)

    if err <= 0:
      inc y
      err += dy
      dy += 2
    if err > 0:
      dec x
      dx += 2
      err += dx - (radius shl 1)


proc renderRealGlobe(app: var ExamState, cx, cy, radius: cint) =
  # Draw the oceanic background
  app.renderer.fillCircle(cx, cy, radius, 30, 45, 65, 255) 

  # Set the drawing color for the continent lines (Vibrant Green)
  discard app.renderer.setDrawColor(100, 200, 100, 255)

  # --- TRAVEL ANIMATION LOGIC ---
  let t = app.travelProgress
  let easeT = t * t * (3.0 - 2.0 * t)

  let currentLon = app.startLon + (app.targetLon - app.startLon) * easeT
  let currentLat = app.startLat + (app.targetLat - app.startLat) * easeT

  app.travelProgress += 0.0025 # Adjusted slightly for a relaxed sightseeing pace
  
  if app.travelProgress >= 1.0:
    # Move to the next leg of the tour
    app.arrivalFlashTimer = 600
    app.lastTargetLon = app.targetLon
    app.lastTargetLat = app.targetLat

    app.tourIndex = (app.tourIndex + 1) mod app.tourRoute.len
    let nextIndex = (app.tourIndex + 1) mod app.tourRoute.len
    
    # Update coordinates
    app.startLon = app.tourRoute[app.tourIndex].lon
    app.startLat = app.tourRoute[app.tourIndex].lat
    app.targetLon = app.tourRoute[nextIndex].lon
    app.targetLat = app.tourRoute[nextIndex].lat
    
    app.travelProgress = 0.0
    
    # Optional: Print to the terminal so you know where you are flying!
    # echo "Leaving ", app.tourRoute[app.tourIndex].name, " -> Flying to ", app.tourRoute[nextIndex].name
  
  # Convert the current camera look-at point to radians for the math
  let camLon = degToRad(currentLon)
  let camTilt = degToRad(currentLat) # We use Latitude directly as the Tilt!
  let rFloat = float(radius)

  # --- DRAW GRATICULE (LAT/LON LINES) ---
  # Use a faint, semi-transparent blue/white for the grid
  discard app.renderer.setDrawColor(100, 150, 200, 80) 

  # Draw Longitude Lines (Meridians) - Every 30 degrees
  for lonStep in countup(-180, 150, 30):
    let lonRad = degToRad(float(lonStep))
    var prevX, prevY: cint
    var prevVisible = false

    # Step down from North Pole to South Pole in 5-degree increments for a smooth curve
    for latStep in countup(-90, 90, 5):
      let latRad = degToRad(float(latStep))
      let cosLat = cos(latRad)
      let sinLat = sin(latRad)
      let cosLonDif = cos(lonRad - camLon)

      if cosLat * cosLonDif * cos(camTilt) + sinLat * sin(camTilt) > 0.0:
        let xProj = rFloat * cosLat * sin(lonRad - camLon)
        let yProj = -rFloat * (sinLat * cos(camTilt) - cosLat * sin(camTilt) * cosLonDif)
        
        let screenX = cint(float(cx) + xProj)
        let screenY = cint(float(cy) + yProj)

        if prevVisible:
          discard app.renderer.drawLine(prevX, prevY, screenX, screenY)

        prevX = screenX
        prevY = screenY
        prevVisible = true
      else:
        prevVisible = false

  # Draw Latitude Lines (Parallels) - Every 30 degrees
  for latStep in countup(-60, 60, 30): # Exclude poles (-90, 90) as they are just dots
    let latRad = degToRad(float(latStep))
    let cosLat = cos(latRad)
    let sinLat = sin(latRad)
    var prevX, prevY: cint
    var prevVisible = false

    # Wrap completely around the globe in 5-degree increments
    for lonStep in countup(-180, 180, 5):
      let lonRad = degToRad(float(lonStep))
      let cosLonDif = cos(lonRad - camLon)

      if cosLat * cosLonDif * cos(camTilt) + sinLat * sin(camTilt) > 0.0:
        let xProj = rFloat * cosLat * sin(lonRad - camLon)
        let yProj = -rFloat * (sinLat * cos(camTilt) - cosLat * sin(camTilt) * cosLonDif)
        
        let screenX = cint(float(cx) + xProj)
        let screenY = cint(float(cy) + yProj)

        if prevVisible:
          discard app.renderer.drawLine(prevX, prevY, screenX, screenY)

        prevX = screenX
        prevY = screenY
        prevVisible = true
      else:
        prevVisible = false


  # Iterate over the dynamically loaded map data
  for path in app.worldMap:
    var prevX, prevY: cint
    var firstPoint = true
    var prevVisible = false
 
    for point in path:
      let lonRad = degToRad(point.lon)
      let latRad = degToRad(point.lat)
      
      let cosLat = cos(latRad)
      let sinLat = sin(latRad)
      let cosLonDif = cos(lonRad - camLon)
      
      # 3D Visibility check with dynamic camera tilt applied
      if cosLat * cosLonDif * cos(camTilt) + sinLat * sin(camTilt) > 0.0:
        
        # Orthographic Projection with dynamic X-axis Tilt (Pitch)
        let xProj = rFloat * cosLat * sin(lonRad - camLon)
        let yProj = -rFloat * (sinLat * cos(camTilt) - cosLat * sin(camTilt) * cosLonDif)
        
        let screenX = cint(float(cx) + xProj)
        let screenY = cint(float(cy) + yProj)

        if not firstPoint and prevVisible:
          discard app.renderer.drawLine(prevX, prevY, screenX, screenY)

        prevX = screenX
        prevY = screenY
        prevVisible = true
      else:
        prevVisible = false
        
      firstPoint = false

  # Atmosphere ring
  discard app.renderer.setDrawColor(100, 200, 255, 100)
  drawCircle(app.renderer, cx, cy, radius + 1)
  drawCircle(app.renderer, cx, cy, radius + 2)
 

  # --- DRAW ARRIVAL FLASH ---
  if app.arrivalFlashTimer > 0:
    let flashLon = degToRad(app.lastTargetLon)
    let flashLat = degToRad(app.lastTargetLat)

    let cosLat = cos(flashLat)
    let sinLat = sin(flashLat)
    let cosLonDif = cos(flashLon - camLon)

    # 3D Visibility check (Make sure it's facing the camera)
    if cosLat * cosLonDif * cos(camTilt) + sinLat * sin(camTilt) > 0.0:
      let xProj = rFloat * cosLat * sin(flashLon - camLon)
      let yProj = -rFloat * (sinLat * cos(camTilt) - cosLat * sin(camTilt) * cosLonDif)

      let screenX = cint(float(cx) + xProj)
      let screenY = cint(float(cy) + yProj)

      # Calculate the fade ratio (1.0 down to 0.0)
      let alphaRatio = float(app.arrivalFlashTimer) / 600.0
      let alpha = uint8(alphaRatio * 255.0)
      
      # Make the circle expand slightly as it fades (radius from 3 up to 8)
      let pulseRadius = cint(1.0 + (1.0 - alphaRatio) * 2.0)

      # Draw a glowing yellow dot using your custom fillCircle proc
      app.renderer.fillCircle(screenX, screenY, pulseRadius, 250, 250, 220, alpha)


# ==========================================
# RENDER PROCEDURES
# ==========================================

proc renderStaff(app: var ExamState) =
  let staffStartX = 50
  let staffStartY = 40 
  let lineSpacing = 8 
  let noteSpacingX = 25 

  # Draw staff lines
  discard app.renderer.setDrawColor(150, 150, 150, 255)
  for i in 0..4:
    let yPos = cint(staffStartY + i * lineSpacing)
    app.renderer.drawLine(cint(staffStartX), yPos, 
                        cint(staffStartX + (app.targetRuneSeq.len * noteSpacingX) + 20), yPos)

  for i, r in app.targetRuneSeq:
    let charStr = $r
    if charStr == " ":
      continue 
    let (_, wave, verticalStep, _) = getAudioSpec(charStr)

    # Define instrument colors
    var noteColor: Color
    if i == app.audioIdx - 1:
        noteColor = color(240, 240, 240, 255) # Current playing note
    else:
        case wave:
        of wfFlute:   noteColor = color(100, 200, 255, 255) # Vowels = Blue
        of wfMarimba: noteColor = color(255, 200, 100, 255) # Consonants = Orange
        of wfPluck:   noteColor = color(150, 255, 150, 255) # Rare = Green
        else:         noteColor = color(220, 220, 220, 255) # Others = White
    # Calculate Y
    let noteY = staffStartY + (4 * lineSpacing) - cint(verticalStep * (lineSpacing div 2)) + 1
    let noteX = staffStartX + 20 + (i * noteSpacingX)

    # Ledger Lines (Same logic, relying on the clean steps)
    if verticalStep <= -2:
      discard app.renderer.setDrawColor(150, 150, 150, 255)
      let ly = staffStartY + (4 * lineSpacing) + lineSpacing
      app.renderer.drawLine(cint(noteX - 8), cint(ly), cint(noteX + 25), cint(ly))
    
    if verticalStep <= -4:
      let ly2 = staffStartY + (4 * lineSpacing) + (lineSpacing * 2)
      app.renderer.drawLine(cint(noteX - 5), cint(ly2), cint(noteX + 20), cint(ly2))

    # Render Note
    # let noteColor = if i == app.audioIdx - 1: color(255, 100, 100, 255) else: color(255, 255, 255, 255)
    let noteSurf = renderUTF8_Blended(app.noteFont, "♩".cstring, noteColor)
    
    if noteSurf != nil:
      let noteTex = createTextureFromSurface(app.renderer, noteSurf)
      let scaleHeight = lineSpacing.float * 12.0 
      let aspect = noteSurf.w.float / noteSurf.h.float
      let targetW = cint(scaleHeight * aspect)
      let targetH = cint(scaleHeight)
      let headCenterOffset = cint(targetH.float * 0.22)
      # Center the note head on the verticalStep coordinate
      var noteDest = rect(
        cint(noteX - (targetW div 4)), # Slight left shift to center the head horizontally
        cint(noteY - (targetH - headCenterOffset)), 
        targetW, 
        targetH
      )    
      app.renderer.copy(noteTex, nil, addr noteDest)
      destroyTexture(noteTex)
      freeSurface(noteSurf)
    
    if app.showCurrentHint and i == app.audioIdx - 1:
      let letterColor = color(200, 220, 255, 255) 
      
      let upperCharStr = unicode.toUpper(charStr) 
      let letterSurf = renderUTF8_Blended(app.hintFont, upperCharStr.cstring, letterColor)
      
      if letterSurf != nil:
        # ... [The rest of your letter drawing logic remains exactly the same] ...
        let letterTex = createTextureFromSurface(app.renderer, letterSurf)
        let destY = staffStartY + (5 * lineSpacing) 
        
        var letterDest = rect(
          cint(noteX - (letterSurf.w div 2) + 5), 
          cint(destY), 
          letterSurf.w, 
          letterSurf.h
        )
        app.renderer.copy(letterTex, nil, addr letterDest)
        destroyTexture(letterTex)
        freeSurface(letterSurf)

   
  

proc renderOptions(app: var ExamState) =
  let cWhite = color(255, 255, 255, 255)
  let cGray = color(150, 150, 150, 255)
  
  app.isHoveringCorrect = false # Reset evaluation for this frame
  
  for i, opt in app.optionsText:
    let tempSurf = renderUTF8_Blended(app.font, opt.cstring, cWhite)
    let destX = WindowWidth - tempSurf.w - 50 
    let destY = 80 + cint(i * 45)
    var dest = rect(destX, destY, tempSurf.w, tempSurf.h)
    freeSurface(tempSurf) 
    
    var isHovered = (app.mouseX >= dest.x and app.mouseX <= dest.x + dest.w and
                     app.mouseY >= dest.y and app.mouseY <= dest.y + dest.h)

    var drawColor = cWhite
   
    if opt == app.targetCountry:
      if isHovered: app.isHoveringCorrect = true
      
      # Use targetAlpha whenever it's not 1.0, or if the question is already answered
      if app.targetAlpha < 1.0 or app.questionAnswered:
        drawColor = color(100, 255, 100, uint8(app.targetAlpha * 255.0))
      else:
        drawColor = cWhite 
    else:
      # Mute incorrect options when hovering
      if isHovered and not app.questionAnswered: 
        drawColor = cGray 

    # Skip rendering entirely if alpha is 0 to save performance
    if app.targetAlpha > 0.0 or opt != app.targetCountry:
      let surf = renderUTF8_Blended(app.font, opt.cstring, drawColor)
      if surf != nil:
        let tex = createTextureFromSurface(app.renderer, surf)
        app.renderer.copy(tex, nil, addr dest)
        destroyTexture(tex)
        freeSurface(surf)


proc renderSpeedMenu(app: var ExamState) =
  if not app.showSpeedMenu: return

  # --- UPDATED: Expanded BPM array ---
  let bpms = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
  let menuY = WindowHeight - 40
  let cWhite = color(255, 255, 255, 255)
  let cGreen = color(255, 255, 100, 255)
  # --- 1. Calculate the exact total width of the menu ---
  var totalWidth: cint = 0
  var w, h: cint
  
  discard app.smallFont.sizeText("Tempo: ".cstring, addr w, addr h)
  totalWidth += w + 10
  
  for bpm in bpms:
    discard app.smallFont.sizeText(($bpm).cstring, addr w, addr h)
    # --- OPTIMIZATION: Reduced spacing from 15 to 10 so 14 numbers fit perfectly ---
    totalWidth += w + 10 
    
  discard app.smallFont.sizeText(" BPM".cstring, addr w, addr h)
  totalWidth += w

  # --- 2. Dynamically set the starting X position ---
  var currentX = (WindowWidth - totalWidth) div 2
  var anyoneHovered = false

  # Draw "Tempo: "
  let prefixSurf = renderUTF8_Blended(app.smallFont, "Tempo: ".cstring, cWhite)
  if prefixSurf != nil:
    let prefixTex = createTextureFromSurface(app.renderer, prefixSurf)
    var textDest = rect(cint(currentX), cint(menuY), prefixSurf.w, prefixSurf.h)
    app.renderer.copy(prefixTex, nil, addr textDest)
    destroyTexture(prefixTex)
    currentX += prefixSurf.w + 10
    freeSurface(prefixSurf)
  

  # Draw Numbers
  for i, bpm in bpms:
    let label = $bpm
    let tempSurf = renderUTF8_Blended(app.smallFont, label.cstring, cWhite)
    var dest = rect(cint(currentX), cint(menuY), tempSurf.w, tempSurf.h)
    freeSurface(tempSurf)
    
    var hoverDest = rect(cint(currentX - 3), cint(menuY - 5), dest.w + 6, dest.h + 10)
    var isHovered = (app.mouseX >= hoverDest.x and app.mouseX <= hoverDest.x + hoverDest.w and
                     app.mouseY >= hoverDest.y and app.mouseY <= hoverDest.y + hoverDest.h)
    
    var txtColor = cWhite

    if isHovered:
      anyoneHovered = true
      # If this is a brand new number we just moved onto, reset its timer
      if app.lastTargetBpmIdx != i:
        app.lastTargetBpmIdx = i
        app.bpmHoverTimer = 0
      
      # Progress the countdown
      app.bpmHoverTimer += 16
      
      if app.bpmHoverTimer >= 500: # 500ms continuous hover completes the lock-in
        app.activeBpmIdx = i
        app.delayMs = 60000 div (bpm * 4)
        txtColor = cGreen
      else:
        # Visual transition effect: Text gets increasingly yellow as it approaches locking threshold
        let progressRatio = float(app.bpmHoverTimer) / 500.0
        let redComponent = uint8(255)
        let greenComponent = uint8(255 * progressRatio) # Fades up to full yellow (255, 255, 0)
        txtColor = color(redComponent, greenComponent, 100, 255)
        
    elif i == app.activeBpmIdx:
      txtColor = cGreen

    let surf = renderUTF8_Blended(app.smallFont, label.cstring, txtColor)
    if surf != nil:
      let tex = createTextureFromSurface(app.renderer, surf)
      app.renderer.copy(tex, nil, addr dest)
      destroyTexture(tex)
      freeSurface(surf)
    
    currentX += dest.w + 10

  # If the mouse left the options row completely, reset the selection timers
  if not anyoneHovered:
    app.lastTargetBpmIdx = -1
    app.bpmHoverTimer = 0
    
  # Draw " BPM" suffix
  let suffixSurf = renderUTF8_Blended(app.smallFont, " BPM".cstring, cWhite)
  if suffixSurf != nil:
    let suffixTex = createTextureFromSurface(app.renderer, suffixSurf)
    var textDest = rect(cint(currentX), cint(menuY), suffixSurf.w, suffixSurf.h)
    app.renderer.copy(suffixTex, nil, addr textDest)
    destroyTexture(suffixTex)
    freeSurface(suffixSurf)

  

proc renderAll(app: var ExamState) =
  discard app.renderer.setDrawColor(51, 51, 51, 255)
  app.renderer.clear()

  app.renderRealGlobe(400, 300, 160)

  app.renderStaff()
  app.renderOptions()
  app.renderSpeedMenu()

  app.renderer.present()

proc cleanup(app: var ExamState) =
  closeAudioDevice(app.device)
  app.font.close()
  app.smallFont.close()
  app.noteFont.close()
  app.hintFont.close()
  destroyRenderer(app.renderer)
  destroyWindow(app.window)
  ttfQuit()
  sdl2.quit()

# ==========================================
# MAIN EXECUTION
# ==========================================
proc main() =
  randomize()
  var p = initOptParser()
  for kind, key, val in p.getopt():
    case kind
    of cmdLongOption, cmdShortOption:
      if key == "logging" or key == "l":
        gLoggingEnabled = true
    else: discard
  var app = initExamState()
  
  app.loadCountries("exercise/paises-1.txt")
  app.loadNextQuestion()

  while app.running:
    app.handleEvents()
    app.updateAudioAndTimers()
    app.renderAll()
    sdl2.delay(16) # ~60 FPS cap

  app.cleanup()

main()

