# Put an "import pudb; pu.db" in SimIRExpr_Op and just run this

import angr, claripy

p = angr.Project('/Users/boris/lamya/ppc_addi')
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
state.regs.r3 = claripy.BVS('xxx', 32, explicit_name=True);
s = simgr.step(num_inst = 1)

