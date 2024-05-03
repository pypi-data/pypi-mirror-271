#! /usr/bin/env python3

"""
A reference copy of this program is maintained at /GNAS/PROJ/PycharmProjects/libsrg/DiskInfo.py

Active copy is /GNAS/PROJ/PycharmProjects/ANS_PROJECT/scripts/DiskInfo.py

See also QT version at /GNAS/PROJ/PycharmProjects/ANS_PROJECT/scripts/DiskInfo.py
"""

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk
from typing import Optional

from libsrg.Runner import Runner
from libsrg.TKGUI.GuiBase import GuiBase
from libsrg.TKGUI.GuiRequest import GuiRequest
from libsrg.TKGUI.GuiRequestQueue import GuiRequestQueue


# class MyGui(GuiBase):


class AppControl:
    logger = logging.getLogger("AppControl")

    def __init__(self):
        self.zpool = None
        self.parser = None
        self.args = None
        self.thread = threading.Thread(target=self.body, daemon=True)
        self.guirequests = GuiRequestQueue.get_instance()
        ttl = "DiskInfo -- Clicking copies to clipboard, red items in zpool"
        self.gui = GuiBase(self, self.guirequests, width=1200, title=ttl)
        self.gui.takeover_main_thread()

    def extend_parser(self, parser):
        self.parser = parser
        self.logger.info("extending parser")

    def parsed_args(self, args):
        self.args = args

    def body(self):
        devpath = Path("/dev")
        byidpath = devpath / "disk" / "by-id"

        devset: set[Path] = set()
        idmap: dict[Path, Path] = {}
        wwnlist: list[Path] = []
        atalist: list[Path] = []

        dev2ata_map: dict[Path, Path] = {}
        dev2wwn_map: dict[Path, Path] = {}

        # scan the by-id folder, skipping xxx-partM names
        for idpath in byidpath.iterdir():
            name = str(idpath.name)
            if name.split("-")[-1].startswith("part"):
                continue
            if not idpath.is_symlink():
                continue
            if name.startswith("lvm-") or name.startswith("dm-"):
                continue
            linked = idpath.readlink()
            physpath = idpath.resolve()
            devset.add(physpath)
            idmap[idpath] = physpath
            if name.startswith("wwn"):
                wwnlist.append(idpath)
                dev2wwn_map[physpath] = idpath
            else:
                atalist.append(idpath)
                dev2ata_map[physpath] = idpath

        devlist = list(devset)
        devlist.sort()

        style_red = ttk.Style()
        sname = 'R.TButton'
        style_red.configure(sname, foreground='red')

        zp = Runner(["zpool", "status"])
        self.zpool = zp.so_lines
        if zp.success:
            self.logger.info(zp)
        else:
            self.logger.error(zp)

        row = 1
        h_hs = self.add_label_ask_gui("/dev/*", x=1, y=row)
        h_ata = self.add_label_ask_gui("/dev/disk/by-id/ata*", x=2, y=row)
        h_wwn = self.add_label_ask_gui("/dev/disk/by-id/wwn*", x=3, y=row)
        h_fmt = self.add_label_ask_gui("lsblk -f", x=4, y=row)

        for sd in devlist:
            row += 1
            l_sd = self.add_button_ask_gui(f"{sd.name}", x=1, y=row)
            l_ata = self.add_button_ask_gui("no ata", x=2, y=row)
            l_wwn = self.add_button_ask_gui("no wwn", x=3, y=row)
            l_part = self.add_button_ask_gui("part", x=4, y=row)
            if self.inzpool(sd.name):
                l_sd.configure(style=sname)

            ata = dev2ata_map.get(sd, None)
            if ata:
                l_ata['text'] = f"{ata.name}"
                if self.inzpool(ata.name):
                    l_ata.configure(style=sname)

            wwn = dev2wwn_map.get(sd, None)
            if wwn:
                l_wwn['text'] = f"{wwn.name}"
                if self.inzpool(wwn.name):
                    l_wwn.configure(style=sname)
            r = Runner(["lsblk", "-f", str(sd)])
            if r.success:
                l_part['text'] = "\n".join(r.so_lines)

    def copy_button(self, button):
        txt = button['text']
        self.gui.get_root().clipboard_clear()
        self.gui.get_root().clipboard_append(txt)

    def inzpool(self, disk):
        for line in self.zpool:
            if disk in line:
                return True
        return False

    def _add_button_as_gui(self, req: GuiRequest):
        # lab = ttk.Label(self.gui.get_root(), text=req.kwargs['txt'], anchor='w', relief=tk.RAISED, justify=tk.LEFT)
        but = ttk.Button(self.gui.get_root(), text=req.kwargs['txt'])
        # lab.pack(fill=tk.X)
        but.grid(column=req.kwargs['x'], row=req.kwargs['y'], sticky='NSEW', padx=3, pady=3)
        req.kwargs['label'] = but
        but.configure(command=lambda: self.copy_button(but))

    def add_button_ask_gui(self, msg: str, x: int, y: int) -> Optional[ttk.Button]:
        self.guirequests.register_callback("add_button", self._add_button_as_gui)

        self.logger.info(f"msg={msg}")
        qreq = GuiRequest("add_button", txt=msg, x=x, y=y)
        res = self.guirequests.client_one_request(qreq)
        if res:
            return qreq.kwargs['label']
        else:
            return None

    def _add_label_as_gui(self, req: GuiRequest):
        lab = ttk.Label(self.gui.get_root(), text=req.kwargs['txt'], anchor='w', relief=tk.RAISED, justify=tk.LEFT)
        # but = ttk.Button(self.gui.get_root(), text=req.kwargs['txt'])
        # lab.pack(fill=tk.X)
        lab.grid(column=req.kwargs['x'], row=req.kwargs['y'], sticky='NSEW', padx=3, pady=3)
        lab.configure(background='black', foreground='cyan')
        req.kwargs['label'] = lab

    def add_label_ask_gui(self, msg: str, x: int, y: int) -> Optional[ttk.Label]:
        self.guirequests.register_callback("add_label", self._add_label_as_gui)

        self.logger.info(f"msg={msg}")
        qreq = GuiRequest("add_label", txt=msg, x=x, y=y)
        res = self.guirequests.client_one_request(qreq)
        if res:
            return qreq.kwargs['label']
        else:
            return None


if __name__ == '__main__':
    appcontrol = AppControl()
