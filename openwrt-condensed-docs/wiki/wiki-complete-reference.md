---
module: "wiki"
total_token_count: 5023
section_count: 2
is_monolithic: true
generated: "2026-03-08T10:55:03.410578+00:00"
---

# wiki Complete Reference

> **Contains:** 2 documents concatenated
> **Tokens:** ~5023 (cl100k_base)

---

# 21.02: Major cosmetic changes

This page intends to give an overview over major cosmetic changes since 19.07, focusing on those that will require adjustments/adaption downstream.

The idea is to give a broad overview like a Table of Contents, without too much details on the specific issues.

Note that this page is not even close to being complete.

## Device/target renames

Recently, most obvious through the transition from ar71xx to ath79, we tried to make device/image names more systematic by applying a vendor_model-variant scheme.

This has already been used in 19.07 in some cases (ath79, ipq40xx, ipq806x, mpc85xx, new ramips devices, …).

After 19.07 had been released, the attempt was made to apply this more widely, and use the momentum to also achieve a more unified and systematic naming scheme for the different locations where the “device name” is used in its variations:

- device name in image/Makefile (will be used for image name)
- DEVICE_TITLE in image/Makefile
- DTS file name (soc_vendor_model or soc-vendor-model)
- DTS model name
- DTS compatible
- board_name (which should be derived from compatible instead of setting board names manually)
- SUPPORTED_DEVICES

The following subchapters will provide details on which changes have been applied to which targets so far.

### arc770

Manual board names (/tmp/sysinfo/board_name) have been replaced by compatible (vendor,model-variant)

So, all local scripts using the board name need to be updated.

<https://github.com/openwrt/openwrt/commit/0a5d74fa68bce598302236ca0f3eb2db2bc1592d>

### archs38

Manual board names (/tmp/sysinfo/board_name) have been replaced by compatible (vendor,model-variant)

So, all local scripts using the board name need to be updated.

<https://github.com/openwrt/openwrt/commit/3c190ef112979793cd0e2148c53c6208a642a463>

### ath79/ar71xx

In 21.02, ar71xx will finally be dropped. As already relevant in 19.07, ath79 introduces vendor_model-variant scheme for image names. It also drops the board_names used in ar71xx, so the compatible (from DTS) will be used as board name instead (being equivalent to vendor,model-variant, and unique for a specific device). While creating the new and shiny target, we again took the opportunity to use more systematic names on devices, using less abbreviations and staying closer to the device name. This will it result in several changed names compared to ar71xx additional to just adding the vendor to the name.

For downstream, (at least) the following will require adjustment:

- CONFIG_TARGET_DEVICE\_\* variables
- image names (e.g. if copied)
- board names (/tmp/sysinfo/board_name) if used for anything on device

Note that ath79 might also include several changes after 19.07.

### bcm27xx/brcm2708

The whole target has been renamed from “brcm2708” to “bcm27xx”. This will affect all cases where target variables are used, i.e. CONFIG_TARGET\_\* or TARGET\_\* dependencies. Despite, image names will change. The same rename applies to packages brcm2708-userland and brcm2708-gpu-fw.

This can be easily addressed downstream by just grepping for “brcm2708”.

### bcm47xx/brcm47xx

The whole target has been renamed from “brcm47xx” to “bcm47xx”. This will affect all cases where target variables are used, i.e. CONFIG_TARGET\_\* or TARGET\_\* dependencies. Despite, image names will change.

This can be easily addressed downstream by just grepping for “brcm47xx”.

### bcm63xx/brcm63xx

The whole target has been renamed from “brcm63xx” to “bcm63xx”. This will affect all cases where target variables are used, i.e. CONFIG_TARGET\_\* or TARGET\_\* dependencies. Despite, image names will change.

This can be easily addressed downstream by just grepping for “brcm63xx”.

Despite, this target has also been subject to an ath79-like unification of device names:

- device/image names and compatible have been adjusted to match device names (using vendor_model-variant scheme)
- DTS files have been renamed with soc-vendor-model scheme
- manual board names (/tmp/sysinfo/board_name) have been replaced by compatible (vendor,model-variant)

