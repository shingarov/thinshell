#
# python2 -m pudb.run debugme.py
#

import angr
p = angr.Project('/home/boris/work/thinshell/vmil19/ppc/jit')
#b = p.factory.block(p.entry)
state = p.factory.entry_state()
simgr = p.factory.simulation_manager(state)
s = simgr.step(num_inst = 1)
