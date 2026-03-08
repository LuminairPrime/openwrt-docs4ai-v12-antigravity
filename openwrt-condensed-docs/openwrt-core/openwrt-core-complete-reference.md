---
module: "openwrt-core"
total_token_count: 19845
section_count: 7
is_monolithic: true
generated: "2026-03-08T11:15:44.906113+00:00"
---

# openwrt-core Complete Reference

> **Contains:** 7 documents concatenated
> **Tokens:** ~19845 (cl100k_base)

---

# OpenWrt Buildroot: boot packages

> **Source:** https://github.com/openwrt/openwrt/tree/master/package/boot
---

## apex

| Field | Value |
|---|---|
| Version | 1.6.10-openwrt |
| License | GPL-2.0 |
| Source URL | https://github.com/linusw/apex.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/apex
---

## arm-trusted-firmware-bcm63xx

| Field | Value |
|---|---|
| Version | 2.2 |
| Maintainer | Rafał Miłecki <rafal@milecki.pl> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default PLAT:=bcm DEFAULT:=y  |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-bcm63xx
---

## arm-trusted-firmware-mediatek

| Field | Value |
|---|---|
| Maintainer | Daniel Golle <daniel@makrotopia.org> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default BUILD_TARGET:=med |
| Source URL | https://github.com/mtk-openwrt/arm-trusted-firmware.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-mediatek
---

## arm-trusted-firmware-microchipsw

| Field | Value |
|---|---|
| Maintainer | Robert Marko <robert.marko@sartura.hr> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default BUILD_TARGET:=m |
| Source URL | https://github.com/microchip-ung/arm-trusted-firmware.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-microchipsw
---

## arm-trusted-firmware-mvebu

| Field | Value |
|---|---|
| Version | 2.9 |
| Maintainer | Vladimir Vid <vladimir.vid@sartura.hr> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default BUILD_TARGET:=m |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-mvebu
---

## arm-trusted-firmware-rockchip

| Field | Value |
|---|---|
| Version | 2.14.0 |
| Maintainer | Sarah Maedel <openwrt@tbspace.de> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default NAME:=Rockchip $(1)  |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-rockchip
---

## arm-trusted-firmware-stm32

| Field | Value |
|---|---|
| Version | 2.14 |
| Maintainer | Thomas Richard <thomas.richard@bootlin.com> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default BUILD_TARG |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-stm32
---

## arm-trusted-firmware-sunxi

| Field | Value |
|---|---|
| Version | 2.14 |
| License | BSD-3-Clause |
| Maintainer | Hauke Mehrtens <hauke@hauke-m.de> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default BUILD_TARGET:=sunxi  |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-sunxi
---

## arm-trusted-firmware-tools

| Field | Value |
|---|---|
| Version | 2.12 |
| Maintainer | Daniel Golle <daniel@makrotopia.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/arm-trusted-firmware-tools
---

## at91bootstrap

| Field | Value |
|---|---|
| Version | v4.0.10 |
| Source URL | https://github.com/linux4sam/at91bootstrap.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/at91bootstrap
---

## fconfig

| Field | Value |
|---|---|
| Version | 20080329 |
| Source URL | @OPENWRT |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/fconfig
---

## grub2

| Field | Value |
|---|---|
| Version | 2.12 |
| License | GPL-3.0-or-later |
| Source URL | @GNU/grub |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/grub2
---

## imx-bootlets

| Field | Value |
|---|---|
| Version | 10.12.01 |
| Source URL | http://trabant.uid0.hu/openwrt/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/imx-bootlets
---

## kexec-tools

| Field | Value |
|---|---|
| Version | 2.0.32 |
| License | GPL-2.0-only |
| Source URL | @KERNEL/linux/utils/kernel/kexec |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/kexec-tools
---

## kobs-ng

| Field | Value |
|---|---|
| Version | 5.4 |
| License | GPLv2 |
| Source URL | http://www.freescale.com/lgfiles/NMG/MAD/YOCTO/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/kobs-ng
---

## mt7623n-preloader

| Field | Value |
|---|---|
| Version | 2020-03-11 |
| Maintainer | David Woodhouse <dwmw2@infradead.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/mt7623n-preloader
---

## opensbi

| Field | Value |
|---|---|
| License | BSD-2-Clause |
| Maintainer | Zoltan HERPAI <wigyori@uid0.hu> include $(INCLUDE_DIR)/package.mk define Package/opensbi SECTION:=boot CATEGORY:=Boot Loaders DEPENDS:=@(TARGET_sifiveu||TARGET_d1) URL:=https://github.com/riscv/opensb |
| Source URL | https://github.com/riscv/opensbi |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/opensbi
---

## optee-os-stm32

| Field | Value |
|---|---|
| Version | 4.9.0 |
| Maintainer | Thomas Richard <thomas.richard@bootlin.com> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/optee-os-stm32
---

## rkbin

| Field | Value |
|---|---|
| Maintainer | Tianling Shen <cnsztl@immortalwrt.org> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/trusted-firmware-a.mk include $(INCLUDE_DIR)/package.mk define Trusted-Firmware-A/Default NAME:=Rockchip  |
| Source URL | https://github.com/rockchip-linux/rkbin.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/rkbin
---

## tfa-layerscape

| Field | Value |
|---|---|
| Version | 6.12.20.2.0.0 |
| Source URL | https://github.com/nxp-qoriq/atf |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/tfa-layerscape
---

## uboot-airoha

| Field | Value |
|---|---|
| Version | 2026.01 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-airoha
---

## uboot-armsr

| Field | Value |
|---|---|
| Version | 2025.04 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-armsr
---

## uboot-at91

| Field | Value |
|---|---|
| Version | linux4sam-2022.04 |
| Source URL | https://github.com/linux4sam/u-boot-at91.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-at91
---

## uboot-ath79

| Field | Value |
|---|---|
| Version | 2025.10 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-ath79
---

## uboot-bcm4908

| Field | Value |
|---|---|
| Source URL | https://git.openwrt.org/project/bcm63xx/u-boot.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-bcm4908
---

## uboot-bcm53xx

| Field | Value |
|---|---|
| Version | 2025.10 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-bcm53xx
---

## uboot-bmips

| Field | Value |
|---|---|
| Version | 2024.04 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-bmips
---

## uboot-d1

| Field | Value |
|---|---|
| Version | 2024.01 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-d1
---

