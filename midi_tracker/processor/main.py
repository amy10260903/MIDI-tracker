# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Project midigen 2022.11
Requirement
python==3.6

'''
import os, collections, datetime, shutil
import time

import pretty_midi

from .extremidi_v3_1 import Extremidi

# imputMIDI = 'input.mid'
midi_template_FILEPATH = 'midi_templates'
midi_output_FILEPATH = 'midi_output'
# outputMIDIdir = 'download'

LOWEND_RANGE = [20, 45]

def flatten(x):
    return [a for i in x for a in flatten(i)] if isinstance(x, collections.Iterable) else [x]

def flatten_list(l):
    return [item for sublist in l for item in sublist]




###==========bass
def snap_to_lowendbass(note, rootnote):
    ref_root = [rootnote+12*i for i in range(-2, 4)]
    # print(ref_root)
    # print('in', note)
    note = min(ref_root, key=lambda x: abs(x - note))
    # while note > LOWEND_RANGE[1]: note -=12
    # while note < LOWEND_RANGE[0]: note +=12
    # print('out', note)
    return note

def build_bass(ref_time_interval, ref_chord, base_dir=None):
    # template processing: bass
    INPUT_FILEPATH = os.path.join(base_dir, midi_template_FILEPATH, "bass")
    OUTPUT_FILEPATH = os.path.join(base_dir, midi_output_FILEPATH, "bass")
    for dirPath, dirNames, files in os.walk(INPUT_FILEPATH):
        for file in files:
            if file[0] == '.': continue
            midi_data = pretty_midi.PrettyMIDI(os.path.join(INPUT_FILEPATH, file))
            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        for i in range(0, len(ref_time_interval)):
                            if note.start >= ref_time_interval[i][0] and note.start <= ref_time_interval[i][1]:
                                note.pitch=snap_to_lowendbass(note.pitch, ref_chord[i][1])
            # output_filename = os.path.join(outputMIDIdir, file.split('/')[-1])
            midi_data.write(os.path.join(OUTPUT_FILEPATH,file))
            print(file + '... Done')


###==========pad
def snap_to_ref_chord_pad(note, ref_chordNotes, root, highend_avg, used_notes):
    ref_chordNotes.sort()
    ref_chordExt = ref_chordNotes + flatten([[n+12 if n <= highend_avg else n-12] for n in ref_chordNotes[1:]]) + flatten([[n+24 if n <= highend_avg else n] for n in ref_chordNotes[1:]])
    ref_chordExt += [root+12*k for k in range(-2, 0)]
    ref_chordExt = [j for j in ref_chordExt if j not in used_notes]
    target_note = min(ref_chordExt, key=lambda x:abs(x-note))
    ref_chordNotes = [i for i in ref_chordNotes if i !=target_note]
    return target_note, ref_chordNotes
def build_pad(ref_time_interval, ref_chord, base_dir=None):
    # template processing: pad
    INPUT_FILEPATH = os.path.join(base_dir, midi_template_FILEPATH, "pad")
    OUTPUT_FILEPATH = os.path.join(base_dir, midi_output_FILEPATH, "pad")
    for dirPath, dirNames, files in os.walk(INPUT_FILEPATH):
        for file in files:
            if file[0] == '.': continue
            midi_data = pretty_midi.PrettyMIDI(os.path.join(INPUT_FILEPATH, file))
            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for i in range(0, len(ref_time_interval)):
                        ref_chordNotes = ref_chord[i][0]
                        used_notes = []
                        for note in instrument.notes:
                            if note.start >= ref_time_interval[i][0] and note.start < ref_time_interval[i][1]:
                                note.pitch, ref_chordNotes = snap_to_ref_chord_pad(note = note.pitch,
                                                                                   ref_chordNotes = ref_chordNotes,
                                                                                   root = ref_chord[i][1],
                                                                                   highend_avg = ref_chord[i][2],
                                                                                   used_notes = used_notes)
                                used_notes.append(note.pitch)
                            if len(ref_chordNotes) <1:
                                ref_chordNotes = ref_chord[i][0]
                                used_notes = []
            midi_data.write(os.path.join(OUTPUT_FILEPATH, file))
            print(file + '... Done')


###==========chord
def snap_to_ref_chord_chord(note, ref_chordNotes, root, highend_avg, used_notes):
    print('1',  ref_chordNotes)
    ref_chordNotes.sort()
    # ref_chordExt = ref_chordNotes + flatten([[n+12 if n <= highend_avg else n-12] for n in ref_chordNotes[1:]]) + flatten([[n+24 if n <= highend_avg else n] for n in ref_chordNotes[1:]]) +  [root]
    ref_chordExt = flatten_list([[n + 12*i for n in ref_chordNotes[1:]] for i in range(-2, 4)])
    print(ref_chordExt)
    print(used_notes)
    # ref_chordExt = [j for j in ref_chordExt if j not in used_notes]
    print(ref_chordExt)
    target_note = min(ref_chordExt, key=lambda x:abs(x-note))
    # ref_chordNotes = [i for i in ref_chordNotes if i !=target_note]
    print('2', ref_chordNotes)
    return target_note, ref_chordNotes

def build_chord(ref_time_interval, ref_chord, base_dir=None):
    # template processing: chord
    INPUT_FILEPATH = os.path.join(base_dir, midi_template_FILEPATH, "chord")
    OUTPUT_FILEPATH = os.path.join(base_dir, midi_output_FILEPATH, "chord")
    for dirPath, dirNames, files in os.walk(INPUT_FILEPATH):
        for file in files:
            if file[0] == '.': continue
            midi_data = pretty_midi.PrettyMIDI(os.path.join(INPUT_FILEPATH, file))
            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    # last_note = 0
                    for i in range(0, len(ref_time_interval)):
                        ref_chordNotes = ref_chord[i][0]
                        used_notes = []
                        print('refresh A', ref_chordNotes)
                        for note in instrument.notes:
                            if note.start >= ref_time_interval[i][0] and note.start < ref_time_interval[i][1]:
                                print(i, note)
                                note.pitch, ref_chordNotes = snap_to_ref_chord_chord(note=note.pitch,
                                                                                     ref_chordNotes=ref_chordNotes,
                                                                                     root=ref_chord[i][1],
                                                                                     highend_avg=ref_chord[i][2],
                                                                                     used_notes=used_notes)
                                print(note.pitch, ref_chordNotes)
                                used_notes.append(note.pitch)
                            if len(ref_chordNotes) < 1:
                                ref_chordNotes = ref_chord[i][0]
                                used_notes = []
                                print('refresh B', ref_chordNotes)
                        # last_note = note.pitch
                        # ref_chord[i][0] = ref_chord[i][0][:1] + ref_chord[i][1:].remove(note.pitch)

            # output_filename = os.path.join(outputMIDIdir, file.split('/')[-1])
            midi_data.write(os.path.join(OUTPUT_FILEPATH, file))
            print(file + '... Done')

def package(outputDir, outMIDIDir):
    output_zipfilename = str(datetime.datetime.now()).split('.')[0].replace('-','').replace(':','').replace(' ','_')
    output_zipfilepath = os.path.join(outputDir, output_zipfilename)
    print(output_zipfilepath)
    shutil.make_archive(output_zipfilepath, 'zip', outMIDIDir)

    return f'{output_zipfilename}.zip'

def main(inputMIDI, baseDir):
    # get input chord info
    refmidi = Extremidi()
    refmidi.import_midi(inputMIDI)
    ref_time_interval = [(chord.start, chord.end) for chord in refmidi.chordSeries]
    ref_chord = [[chord.notes, chord.root,  sum(chord.notes[1:])/len(chord.notes[1:])] for chord in refmidi.chordSeries]
    # print(ref_time_interval)
    # print(ref_chord)

    refMIDIDir = os.path.join(baseDir, 'processor')
    build_bass(ref_time_interval=ref_time_interval, ref_chord=ref_chord, base_dir=refMIDIDir)
    build_pad(ref_time_interval=ref_time_interval, ref_chord=ref_chord, base_dir=refMIDIDir)
    build_chord(ref_time_interval=ref_time_interval, ref_chord=ref_chord, base_dir=refMIDIDir)
    time.sleep(1)

    outputDir = os.path.join(baseDir, 'download')
    outMIDIDir = os.path.join(baseDir, 'processor', midi_output_FILEPATH)
    output_filename = package(outputDir, outMIDIDir)

    print('done')  # Press ⌘F8 to toggle the breakpoint.
    return output_filename

if __name__ == '__main__':
    main()