Patches:

- <https://github.com/openwrt/openwrt/commit/e4ba8c82947efd39b014496de32ee73e1bec9c71>
- <https://github.com/openwrt/openwrt/commit/0a3350d908ec466206f58b9e6b300c49e4fb3b13>
- <https://github.com/openwrt/openwrt/commit/d0e8e6db6b22b893da2f3a2cbe84adb753cb3303>

### imx6

Manual board names (/tmp/sysinfo/board_name) have been replaced by compatible (vendor,model-variant)

So, all local scripts using the board name need to be updated.

<https://github.com/openwrt/openwrt/commit/8126e572dd4f531c5f105b7197bc119b2b1ebb07>

### layerscape

Device nodes and thus image names have been changed to apply to vendor_model scheme.

This will affect CONFIG_TARGET_DEVICE\_\* variables and image names.

<https://github.com/openwrt/openwrt/commit/0f3c3a5fb2738b25c62eb0ff8ef7d0654c0b9300>

### mediatek

Device nodes and thus image names have been changed to apply to vendor_model scheme.

This will affect CONFIG_TARGET_DEVICE\_\* variables and image names.

<https://github.com/openwrt/openwrt/commit/49d66e0468c14d8a05bd6c33056708d2051437cb>

### mpc85xx

Device nodes and thus image names have been changed to apply to vendor_model scheme.

This will affect CONFIG_TARGET_DEVICE\_\* variables and image names.

<https://github.com/openwrt/openwrt/commit/118749271b311413307f0b6be91786d7ac368f8b>

### octeon

Device nodes and thus image names have been changed to apply to vendor_model scheme.

This will affect CONFIG_TARGET_DEVICE\_\* variables and image names.

<https://github.com/openwrt/openwrt/commit/1e3bfbafd37ccb32d0ed6618f4886e1dec6643d2>

### ramips

In ramips, the situation in 19.07 can be described as a mix of ar71xx and ath79. After 19.07, the target was updated and the same naming logic as for ath79 was applied. Thus, for this target effectively the same comments as for ath79/ar71xx apply.

### samsung

Device nodes and thus image names have been changed to apply to vendor_model scheme.

This will affect CONFIG_TARGET_DEVICE\_\* variables and image names.

<https://github.com/openwrt/openwrt/commit/6e70e4a071b233da83486414e65d15756ede63d2>

### sunxi

Device nodes and thus image names have been changed to apply to vendor_model scheme.

This will affect CONFIG_TARGET_DEVICE\_\* variables and image names.

<https://github.com/openwrt/openwrt/commit/a4cdb537b17ede9785ddbaef5ed9d69f3ab89052>

## DEVICE_TITLE split and tidy-up

To make device names more systematic, the DEVICE_TITLE make variable (primarily used for display in make menuconfig) was split into DEVICE_VENDOR, DEVICE_MODEL and DEVICE_VARIANT *for all targets.* DEVICE_TITLE is still available as (simplified)

    DEVICE_TITLE := $(DEVICE_VENDOR) $(DEVICE_MODEL) $(DEVICE_VARIANT)

During this update process, we took the opportunity to make names more systematic. Thus, several DEVICE_TITLEs will have changed effectively.

Despite, a new syntax to specify alternate device names has been introduced (ALT0 to ALT3):

    DEVICE_ALT0_VENDOR
    DEVICE_ALT0_MODEL
    DEVICE_ALT0_VARIANT

As for DEVICE_TITLE, those will not affect image names.

## Label MAC address

Many devices supported by OpenWrt bear one or many MAC addresses on them, which allow to identify those devices in large network. This fact has been exploited by downstream communities, which implemented those addresses locally. OpenWrt has now added a mechanism to store and retrieve those addresses:

Developer reference: <https://openwrt.org/docs/guide-developer/mac.address#label_mac_address>

Use:

    . /lib/functions/system.sh
    label_mac_addr=$(get_mac_label)

