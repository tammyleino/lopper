# Simplified YAML

This document describes a YAML-based source representation for
DeviceTree which is an alternative to DeviceTree Source (DTS). It is
functionally equivalent to DTS and it comes with several simplifications
to make the source easier to read and to write.


## Basics

### Nodes, Properties, and Hierarchy

DeviceTree nodes are represented as YAML mappings. The content of the
mapping corresponds to the content of the DeviceTree node. The key of
the YAML mapping is the DeviceTree node label, or, if the label is not
present, the DeviceTree node name (the @address portion can be skipped).

When converting from YAML to DeviceTree Source, the node names are
generated from the YAML keys and compatible strings.

DeviceTree properties are expressed in YAML as unordered key: value
pairs. The difference between a node and a property in YAML is that a
node is a key: value pair with one or more key: value pairs as value.
A property is a single key: value pair, the value can be a scalar or a
sequence.

The DeviceTree hierarchy is preserved in YAML by using the appropriate
indentation.

### Example

#### YAML

~~~
  axi:
    compatible: simple-bus;

    can0:
      compatible: xlnx,zynq-can-1.0
      reg:
        - start: 0xff060000
          size: 0x1000
~~~

#### Device Tree

~~~
	axi {
		compatible = "simple-bus";

		can0: can@ff060000 {
			compatible = "xlnx,zynq-can-1.0";
			reg = <0x0 0xff060000 0x0 0x1000>;
		};
	};
~~~


## Simplifications

The Simplified YAML format comes with simplifications to make the source
easier to read and more intuitive to write. The simplifications are
described here with the description of how they can be translated back
to DeviceTree Source.

### Strings

Simplified YAML doesn't use quoted strings.

Example:
~~~
  compatible: openamp,domain-v1
~~~

### reg and other address ranges

List of address ranges, such as *reg*, are expressed as a YAML sequence
of key: value pairs, with *start* and *size* as keys. The *start* and
*size* scalars are as large as needed: they are not broken down into
32-bit cells.

Furthermore, addresses and sizes can also be expressed in human-readable
formats, e.g. 2M, 4G, 1T.

Example:
~~~
  reg:
    - start: 0xff060000
      size: 0x1000
    - start: 0x400000000
      size: 0x10000
    - start: 32G
      size: 1G
~~~

### \#address\_cells and \#size\_cells

\#address\_cells and \#size\_cells are not used in simplified YAML. When
converting Simplified YAML to DeviceTree Source, \#address\_cells and
\#size\_cells are generated as appropriate.

### \#interrup\_cells and others

#interrupt\_cells and other \*\_cells definitions are not used in
Simplified YAML. Instead, the value of the related property is expressed
as a sequence with a corresponding number of entries. If multiple sets
need to be described, a sequence of sequences is used.

Example:
~~~
    interrupts:
      - [0x1, 0xd, 0xf08]
      - [0x1, 0xe, 0xf08]
      - [0x1, 0xb, 0xf08]
      - [0x1, 0xa, 0xf08]
~~~

### Phandles

Phandles are not used in Simplified YAML. Instead, only references are
used. The \& is not used in Simplified YAML for references.

Example:
~~~
    interrupt-parent: interrupt-controller
~~~

### Boolean Properties

Boolean properties use true/false as value instead of 0x1/0x0.

Example:
~~~
    enabled: true
~~~


# Full Example
~~~
  compatible: xlnx,zynqmp-zcu102-rev1.0, xlnx,zynqmp-zcu102, xlnx,zynqmp
  model: ZynqMP ZCU102 Rev1.0

  cpus:
    cpu@0:
      compatible: arm,cortex-a53
      device_type: cpu
      enable-method: psci
      operating-points-v2: 0x1
      reg: 0x0
      cpu-idle-states: 0x2
      clocks: 0x3 0xa

    cpu@1:
      compatible: arm,cortex-a53
      device_type: cpu
      enable-method: psci
      reg: 0x1
      operating-points-v2: 0x1
      cpu-idle-states: 0x2

    cpu@2:
      compatible: arm,cortex-a53
      device_type: cpu
      enable-method: psci
      reg: 0x2
      operating-points-v2: 0x1
      cpu-idle-states: 0x2

    cpu@3:
      compatible: arm,cortex-a53
      device_type: cpu
      enable-method: psci
      reg: 0x3
      operating-points-v2: 0x1
      cpu-idle-states: 0x2

  timer:
    compatible: arm,armv8-timer
    interrupt-parent: interrupt-controller
    interrupts:
      - [0x1, 0xd, 0xf08]
      - [0x1, 0xe, 0xf08]
      - [0x1, 0xb, 0xf08]
      - [0x1, 0xa, 0xf08]

  axi:
    compatible: simple-bus
    ranges: true

    interrupt-controller:
      compatible: arm,gic-400
      reg:
        - start: 0xf9010000
          size: 0x10000
        - start: 0xf9020000
          size: 0x20000
        - start: 0xf9040000
          size: 0x20000
        - start: 0xf9060000
          size: 0x20000
      interrupt-parent: interrupt-controller
      interrupts: [0x1, 0x9, 0xf04]
      num_cpus: 0x2
      num_interrupts: 0x60

    can0:
      compatible: xlnx,zynq-can-1.0
      status: okay
      clock-names: can_clk, pclk
      reg:
        - start: 0xff060000
          size: 0x1000
      interrupts: [0x0, 0x17, 0x4]
      interrupt-parent: interrupt-controller
      tx-fifo-depth: 0x40
      rx-fifo-depth: 0x40

    ethernet0:
      compatible: cdns,zynqmp-gem, cdns,gem
      status: okay
      interrupt-parent: interrupt-controller
      interrupts:
        - [0x0 0x3f 0x4]
        - [0x0 0x3f 0x4]
      reg:
        - start: 0xff0e0000
          size: 0x1000
      phy-handle: 0x29
      pinctrl-names: default
      pinctrl-0: 0x2a
      phy-mode: rgmii-id
      xlnx,ptp-enet-clock: 0x0
      local-mac-address: [00, 0a, 35, 00, 22, 01]

      ethernet-phy:
        reg: 0xc
        ti,rx-internal-delay: 0x8
        ti,tx-internal-delay: 0xa
        ti,fifo-depth: 0x1
        ti,dp83867-rxctrl-strap-quirk
~~~
