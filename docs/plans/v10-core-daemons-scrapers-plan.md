# openwrt-docs4ai: Core Daemons High-Level Scraping Plan

## Overview
OpenWrt's core daemons (`procd`, `netifd`, `ubus`) are written in C, but **app developers almost never interact with the C code.** They interface with these daemons via:
1. Shell script helper libraries (`procd.sh`)
2. Structured configuration schemas (`/etc/config/xyz`)
3. Environment variables passed during events (`hotplug.d`)

To provide LLMs with perfect app-developer context without drowning them in millions of lines of irrelevant C codebase compilation details, we must perform **precision extraction** targeting the shell wrappers and schema defaults located inside the main `openwrt/openwrt` repository.

---

## 1. `procd` (Process Manager & Init Scripts)

When a developer asks "How do I make my script start on boot and restart if it crashes?", they need the `procd.sh` helper API.

**Target File in Repository:**  
`package/system/procd/files/procd.sh`  
`package/base-files/files/etc/rc.common`

**Extraction Strategy:**  
Instead of parsing the C repository for `procd`, we write a python scraper `02f-scrape-procd-api.py` that targets those two shell files in the cloned `openwrt/openwrt` repo. 
* **Regex Filter:** We extract block comments and function signatures matching `procd_open_instance`, `procd_set_param`, `procd_close_instance`, `procd_add_reload_trigger`, etc.
* **Output:** A single heavily condensed markdown file `procd-api.md` containing just the shell functions a developer is allowed to call inside an `/etc/init.d/` script, plus their expected arguments.

---

## 2. UCI (Unified Configuration Interface) Schemas

When a developer asks "How do I add a new WiFi network via command line?", the LLM needs to know the exact fields of the `/etc/config/wireless` file.

**Target Files in Repository:**  
`package/base-files/files/etc/config/*` (network, system, dhcp, firewall, etc.)

**Extraction Strategy:**  
We write a python scraper `02g-scrape-uci-schemas.py` that simply copies all the default configuration config files located inside the base-files folder of the openwrt source tree.
* **Filter:** Strip out all bash scripting and isolate just the `config type 'name'` and `option key 'value'` blocks.
* **Output:** A single `uci-default-schemas.md` file. Because default config files are highly readable, giving an LLM the raw concatenated defaults for `network`, `firewall`, and `wireless` instantly teaches it the entire OpenWrt configuration schema system with zero C-code required.

---

## 3. `netifd` (Network Interfaces & Hotplug Events)

When a developer asks "How do I run a script automatically when the VPN wireguard tunnel goes up?", they need `hotplug.d` and `netifd` environmental variables.

**Target Files in Repository:**  
`package/network/config/netifd/files/*`  
`package/base-files/files/etc/hotplug.d/*`

**Extraction Strategy:**  
We write a python scraper `02h-scrape-hotplug-events.py`.
* **Knowledge Goal:** The LLM needs to know that when an event happens, OpenWrt injects `$ACTION` and `$INTERFACE` variables into the environment of the scripts. 
* **Filter:** We regex scan the `hotplug.d` default scripts in the repo to catalog the standard environmental variables and case-switch structures used by OpenWrt to handle interfaces, tracking the `ifup` and `ifdown` patterns.
* **Output:** A `netifd-hotplug-events.md` guide.

---

## 4. `ubus` (Inter-process RPC)

**The Challenge:** `ubus` namespaces and methods (e.g., `network.interface.wan status`) are strictly generated dynamically at runtime by whatever packages happen to be installed on the router. They do not exist as static files in the GitHub repository.

**Extraction Strategy:**  
We **cannot** easily scrape this from the GitHub repository without building a complex C-parser that searches for `UBUS_METHOD(` declarations across 100 different folders. 
* **The Solution:** The OpenWrt Wiki scraper (`02a`) already pulls the "Ubus" developer guide. We should update the Wiki scraper's routing hints (part of the synergy roadmap) to ensure the LLM prioritizes reading the `openwrt-wiki-docs/Ubus.md` page whenever a developer asks about Inter-Process Communication (IPC). If we need deeper runtime `ubus` schemas, they should be generated on a live router via `ubus -v list` and committed to this repo manually, rather than scraped via GitHub Actions.
