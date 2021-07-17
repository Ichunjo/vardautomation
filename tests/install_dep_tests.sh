#!/bin/sh

# Upgrade pip
python -m pip install --upgrade pip

# Install meson
sudo python -m pip install meson

# Install Ninja
sudo apt-get update
sudo apt-get install ninja-build

# Install Ffmpeg
git clone https://github.com/FFmpeg/FFmpeg --branch release/4.4 --depth 1
pushd FFmpeg
./configure --enable-gpl --enable-version3 --disable-static --enable-shared --disable-all --disable-autodetect --enable-avcodec --enable-avformat --enable-swresample --enable-swscale --disable-asm --disable-debug
make -j2
sudo make install -j2
popd
rm -rf FFmpeg

# Install l-smash
git clone https://github.com/l-smash/l-smash --depth 1
pushd l-smash
mv configure configure.old
sed 's/-Wl,--version-script,liblsmash.ver//g' configure.old >configure
chmod +x configure
./configure --disable-static
make lib -j2
sudo make install-lib -j2
popd
rm -rf l-smash

# Install zimg
git clone https://github.com/sekrit-twc/zimg --branch v3.0 --depth 1
pushd zimg
./autogen.sh
./configure --disable-static --disable-simd
make -j2
sudo make install -j2
popd
rm -rf zimg

# Install vapoursynth
git clone https://github.com/vapoursynth/vapoursynth --depth 1 vapoursynth-build
pushd vapoursynth-build
./autogen.sh
./configure --disable-static --disable-x86-asm --disable-vsscript --disable-vspipe --disable-python-module --disable-plugins
make -j2
sudo make install -j2
popd
rm -rf vapoursynth-build

# Install L-SMASH-Works
git clone https://github.com/AkarinVS/L-SMASH-Works.git --depth 1
pushd L-SMASH-Works/VapourSynth
sudo meson build
sudo ninja -C build
sudo ninja -C build install
popd