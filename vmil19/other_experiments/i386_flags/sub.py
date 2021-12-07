import os
import angr

import pudb ; pu.db

p = angr.Project('sub')
start = p.loader.main_object.get_symbol('_start').linked_addr
#b = p.factory.block(p.entry)
state0 = p.factory.call_state(start)
x = state0.solver.BVS('x', 32, explicit_name=True)
state0.regs.eax = x

state1 = p.factory.simulation_manager(state0).step(num_inst=1)

state2 = p.factory.simulation_manager(state1.active[0]).step(num_inst=1)

print(state2.active[0].regs.eip)
print(state2.active[0].solver.eval(x))

print(state2.active[1].regs.eip)
print(state2.active[1].solver.eval(x))
