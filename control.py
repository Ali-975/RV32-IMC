from amaranth import *

class control(Elaboratable):
    def __init__(self):

        self.instr = Signal(32)
        self.funct3 = Signal(3)
        self.funct7 = Signal()
        self.rs1 = Signal(32)
        self.rs2 = Signal(32)
        self.rd = Signal(32)
        self.op = Signal(7)
        self.wen = Signal()
        self.alu_op = Signal(4)

        self.iimm = Signal(12)
        self.simm = Signal(12)
        self.simm1 = Signal(5)
        self.simm2 = Signal(7)

        self.op_b_sel = Signal()


    def elaborate(self, platform):
        m = Module()

        # funct3 = Signal(3)
        # funct7 = Signal()
        # rs1 = Signal(32)
        # rs2 = Signal(32)
        # rd = Signal(32)
        # op = Signal(7)
        # wen = Signal()

        # iimm = Signal(12)
        # simm = Signal(12)
        # simm1 = Signal(5)
        # simm2 = Signal(7)


        m.d.sync += [
            self.op.eq (self.instr[0:]),
            self.rd.eq (self.instr[7:]),
            self.funct3.eq (self.instr[12:]),
            self.rs1.eq (self.instr[15:]),
            self.rs2.eq (self.instr[20:]),
            self.funct7.eq (self.instr[31]),

            self.iimm.eq (self.instr[20:]),

            self.simm1.eq (self.instr[7:]),
            self.simm2.eq (self.instr[25:]),
            self.simm.eq (Cat(self.simm1, self.simm2)),

            self.alu_op.eq (Cat(self.funct7, self.funct3)),

        ]


        with m.Switch(self.op):
            with m.Case(0b0110011):

                m.d.sync += [
                    #self.type.eq("R"),

                    self.wen.eq(1),
                    self.op_b_sel.eq(0)
                ]

            with m.Case(0b0010011):

                m.d.sync += [
                    #self.type.eq("I"),

                    self.wen.eq(1),
                    self.op_b_sel.eq(1)      
                ]
            with m.Case(0b0100011):

                m.d.sync += [
                    #self.type.eq("S"),

                    self.wen.eq(0),
                    self.op_b_sel.eq(1)
                ]

        return m


from amaranth.sim import Simulator

dut = control()
def bench():
    for i in range(0xf1):
        yield dut.instr.eq(i)
        yield dut.op
        #(yield dut.op.eq(dut.instr[0:2]))
        #(yield dut.op)
        yield
        yield
        yield
        yield


sim = Simulator(dut)
sim.add_clock(1e-6) # 1 MHz
sim.add_sync_process(bench)
with sim.write_vcd("control.vcd"):
    sim.run()

from amaranth.back import verilog


top = control()
with open("control.v", "w") as f:
    f.write(verilog.convert(top, ports=[top.instr, top.op]))