## uboot-fritz4040

| Field | Value |
|---|---|
| Source URL | https://github.com/chunkeey/FritzBox-4040-UBOOT |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-fritz4040
---

## uboot-imx

| Field | Value |
|---|---|
| Version | 2022.01 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-imx
---

## uboot-kirkwood

| Field | Value |
|---|---|
| Version | 2020.04 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-kirkwood
---

## uboot-lantiq

| Field | Value |
|---|---|
| Version | 2013.10 |

**README:**

# README
```markdown
# How to refresh patches

$ git clone git@github.com:danielschwierzeck/u-boot-lantiq.git
$ mkdir -p $OPENWRT_ROOT/packages/boot/uboot-lantiq/patches
$ cd u-boot-lantiq.git
$ git format-patch -p -k --no-renames --no-binary -o $OPENWRT_ROOT/package/boot/uboot-lantiq/patches v2013.10..u-boot-lantiq-v2013.10-openwrtN
```


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-lantiq
---

## uboot-layerscape

| Field | Value |
|---|---|
| Version | 6.12.20.2.0.0 |
| Source URL | https://github.com/nxp-qoriq/u-boot |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-layerscape
---

## uboot-mediatek

| Field | Value |
|---|---|
| Version | 2026.01 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-mediatek
---

## uboot-microchipsw

| Field | Value |
|---|---|
| Maintainer | Robert Marko <robert.marko@sartura.hr> include $(INCLUDE_DIR)/u-boot.mk include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/kernel.mk define U-Boot/Default BUILD_TARGET:=microchipsw HIDDEN:=1 UBO |
| Source URL | https://github.com/microchip-ung/u-boot.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-microchipsw
---

## uboot-mvebu

| Field | Value |
|---|---|
| Version | 2026.01 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-mvebu
---

## uboot-mxs

| Field | Value |
|---|---|
| Version | 2020.04 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-mxs
---

## uboot-omap

| Field | Value |
|---|---|
| Version | 2021.07 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-omap
---

## uboot-qoriq

| Field | Value |
|---|---|
| Version | 2025.01 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-qoriq
---

## uboot-rockchip

| Field | Value |
|---|---|
| Version | 2026.01 |
| Maintainer | Sarah Maedel <openwrt@tbspace.de> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-rockchip
---

## uboot-sifiveu

| Field | Value |
|---|---|
| Version | 2023.10 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-sifiveu
---

## uboot-stm32

| Field | Value |
|---|---|
| Version | 2026.01 |
| Maintainer | Thomas Richard <thomas.richard@bootlin.com> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-stm32
---

## uboot-sunxi

| Field | Value |
|---|---|
| Version | 2025.10 |
| Maintainer | Zoltan HERPAI <wigyori@uid0.hu> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-sunxi
---

## uboot-tegra

| Field | Value |
|---|---|
| Version | 2025.04 |
| Maintainer | Tomasz Maciej Nowak <tmn505@gmail.com> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-tegra
---

## uboot-tools

| Field | Value |
|---|---|
| Version | 2026.01 |
| License | GPL-2.0 GPL-2.0+ |
| Source URL | https://ftp.denx.de/pub/u-boot https://mirror.cyberbits.eu/u-boot ftp://ftp.denx.de/pub/u-boot |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-tools
---

## uboot-zynq

| Field | Value |
|---|---|
| Version | 2019.07 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/boot/uboot-zynq
---

---

# OpenWrt Buildroot: firmware packages

> **Source:** https://github.com/openwrt/openwrt/tree/master/package/firmware
---

## ath10k-ct-firmware

| Field | Value |
|---|---|
| Version | 2023.04.04 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/ath10k-ct-firmware
---

## ath11k-firmware

| Field | Value |
|---|---|
| Maintainer | Robert Marko <robimarko@gmail.com> include $(INCLUDE_DIR)/package.mk |
| Source URL | https://git.codelinaro.org/clo/ath-firmware/ath11k-firmware.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/ath11k-firmware
---

## broadcom-sprom

| Field | Value |
|---|---|
| Maintainer | Álvaro Fernández Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/package.mk define Package/broadcom-sprom-default SECTION:=firmware CATEGORY:=Firmware endef define Build/Compile true endef # BCM4306  |
| Source URL | https://github.com/openwrt/broadcom-sprom.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/broadcom-sprom
---

## cypress-firmware

| Field | Value |
|---|---|
| Maintainer | Álvaro Fernández Rojas <noltari@gmail.com> |
| Source URL | https://github.com/Infineon/ifx-linux-firmware/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/cypress-firmware
---

## cypress-nvram

| Field | Value |
|---|---|
| Maintainer | Álvaro Fernández Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/package.mk define Package/cypress-nvram-default SECTION:=firmware CATEGORY:=Firmware endef define Build/Compile true endef # Cypress 4 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/cypress-nvram
---

## intel-microcode

| Field | Value |
|---|---|
| Version | 20251111 |
| Source URL | @DEBIAN/pool/non-free-firmware/i/intel-microcode/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/intel-microcode
---

## ipq-wifi


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/ipq-wifi
---

## ixp4xx-microcode

| Field | Value |
|---|---|
| Version | 2.4 |
| Source URL | http://downloads.openwrt.org/sources |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/ixp4xx-microcode
---

## linux-firmware

| Field | Value |
|---|---|
| Version | 20260221 |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | @KERNEL/linux/kernel/firmware |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/linux-firmware
---

## murata-firmware

| Field | Value |
|---|---|
| Maintainer | Thomas Richard <thomas.richard@bootlin.com> |
| Source URL | https://github.com/murata-wireless/cyw-fmac-fw.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/murata-firmware
---

## murata-nvram

| Field | Value |
|---|---|
| Maintainer | Thomas Richard <thomas.richard@bootlin.com> |
| Source URL | https://github.com/murata-wireless/cyw-fmac-nvram.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/murata-nvram
---

## omnia-mcu-firmware

| Field | Value |
|---|---|
| Version | 4.1 |
| License | GPL-3.0-or-later |
| Maintainer | Marek Mojik <marek.mojik@nic.cz> |
| Source URL | https://gitlab.nic.cz/turris/hw/$(PKG_DISTNAME)/-/releases/v$(PKG_VERSION)/downloads/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/omnia-mcu-firmware
---

## prism54-firmware


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/prism54-firmware
---

## wireless-regdb