The label MAC address has to be provided in OpenWrt on a per-device basis. While a lot of devices has already been covered, there also is still a lot of devices to take care of.

## Support of Ed25519 SSH keys

With the commit [d0f295837a03f7f52000ae6d395827bdde7996a4](commit>d0f295837a03f7f52000ae6d395827bdde7996a4) it is now possible to use Ed25519 SSH keys on regular (aka not tiny) devices. These keys are much shorter than RSA keys while being equally secure. For embedded devices this should speed up the login process as the keys are much faster processed.

---

# Adding new device support

This article assumes your device is based on a platform already supported by OpenWrt. If you need to add a new platform, see -\>[add.new.platform](/docs/guide-developer/add.new.platform)

If you already solved the puzzle and are looking for device support submission guidelines, check out [Device support policies / best practices](/docs/guide-developer/device-support-policies)

## General Approach

1.  Make a detailed list of chips on the device and find info about support for them. Focus on processor, flash, ethernet and wireless. Some helpful tips are available on [hw.hacking.first.steps](/docs/guide-developer/hw.hacking.first.steps)
2.  Make sure you have working serial console and access to the bootloader.
3.  Prepare and install firmware, watch the bootlog for problems and errors.
4.  Verify flash partitioning, LEDs and buttons.

## GPIOs

Most of devices use [GPIOs](/docs/techref/hardware/port.gpio) for controlling LEDs and buttons. There aren’t any generic GPIOs numbers, so OpenWrt has to use device specific mappings. It means we need to find out GPIOs for every controllable LED and button on every supported device.

### GPIO LEDs

If LED is controlled by GPIO, direction has to be set to `out` and we need to know the polarity:

- If LED turns on for value 1, it’s active high
- If LED turns on for value 0, it’s active low

A single GPIO can be tested in the following way:

    cd /sys/class/gpio
    GPIO=3
    echo $GPIO > export
    echo "out" > gpio$GPIO/direction
    echo 0 > gpio$GPIO/value
    sleep 1s
    echo 1 > gpio$GPIO/value
    sleep 1s
    echo $GPIO > unexport

Of course every GPIO (starting with 0) has to be tested, not only a GPIO 3 as in the example above.

So basically you need to create a table like:

| Color | Name  | GPIO | Polarity    |
|-------|-------|------|-------------|
| Green | Power | 0    | Active high |
| Blue  | WLAN  | 7    | Active high |
| Blue  | USB   | 12   | Active low  |

To speed up testing all GPIOs one by one you can use following bash script. Please note you have to follow LEDs state and console output. If the USB LED turns on and the last console message is `[GPIO12] Trying value 0` it means USB LED uses GPIO 12 and is active low.

``` bash
#!/bin/sh
GPIOCHIP=0
BASE=$(cat /sys/class/gpio/gpiochip${GPIOCHIP}/base)
NGPIO=$(cat /sys/class/gpio/gpiochip${GPIOCHIP}/ngpio)
max=$(($BASE+$NGPIO))
gpio=$BASE
while [ $gpio -lt $max ] ; do
    echo $gpio > /sys/class/gpio/export
    [ -d /sys/class/gpio/gpio${gpio} ] && {
        echo out > /sys/class/gpio/gpio$gpio/direction

        echo "[GPIO$gpio] Trying value 0"
        echo 0 > /sys/class/gpio/gpio$gpio/value
        sleep 3s

        echo "[GPIO$gpio] Trying value 1"
        echo 1 > /sys/class/gpio/gpio$gpio/value
        sleep 3s

        echo $gpio > /sys/class/gpio/unexport
    }
    gpio=$((gpio+1))
done
```

- Save the above content as a file `gpio-test.sh` & then transfer inside router‘s ’‘/tmp’’ directory, or copy above content & paste inside `vi` editor in router & save as `gpio-test.sh` file.
- to make it executable, run: `chmod +x /tmp/gpio-test.sh`

### GPIO buttons

In case of GPIO controlled buttons value changes during button press. So the best idea to find out which GPIO is connected to some hardware button is to:

