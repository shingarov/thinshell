#
# python2 -m pudb.run highlevel_ppcjump.py
#

import angr
p = angr.Project('/home/boris/work/thinshell/ppc_jmp')
#b = p.factory.block(p.entry)
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
s = simgr.step(num_inst = 1)