| Field | Value |
|---|---|
| Version | 2026.02.04 |
| License | ISC |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk define Package/wireless-regdb PKGARCH:=all SECTION:=firmware CATEGORY:=Firmware URL:=https://git.kernel.org/pub/scm/linux/kernel/git/wens |
| Source URL | @KERNEL/software/network/wireless-regdb/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/firmware/wireless-regdb
---

---

# OpenWrt Buildroot: kernel packages

> **Source:** https://github.com/openwrt/openwrt/tree/master/package/kernel
---

## ath10k-ct

| Field | Value |
|---|---|
| License | GPLv2 |
| Maintainer | Ben Greear <greearb@candelatech.com> |
| Source URL | https://github.com/greearb/ath10k-ct.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/ath10k-ct
---

## bcm27xx-gpu-fw

| Field | Value |
|---|---|
| Version | 2025.04.30 |
| Source URL | https://github.com/raspberrypi/firmware/releases/download/$(PKG_VERSION_REAL) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/bcm27xx-gpu-fw
---

## bcm63xx-cfe

| Field | Value |
|---|---|
| Source URL | https://github.com/openwrt/bcm63xx-cfe.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/bcm63xx-cfe
---

## bpf-headers

| Field | Value |
|---|---|
| Source URL | @KERNEL/linux/kernel/v$(word 1,$(subst ., ,$(PKG_PATCHVER))).x |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/bpf-headers
---

## button-hotplug

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/button-hotplug SUBMENU:=Other modules TITLE:=Button Hotplug driver DEPENDS:=+kmod-input-core FILES:=$(PKG_BUILD_DIR)/button-hotplug.ko AU |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/button-hotplug
---

## cryptodev-linux

| Field | Value |
|---|---|
| Version | 1.14 |
| License | GPL-2.0 |
| Maintainer | Ansuel Smith <ansuelsmth@gmail.com> |
| Source URL | https://codeload.github.com/$(PKG_NAME)/$(PKG_NAME)/tar.gz/$(PKG_NAME)-$(PKG_VERSION)? |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/cryptodev-linux
---

## econet-eth

| Field | Value |
|---|---|
| Source URL | https://github.com/cjdelisle/econet_eth.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/econet-eth
---

## gpio-button-hotplug

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/gpio-button-hotplug SUBMENU:=GPIO support TITLE:=Simple GPIO Button Hotplug driver FILES:=$(PKG_BUILD_DIR)/gpio-button-hotplug.ko AUTOLOA |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/gpio-button-hotplug
---

## gpio-nct5104d

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/gpio-nct5104d SUBMENU:=GPIO support TITLE:= GPIO nct5104d support DEPENDS:= @GPIO_SUPPORT @TARGET_x86 FILES:=$(PKG_BUILD_DIR)/gpio-nct510 |
| Maintainer | Florian Eckert <Eckert.Florian@googlemail.com> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/gpio-nct5104d
---

## leds-gca230718

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/leds-gca230718 SUBMENU:=LED modules TITLE:=GCA230718 LED support (e.g. for D-Link M30) FILES:= $(PKG_BUILD_DIR)/leds-gca230718.ko AUTOLOA |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/leds-gca230718
---

