---
title: 'OpenWrt Buildroot: system packages'
module: openwrt-core
origin_type: makefile_meta
token_count: 1611
version: unknown
source_file: L1-raw/openwrt-core/makefile_meta-category-system.md
last_pipeline_run: '2026-03-08T11:43:24.421257+00:00'
upstream_path: package/system
language: makefile
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
