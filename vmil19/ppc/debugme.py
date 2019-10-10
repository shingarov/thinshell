#
# python2 -m pudb.run debugme.py
#

import angr
p = angr.Project('/home/boris/work/thinshell/vmil19/ppc/jit')
nZone        = p.loader.main_object.get_symbol('nZoneBuffer').linked_addr
main         = p.loader.main_object.get_symbol('main').linked_addr
loadConstant = p.loader.main_object.get_symbol('loadConstant').linked_addr
generateLis  = p.loader.main_object.get_symbol('generateLis').linked_addr
call         = p.loader.main_object.get_symbol('call').linked_addr
#b = p.factory.block(p.entry)
s = p.factory.call_state(main)
s.regs.r3 = s.solver.BVS('x', 32, explicit_name=True)
# start executing main
s = p.factory.simulation_manager(s).step().active[0]
# now we are at the beginning of loadConstant()
s = p.factory.simulation_manager(s).step().active[0]
# generateLis()
s = p.factory.simulation_manager(s).step().active[0]
# just returned from generateLis()
lis = s.memory.load(nZone,4)
# let's run a few instructions before calling generateOri()
s = p.factory.simulation_manager(s).step().active[0]
# now we are at the beginning of generateOri()
s = p.factory.simulation_manager(s).step().active[0]
# just returned from generateOri()
ori = s.memory.load(nZone+4,4)
# epilogue of loadConstant()
s = p.factory.simulation_manager(s).step().active[0]
# ...and get into call()
s = p.factory.simulation_manager(s).step().active[0]

# now we are at the beginning of call()
# let's execute the bb containing the jump into nZone
s = p.factory.simulation_manager(s).step().active[0]

# we are in the nZone
assert(s.regs.pc.args[0] == nZone)

# Now execute the symbolic instructions
simgr = p.factory.simulation_manager(s)
# break in angr.engines.vex.engine.SimEngineVEX>>_process() to see cool things
ss = simgr.step()
jumpkind = ss.active[0].jumpkind
assert(jumpkind == 'Ijk_NoDecode')
