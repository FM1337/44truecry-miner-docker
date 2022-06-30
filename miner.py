import os
import subprocess
import random
import time
import requests
import shutil
import base64
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook


def random_corruption_sequence():
    return [str(random.randrange(1, 200))
            for i in range(0, random.randrange(2, 15))]


def pushover_notify(cs, sf):
    if (os.getenv("PUSHOVER_TOKEN") is not None and os.getenv("PUSHOVER_USER_KEY") is not None):
        # If you have pushover's vars in the env, then we can notify on success
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER_KEY"),
            "message": "A truecry result was found, corruption sequence is %s\nState file can be found under %s" % (cs, sf)
        },
            files={
            "attachment": ("image.bmp", open("helpers/temp_screen.bmp", "rb"), "image/bmp")
        })


def discord_notify(cs, sf):
    if(os.getenv("DISCORD_WEBHOOK") is not None):
        message = "Oh hey, a non-`rst 38`-crash truecry result has been found!\nCorruption Sequence is `%s`\nAttached is both the save state file and emulator image from the result" % (
            cs)
        webhook = DiscordWebhook(url=os.getenv(
            "DISCORD_WEBHOOK"), content=message)
        with open("./results/%s" % (sf), "rb") as f:
            webhook.add_file(file=f.read(), filename=sf)
        with open("./helpers/temp_screen.bmp", "rb") as f:
            webhook.add_file(file=f.read(), filename="emulator_screenshot.bmp")
        webhook.execute()


def discord_error_notify(code, stdout, stderr):
    if(os.getenv("DISCORD_WEBHOOK") is not None):
        message = "It looks like BGB in the 44truecry-miner docker container returned a non-zero return code, this is unexpected, the code it returned was %d" % (
            code)
        webhook = DiscordWebhook(url=os.getenv(
            "DISCORD_WEBHOOK"), content=message)
        webhook.execute()
        # We also want to send the output of the command to the discord channel
        message = "The following is base64 encoded stdout and stderr from the miner:\n%s\n%s" % (
            stdout, stderr)
        webhook = DiscordWebhook(url=os.getenv(
            "DISCORD_WEBHOOK"), content=message)
        webhook.execute()


load_dotenv()

bgb_path = os.path.join("helpers", "bgb.exe")
sna_path = os.path.join("helpers", "state.sna")
base_sna_path = os.path.join("helpers", "base.sna")
demo_path = os.path.join("helpers", "demo.dem")
output_screen_path = os.path.join("temp_screen.bmp")
output_sna_path = os.path.join("helpers", "temp_state.sna")

# os.path.join("helpers", "generator", "corruption_generator")
generator_path = "./corruption_generator"
generator_output = os.path.join("helpers", "generator", "sram_final.dmp")
generator_cwd = os.path.join("helpers", "generator")

sentinel = b"magicalsentinelstringthatisprettymuchguaranteedtoappearonlyonce"

cmdline = [
    "wine64",
    bgb_path,
    "-rom", sna_path,
    "-demoplay", demo_path,
    "-screenonexit", output_screen_path,
    "-stateonexit", output_sna_path,
    "-nowarn", "-hf"
]

print("==============================================================")
print("     THEZZAZZGLITCH'S TRUECRYCOIN MINER (LINUX EDITION)       ")
print("==============================================================")
print("\"Truecrycoin\" is a distributed computing project of the")
print("Pokemon glitching community, attempting to reproduce some rare")
print("effects of certain glitch Pokemon species - the most prevalent")
print("of them all being the \"4 4's true cry\".")
print("==============================================================")
print("Partaking in the Truecrycoin project is fully voluntary.")
print("If you found this software running on your computer system")
print("without consent, close this program immediately.")
print("==============================================================")
print("A notification will be displayed if anything useful is found.")
print("You can leave this software running in the background and")
print("check periodically for updates.")
print("==============================================================")
print("Dockerfile and modifications to get functioning on Linux by FM1337")
print("Requires wine, because BGB is closed source and won't be built for Linux >_<")
print("So it's slower, but hey, at-least you can throw it on a cheap 5 dollar VPS and let it go")
print("ROM isn't included, dump your own, or do what you gotta do.")
print("==============================================================")
print("As an added benefit, I added support for sending notifications.")
print("As of this version, it supports discord webhooks and pushover")
print("Might add some more later, who knows?")
print("==============================================================")

total_counter = 0
success_counter = 0
hash_rate = 0.0

t_start = time.time()

while 1:
    corruption_sequence = random_corruption_sequence()
    print("\r%i iterations, %i successes (%.2f corruptions/min)".ljust(62)
          % (total_counter, success_counter, hash_rate), end="")
    # generate the actual SRAM corruption from sequence
    subprocess.call(executable=generator_path,
                    args=corruption_sequence, cwd=generator_cwd, shell=True)
    # copy the SRAM corruption data into savestate
    with open(base_sna_path, "rb") as f:
        sna_data = bytearray(f.read())
    with open(generator_output, "rb") as f:
        sram_data = f.read()
    sna_sram_data_at = sna_data.index(sentinel)
    if len(sram_data) != 0x2000:
        raise ValueError("invalid sram data")
    sna_data[sna_sram_data_at:sna_sram_data_at+0x2000] = sram_data
    with open(sna_path, "wb") as f:
        f.write(sna_data)
    # run the emulation
    output = subprocess.run(cmdline, capture_output=True, encoding="utf-8")
    if output.returncode != 0:
        # base64 encode the output of the command
        stdout = base64.b64encode(output.stdout).decode("utf-8")
        stderr = base64.b64encode(output.stderr).decode("utf-8")
        discord_error_notify(output.returncode, stdout, stderr)
        continue
    # check the resulting state
    with open(output_sna_path, "rb") as f:
        sna_data = f.read()
    if sna_data.find(b"PC\x00\x02\x00\x00\x00\x38\x00") == -1:
        temp_file_name = "success_%i_%i_%f.sna" % (
            total_counter, random.randrange(1, 100000), time.time())
        shutil.copyfile(output_sna_path, "./results/%s" % (temp_file_name))
        print("")
        print("==============================================================")
        print("Encountering 4 4 with the currently checked data didn't yield")
        print("an rst 38 crash. Either 4 4's true cry was finally reproduced,")
        print("or you just found some other interesting effect.")
        print("In either case, it really looks like you've successfully mined")
        print("a Truecrycoin. Congratulations!")
        print("==============================================================")
        print("The SRAM corruption sequence in question:")
        print(":".join(corruption_sequence))
        print("Report this to the nearest glitch scientist in your area!")
        print("==============================================================")
        print("To aid in further research, relevant save state file has been")
        print("copied to %s." % temp_file_name)
        print("==============================================================")
        success_counter += 1
        pushover_notify(":".join(corruption_sequence),
                        "./results/%s" % (temp_file_name))
        discord_notify(":".join(corruption_sequence), temp_file_name)
    # update counters
    total_counter += 1
    hash_rate = (total_counter * 60) / (time.time() - t_start)
