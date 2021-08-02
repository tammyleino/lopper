# /*
# * Copyright (c) 2021 Xilinx Inc. All rights reserved.
# *
# * Author:
# *       Izhar Shaikh <izhar.ameer.shaikh@xilinx.com>
# *
# * SPDX-License-Identifier: BSD-3-Clause
# */

import xppu
import cdogen
from lopper import Lopper
import lopper
from lopper_tree import *
from xlnx_versal_power import xlnx_pm_devid_to_name, xlnx_pm_devname_to_id

sys.path.append(os.path.dirname(__file__))

class MidEntry:
    def __init__(self, smid, mask, name=''):
        self.name = name
        self.smid = smid
        self.mask = mask

    def __str__(self):
        return "{0}/{1}".format(
            hex(self.smid),
            hex(self.mask))

class FirewallTableEntry:
    def __init__(self,
                 subsystem_id: int,
                 base_addr: int,
                 size: int,
                 rw: int,
                 tz: int,
                 mid_list: [[MidEntry]],    # [[name, smid, mask], ...]
                 module_tag: str,
                 pm_tag='',
                 priority=10):
        self.subsystem_id = subsystem_id
        self.base_addr = base_addr
        self.size = size
        self.rw = rw
        self.tz = tz
        self.mid_list = mid_list
        self.module_tag = module_tag
        self.pm_tag = pm_tag
        self.priority = priority

    def __str__(self):
        printstr = "{0} {1:10} {2:8} {3} {4} {5} {6:15}".format(
            hex(self.subsystem_id), hex(self.base_addr),
            hex(int(self.size)) if self.size != "*" else self.size,
            self.rw, self.tz, self.priority, self.pm_tag)
        for m in self.mid_list:
            printstr += " " + m.__str__()
        return printstr

    def print_entry(self, fp=None):
        print("{0:10}\t{1:10}\t{2:8}\t{3:1}\t{4:1}\t{5:2}\t"
              .format(hex(self.subsystem_id),
                      hex(self.base_addr),
                      hex(int(self.size)) if self.size != "*" else self.size,
                      self.rw,
                      self.tz,
                      self.priority),
              end='',
              file=fp)
        print(" ".join(m.__str__() for m in self.mid_list), file=fp)

