---
title: 'OpenWrt Buildroot: utils packages'
module: openwrt-core
origin_type: makefile_meta
token_count: 4642
version: unknown
source_file: L1-raw/openwrt-core/makefile_meta-category-utils.md
last_pipeline_run: '2026-03-08T11:43:24.421257+00:00'
upstream_path: package/utils
language: makefile
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
