#Project: SDB: FPGA ROM Generator and Parser

##Goal: Tool to Generate/Parse SDB ROM

##Problem:

In order to interact with FPGAs software developers must have knowledge of both the internal organization of the FPGA code as well as information such as the individual cores size and version number. SDB is a protocol developed by CERN to answer this problem.

A more detailed description of the SDB protocol can be found here:
http://www.ohwr.org/projects/sdb/wiki

##Description

SDB Parser/Generator is a tool used to both generate and parse SDB ROMs.

For reference a parsed SDB output can look something like this:

SDB
Bus: top        @ 0x0000000000000000 : Size: 0x200000000
Number of components: 2
   Bus: peripheral @ 0x0000000000000000 : Size: 0x03000000
   Number of components: 3
     SDB                  Type (Major:Minor) (01:00): SDB
     Address:        0x0000000000000000-0x0000000000000380 : Size: 0x00000380
     Vendor:Product: 8000000000000000:00000000

     uart1                Type (Major:Minor) (03:01): UART
     Address:        0x0000000001000000-0x0000000001000008 : Size: 0x00000008
     Vendor:Product: 800000000000C594:00000003

     gpio1                Type (Major:Minor) (02:01): GPIO
     Address:        0x0000000002000000-0x0000000002000008 : Size: 0x00000008
     Vendor:Product: 800000000000C594:00000002

   Bus: memory     @ 0x0000000100000000 : Size: 0x00800000
   Number of components: 1
     mem1                 Type (Major:Minor) (06:02): Memory
     Address:        0x0000000000000000-0x0000000000800000 : Size: 0x00800000
     Vendor:Product: 800000000000C594:00000000

This describes an internal structure of an FPGA with a main bus called 'top' and two sub busses called 'peripheral' and 'memory'. The peripheral bus contains 3 components. The information for each of the entries defines the address range and size. Some of the entries contain other information such as 'Major' and 'Minor' types which, for a 'Nysa' implementation is used to identify the type of device. This is not explicitly defined by SDB at the moment.

SDB will generate a ROM that is downloaded to the FPGA. For reference the ROM looks like the following (with comments added)

//Bus (top bus)
5344422D 00020100 00000000 00000000
00000002 00000000 80000000 0000C594
00000001 00000001 140F0C09 746F7000
00000000 00000000 00000000 00000000

//Bridge (Pointer to a Sub Bus 'peripheral')
00000000 00000020 00000000 00000000
00000000 03000000 80000000 0000C594
00000001 00000001 140F0C09 70657269
70686572 616C0000 00000000 00000002

//Bridge (Pointer to a Sub Bus 'memory')
00000000 00000048 00000001 00000000
00000001 00800000 80000000 0000C594
00000001 00000001 140F0C09 6D656D6F
72790000 00000000 00000000 00000002

//Empty (Used to indicate the end of a bus entry)
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 000000FF

//Bus (perpheral)
5344422D 00030100 00000000 00000000
00000000 03000000 80000000 0000C594
00000001 00000001 140F0C09 70657269
70686572 616C0000 00000000 00000000

//Device (SDB)
00000100 00000207 00000000 00000000
00000000 00000380 80000000 00000000
00000000 00000001 140F0C09 53444200
00000000 00000000 00000000 00000001

//Device (UART)
00000201 00000207 00000000 01000000
00000000 01000008 80000000 0000C594
00000002 00000001 140F0107 6770696F
31000000 00000000 00000000 00000001

//Device (GPIO)
00000C01 00000207 00000000 02000000
00000000 02000008 80000000 0000C594
0000000A 00000001 140F0107 69327300
00000000 00000000 00000000 00000001

//Empty (Used to indicate the end of a bus entry)
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 000000FF

//Bus (memory)
5344422D 00010100 00000001 00000000
00000001 00800000 80000000 0000C594
00000001 00000001 140F0C09 6D656D6F
72790000 00000000 00000000 00000000

//Device (Memory Device)
00000602 00000207 00000000 00000000
00000000 00800000 80000000 0000C594
00000000 00000001 140F0107 6D656D31
00000000 00000000 00000000 00000001

//Empty (Used to indicate the end of a bus entry)
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 000000FF



