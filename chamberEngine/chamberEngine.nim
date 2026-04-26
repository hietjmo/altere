
# chamberEngine.nim

import std/[strutils, unicode, math, streams]
import sdl2/audio

type WaveForm* = enum 
  wfFlute, wfMarimba, wfPluck, wfXylo, wfGlock, 
  wfKick, wfSnare, wfWoodClick, wfThud, wfBling

proc toStrSeq(s: string): seq[string] =
  for r in s.runes: result.add($r)

let g1 = toStrSeq("EAIOUY")
let g2 = toStrSeq("NSTRLCDPM")
let g3 = toStrSeq("VBGHFQXJKZW")
let g4 = toStrSeq("01234")
let g5 = toStrSeq("56789")

proc getAudioSpec(s: string): tuple[freq: float, wave: WaveForm] =
  if s == " ": return (0.0, wfFlute)
  if s == "\n" or s == "\r": return (60.0, wfKick)  
  if s == ".": return (100.0, wfKick)
  if s == ",": return (2093.00, wfBling)
  if s == "!": return (0.0, wfSnare)                
  if s == "?": return (400.0, wfMarimba)            
  if s == "\b": return (100.0, wfThud)

  let upC = s.toUpper()
  
  let vowelFreqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00] 
  let consFreqs  = [130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94, 261.63, 293.66] 
  let rareFreqs  = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25, 587.33, 659.25, 698.46] 
  let xyloFreqs  = [523.25, 587.33, 659.25, 783.99, 880.00]
  let glockFreqs = [1046.50, 1174.66, 1318.51, 1567.98, 1760.00]

  let i1 = g1.find(upC)
  if i1 >= 0: return (vowelFreqs[i1], wfFlute)
  let i2 = g2.find(upC)
  if i2 >= 0: return (consFreqs[i2], wfMarimba)
  let i3 = g3.find(upC)
  if i3 >= 0: return (rareFreqs[i3], wfPluck)
  let i4 = g4.find(s)
  if i4 >= 0: return (xyloFreqs[i4], wfXylo)
  let i5 = g5.find(s)
  if i5 >= 0: return (glockFreqs[i5], wfGlock)

  return (200.0, wfWoodClick)

proc saveWav*(filename: string, samples: seq[int16], sampleRate: int = 44100) =
  var f = newFileStream(filename, fmWrite)
  if f == nil:
    quit("Could not open file for writing: " & filename)
    
  let dataSize = samples.len * 2 # 2 bytes per int16 sample
  let fileSize = 36 + dataSize
  
  # Write the standard WAV Header
  f.write("RIFF")
  f.write(int32(fileSize))
  f.write("WAVE")
  f.write("fmt ")
  f.write(int32(16))              # Subchunk1Size (16 for PCM)
  f.write(int16(1))               # AudioFormat (1 = PCM)
  f.write(int16(1))               # NumChannels (1 = Mono)
  f.write(int32(sampleRate))      # SampleRate
  f.write(int32(sampleRate * 2))  # ByteRate (SampleRate * NumChannels * BitsPerSample/8)
  f.write(int16(2))               # BlockAlign (NumChannels * BitsPerSample/8)
  f.write(int16(16))              # BitsPerSample
  
  # Write the Data chunk
  f.write("data")
  f.write(int32(dataSize))
  for s in samples:
    f.write(s)
    
  f.close()
  echo "Successfully saved audio to: ", filename



proc generateTone*(s: string, durationMs: int): seq[int16] =
  let (freq, wave) = getAudioSpec(s)
  let sampleRate = 44100.0
  let duration = durationMs.float / 1000.0 
  let amplitude = 4000.0
  let samples = int(sampleRate * duration)
  var buffer = newSeq[int16](samples)
  
  for i in 0 ..< samples:
    let t = i.float / sampleRate
    var val = 0.0
    var envelope = 0.0
    
    case wave:
    of wfFlute:
      val = sin(2.0 * PI * freq * t)
      envelope = exp(-4.0 * t)  
    of wfMarimba:
      let period = 1.0 / freq
      let phase = (t mod period) / period
      val = (if phase < 0.5: 4.0 * phase - 1.0 else: 3.0 - 4.0 * phase) * 1.5
      envelope = exp(-12.0 * t) 
    of wfPluck:
      let period = 1.0 / freq
      let phase = (t mod period) / period
      val = if phase < 0.5: 4.0 * phase - 1.0 else: 3.0 - 4.0 * phase
      envelope = exp(-25.0 * t) 
    of wfXylo:
      let period = 1.0 / freq
      let phase = (t mod period) / period
      val = (if phase < 0.5: 4.0 * phase - 1.0 else: 3.0 - 4.0 * phase) * 1.5
      envelope = exp(-8.0 * t)  
    of wfGlock:
      val = sin(2.0 * PI * freq * t)
      envelope = exp(-3.0 * t)  
    of wfKick:
      val = sin(2.0 * PI * freq * t)
      envelope = exp(-10.0 * t) 
    of wfSnare:
      val = sin(t * 50000.0) 
      envelope = exp(-25.0 * t) 
    of wfThud:
      # The classic low, ugly square wave for errors
      let period = 1.0 / freq
      let phase = (t mod period) / period
      val = if phase < 0.5: 1.0 else: -1.0
      envelope = exp(-15.0 * t)
    of wfWoodClick:
      let period = 1.0 / freq
      let phase = (t mod period) / period
      val = if phase < 0.5: 4.0 * phase - 1.0 else: 3.0 - 4.0 * phase
      envelope = exp(-25.0 * t)
    of wfBling:
      val = sin(2.0 * PI * freq * t)
      envelope = exp(-12.0 * t)
    var currentAmp = amplitude
    if wave == wfWoodClick:
      currentAmp = if s == ",": amplitude * 0.5 else: amplitude * 0.2
    elif wave == wfBling:
      currentAmp = amplitude * 0.4
      
    # Save the math to the buffer for EVERY instrument!
    buffer[i] = int16(val * currentAmp * envelope)
  return buffer


proc playTone*(device: AudioDeviceID, s: string, delayMs: int) =
  var buffer = generateTone(s, delayMs)
  if buffer.len > 0:
    discard queueAudio(device, addr buffer[0], uint32(buffer.len * 2))



