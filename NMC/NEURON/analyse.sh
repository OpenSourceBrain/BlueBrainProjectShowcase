#Ca.mod CaDynamics_E2.mod Ca_LVAst.mod Ih.mod Im.mod K_Pst.mod K_Tst.mod KdShu2007.mod NaTa_t.mod NaTs2_t.mod Nap_Et2.mod SK_E2.mod SKv3_1.mod

# pynml-modchananalysis Im -stepV 5 # Small tau -> requires small dt...
pynml-modchananalysis Ih -stepV 5 -temperature 22 -nogui

pynml-modchananalysis K_Tst -stepV 5 -temperature 22 -nogui
pynml-modchananalysis K_Pst -stepV 5 -temperature 22 -nogui
pynml-modchananalysis KdShu2007 -stepV 5 -temperature 22 -nogui

pynml-modchananalysis NaTa_t -stepV 5 -temperature 22 -nogui
pynml-modchananalysis Nap_Et2 -stepV 5 -temperature 22 -nogui
pynml-modchananalysis NaTs2_t -stepV 5 -temperature 22 -nogui

pynml-modchananalysis Ca_HVA -stepV 5 -temperature 22 -nogui
pynml-modchananalysis Ca_LVAst -stepV 5 -temperature 22 -nogui

pynml-modchananalysis SKv3_1 -stepV 5 -temperature 22 -nogui
# pynml-modchananalysis SK_E2 -stepV 5 # Constant tau...?



