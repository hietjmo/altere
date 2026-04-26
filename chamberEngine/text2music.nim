
# nim c -d:release -r text2music.nim texts/europa.txt 120

import std/[os, strutils, unicode, math, sequtils, strformat]
import sdl2, sdl2/audio, sdl2/ttf
import chamberEngine

proc main() =
  if paramCount() < 1:
    quit("Usage: ./text2music <textfile.txt> [bpm] [output.wav]")

  let filename = paramStr(1)
  var text = ""
  try: text = readFile(filename)
  except IOError: quit("Could not read file: " & filename)

  var bpm = 120 # Default to 120 Beats Per Minute
  if paramCount() >= 2: bpm = parseInt(paramStr(2))
  var outFile = ""
  if paramCount() >= 3: outFile = paramStr(3)
  var delayMs = 60000 div (bpm * 4)
  if delayMs <= 0: delayMs = 1


  # ==========================================
  # PATH A: OFFLINE FILE EXPORT (WORD-BY-WORD SRT)
  # ==========================================
  if outFile != "":
    echo "Rendering ", filename, " to ", outFile, " at ", bpm, " BPM..."
    var masterTrack: seq[int16] = @[]
    var lastWasPeriod = false
    let runeSeq = toSeq(text.runes)
    
    var currentTimeMs = 0
    var srtContent = ""
    var subtitleIndex = 1
    
    # This stores the "accumulated" text for the CURRENT word
    var runningText = ""
    var clearTextNext = false
    
    for i in 0 ..< runeSeq.len:
      let charStr = $runeSeq[i]
      
      # 1. Capture start time BEFORE the pre-breath.
      # This prevents 1-frame flickering in the video player.
      let startTime = currentTimeMs
      
      if charStr in [",", ".", "!", "?", "\n"]:
        masterTrack.add(newSeq[int16](int(44.1 * 5.0)))
        currentTimeMs += 5

      # 2. Add the actual character tone
      masterTrack.add(generateTone(charStr, delayMs))
      
      # 3. Context-Aware Delays
      var pauseMs = 0
      if lastWasPeriod and charStr == " ": pauseMs = delayMs * 2
      elif charStr == "!" or charStr == "?": pauseMs = delayMs * 2
      elif charStr == "," or charStr == "\n": pauseMs = delayMs
      elif charStr == " ": pauseMs = delayMs div 2
      
      # --- NEW: WORD-BY-WORD RESET LOGIC ---
      if clearTextNext:
        runningText = ""
        clearTextNext = false
        
      if charStr == "\n":
        currentTimeMs += delayMs + pauseMs
        if pauseMs > 0:
          masterTrack.add(newSeq[int16](int(44.1 * float(pauseMs))))
        
        lastWasPeriod = false
        clearTextNext = true # The next character starts a fresh word
        continue 
      
      # 4. Prepare and format the subtitle text
      runningText.add(charStr)
      let textToPrint = runningText.strip() # Removes trailing spaces for the visual output
      
      # Include the pauseMs in the endTime so the word STAYS on screen during the silence!
      let endTime = currentTimeMs + delayMs + pauseMs
      
      # Only write a subtitle if there are actual letters to show
      if textToPrint.len > 0:
        let startStr = fmt"{startTime div 3600000:02}:{(startTime mod 3600000) div 60000:02}:{(startTime mod 60000) div 1000:02},{startTime mod 1000:03}"
        let endStr = fmt"{endTime div 3600000:02}:{(endTime mod 3600000) div 60000:02}:{(endTime mod 60000) div 1000:02},{endTime mod 1000:03}"
        
        srtContent.add($subtitleIndex & "\n" & startStr & " --> " & endStr & "\n" & textToPrint & "\n\n")
        subtitleIndex += 1
      
      # 5. Finalize timing for this loop iteration
      currentTimeMs += delayMs + pauseMs
      if pauseMs > 0:
        masterTrack.add(newSeq[int16](int(44.1 * float(pauseMs))))
        
      lastWasPeriod = (charStr == ".")
      
      # If this character was a space, tell the loop to clear the text on the NEXT letter
      if charStr == " ":
        clearTextNext = true
        

    # Save the files
    saveWav(outFile, masterTrack)
    let srtFile = outFile.changeFileExt("srt")
    writeFile(srtFile, srtContent)
    
    # Print the command
    let mp3File = outFile.changeFileExt("mp3")
    let mp4File = outFile.changeFileExt("mp4")
    echo "\n=== EXPORT COMPLETE ==="
    echo "Audio: ", outFile, " | Subtitles: ", srtFile
    
    echo fmt"ffmpeg -i {outFile} -q:a 2 {mp3File} && rm {outFile}"
    echo fmt"""ffmpeg -f lavfi -i color=c=gray:s=1280x720:r=30 -i {outFile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {mp4File} && rm {outFile}"""
    return

  # ==========================================
  # PATH B: LIVE SDL PLAYBACK (Original Code)
  # ==========================================


  if sdl2.init(INIT_VIDEO or INIT_AUDIO) != SdlSuccess: quit("Failed to init SDL.")
  if ttfInit() != SdlSuccess: quit("Failed to init TTF.")
  
  let window = createWindow("Text2Music Player", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, SDL_WINDOW_SHOWN)
  let renderer = createRenderer(window, -1, Renderer_Accelerated)
  
  let font = openFont("fonts/DejaVuSansMono.ttf", 12)
  if font == nil: quit("Failed to load fonts/DejaVuSansMono.ttf")
  
  var want, have: AudioSpec
  want.freq = 44100
  want.format = AUDIO_S16
  want.channels = 1
  want.samples = 1024
  want.callback = nil 
  
  var device = openAudioDevice(nil, 0, addr want, addr have, 0)
  if device == 0: quit("Failed to open audio device.")
  pauseAudioDevice(device, 0)

  echo "Playing: ", filename, " at ", delayMs, "ms per character..."
  echo "[Controls] Space: Pause | R: Restart | Esc/Q: Quit\n"
  sdl2.delay(1000)

  var event = defaultEvent
  var running = true
  var paused = false

  let maxLines = 30
  let cWhite = color(255, 255, 255, 255)
  # --- NEW: Outer loop to handle restarts ---
  while running:
    var displayLines = @[""]
    var shouldRestart = false
    
    closeAudioDevice(device)
    device = openAudioDevice(nil, 0, addr want, addr have, 0)
    pauseAudioDevice(device, 0)

    # --- THE NEW INFINITE TYPEWRITER LOOP ---
    let runeSeq = toSeq(text.runes)
    var i = 0
    var lastWasPeriod = false
    
    while running and not shouldRestart:
      # If we hit the end of the text, loop back to the first character!
      if i >= runeSeq.len: 
        i = 0
        displayLines = @[""] # Optional: Clears the screen when it restarts
      
      let r = runeSeq[i]
      let charStr = $r

      # 1. Main Event Poll
      while pollEvent(event):
        if event.kind == QuitEvent: running = false
        elif event.kind == KeyDown:
          let sym = event.evKeyboard.keysym.sym
          if sym == K_ESCAPE or sym == K_q: running = false
          elif sym == K_SPACE: paused = not paused
          elif sym == K_r: shouldRestart = true 

      # 2. Pause Trap
      while paused and running and not shouldRestart:
        sdl2.delay(50) 
        while pollEvent(event):
          if event.kind == QuitEvent: running = false
          elif event.kind == KeyDown:
            let sym = event.evKeyboard.keysym.sym 
            if sym == K_ESCAPE or sym == K_q: running = false
            elif sym == K_SPACE: paused = not paused
            elif sym == K_r: shouldRestart = true 

      if not running or shouldRestart: break
      
      # Update Text State
      if charStr == "\n":
        displayLines.add("")
      else:
        displayLines[^1].add(charStr)
        if displayLines[^1].runeLen > 95 and charStr == " ":
          displayLines.add("")

      if displayLines.len > maxLines:
        displayLines.delete(0)

      # Render Screen
      discard renderer.setDrawColor(51, 51, 51, 255) 
      renderer.clear()

      for i, line in displayLines:
        if line.len > 0:
          let surf = renderUTF8_Blended(font, line.cstring, cWhite)
          if surf != nil:
            let tex = createTextureFromSurface(renderer, surf)
            var dest = rect(30, 30 + cint(i * 18), surf.w, surf.h)
            renderer.copy(tex, nil, addr dest)
            destroyTexture(tex)
            freeSurface(surf)
      
      renderer.present()

      # --- THE PRE-BREATH FOR PUNCTUATION ---
      if charStr in [",", ".", "!", "?", "\n"]:
        while getQueuedAudioSize(device) > 0 and running and not shouldRestart:
          sdl2.delay(5)

      # Play Audio
      playTone(device, charStr, delayMs)

      # 3. Smart Wait Loop
      while getQueuedAudioSize(device) > 4000 and running and not shouldRestart:
        sdl2.delay(10)
        while pollEvent(event):
          if event.kind == QuitEvent: running = false
          elif event.kind == KeyDown:
            let sym = event.evKeyboard.keysym.sym
            if sym == K_ESCAPE or sym == K_q: running = false
            elif sym == K_SPACE: paused = not paused
            elif sym == K_r: shouldRestart = true 

      if not running or shouldRestart: break

      # --- CONTEXT-AWARE PUNCTUATION DELAYS ---
      if lastWasPeriod and charStr == " ":
        sdl2.delay(uint32(delayMs * 2)) # Extra pause for period followed by space
      
      lastWasPeriod = (charStr == ".")

      if charStr == "!" or charStr == "?":
        sdl2.delay(uint32(delayMs * 2))
      elif charStr == "," or charStr == "\n":
        sdl2.delay(uint32(delayMs))
      elif charStr == " ":
        sdl2.delay(uint32(delayMs div 2))
        
      # --- MOVE TO NEXT CHARACTER ---
      inc i

    # If we manually quit or restarted, break the outer loop so it closes cleanly
    if not shouldRestart:
      break 

  sdl2.delay(1000)
  closeAudioDevice(device)
  font.close()
  destroyRenderer(renderer)
  destroyWindow(window)
  ttfQuit()
  sdl2.quit()
  echo "\n\nPlayback stopped."

main()


