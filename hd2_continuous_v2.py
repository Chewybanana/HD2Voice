# import RealtimeSTT as rt
import RealtimeSTT.audio_recorder as rt
import logging
import os
import pyautogui
import string
import time
from difflib import SequenceMatcher as SM
import pyaudio

rt.ALLOWED_LATENCY_LIMIT = 1

os.environ["CUDA_VISIBLE_DEVICES"]=""
pyautogui.PAUSE = .05

device = 11
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print(f"Device {i}: {dev['name']} - Input Channels: {dev['maxInputChannels']}")
    if 'QuadCast' in dev['name']:
        device = i
p.terminate()

logging.basicConfig(level=logging.INFO)
DEBUG = True


stratagems = {
    "machine_gun"              : ['down', 'left', 'down', 'up', 'right'],
    "heavy_machine_gun"        : ['down', 'left', 'up', 'down', 'down'],
    "anti_material_rifle"      : ['down', 'left', 'right', 'up', 'down'],
    "stalwart"                 : ['down', 'left', 'down', 'up', 'up', 'left'],
    "expendable_anti_tank"     : ['down', 'down', 'left', 'up', 'right'],
    "recoilless_rifle"         : ['down', 'left', 'right', 'right', 'left'],
    "flamethrower"             : ['down', 'left', 'up', 'down', 'up'],
    "autocannon"               : ['down', 'left', 'down', 'up', 'up', 'right'],
    "railgun"                  : ['down', 'right', 'down', 'up', 'left', 'right'],
    "spear"                    : ['down', 'down', 'up', 'down', 'down'],
    "orbital_gatling_barrage"  : ['right', 'down', 'left', 'up', 'up'],
    "orbital_airburst_strike"  : ['right', 'right', 'right'],
    "orbital_120mm_he_barrage" : ['right', 'right', 'down', 'left', 'right', 'down'],
    "orbital_380mm_he_barrage" : ['right', 'down', 'up', 'up', 'left', 'down', 'down'],
    "orbital_walking_barrage"  : ['right', 'down', 'right', 'down', 'right', 'down'],
    "orbital_laser_strike"     : ['right', 'down', 'up', 'right', 'down'],
    "orbital_railcannon_strike": ['right', 'up', 'down', 'down', 'right'],
    "eagle_rearm"              : ['up', 'up', 'left', 'up', 'right'],
    "eagle_strafing_run"       : ['up', 'right', 'right'],
    "eagle_airstrike"          : ['up', 'right', 'down', 'right'],
    "eagle_cluster_bomb"       : ['up', 'right', 'down', 'down', 'right'],
    "eagle_napalm_airstrike"   : ['up', 'right', 'down', 'up'],
    "jump_pack"                : ['down', 'up', 'up', 'down', 'up'],
    "eagle_smoke_strike"       : ['up', 'right', 'up', 'down'],
    "eagle_110mm_rocket_pods"  : ['up', 'right', 'up', 'left'],
    "eagle_500kg_bomb"         : ['up', 'right', 'down', 'down', 'down'],
    "orbital_precision_strike" : ['right', 'right', 'up'],
    "orbital_gas_strike"       : ['right', 'right', 'down', 'right'],
    "orbital_ems_strike"       : ['right', 'right', 'left', 'down'],
    "orbital_smoke_strike"     : ['right', 'right', 'down', 'up'],
    "hmg_emplacement"          : ['down', 'up', 'left', 'right', 'right', 'left'],
    "shield_generator_relay"   : ['down', 'down', 'left', 'right', 'left', 'right'],
    "tesla_tower"              : ['down', 'up', 'right', 'up', 'left', 'right'],
    "anti_personnel_minefield" : ['down', 'left', 'down', 'up', 'right'],
    "supply_pack"              : ['down', 'left', 'down', 'up', 'up', 'down'],
    "grenade_launcher"         : ['down', 'left', 'up', 'left', 'down'],
    "laser_cannon"             : ['down', 'left', 'down', 'up', 'left'],
    "incendiary_mines"         : ['down', 'left', 'left', 'down'],
    "guard_dog_rover"          : ['down', 'up', 'left', 'up', 'right', 'right'],
    "ballistic_shield_backpack": ['down', 'left', 'down', 'down', 'up', 'left'],
    "arc_thrower"              : ['down', 'right', 'down', 'up', 'left', 'left'],
    "shield_generator_pack"    : ['down', 'up', 'left', 'right', 'left', 'right'],
    "machine_gun_sentry"       : ['down', 'up', 'right', 'right', 'up'],
    "gatling_sentry"           : ['down', 'up', 'right', 'left'],
    "mortar_sentry"            : ['down', 'up', 'right', 'right', 'down'],
    "guard_dog"                : ['down', 'up', 'left', 'up', 'right', 'down'],
    "autocannon_sentry"        : ['down', 'up', 'right', 'up', 'left', 'up'],
    "rocket_sentry"            : ['down', 'up', 'right', 'right', 'left'],
    "ems_mortar_sentry"        : ['down', 'up', 'right', 'down', 'right'],
    "sos_beacon"               : ['up', 'down', 'right', 'up'],
    "reinforce"                : ['up', 'down', 'right', 'left', 'up'],
    "upload_data"              : ['left', 'right', 'up', 'up', 'up'],
    "hellbomb"                 : ['down', 'up', 'left', 'down', 'up', 'right', 'down', 'up'],
    "resupply"                 : ['down', 'down', 'up', 'right'],
    "seaf_artillery"           : ['right', 'up', 'up', 'down'],
    "global_illumination_flare": ['right', 'right', 'left', 'left'],
    "patriot_exosuit"          : ['left', 'down', 'right', 'up', 'left', 'down', 'down'],
    "quasar_cannon"            : ['down', 'down', 'up', 'left', 'right'],
    "airburst_rocket_launcher" : ['down', 'up', 'up', 'left', 'right']
}

