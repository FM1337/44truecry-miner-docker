FROM scottyhardy/docker-wine

# Install some prereqs
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3-pip \
    g++\
    gcc\
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install python-dotenv discord-webhook

WORKDIR /44cry

# Grab latest version of bgb
RUN mkdir helpers
RUN wget https://bgb.bircd.org/bgb.zip
RUN unzip -j bgb.zip bgb.exe -d helpers/
RUN rm bgb.zip

# Copy the needed files
COPY ./miner.py /44cry/miner.py
COPY ./helpers/bgb.ini /44cry/helpers/bgb.ini
COPY ./helpers/demo.dem /44cry/helpers/demo.dem
COPY ./helpers/state.sna /44cry/helpers/state.sna
COPY ./helpers/base.sna /44cry/helpers/base.sna
COPY ./helpers/yellow.sav /44cry/helpers/yellow.sav
COPY ./helpers/generator/corruption_generator.cpp /44cry/helpers/generator/corruption_generator.cpp
COPY ./helpers/generator/sram.cpp /44cry/helpers/generator/sram.cpp
COPY ./helpers/generator/behavior_c6.txt /44cry/helpers/generator/behavior_c6.txt
COPY ./helpers/generator/behavior_dc.txt /44cry/helpers/generator/behavior_dc.txt
COPY ./helpers/generator/sram_start.dmp /44cry/helpers/generator/sram_start.dmp
COPY ./run.sh /44cry/run.sh

# Build the generator
RUN g++ ./helpers/generator/corruption_generator.cpp -o ./helpers/generator/corruption_generator

# Remove g++ and gcc
RUN apt-get remove -y \
    g++ \
    gcc

RUN mkdir /44cry/results

RUN chmod +x /44cry/run.sh

RUN WINEDEBUG=-all winecfg

# Running as root is insecure, BUT this image is also a pain in the ass
# to work with, so you get what you get and you don't get upset.
ENV RUN_AS_ROOT=yes 
# Run the application
CMD [ "/bin/sh", "/44cry/run.sh"]