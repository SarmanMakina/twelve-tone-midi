import random
import os
from datetime import datetime
from midiutil import MIDIFile

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

def create_midi(note_list, folder, filename="twelve_tone.mid", tempo=120, start_time=0):
    midi = MIDIFile(1)
    track = 0
    channel = 0
    volume = 100

    midi.addTempo(track, start_time, tempo)

    for i, note in enumerate(note_list):
        midi_note = 60 + note  # C4 = 60
        midi.addNote(track, channel, midi_note, start_time + i, 1, volume)

    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as output_file:
        midi.writeFile(output_file)

    print(f"{filepath} dosyası oluşturuldu.")
    return filepath  # Geri dön, gerekirse kullan

def generate_tone_row():
    row = list(range(12))
    random.shuffle(row)
    return row

def invert_tone_row(row):
    first = row[0]
    return [(first - (n - first)) % 12 for n in row]

def retrograde_tone_row(row):
    return row[::-1]

def retrograde_inversion_tone_row(row):
    inversion = invert_tone_row(row)
    return inversion[::-1]

def create_combined_midi(sequences, folder, filename="combined.mid", tempo=120):
    midi = MIDIFile(1)
    track = 0
    channel = 0
    volume = 100
    time = 0

    midi.addTempo(track, time, tempo)

    for seq in sequences:
        for i, note in enumerate(seq):
            midi_note = 60 + note
            midi.addNote(track, channel, midi_note, time + i, 1, volume)
        time += len(seq) + 1  # +1 boşluk

    filepath = os.path.join(folder, filename)
    with open(filepath, "wb") as output_file:
        midi.writeFile(output_file)

    print(f"{filepath} dosyası oluşturuldu (birleştirilmiş).")

while True:
    # 1) Her çalıştırmada klasör oluştur
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"output_{now}"
    os.makedirs(folder_name, exist_ok=True)
    print(f"\nÇıktı klasörü: {folder_name}")

    print("\n=== 12 Ton Dizisi Üretici ===")
    print("1. Rastgele dizi oluştur")
    print("2. Kromatik dizi kullan (0-11)")
    choice = input("Seçiminiz (1 veya 2): ")

    if choice == '1':
        row = generate_tone_row()
    elif choice == '2':
        row = list(range(12))
    else:
        print("Geçersiz seçim!")
        continue

    print("Başlangıç dizisi:")
    print([note_names[n] for n in row])

    # Orijinal her zaman kaydedilir
    create_midi(row, folder_name, "original.mid")

    print("\nDönüşüm seçin:")
    print("1. Inversiyon")
    print("2. Retrograd")
    print("3. Retrograd Inversiyon")
    print("4. Hepsi (Orijinal + tüm dönüşümler + birleşik)")
    print("5. Çıkış")

    transform = input("Seçiminiz: ")

    if transform == '1':
        inversion = invert_tone_row(row)
        print("Inversiyon:", [note_names[n] for n in inversion])
        create_midi(inversion, folder_name, "inversion.mid")
        create_combined_midi([row, inversion], folder_name, "combined.mid")

    elif transform == '2':
        retrograde = retrograde_tone_row(row)
        print("Retrograd:", [note_names[n] for n in retrograde])
        create_midi(retrograde, folder_name, "retrograde.mid")
        create_combined_midi([row, retrograde], folder_name, "combined.mid")

    elif transform == '3':
        retro_inv = retrograde_inversion_tone_row(row)
        print("Retrograd Inversiyon:", [note_names[n] for n in retro_inv])
        create_midi(retro_inv, folder_name, "retrograde_inversion.mid")
        create_combined_midi([row, retro_inv], folder_name, "combined.mid")

    elif transform == '4':
        inversion = invert_tone_row(row)
        retrograde = retrograde_tone_row(row)
        retro_inv = retrograde_inversion_tone_row(row)
        print("Inversiyon:", [note_names[n] for n in inversion])
        print("Retrograd:", [note_names[n] for n in retrograde])
        print("Retrograd Inversiyon:", [note_names[n] for n in retro_inv])
        create_midi(inversion, folder_name, "inversion.mid")
        create_midi(retrograde, folder_name, "retrograde.mid")
        create_midi(retro_inv, folder_name, "retrograde_inversion.mid")
        create_combined_midi([row, inversion, retrograde, retro_inv], folder_name, "combined.mid")

    elif transform == '5':
        print("Program sonlandırıldı.")
        break

    else:
        print("Geçersiz seçim!")

    again = input("\nYeni bir dizi üretmek ister misiniz? (e/h): ")
    if again.lower() != 'e':
        print("Hoşça kal!")
        break