1.  Dump values of all GPIOs
2.  Push button and keep it pushed
3.  Dump values of all GPIOs
4.  Find out which GPIO changed its value

For dumping GPIO values following script can be used:

``` bash
#!/bin/sh
GPIOCHIP=0
BASE=$(cat /sys/class/gpio/gpiochip${GPIOCHIP}/base)
NGPIO=$(cat /sys/class/gpio/gpiochip${GPIOCHIP}/ngpio)
max=$(($BASE+$NGPIO))
gpio=$BASE
while [ $gpio -lt $max ] ; do
    echo $gpio > /sys/class/gpio/export
    [ -d /sys/class/gpio/gpio${gpio} ] && {
        echo in > /sys/class/gpio/gpio${gpio}/direction
        echo "[GPIO${gpio}] value $(cat /sys/class/gpio/gpio${gpio}/value)"
        echo ${gpio} > /sys/class/gpio/unexport
    }
    gpio=$((gpio+1))
done
```

- Save the above content as a file `gpio-dump.sh` & then transfer inside router‘s ’‘/tmp’’ directory, or copy above content & paste inside `vi` editor in router & save as `gpio-dump.sh` file
- to make it executable, run: `chmod +x /tmp/gpio-dump.sh`

If GPIO value changes from 1 to 0 while pressing the button, it’s active low. Otherwise it’s active high.

Example table:

| Name  | GPIO | Polarity   |
|-------|------|------------|
| WPS   | 4    | Active low |
| Reset | 6    | Active low |

### KSEG1ADDR() and accessing NOR flash

For getting MAC addresses, EEPROM and other calibration data for your board, you may need to read from flash in the kernel. In the case of many Atheros chips using NOR flash, done using the KSEG1ADDR() macro which translates the hardware address of the flash to the virtual address for the process context which is executing your init function.

If you are reviewing the code for initializing a board similar to your own and you see this idium: KSEG1ADDR(0x1fff0000), the number at first appears to be magic but it is logical if you understand two things. Firstly, Atheros SoCs using NOR flash wire it to the physical address 0x1f000000 (there are no guarantees about where the flash will be wired for your board but this is a common location). You cannot rely on the address given in the bootloader, you might see 0xbf000000 but this is probably also a virtual address. If your board wires flash to these memory locations, you may obviously access flash using KSEG1ADDR(0x1f000000 + OFFSET_FROM_BEGIN) but in the event that you have to access data which you know will exist at the very end of the flash, you can use a trick to make your code compatible with multiple sizes of flash memory.

Often flash will be mapped to a full 16MB of address space no matter whether it is 4MB, 8MB or 16MB so in this case KSEG1ADDR(0x20000000 - OFFSET_FROM_END) will work for accessing things which you know to be a certain distance from the end of the flash memory. When you see KSEG1ADDR(0x1fff0000), on devices with 4MB or 8MB of flash, it’s fair to guess that it’s using this trick to reference the flash which resides 64k below the end of the flash (where Atheros Radio Test data is stored).

## Examples

### Brcm63xx Platform

If you have the OEM sourcecode for your [bcm63xx](/docs/techref/hardware/soc/soc.broadcom.bcm63xx) specific device, it may be useful some things for later adding the OpenWrt support:

- Look for your Board Id at `shared/opensource/boardparms/boardparms.c`
- Adapt the `imagetag.c` to create a different tag (see `shared/opensource/inlude/bcm963xx/bcmTag.h` in the GPL tar for the layout)
- Finally xor the whole image with ‘12345678’ (the ascii string, not hex).