command_map = {
    '110': 'eagle_110mm_rocket_pods',
    'napalm': 'eagle_napalm_airstrike',
    '500': 'eagle_500kg_bomb',
    '500kg': 'eagle_500kg_bomb',
    'air strike': 'eagle_airstrike',
    'cluster': 'eagle_cluster_bomb',
    'hell': 'hellbomb',
    'nuke': 'hellbomb',
    'supply': 'resupply',
    'resupply': 'resupply',
    'quasar': 'quasar_cannon',
    'airburst': 'orbital_airburst_strike',
    'air burst': 'orbital_airburst_strike',
    'shield gen': 'shield_generator_pack',
    'rearm': 'eagle_rearm',
    're arm': 'eagle_rearm',
    '380': 'orbital_380mm_he_barrage',
    '120': 'orbital_120mm_he_barrage',
    'auto cannon': 'autocannon',
    'eat': 'expendable_anti_tank',
    'amr': 'anti_material_rifle',
    'strafing': 'eagle_strafing_run',
    'sos': 'sos_beacon',
    'artillery': 'seaf_artillery',
    'cf': 'seaf_artillery',
    'laser dog': 'guard_dog_rover',
    'rover' : 'guard_god_rover',
    'gatling': 'orbital_gatling_barrage',
    'mech': 'patriot_exosuit',  #
    'mecha': 'patriot_exosuit',  #
    'exosuit': 'patriot_exosuit',
    'hmg': 'hmg_emplacement',
    'ballistic': 'ballistic_shield_backpack',
    'laser': 'orbital_laser_strike'

}
stratagems_spaces = {k.replace('_', ' '): k for k, v in stratagems.items()}
command_map.update(stratagems_spaces)
# wake_words = ["foundation", 'foundations']
wake_words = ['destroyer']


class HDParse:
    def __init__(self, device, frame_buffer_seconds=2, sample_rate=16000, buffer_size=512):
        self.frame_buffer_seconds = frame_buffer_seconds
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size

        self.recorder = rt.AudioToTextRecorder(
            input_device_index=device, spinner=False, compute_type='float32', model='tiny.en',
            enable_realtime_transcription=True, 
            realtime_processing_pause=.1,
            on_realtime_transcription_update=self.on_rt_update, 
            initial_prompt="destroyer"
            # on_realtime_transcription_stabilized=self.on_rt_stable,
        )

    def snip_frames(self):
        total_frames = self.sample_rate * self.frame_buffer_seconds
        total_buffers = total_frames / self.buffer_size

        frame_limit = round(total_buffers)
        self.recorder.frames = self.recorder.frames[-frame_limit:]

    # def on_wakeword_detection_start(self):
    #     print("Listening for wakeword")
    #
    # def on_wakeword_detection_end(self):
    #     print("Heard wakeword")
    #
    # def on_wake(self):
    #     self.start_time = time.perf_counter()
    #     return
    #
    # def on_wake_end(self):
    #     print(time.perf_counter() - self.start_time)
    #     return

    def on_rt_update(self, updated_text):
        if DEBUG:
            print(len(self.recorder.frames))
        found = process(updated_text)
        if found:
            self.recorder.frames = self.recorder.frames[-50:]
        else:
            self.snip_frames()
        if DEBUG:
            print(len(self.recorder.frames))


def clean_text(text):
    if DEBUG:
        print(F"Raw  : {text}")
    text = text.lower()
    text = text.replace('-', ' ')
    text = text.translate(str.maketrans('', '', string.punctuation))
    if DEBUG:
        print(F"Clean: {text}")

    return text


def find_matching_command(text, command_map, threshold=.75):
    text = clean_text(text)
    matches = []
    for k, v in command_map.items():
        if k in text:
            similarity = SM(None, text, k).ratio()
            matches.append((similarity, k, v))

    # If we don't find an exact-match
    if len(matches) == 0:
        for k, v in command_map.items():
            similarity = SM(None, text, k).ratio()
            if similarity >= threshold:
                matches.append((similarity, k, v))
    print(matches)
    if len(matches) > 0:
        best_match = sorted(matches, key=lambda x: x[0], reverse=True)[0]
        return best_match[2]
    return None


def input_command(command_list):
    with pyautogui.hold('ctrlright'):
        time.sleep(.05)
        for i in command_list:
            pyautogui.keyDown(i)
            pyautogui.keyUp(i)
            time.sleep(.05)


def process(text):
    found = False
    text = clean_text(text)
    for wake_word in wake_words:
        if F"{wake_word} " in text:
            found = True
            text = text.split(F"{wake_word} ")[1]
            print(text)
            command = find_matching_command(text, command_map)
            if command is None:
                return
            print(stratagems[command])
            input_command(stratagems[command])
            break

    return found


if __name__ == '__main__':
    hd = HDParse(device=device)
    hd.recorder.start()
