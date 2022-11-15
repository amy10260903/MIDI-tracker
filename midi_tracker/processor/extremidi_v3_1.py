# coding: utf-8
'''
Extremidi class
latest update: 20190609
Author: PCC @ TPE
1. 只能讀取 midi、得到該有資訊，無法更改或輸出
2. 該有資訊為： noteSeries, chordSeries, pitchSeries, grooving, bpm, track_num, end_time, note_num, note_num_list, sixteenth_note_duration
'''
import pretty_midi, collections, copy, math, glob, random
import numpy as np


class Extremidi():

    def __init__(self):
        ''''''
        self.noteSeries = []
        self.chordSeries = []
        self.pitchSeries = []
        self.grooving = []
        self.bpm = []
        self.track_num = 0
        self.end_time = 0
        self.note_num = 0
        self.note_num_list = []
        self.sixteenth_note_duration = 0


    def import_midi(self, inputMIDI):
        ''''''
        midi_data = pretty_midi.PrettyMIDI(inputMIDI)
        self.bpm = int(round(midi_data.get_tempo_changes()[1][0]))
        self.end_time = midi_data.get_end_time()
        self.sixteenth_note_duration = 60.0 / 4.0 / self.bpm  # resolition = 1/16 note

        for instrument in midi_data.instruments:
            self.set_chordSeries_from_midi(instrument)
            # self.track_num += 1
            # if instrument.name == 'melody':
            #     self.set_noteSeries_from_midi(instrument)
            # if instrument.name == 'chord':
            #     self.set_chordSeries_from_midi(instrument)

        # else:
        #     print('extremidi ERROR: no melody and chord tracks. in read_midi().')

        self.match_melody_chord_info()
        self.pitchSeries = [note.pitch for note in self.noteSeries if note.pitch != 0] if self.noteSeries != [] else []
        self.note_num_list = set_note_nume_list(self.noteSeries)
        self.note_num = sum(self.note_num_list)
        self.grooving = [note.duration for note in self.noteSeries if note.pitch!=0] if self.noteSeries!=[] else []


    def set_chordSeries_from_midi(self, instrument): #input pretty midid format

        self.chordSeries = []
        s, e, v, n = 0.0, 0.0, 0.0, []
        lastChord = 0

        try:
            location = 1
            for note in instrument.notes:
                if note.start == s:
                    n.append(note.pitch)
                    s = note.start
                    e = note.end
                    v = note.velocity
                else:
                    current_chord = extremidiChord(s, e, n, v, location, self.sixteenth_note_duration, lastChord)
                    self.chordSeries.append(current_chord)
                    lastChord = current_chord
                    s = note.start
                    e = note.end
                    v = note.velocity
                    n = []
                    location += current_chord.duration
                    n.append(note.pitch)
            self.chordSeries.append(
                extremidiChord(s, e, n, v, location, self.sixteenth_note_duration, lastChord))  # 補最後一個和弦

        except IndexError:
            print('extremidi ERROR: chordSeries unset due to IndexError in set_chordSeries_from_midi().')


    def set_noteSeries_from_midi(self, instrument):

        self.noteSeries = []
        location = 1

        for note in instrument.notes:
            n = extremidiNote(note, self.chordSeries, location, self.sixteenth_note_duration)
            location += n.duration
            location = int(round(location))
            self.noteSeries.append(n)


    def match_melody_chord_info(self):

        if len(self.noteSeries)!=0 and len(self.chordSeries)!=0:
            for note in self.noteSeries:
                for chord in self.chordSeries:
                    if note.location == chord.location:
                        note.onChordDownbeat = True
                        break
                for chord in self.chordSeries:
                    if note.start >= chord.start:
                        note.correspondingChord = chord.notes
                        note.inChord = True if note.pitch % 12 in [x % 12 for x in note.correspondingChord] else False
                        if note.pitch == 0: note.inChord = False
                        continue
                    else:
                        break
        else:
            print('Please set noteSeries and chordSeries first.')


    def show_chordSeries(self):

        print('chordSeries:')
        if self.chordSeries:
            for note in self.chordSeries:
                note.show()
        else:
            print('chordSeries not set.')
        print()


    def show_noteSeries(self):

        print('noteSeries:')
        if self.noteSeries:
            for note in self.noteSeries:
                note.show()
        else:
            print('noteSeries not set.')
        print()



