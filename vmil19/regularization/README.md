# VEX regularization
Here is a little experiment with vex regularization.

In Pharo-ArchC and related fundamental parts of Smalltalk-25,
we call things of the form (using PPC example here)
```
    addis RT, RA, D
```
_instruction declarations_, and things of the form
```
    addis r3, r1, 0x1234
```
_ground instruction instances_.

We say that two VEX IRSBs _have the same shape_ if they only differ
in the leaf constants.  This means, the `U16`/`U32`/etc constants in `Const`
expressions, but also things like register offsets in `GET` and `PUT`
(because, say, when _RA_ varies those will vary too).  This has the
disadvantage that special offsets like PC=1168 on PPC, are not recognized
as special; cf. criticism of ARM uniform SPRs in Waterman's thesis.

Of course, two IRSBs of different shapes can still denote the same
function; in this sense shape is not a hash for homotopy.

An instruction is called _vex-regular_ if all its ground instances
lift to VEX of the same shape.  For example, `bla` on PPC is regular.
However, `addis` is irregular, because in the special case of _RA_=0
VEX short-circuits the `Add32` binop.

Therefore, the equality ralation on vex shapes classifies the total
space of instances into disjoint shape classes.  The function
```
vexshape.shape_specimens(spec, arch)
```
computes a section of the total instance-encoding space:  out of each
shape class, it picks one representative.  It returns the list of these
representatives.

Note how different ISAs differ in terminology regarding what is an
instruction, a page, or an extended mnemonic -- and how ArchC reflects
these differences.  Take the branch instruction as an example.  The PPC
"Branch I-Form" instructions (`b`, `ba`, `bl`, `bla`) form a single
`# Branch` page but are considered separate instructions -- the `LK` and
'AA' bits are part of the decoder; this is especially evident in the
ArchC model.  Contrast this with the `H` bit in ARM `b` instruction:
`b` and `bl` are considered extended mnemonics of the same `b` instruction.
One can think of editing the ISA to split `b` and `bl` into separate
instructions.  If one goes on far enough, one can arrive at an ISA
formulation where all instructions are vex-regular.  We call this process
_vex-regularization_.  Obviously, decoder functions in this regularized
ISA will not be nicely aligned along the bit boundaries; instruction
decode will include some _guard predicates_, e.g. PPC `addis` above will
have guards _RA_==0, _RA_!=0.