## leds-ws2812b

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/leds-ws2812b SUBMENU:=LED modules TITLE:=Worldsemi WS2812B (NeoPixel) LED support FILES:= $(PKG_BUILD_DIR)/leds-ws2812b.ko AUTOLOAD:=$(ca |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/leds-ws2812b
---

## linux

| Field | Value |
|---|---|
| License | GPL-2.0-only |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/linux
---

## mac80211

| Field | Value |
|---|---|
| Version | 6.18.7 |
| License | GPL-2.0-only |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | https://github.com/openwrt/backports/releases/download/backports-v$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/mac80211
---

## mt76

| Field | Value |
|---|---|
| License | BSD-3-Clause-Clear |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | https://github.com/openwrt/mt76 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/mt76
---

## mt7621-qtn-rgmii

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Bjørn Mork <bjorn@mork.no> include $(INCLUDE_DIR)/package.mk define KernelPackage/mt7621-qtn-rgmii SECTION:=kernel SUBMENU:=Other modules TITLE:=Enable RGMII connected Quantenna module on MT7621 DEPEN |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/mt7621-qtn-rgmii
---

## mwlwifi

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Imre Kaloz <kaloz@openwrt.org> |
| Source URL | https://github.com/kaloz/mwlwifi |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/mwlwifi
---

## nat46

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/nat46 DEPENDS:=@IPV6 +kmod-nf-conntrack TITLE:=Stateless NAT46 translation kernel module SECTION:=kernel SUBMENU:=Network Support FILES:= |
| Maintainer | Hans Dedecker <dedeckeh@gmail.com> |
| Source URL | https://github.com/ayourtch/nat46.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/nat46
---

## qca-nss-dp

| Field | Value |
|---|---|
| Source URL | https://github.com/openwrt/qca-nss-dp.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/qca-nss-dp
---

## qca-ssdk

| Field | Value |
|---|---|
| Source URL | https://github.com/openwrt/qca-ssdk.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/qca-ssdk
---

## r8101

| Field | Value |
|---|---|
| Version | 1.039.00 |
| License | GPLv2 |
| Maintainer | Alvaro Fernandez Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/package.mk define KernelPackage/r8101 SUBMENU:=Network Devices TITLE:=Realtek RTL8101 PCI Fast Ethern |
| Source URL | https://github.com/openwrt/rtl8101/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/r8101
---

## r8125

| Field | Value |
|---|---|
| Version | 9.016.01 |
| License | GPLv2 |
| Maintainer | Alvaro Fernandez Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/package.mk define KernelPackage/r8125 SUBMENU:=Network Devices TITLE:=Realtek RTL8125 PCI 2.5 Gigabit |
| Source URL | https://github.com/openwrt/rtl8125/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/r8125
---

## r8126

| Field | Value |
|---|---|
| Version | 10.016.00 |
| License | GPLv2 |
| Maintainer | Alvaro Fernandez Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/package.mk define KernelPackage/r8126 SUBMENU:=Network Devices TITLE:=Realtek RTL8126 PCI 5 Gigabit E |
| Source URL | https://github.com/openwrt/rtl8126/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/r8126
---

## r8127

| Field | Value |
|---|---|
| Version | 11.015.00 |
| License | GPLv2 |
| Maintainer | Alvaro Fernandez Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/package.mk define KernelPackage/r8127 SUBMENU:=Network Devices TITLE:=Realtek RTL8127 PCI 10 Gigabit  |
| Source URL | https://github.com/openwrt/rtl8127/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/r8127
---

## r8168

| Field | Value |
|---|---|
| Version | 8.055.00 |
| License | GPLv2 |
| Maintainer | Alvaro Fernandez Rojas <noltari@gmail.com> include $(INCLUDE_DIR)/kernel.mk include $(INCLUDE_DIR)/package.mk define KernelPackage/r8168 SUBMENU:=Network Devices TITLE:=Realtek RTL8168 PCI Gigabit Eth |
| Source URL | https://github.com/openwrt/rtl8168/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/r8168
---

## rtc-rv5c386a


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/rtc-rv5c386a
---

## rtl8812au-ct

| Field | Value |
|---|---|
| License | GPLv2 |
| Maintainer | Ben Greear <greearb@candelatech.com> |
| Source URL | https://github.com/greearb/rtl8812AU_8821AU_linux.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/rtl8812au-ct
---

## trelay


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/trelay
---

## ubnt-ledbar

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/leds-ubnt-ledbar SUBMENU:=LED modules TITLE:=Ubiquiti UniFi 6 LR LED support FILES:= $(PKG_BUILD_DIR)/leds-ubnt-ledbar.ko AUTOLOAD:=$(cal |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/ubnt-ledbar
---

## ubootenv-nvram

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define KernelPackage/ubootenv-nvram SUBMENU:=Other modules TITLE:=NVRAM environment for uboot-envtools FILES:=$(PKG_BUILD_DIR)/ubootenv-nvram.ko AUTOLOAD:=$(c |


> Source: https://github.com/openwrt/openwrt/tree/master/package/kernel/ubootenv-nvram
---

---

# OpenWrt Buildroot: libs packages

> **Source:** https://github.com/openwrt/openwrt/tree/master/package/libs
---

## argp-standalone

| Field | Value |
|---|---|
| Version | 1.3 |
| License | LGPL-2.1 |
| Maintainer | Ted Hess <thess@kitschensync.net> |
| Source URL | https://www.lysator.liu.se/~nisse/misc/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/argp-standalone
---

## elfutils

| Field | Value |
|---|---|
| Version | 0.192 |
| License | GPL-2.0-or-later LGPL-3.0-or-later |
| Maintainer | Luiz Angelo Daros de Luca <luizluca@gmail.com> |
| Source URL | https://sourceware.org/$(PKG_NAME)/ftp/$(PKG_VERSION) https://mirrors.kernel.org/sourceware/$(PKG_NAME)/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/elfutils
---

## gettext-full

| Field | Value |
|---|---|
| Version | 0.24.1 |
| License | LGPL-2.1-or-later |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | @GNU/gettext |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/gettext-full
---

## gmp

| Field | Value |
|---|---|
| Version | 6.3.0 |
| License | GPL-2.0-or-later |
| Source URL | @GNU/gmp/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/gmp
---

## gnulib-l10n

| Field | Value |
|---|---|
| Version | 20241231 |
| Source URL | @GNU/gnulib |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/gnulib-l10n
---

## jansson

| Field | Value |
|---|---|
| Version | 2.15.0 |
| License | MIT |
| Source URL | https://codeload.github.com/akheron/$(PKG_NAME)/tar.gz/v$(PKG_VERSION)? |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/jansson
---

## libbpf

| Field | Value |
|---|---|
| Version | 1.6.2 |
| Maintainer | Tony Ambardar <itugrok@yahoo.com> |
| Source URL | https://github.com/libbpf/libbpf |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libbpf
---

## libbsd

| Field | Value |
|---|---|
| Version | 0.12.2 |
| License | BSD-4-Clause |
| Source URL | https://libbsd.freedesktop.org/releases |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libbsd
---

## libcap

| Field | Value |
|---|---|
| Version | 2.69 |
| License | GPL-2.0-only |
| Maintainer | Paul Wassi <p.wassi@gmx.at> |
| Source URL | @KERNEL/linux/libs/security/linux-privs/libcap2 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libcap
---

## libevent2

| Field | Value |
|---|---|
| Version | 2.1.12 |
| License | BSD-3-Clause |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | https://github.com/libevent/libevent/releases/download/release-$(PKG_VERSION)-stable |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libevent2
---

## libiconv-full

| Field | Value |
|---|---|
| Version | 1.18 |
| License | LGPL-2.1-or-later |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | @GNU/libiconv |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libiconv-full
---

## libjson-c

| Field | Value |
|---|---|
| Version | 0.18 |
| License | MIT |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | https://s3.amazonaws.com/json-c_releases/releases/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libjson-c
---

## libmd

| Field | Value |
|---|---|
| Version | 1.1.0 |
| License | BSD-3-Clause |
| Source URL | https://archive.hadrons.org/software/libmd/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libmd
---

## libmnl

| Field | Value |
|---|---|
| Version | 1.0.5 |
| License | LGPL-2.1+ |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | http://www.netfilter.org/projects/libmnl/files ftp://ftp.netfilter.org/pub/libmnl |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libmnl
---

## libnetfilter-conntrack

| Field | Value |
|---|---|
| Version | 1.1.0 |
| License | GPL-2.0-or-later |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | https://www.netfilter.org/projects/libnetfilter_conntrack/files |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libnetfilter-conntrack
---

## libnfnetlink

| Field | Value |
|---|---|
| Version | 1.0.2 |
| License | GPL-2.0+ |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | http://www.netfilter.org/projects/libnfnetlink/files/ ftp://ftp.netfilter.org/pub/libnfnetlink/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libnfnetlink
---

## libnftnl

| Field | Value |
|---|---|
| Version | 1.3.1 |
| License | GPL-2.0-or-later |
| Maintainer | Steven Barth <steven@midlink.org> |
| Source URL | https://netfilter.org/projects/$(PKG_NAME)/files |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libnftnl
---

## libnl

| Field | Value |
|---|---|
| Version | 3.12.0 |
| License | LGPL-2.1 |
| Source URL | https://github.com/thom311/libnl/releases/download/libnl$(subst .,_,$(PKG_VERSION)) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libnl
---

## libnl-tiny

| Field | Value |
|---|---|
| License | LGPL-2.1 |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk define Package/libnl-tiny SECTION:=libs CATEGORY:=Libraries TITLE:=netlink socket library ABI_VERSION:=1  |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libnl-tiny
---

## libpcap

| Field | Value |
|---|---|
| Version | 1.10.6 |
| License | BSD-3-Clause |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | https://www.tcpdump.org/release/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libpcap
---

## libselinux

| Field | Value |
|---|---|
| Version | 3.9 |
| License | libselinux-1.0 |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/SELinuxProject/selinux/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libselinux
---

## libsemanage

| Field | Value |
|---|---|
| Version | 3.9 |
| License | LGPL-2.1 |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/SELinuxProject/selinux/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libsemanage
---

## libsepol

| Field | Value |
|---|---|
| Version | 3.9 |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/SELinuxProject/selinux/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libsepol
---

## libtool

| Field | Value |
|---|---|
| Version | 2.5.4 |
| License | GPL-2.0+ |
| Source URL | @GNU/libtool |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libtool
---

## libtraceevent

| Field | Value |
|---|---|
| Version | 1.9.0 |
| Maintainer | Nick Hainke <vincent@systemli.org> |
| Source URL | https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libtraceevent
---

## libtracefs

| Field | Value |
|---|---|
| Version | 1.8.3 |
| Maintainer | Nick Hainke <vincent@systemli.org> |
| Source URL | https://git.kernel.org/pub/scm/libs/libtrace/libtracefs.git/snapshot/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libtracefs
---

## libubox

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Felix Fietkau <nbd@nbd.name> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libubox
---

## libunistring

| Field | Value |
|---|---|
| Version | 1.4.2 |
| License | GPL-3.0 |
| Source URL | @GNU/$(PKG_NAME) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libunistring
---

## libunwind

| Field | Value |
|---|---|
| Version | 1.8.3 |
| License | X11 |
| Maintainer | Yousong Zhou <yszhou4tech@gmail.com> |
| Source URL | https://github.com/libunwind/libunwind/releases/download/v$(PKG_VERSION)/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libunwind
---

## libusb

| Field | Value |
|---|---|
| Version | 1.0.29 |
| License | LGPL-2.1-or-later |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | https://github.com/libusb/libusb/releases/download/v$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libusb
---

## libxml2

| Field | Value |
|---|---|
| Version | 2.15.1 |
| License | MIT |
| Source URL | @GNOME/libxml2/$(basename $(PKG_VERSION)) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/libxml2
---

## mbedtls

| Field | Value |
|---|---|
| Version | 3.6.5 |
| License | GPL-2.0-or-later |
| Source URL | https://github.com/Mbed-TLS/$(PKG_NAME)/releases/download/$(PKG_NAME)-$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/mbedtls
---

## mpfr

| Field | Value |
|---|---|
| Version | 4.2.2 |
| License | LGPL-3.0-or-later |
| Maintainer | Jeffery To <jeffery.to@gmail.com> |
| Source URL | @GNU/mpfr http://www.mpfr.org/mpfr-$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/mpfr
---

## musl-fts

| Field | Value |
|---|---|
| Version | 1.2.7 |
| License | LGPL-2.1 |
| Maintainer | Lucian Cristian <lucian.cristian@gmail.com> |
| Source URL | https://github.com/pullmoll/musl-fts.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/musl-fts
---

## ncurses

| Field | Value |
|---|---|
| Version | 6.4 |
| License | MIT |
| Source URL | @GNU/$(PKG_NAME) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/ncurses
---

## nettle

| Field | Value |
|---|---|
| Version | 3.10.2 |
| License | GPL-2.0-or-later |
| Source URL | @GNU/nettle |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/nettle
---

## openssl

| Field | Value |
|---|---|
| Version | 3.5.5 |
| License | Apache-2.0 |
| Maintainer | Eneas U de Queiroz <cotequeiroz@gmail.com> |
| Source URL | https://www.openssl.org/source/ https://www.openssl.org/source/old/$(PKG_BASE)/ https://github.com/openssl/openssl/relea |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/openssl
---

## pcre2

| Field | Value |
|---|---|
| Version | 10.47 |
| License | BSD-3-Clause |
| Maintainer | Shane Peelar <lookatyouhacker@gmail.com> |
| Source URL | https://github.com/PCRE2Project/pcre2/releases/download/$(PKG_NAME)-$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/pcre2
---

## popt

| Field | Value |
|---|---|
| Version | 1.19 |
| License | MIT |
| Source URL | http://ftp.rpm.org/popt/releases/popt-1.x/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/popt
---

## readline

| Field | Value |
|---|---|
| Version | 8.3 |
| License | GPL-3.0-or-later |
| Source URL | @GNU/readline |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/readline
---

## sysfsutils

| Field | Value |
|---|---|
| Version | 2.1.0 |
| License | LGPL-2.1 |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | @SF/linux-diag |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/sysfsutils
---

## toolchain

| Field | Value |
|---|---|
| License | GPL-3.0-with-GCC-exception |
| Maintainer | Felix Fietkau <nbd@nbd.name> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/toolchain
---

## uclient

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Felix Fietkau <nbd@nbd.name> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/uclient
---

## udebug

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk define Package/libudebug SECTION:=libs CATEGORY:=Libraries TITLE:=udebug client library DEPENDS:=+libubox |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/udebug
---

## ustream-ssl

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk define Package/libustream/default SECTION:=libs CATEGORY:=Libraries TITLE:=ustream SSL Library DEPENDS:=+ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/ustream-ssl
---

## wolfssl

| Field | Value |
|---|---|
| Version | 5.8.4 |
| License | GPL-3.0-or-later |
| Maintainer | Eneas U de Queiroz <cotequeiroz@gmail.com> |
| Source URL | https://github.com/wolfSSL/wolfssl/archive/v$(PKG_REAL_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/wolfssl
---

## zlib

| Field | Value |
|---|---|
| Version | 1.3.1 |
| License | Zlib |
| Source URL | https://github.com/madler/zlib |


> Source: https://github.com/openwrt/openwrt/tree/master/package/libs/zlib
---

---

# OpenWrt Buildroot: system packages

> **Source:** https://github.com/openwrt/openwrt/tree/master/package/system
---

## apk

| Field | Value |
|---|---|
| Version | 3.0.5 |
| License | GPL-2.0-only |
| Maintainer | Paul Spooren <mail@aparcar.org> |
| Source URL | https://gitlab.alpinelinux.org/alpine/apk-tools.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/apk
---

## ca-certificates

| Field | Value |
|---|---|
| Version | 20250419 |
| License | GPL-2.0-or-later MPL-2.0 |
| Maintainer | PKG_LICENSE:=GPL-2.0-or-later MPL-2.0 |
| Source URL | @DEBIAN/pool/main/c/ca-certificates |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/ca-certificates
---

## fstools

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | John Crispin <john@phrozen.org> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/fstools
---

## fwtool

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Felix Fietkau <nbd@nbd.name> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/fwtool
---

## iucode-tool

| Field | Value |
|---|---|
| Version | 2.3.1 |
| License | GPL-2.0 |
| Maintainer | Zoltan HERPAI <wigyori@uid0.hu> |
| Source URL | https://gitlab.com/iucode-tool/releases/raw/latest |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/iucode-tool
---

## mtd

| Field | Value |
|---|---|
| License | GPL-2.0+ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/mtd
---

## openwrt-keyring

| Field | Value |
|---|---|
| License | GPL-2.0 include $(INCLUDE_DIR)/package.mk define Package/openwrt-keyring SECTION:=base CATEGORY:=Base system PROVIDES:=lede-keyring TITLE:=OpenWrt Developer Keyring URL:=https://openwrt.org/docs/guide |
| Maintainer | John Crispin <john@phrozen.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/openwrt-keyring
---

## opkg

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Jo-Philipp Wich <jo@mein.io> # Extend depends from version.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/opkg
---

## procd

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | John Crispin <john@phrozen.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/procd
---

## refpolicy

| Field | Value |
|---|---|
| Version | 2.20250923 |
| License | GPL-2.0-or-later |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/SELinuxProject/refpolicy/releases/download/RELEASE_2_20250923 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/refpolicy
---

## rpcd

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/rpcd
---

## selinux-policy

| Field | Value |
|---|---|
| Version | 2.8.4 |
| License | Unlicense |
| Maintainer | Dominick Grift <dominick.grift@defensec.nl> |
| Source URL | https://git.defensec.nl/selinux-policy.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/selinux-policy
---

## ubox

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | John Crispin <john@phrozen.org> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk define Package/ubox SECTION:=base CATEGORY:=Base system DEPENDS:=+libubox +ubusd +ubus +libubus +libuc |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/ubox
---

## ubus

| Field | Value |
|---|---|
| License | LGPL-2.1 |
| Maintainer | Felix Fietkau <nbd@nbd.name> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/ubus
---

## ucert

| Field | Value |
|---|---|
| License | GPL-3.0+ |
| Maintainer | Daniel Golle <daniel@makrotopia.org> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/host-build.mk include $(INCLUDE_DIR)/cmake.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/ucert
---

## uci

| Field | Value |
|---|---|
| License | LGPL-2.1 |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk # set to 1 to enable debugging |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/uci
---

## urandom-seed

| Field | Value |
|---|---|
| License | GPL-2.0-only include $(INCLUDE_DIR)/package.mk define Package/urandom-seed SECTION:=base CATEGORY:=Base system DEPENDS:=+getrandom TITLE:=/etc/urandom.seed handling for OpenWrt URL:=https://openwrt.or |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/urandom-seed
---

## urngd

| Field | Value |
|---|---|
| License | GPL-2.0 BSD-3-Clause |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/urngd
---

## usign

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/host-build.mk include $(INCLUDE_DIR)/cmake.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/usign
---

## zram-swap


> Source: https://github.com/openwrt/openwrt/tree/master/package/system/zram-swap
---

---

# OpenWrt Buildroot: utils packages

> **Source:** https://github.com/openwrt/openwrt/tree/master/package/utils
---

## adb

| Field | Value |
|---|---|
| Version | 5.0.2~$(call version_abbrev,$(PKG_SOURCE_VERSION)) |
| Maintainer | Henryk Heisig <hyniu@o2.pl> |
| Source URL | https://android.googlesource.com/platform/system/core |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/adb
---

## audit

| Field | Value |
|---|---|
| Version | 3.1.5 |
| License | GPL-2.0-or-later LGPL-2.1-or-later |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/linux-audit/$(PKG_NAME).git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/audit
---

## bcm27xx-utils

| Field | Value |
|---|---|
| Version | 2025.03.14 |
| License | BSD-3-Clause |
| Source URL | https://github.com/raspberrypi/utils.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/bcm27xx-utils
---

## bcm4908img


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/bcm4908img
---

## bsdiff

| Field | Value |
|---|---|
| Version | 4.3 |
| License | BSD-2-Clause |
| Maintainer | Hauke Mehrtens <hauke@hauke-m.de> |
| Source URL | https://www.daemonology.net/bsdiff/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/bsdiff
---

## busybox

| Field | Value |
|---|---|
| Version | 1.37.0 |
| License | GPL-2.0 |
| Source URL | https://www.busybox.net/downloads https://sources.buildroot.net/$(PKG_NAME) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/busybox
---

## bzip2

| Field | Value |
|---|---|
| Version | 1.0.8 |
| License | bzip2-1.0.8 |
| Maintainer | Steven Barth <cyrus@openwrt.org> |
| Source URL | https://sourceware.org/pub/bzip2 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/bzip2
---

## checkpolicy

| Field | Value |
|---|---|
| Version | 3.9 |
| License | GPL-2.0-or-later |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/SELinuxProject/selinux/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/checkpolicy
---

## cli

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk define Package/cli SECTION:=utils CATEGORY:=Utilities TITLE:=OpenWrt CLI DEPENDS:=+ucode +ucode-mod-uline +ucode-mod-ubus +ucode-mod-uloo |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/cli
---

## ct-bugcheck


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ct-bugcheck
---

## debugcc

| Field | Value |
|---|---|
| License | BSD-3-Clause |
| Maintainer | Christian Marangi <ansuelsmth@gmail.com> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/meson.mk define Package/debugcc SECTION:=utils CATEGORY:=Utilities TITLE:=QCOM debugcc utility DEPENDS |
| Source URL | https://github.com/linux-msm/debugcc.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/debugcc
---

## dns320l-mcu

| Field | Value |
|---|---|
| License | GPL-3.0+ |
| Maintainer | Zoltan HERPAI <wigyori@uid0.hu> |
| Source URL | https://github.com/wigyori/dns320l-daemon.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/dns320l-mcu
---

## dtc

| Field | Value |
|---|---|
| Version | 1.7.2 |
| License | GPL-2.0-only |
| Maintainer | Yousong Zhou <yszhou4tech@gmail.com> |
| Source URL | @KERNEL/software/utils/dtc |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/dtc
---

## e2fsprogs

| Field | Value |
|---|---|
| Version | 1.47.3 |
| License | GPL-2.0 |
| Source URL | @KERNEL/linux/kernel/people/tytso/e2fsprogs/v$(PKG_VERSION)/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/e2fsprogs
---

## f2fs-tools

| Field | Value |
|---|---|
| Version | 1.16.0 |
| License | GPL-2.0-only |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | https://git.kernel.org/pub/scm/linux/kernel/git/jaegeuk/f2fs-tools.git/snapshot/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/f2fs-tools
---

## fbtest


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/fbtest
---

## firmware-utils


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/firmware-utils
---

## fitblk

| Field | Value |
|---|---|
| License | GPL-2.0-only |
| Maintainer | Daniel Golle <daniel@makrotopia.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/fitblk
---

## fritz-tools

**README:**

# README
```markdown
Userspace utilties for accessing TFFS (a name-value storage usually found in AVM Fritz!Box based devices)

## Building

```
mkdir build
cd build
cmake /path/to/fritz_tffs_tools
make
```

## Usage

All command line parameters are documented:
```
fritz_tffs_read -h
```

Show all entries from a TFFS partition dump  (in the format: name=value):
```
fritz_tffs_read -i /path/to/tffs.dump -a
```

Read a TFFS partition and show all entries (in the format: name=value):
```
fritz_tffs_read -i /dev/mtdX -a
```

Output only the value of a specific key (this will only show the value):
```
fritz_tffs_read -i /dev/mtdX -n my_ipaddress
```

## LICENSE

See `LICENSE`:

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
```


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/fritz-tools
---

## jboot-tools

**README:**

# README
```markdown
Userspace utilties for jboot based devices config partition read

## Building

```
mkdir build
cd build
cmake /path/to/jboot-tools
make
```

## Usage

All command line parameters are documented:
```
jboot_config_read -h
```

Show all stored MACs:
```
jboot_config_read -m -i PATH_TO_CONFIG_PARTITIO
```

Extract wifi eeprom data:
```
jboot_config_read  -i PATH_TO_CONFIG_PARTITION -e OUTPUT_PATH
```


## LICENSE

See `LICENSE`:

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
```


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/jboot-tools
---

## jsonfilter

| Field | Value |
|---|---|
| License | ISC include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk define Package/jsonfilter SECTION:=base CATEGORY:=Base system DEPENDS:=+libubox +libjson-c TITLE:=OpenWrt JSON filter utility URL: |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/jsonfilter
---

## lua

| Field | Value |
|---|---|
| Version | 5.1.5 |
| License | MIT |
| Source URL | https://www.lua.org/ftp/ https://www.tecgraf.puc-rio.br/lua/ftp/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/lua
---

## lua5.3

| Field | Value |
|---|---|
| Version | 5.3.5 |
| License | MIT |
| Source URL | https://www.lua.org/ftp/ https://www.tecgraf.puc-rio.br/lua/ftp/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/lua5.3
---

## mdadm

| Field | Value |
|---|---|
| Version | 4.3 |
| Maintainer | Felix Fietkau <nbd@nbd.name> |
| Source URL | @KERNEL/linux/utils/raid/mdadm |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/mdadm
---

## mtd-utils

| Field | Value |
|---|---|
| Version | 2.3.0 |
| License | GPLv2 |
| Maintainer | John Crispin <john@phrozen.org> include $(INCLUDE_DIR)/package.mk define Package/mtd-utils/Default SECTION:=utils CATEGORY:=Utilities URL:=http://www.linux-mtd.infradead.org/ DEPENDS:=@NAND_SUPPORT en |
| Source URL | https://infraroot.at/pub/mtd/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/mtd-utils
---

## nilfs-utils

| Field | Value |
|---|---|
| Version | 2.2.12 |
| License | GPL-2.0 |
| Maintainer | Pavlo Samko <bulldozerbsg@gmail.com> |
| Source URL | https://nilfs.sourceforge.io/download/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/nilfs-utils
---

## nvram


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/nvram
---

## omnia-eeprom

| Field | Value |
|---|---|
| Version | 0.1 |
| License | GPL-2.0-or-later |
| Maintainer | Marek Behun <kabel@kernel.org> |
| Source URL | https://gitlab.nic.cz/turris/omnia-eeprom/-/archive/v$(PKG_VERSION)/ |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/omnia-eeprom
---

## omnia-mcutool

| Field | Value |
|---|---|
| License | GPL-2.0-or-later include $(INCLUDE_DIR)/package.mk define Package/omnia-mcutool SECTION:=utils CATEGORY:=Utilities URL:=https://gitlab.nic.cz/turris/$(PKG_NAME) TITLE:=CZ.NIC Turris Omnia MCU utility  |
| Maintainer | Marek Mojik <marek.mojik@nic.cz> |
| Source URL | https://gitlab.nic.cz/turris/$(PKG_NAME) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/omnia-mcutool
---

## osafeloader


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/osafeloader
---

## policycoreutils

| Field | Value |
|---|---|
| Version | 3.9 |
| License | GPL-2.0-or-later |
| Maintainer | Thomas Petazzoni <thomas.petazzoni@bootlin.com> |
| Source URL | https://github.com/SELinuxProject/selinux/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/policycoreutils
---

## provision

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk define Package/provision SECTION:=utils CATEGORY:=Utilities TITLE:=Utility for managing device provisioning data DEPENDS:=+ucode +ucode-m |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/provision
---

## px5g-mbedtls

| Field | Value |
|---|---|
| License | LGPL-2.1 |
| Maintainer | Jo-Philipp Wich <jo@mein.io> include $(INCLUDE_DIR)/package.mk define Package/px5g-mbedtls SECTION:=utils CATEGORY:=Utilities SUBMENU:=Encryption TITLE:=X.509 certificate generator (using mbedtls) DEP |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/px5g-mbedtls
---

## px5g-wolfssl

| Field | Value |
|---|---|
| License | GPL-2.0-or-later |
| Maintainer | Paul Spooren <mail@aparcar.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/px5g-wolfssl
---

## ravpower-mcu

| Field | Value |
|---|---|
| License | GPL-2.0-or-later include $(INCLUDE_DIR)/package.mk define Package/ravpower-mcu SECTION:=utils CATEGORY:=Utilities TITLE:=Utility to control the RAVPower RP-WD009 PMIC URL:=https://github.com/blocktrro |
| Maintainer | David Bauer <mail@david-bauer.net> |
| Source URL | https://github.com/blocktrron/ravpower-mcu.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ravpower-mcu
---

## secilc

| Field | Value |
|---|---|
| Version | 3.9 |
| License | BSD-2-Clause |
| Maintainer | Dominick Grift <dominick.grift@defensec.nl> |
| Source URL | https://github.com/SELinuxProject/selinux/releases/download/$(PKG_VERSION) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/secilc
---

## spidev_test

| Field | Value |
|---|---|
| License | GPL-2.0-only include $(INCLUDE_DIR)/package.mk define Package/spidev-test SECTION:=utils CATEGORY:=Utilities DEPENDS:=+kmod-spi-dev TITLE:=SPI testing utility VERSION:=$(LINUX_VERSION)-r$(PKG_RELEASE) |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/spidev_test
---

## ucode

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Jo-Philipp Wich <jo@mein.io> |
| Source URL | https://github.com/jow-/ucode.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ucode
---

## ucode-mod-bpf

| Field | Value |
|---|---|
| License | ISC |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/nls.mk define Package/ucode-mod-bpf SECTION:=utils CATEGORY:=Utilities TITLE:=ucode eBPF module DEPENDS:=+libucode |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ucode-mod-bpf
---

## ucode-mod-pkgen

| Field | Value |
|---|---|
| License | GPL-2.0-or-later |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ucode-mod-pkgen
---

## ucode-mod-uline

| Field | Value |
|---|---|
| License | GPL-2.0-or-later |
| Maintainer | Felix Fietkau <nbd@nbd.name> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ucode-mod-uline
---

## uencrypt

| Field | Value |
|---|---|
| License | GPL-2.0-or-later |
| Maintainer | Eneas U de Queiroz <cotequeiroz@gmail.com> include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/uencrypt
---

## ugps

| Field | Value |
|---|---|
| License | GPL-2.0+ include $(INCLUDE_DIR)/package.mk include $(INCLUDE_DIR)/cmake.mk define Package/ugps SECTION:=utils CATEGORY:=Utilities TITLE:=OpenWrt GPS Daemon DEPENDS:=+libubox +libubus endef |
| Maintainer | John Crispin <john@phrozen.org> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/ugps
---

## usbgadget

| Field | Value |
|---|---|
| License | BSD-2-Clause |
| Maintainer | Chuanhong Guo <gch981213@gmail.com> include $(INCLUDE_DIR)/package.mk define Package/$(PKG_NAME) SECTION:=utils CATEGORY:=Utilities DEPENDS:=@USB_GADGET_SUPPORT +kmod-usb-gadget +kmod-fs-configfs +kmo |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/usbgadget
---

## usbmode

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Maintainer | Felix Fietkau <nbd@nbd.name> |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/usbmode
---

## util-linux

| Field | Value |
|---|---|
| Version | 2.41.3 |
| Source URL | @KERNEL/linux/utils/$(PKG_NAME)/v2.41 |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/util-linux
---

## yafut

| Field | Value |
|---|---|
| License | GPL-2.0 |
| Source URL | https://github.com/kempniu/yafut.git |


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/yafut
---

## zyxel-bootconfig


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/zyxel-bootconfig
---

## zyxel-bootconfig-ipq807x


> Source: https://github.com/openwrt/openwrt/tree/master/package/utils/zyxel-bootconfig-ipq807x
---

---

# OpenWrt Buildroot: Build System Include Files

> **Source:** https://github.com/openwrt/openwrt/tree/master/include

Core build system Makefile fragments.

---

## autotools.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/autotools.mk
---

## debug.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/debug.mk
---

## depends.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/depends.mk
---

## download.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2012 OpenWrt.org
Copyright (C) 2016 LEDE project
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/download.mk
---

## feeds.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2014 OpenWrt.org
Copyright (C) 2016 LEDE Project
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/feeds.mk
---

## hardening.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2015-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/hardening.mk
---

## host-build.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/host-build.mk
---

## image.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/image.mk
---

## kernel-build.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/kernel-build.mk
---

## kernel-defaults.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/kernel-defaults.mk
---

## kernel.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/kernel.mk
---

## meson.mk

# Documentation
```text
To build your package using meson:
include $(INCLUDE_DIR)/meson.mk
MESON_ARGS+=-Dfoo -Dbar=baz
To pass additional environment variables to meson:
MESON_VARS+=FOO=bar
Default configure/compile/install targets are provided, but can be
overwritten if required:
define Build/Configure
$(call Build/Configure/Meson)
...
endef
same for Build/Compile and Build/Install
Host packages are built in the same fashion, just use these vars instead:
MESON_HOST_ARGS+=-Dfoo -Dbar=baz
MESON_HOST_VARS+=FOO=bar
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/meson.mk
---

## netfilter.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/netfilter.mk
---

## nls.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2011-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/nls.mk
---

## openssl-module.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2022-2023 Enéas Ulir de Queiroz
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/openssl-module.mk
---

## package-bin.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/package-bin.mk
---

## package-defaults.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/package-defaults.mk
---

## package-dumpinfo.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/package-dumpinfo.mk
---

## package-pack.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2022 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/package-pack.mk
---

## package-seccomp.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2015-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/package-seccomp.mk
---

## package.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/package.mk
---

## prereq-build.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/prereq-build.mk
---

## prereq.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/prereq.mk
---

## quilt.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/quilt.mk
---

## subdir.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/subdir.mk
---

## target.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2008 OpenWrt.org
Copyright (C) 2016 LEDE Project
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/target.mk
---

## toolchain-build.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2009-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/toolchain-build.mk
---

## toplevel.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2007-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/toplevel.mk
---

## unpack.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/unpack.mk
---

## verbose.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2006-2020 OpenWrt.org
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/verbose.mk
---

## version.mk

# Documentation
```text
SPDX-License-Identifier: GPL-2.0-only
Copyright (C) 2012-2015 OpenWrt.org
Copyright (C) 2016 LEDE Project
```


> Source: https://github.com/openwrt/openwrt/blob/master/include/version.mk
---

---