class extremidiNote():

    def __init__(self, note, chordSeries, location, sixteenth_note_duration):
        self.pitch = note.pitch
        self.start = note.start
        self.end = note.end
        self.velocity = note.velocity
        self.location = location
        self.dynamics = self.location % 4
        self.duration = round(round((note.end - note.start) / sixteenth_note_duration, 1) / 0.5) * 0.5
        self.atMeasure = int((self.location - 1) / 16) + 1
        timeFlag = 0.0
        chord_note = []
        if len(chordSeries) != 0:
            for chord in chordSeries:
                if self.location == chord.location:
                    self.onChordDownbeat = True
                    break
            for chord in chordSeries:
                if self.start >= chord.start:
                    self.correspondingChord = chord.notes
                    self.inChord = True if self.pitch%12 in [x%12 for x in self.correspondingChord] else False
                    if self.pitch == 0: self.inChord = False
                    continue
                else:
                    break
        else:
            self.correspondingChord = 'None'
            self.onChordDownbeat = 'None'
            self.inChord = 'None'

    def show(self):
        print('Note(start={0}, end={1}, pitch={2}, velocity={3}, location={4}, duration={5}, correspondingChord＝{6}, inChord={7}, onChordDownbeat={8}, atMeasure={9}, dynamics={10})'.format(
                self.start, self.end, self.pitch, self.velocity,self.location, self.duration, self.correspondingChord, self.inChord, self.onChordDownbeat,self.atMeasure,self.dynamics))


class extremidiChord():

    def __init__(self, start, end, notes, velocity, location, sixteenth_note_duration, lastChord):
        self.notes = notes
        self.start = start
        self.end = end
        self.velocity = velocity
        self.location = location
        self.duration = self.normalize_chord_dur(int( (end - start)/sixteenth_note_duration ) + 1)
        self.pedal_point = []
        self.root = notes[0]
        if lastChord !=0: self.pedal_point = list(set(self.notes).intersection(set(lastChord.notes)))

    def normalize_chord_dur(self, x):
        mapping = [[[0,1],1], [[3,4,5],4], [[7,8,9],8], [(15,16,17),16]]
        for item in mapping:
            if x in item[0]:
                return item[1]
        else:
            return x

    def show(self):
        print('Chord(start={0}, end={1}, chord notes={2}, root={3}, velocity={4}, location={5}, duration={6}, pedal_point={7} )'.format(self.start, self.end, self.notes, self.root, self.velocity, self.location, self.duration, self.pedal_point))


def set_note_nume_list(noteSeries):
    ''''''
    output = []
    for i in range(1, 9, 2):
        c = 0
        for note in noteSeries:
            if note.pitch == 0: continue
            if note.atMeasure == i or note.atMeasure == i+1:
                c += 1
        else:
            output.append(c)
            c = 0
    return output






# UTILS
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]
def flatten(x):
    return [a for i in x for a in flatten(i)] if isinstance(x, collections.Iterable) else [x]

def midiSynth(noteSeries, chordSeries, bpm):
    mymidi = pretty_midi.PrettyMIDI(initial_tempo=bpm)
    melody_track = pretty_midi.Instrument(program=0)
    for n in noteSeries:
        note = pretty_midi.Note(start=n.start, end=n.end, pitch=n.pitch, velocity=n.velocity)
        melody_track.notes.append(note)
    mymidi.instruments.append(melody_track)
    chord_track = pretty_midi.Instrument(program=0)
    for c in chordSeries:
        for n in c.notes:
            note = pretty_midi.Note(start=c.start, end=c.end, pitch=n, velocity=c.velocity)
            chord_track.notes.append(note)
    mymidi.instruments.append(chord_track)
    mymidi.write('tempoutput.mid')





# test
def main_test():
    m = Extremidi()
    m.import_midi('CV0028_A1.mid')

    m.show_chordSeries()
    m.show_noteSeries()

    print(m.pitchSeries)
    print(m.grooving)
    print(m.note_num)


#main_test()