(from <https://forum.openwrt.org/viewtopic.php?pid=123105#p123105>)

For creating the OpenWrt firmware your [bcm63xx](/docs/techref/hardware/soc/soc.broadcom.bcm63xx) device, you can follow the following steps:

1.  Obtain the [source and follow the compile procedure](/docs/guide-developer/toolchain/start) with the make menuconfig as last step.
2.  During **menuconfig** select the correct target system.
3.  Next generate the board_bcm963xx.c file for the selected platform with all board parameters execute the following command:\
        make kernel_menuconfig
4.  Add the board-id to the ./target/linux/brcm63xx/image/Makefile.\
    **Example**\
    \<code\> \# Davolink DV2020

<!-- -->

      $(call Image/Build/CFE,$(1),DV2020,6348)</code>
    - add the board-id with the parameters to ./build_dir/linux-brcm63xx/linux-2.6.37.4/arch/mips/bcm63xx/boards/board_bcm963xx.c\\ **Example**\\ <code>static struct board_info __initdata board_DV2020 = {
          .name                           = "DV2020",
          .expected_cpu_id                = 0x6348,

          .has_uart0                      = 1,
          .has_pci                        = 1,
          .has_ohci0                      = 1,

          .has_enet0                      = 1,
          .has_enet1                      = 1,
          .enet0 = {
                  .has_phy                = 1,
                  .use_internal_phy       = 1,
          },  
          .enet1 = {  
                  .force_speed_100        = 1,    
                  .force_duplex_full      = 1,    
          },  

};

static const struct board_info \_\_initdat : : :

      &board_DV2020,

\</code\>

1.  Finish the [compile instructions](/docs/guide-developer/toolchain/start) according the procedure from the make step.

### Ramips Platform

As long as you are adding support for an ramips board with an existing chipset, this is rather straightforward. You need to create a new *board* definition, which will generate an image file specifically for your device and runs device-specific code. Then you write various board-specific hacks to initialize devices and set the correct default configuration.

Your board identifier will be passed in the following sequence:

     (Image Generator puts it in the kernel command line)
              ↓
     (Kernel command line is executed with BOARD=MY_BOARD)
              ↓
     (Kernel code for ramips finds your board and loads machine-specific code)
              ↓
     (/lib/ramips.sh:ramips_board_name() reads the board name from /proc/cpuinfo)
              ↓
     (Several userspace scripts use ramips_board_name() for board-specific setup)

At a minimum, you need to make the following changes to make a basic build, all under target/linux/ramips/:

- Add a new machine image in `image/Makefile`
- Create a new machine file in `arch/mips/ralink/$CHIP/mach-myboard.c` where you register:
  - GPIO pins for LEDs and buttons
  - Port layout for the device (vlan configuration)
  - Flash memory configuration
  - Wifi
  - USB
  - Watchdog timer
  - And anything else specific to your board
- Reference the new machine file in `arch/mips/ralink/$CHIP/{Kconfig,Makefile}`
- Reference the new machine name in `files/arch/mips/include/asm/mach-ralink/machine.h`
- Add your board to `base-files/lib/ramips.sh` for userspace scripts to read the board name

Then you‘ll want to modify some of these files depending on your board’s features: \* ’‘base-files/etc/diag.sh’’ to set a LED which OpenWRT should blink on bootup

- `base-files/lib/upgrade/platform.sh` to allow sysupgrade to work on your board
- `base-files/etc/uci-defaults/network` to configure default network interface settings, particularly MAC addresses
- `base-files/etc/uci-defaults/leds` if you have configurable LEDs which should default to a behavior, like a WLAN activity LED
- `base-files/etc/hotplug.d/firmware/10-rt2x00-eeprom` to extract the firmware image for the wireless module
- `base-files/lib/preinit/06_set_iface_mac` to set the MAC addresses of any other interfaces

Example commits:

- [Skyline SL-R7205 (rt305x)](https://dev.openwrt.org/changeset/30645)
- [Belkin F5D8235-4 v1 (rt288x)](https://dev.openwrt.org/changeset/29617)
- [Planex DB-WRT01 (MT7620A)](https://dev.openwrt.org/changeset/46918)

## Tips

After add a new board, you may should clean the `tmp` folder first. \<code\> cd trunk rm -rf tmp make menuconfig \</code\>

If you have added a device profile, and it isn’t showing up in “make menuconfig” try touching the main target makefile

    touch target/linux/*/Makefile

---

