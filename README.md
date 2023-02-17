# Dotfiles & Configs

![Qtile](.screenshots/qtile.png)

***Language***
- [🇪🇸 Español](./README.es.md)
- 🇺🇸 English

# Table of contents

- [Introduction](#introduction)
- [Preparation](#preparation)
- [Login & WM](#login--wm)
- [Basic Utilities](#basic-utilities)
    - [Audio](#audio)
    - [Brightness](#brightness)
    - [Fonts](#fonts)
    - [Wallpapers](#wallpapers)
    - [External Devices](#external-devices)
    - [Network-applet](#network-applet) 
    - [Notifications](#notifications)
- [Xprofile](#xprofile)
- [Utilities & Tools](#utilities--tools)
    - [Aur](#aur)
    - [Rofi](#rofi)
    - [Picom](#picom)
    - [Alacritty](#alacritty)
    - [Text Editor](#text-editor)
        - [VSCode](#vscode)
        - [Neovim](#neovim)
    - [File Manager](#file-manager)
        - [Ranger](#ranger)
        - [Thunar](#thunar)
    - [GTK](#gtk)
    - [LightDM Theme](#lightdm-theme)
    - [Grub theme](#grub-theme)
- [Window Managers](#window-managers)
    - [Qtile](#qtile)
        - [Overview](#qtile-overview)
        - [Keybindings](#qtile-keybindings)
        - [Gallery](#qtile-gallery)
    - [Spectrwm](#spectrwm)
        - [Overview](#spectrwm-overview)
        - [Keybindings](#spectrwm-keybindings)
        - [Gallery](#spectrwm-gallery)
    - [I3-gaps](#i3-gaps)
        - [Overview](#i3-overview)
        - [Keybindings](#i3-keybindings)
        - [Gallery](#i3-gallery)
- [App Gallery](#app-gallery)
# Introduction
This is the manual with the hole process for install and build my desktop enviroment as I did. To build the enviroment you must be **comfortable with CLI of Linux** and have **some experience in the Linux world**. You also must know that in this guide I only install **Tiling Window Managers** because are my favourites for work with Linux.

# Preparation
We are going to start on the point of a [Base Arch Linux installation](https://wiki.archlinux.org/title/Installation_guide).In this moment if you have already install and enable or build this dependencies: [NetworkManager](https://wiki.archlinux.org/title/NetworkManager), [GRUB](https://wiki.archlinux.org/title/GRUB), [sudo](https://wiki.archlinux.org/title/Sudo), [xorg](https://wiki.archlinux.org/title/xorg); you can already pass this step. You must know that this **packages are essentials for the operating system**.

So first we must install [Network Manager](https://wiki.archlinux.org/title/NetworkManager) and enable it.
```bash
pacman -S networkmanager
systemctl enable --now NetworkManager 
```

Secondly mount the bootloader that in my case is [grub](https://wiki.archlinux.org/title/GRUB). In my case I mount the efi partition on **/boot/efi** but if you have installed on **/boot** it doesn't matter.
```bash
# Only Arch boot
pacman -S grub efibootmgr 
grub-install --target=x86_64-efi --efi-directory=/boot # if your efi partition is in /boot/efi on --efi-directory put /boot/efi instead
grub-mkconfig -o /boot/grub/grub.cfg

# Dual boot with windows 
pacman -S nfts-3g os-prober
grub-install --target=x86_64-efi --efi-directory=/boot # if your efi partition is in /boot/efi on --efi-directory put /boot/efi instead
# You must go to /etc/default/grub and uncomment or turn to false GRUB_DISABLE_OS_PROBER
os-prober
grub-mkconfig -o /boot/grub/grub.cfg
```

Now create your user and add it to the wheel group.
```bash
useradd -m username
passwd username
usermod -aG wheel username
```
Then we install [sudo](https://wiki.archlinux.org/title/Sudo)
```bash
pacman -S sudo
# Uncomment this line of /etc/sudoers -> # %wheel ALL=(ALL) ALL
```

Afterwards exit and umount of the ISO image.
```bash
exit
umount -R /mnt 
reboot
```

Now login and check if the system is ok and connect to wifi with [nmcli](https://man.archlinux.org/man/nmcli.1.en)

Finally install [Xorg](https://wiki.archlinux.org/title/xorg) that is a package that provide us the posibility of use window managers
```bash
sudo pacman -S xorg-server 
```

# Login & WM
The login manager that I use is **[lightdm](https://wiki.archlinux.org/title/LightDM)** because is very **customizable**, later you will have a deeper explanation of lightdm and how customizate it. You also need to install a window manager for start to configurate your system, in my case the first WM that I installed was **qtile** but you can also install **I3 or spectrwm**. You will also need a [text editor](#text-editor), a browser such as [Firefox](https://wiki.archlinux.org/title/Firefox) and a terminal, if you want the same terminal as me install [alacritty](https://wiki.archlinux.org/title/Alacritty).

```bash
sudo pacman -S lightdm lightdm-gtk-greeter qtile firefox # Here is your desition of install VSCode or nvim
```

# Basic Utilities

This is software that you need unless you want to have a unusefull system

## Audio
For the audio utilities you will need 4 packages: [pulseaudio](https://wiki.archlinux.org/title/PulseAudio) that is the core of the audio controller, [pavucontrol](https://archlinux.org/packages/extra/x86_64/pavucontrol/) that is GUI for control audio, [pamixer](https://archlinux.org/packages/community/x86_64/pamixer/) that is a CLI for control audio, [volumeicon](https://archlinux.org/packages/community/x86_64/volumeicon/) that is for control audio from systray.

```bash
sudo pacman -S pulseaudio pavucontrol volumeicon pamixer
```
## Brightness
Brightness can be control with [brightnessctl](https://archlinux.org/packages/community/x86_64/brightnessctl/) so lets install it.

```bash
sudo pacman -S brightnessctl
```

## Fonts
All the fonts that I use are from [nerd fonts](https://www.nerdfonts.com/), except [cascadia code](https://github.com/microsoft/cascadia-code). All my fonts are on .fonts file.
Small guide to install fonts
```bash
unzip font.zip
sudo mkdir /usr/share/fonts/TTF 
sudo mv font/*.ttf /usr/share/fonts/TTF
```

## Wallpapers
For wallpapers there are two main tools [feh](https://wiki.archlinux.org/title/Feh) and [nitrogen](https://wiki.archlinux.org/title/Nitrogen).

```bash
sudo pacman -S feh nitrogen
```
But in my case I don't like to have the same wallpapers always so I make an utility that it is on .system-scripts/wallpaper.sh that put a random .jpg image of wallpaper you only have to edit some lines.
```bash
#!/usr/bin/bash
num_wallpaper=$(($RANDOM%{Num of wallpapers that you have}}))
feh --bg-scale /path/to/wallpapers/folder/$num_wallpaper.jpg
```

## External devices
For use USBs you only need to install [udiskie](https://archlinux.org/packages/community/any/udiskie/) and [nfts-3g](https://wiki.archlinux.org/title/NTFS-3G)

```bash
sudo pacman -S udiskie nfts-3g
```

## Network-applet
[nm-applet](https://wiki.archlinux.org/title/NetworkManager#nm-applet) is package is for control internet from systray.
```bash
sudo pacman -S network-manager-applet
```

## Notifications
Notification can be used with the packages [libnotify](https://archlinux.org/packages/extra/x86_64/libnotify/) and [notification-daemon](https://archlinux.org/packages/community/x86_64/notification-daemon/).

```bash
sudo pacman -S libnotify notification-daemon
```
```bash
# Create this file with nano
sudo nano /usr/share/dbus-1/services/org.freedesktop.Notifications.service
# Write this
[D-BUS Service]
Name=org.freedesktop.Notifications
Exec=/usr/lib/notification-daemon-1.0/notification-daemon
```

# Xprofile

Xprofile is a file that allows us to init programs when you get logged on the window manager, this is very important to configurate things such as wallpaper or audio. Xprofile by default come with xorg-server package but if you have any problem you must install [xinit](https://wiki.archlinux.org/title/Xinit).

So create **/home/user/.xprofile**
```bash
touch ~/xprofile
```
And add some lines
```bash
# Audio
pulseaudio --kill &
pulseaudio --start &
# Network
nm-applet &
# Automount Devices
udiskie -t &
# systray volume
volumeicon &
# Wallpaper
random-wallpaper # If you didn't make this script write feh --bg-scale /path/to/your/wallpaper
```

When you get logged in you will see the changes

# Utilities & Tools
This are utilities that are not completly necesary but that I recommend.
## AUR
[Aur](https://aur.archlinux.org/) is a software that complement us with more packages than [Pacman](https://wiki.archlinux.org/title/pacman), when you install Aur you have access to a lot resources such as [google-chrome](https://aur.archlinux.org/packages/google-chrome).

Aur could be managed with lots of [AUR helpers](https://wiki.archlinux.org/title/AUR_helpers) but in my case I use [paru](https://aur.archlinux.org/packages/paru).

So first you need to install [git](https://wiki.archlinux.org/title/git)
```bash
sudo pacman -S git
```
Then create a directory to clone repository and build it
```bash
mkdir -p Downloads/repos # You can put any name
```
Afterwards download repository and build it 
```bash
git clone https://aur.archlinux.org/paru-bin.git # Do this command in the previous directory
cd paru-bin/
makepkg -si
```
Now test it 
```bash
paru --version
```
If there is output paru is correctly instaled.
## Rofi
[Rofi](https://wiki.archlinux.org/title/rofi) is a menu that provide us the ability to open programs easily. Also is very customizable.
```bash
sudo pacman -S rofi
```
I recommend to add rofi to your keybindings.
My configs are in *.config/rofi/rofi.rasi* and the One Dark theme for rofi is from https://github.com/davatorium/rofi-themes/blob/master/User%20Themes/onedark.rasi

## Picom
[Picom](https://wiki.archlinux.org/title/picom) is a package that provide us the posibility of give transparency and shadow to our windows, it's very important to configurate alacritty.
```bash
sudo pacman -S picom
```
You also should to agregate to *.xprofile*.
```bash
picom &
```
## Alacritty 
[Alacritty](https://wiki.archlinux.org/title/Alacritty) is a terminal emulator written in Rust that is the fastest of the world.
```bash
sudo pacman -S alacritty
```
My config of alacritty is on *.config/alacritty/alacritty.yml*

## Text Editor
This is not necesary at all but if you are developer text editor are basic.

### VSCode
[VSCode](https://wiki.archlinux.org/title/Visual_Studio_Code) is the most popular text editor. In my case I use allways this code editor because I think that is the best. My settings are on *.config/Code-OSS/settings.json*.
```bash
sudo pacman -S code
```
### Neovim
[Neovim](https://wiki.archlinux.org/title/Neovim) is the other text editor that I use, it is more complex than VSCode but if you have time to learn it, is a good option. My config ais not mine, is from [NvChad](https://nvchad.com/).
```bash
sudo pacman -S neovim
```

## File manager

### Ranger
[Ranger](https://wiki.archlinux.org/title/Ranger) is a terminal file manager so is more complex that the next option that I will give but is fast and lighter. My configs are on *.config/ranger*.
```bash
sudo pacman -S ranger
```
### Thunar
[Thunar](https://wiki.archlinux.org/title/Thunar) is graphicall file manager so is easier than ranger .
```bash
sudo pacman -S thunar
```
## GTK
Gtk theming is basic if you want to have a correctlty custom system. With Gtk we can configurate icons, themes, etc...

My theme is [Material Dark Cherry](https://www.gnome-look.org/p/1316887/)
```bash
unzip Theme.zip
sudo mv Theme /usr/share/themes
```
And my icons are [Material Dark Cherry Suru](https://www.pling.com/p/1333360/)
```bash
unzip Icons.zip
sudo mv Icons /usr/share/icons
```

In this moment theme and icons are installed but are not activated so we have to install [lxappearence](https://archlinux.org/packages/community/x86_64/lxappearance/) that is activate themes and icons graphically.
```bash
sudo pacman -S lxapppearence
``` 
## LightDM theme
LightDM could be configure for have a better user experience and a better session manager. I have the [aether theme](https://aur.archlinux.org/packages/lightdm-webkit-theme-aether)
```bash
sudo pacman -S lightdm-webkit2-greeter
paru -S lightdm-webkit-theme-aether
```

Then in this line greeter-session write lightdm-webkit2-greeter on */etc/lightdm/lightdm.conf*
And in the line webkit_theme write lightdm-webkit-theme-aether on */etc/lightdm/lightdm-webkit2-greeter.conf*

## Grub Theme
Grub could be customize with the package [grub customizer](https://archlinux.org/packages/community/x86_64/grub-customizer/).

```bash
sudo pacman -S grub-customizer
```

My grub theme is from https://github.com/vinceliuice/grub2-themes.

# Window Managers

## Qtile
### Qtile Overview 
Qtile is a perfect option to start in the world of tiling window managers, it is written on python and it has a very easy configuration file, all my config is on *.config/qtile*. In my case I have a custom widget so if you want to copy  my configuration, you also need to copy the widget.  
```bash
sudo pacman -S qtile
# If you want to copy my config
sudo pacman -S pacman-contrib
pip install psutil
```
### Qtile Keybindings
|Key          |Program
--------------|-----------
|MOD+Return   |Alacritty
|MOD+f        |Firefox
|MOD+m        |Rofi
|MOD+Control+w|Random wallpaper (custom command)
|MOD+s        |Scrot

### Qtile Gallery
![Qtile](.screenshots/qtile.png)

## Spectrwm

### Spectrwm Overview
Spectrwm is also a good option to start with tiling window managers, it is written on c, for configure it you only need to edit .config/spectwm/spectrwm.conf and for the top bar you have to make a bash script that gives some output. My configs are on *.config/spectrwm*

```bash
sudo pacman -S spectrwm
```

### Spectrwm Keybindings
|Key          |Program
--------------|-----------
|MOD+Return   |Alacritty
|MOD+f        |Firefox
|MOD+m        |Rofi
|MOD+Shift+w  |Random wallpaper (custom command)
|MOD+s        |Scrot

### Spectrwm Gallery
![Spectrwm](.screenshots/spectrwm.png)

## I3

### I3 Overview
I3 in my opinion is more dificult to configure, so I don't reccomend it to start with tiling window managers, it is written on c, for configure it you only need to edit .config/i3/config and I use [polybar](https://github.com/polybar/polybar) for the top bar. My configs are on *.config/i3* and *.config/polybar*.
```bash
sudo pacman -S i3-wm  polybar
```

### i3 Keybindings
|Key          |Program
--------------|-----------
|MOD+Return   |Alacritty
|MOD+f        |Firefox
|MOD+m        |Rofi


### i3 Gallery
![i3](.screenshots/i3.png)

# App Gallery

## Alacritty
![Alacritty](.screenshots/alacritty.png)
## Nvim & Alacritty
![Alacritty & Nvim](.screenshots/nvim-alacritty.png)
## VSCode
![VSCode](.screenshots/vscode.png)
## Rofi
![rofi](.screenshots/rofi.png)
## Thunar
![thunar](.screenshots/thunar.png)