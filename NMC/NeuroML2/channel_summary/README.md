Channel information
===================
    
<p style="font-family:arial">Channel information at: T = 22.0 degC, E_rev = 0 mV, [Ca2+] = 0.00043 mM</p>

<table>
    <tr>
<td width="120px">
            <sup><b>NaTa_t</b><br/>
            <a href="../NaTa_t.channel.nml">NaTa_t.channel.nml</a><br/>
            <b>Ion: na</b><br/>
            <i>g = gmax * m<sup>3</sup> * h </i><br/>
            Fast inactivating Na+ current
            
Comment from original mod file: 
:Reference :Colbert and Pan 2002</sup>
</td>
<td>
<a href="NaTa_t.inf.png"><img alt="NaTa_t steady state" src="NaTa_t.inf.png" height="220"/></a>
</td>
<td>
<a href="NaTa_t.tau.png"><img alt="NaTa_t time course" src="NaTa_t.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Nap_Et2</b><br/>
            <a href="../Nap_Et2.channel.nml">Nap_Et2.channel.nml</a><br/>
            <b>Ion: na</b><br/>
            <i>g = gmax * m<sup>3</sup> * h </i><br/>
            Persistent Na+ current
            
Comment from original mod file: 
:Comment : mtau deduced from text (said to be 6 times faster than for NaTa)
:Comment : so I used the equations from NaT and multiplied by 6
:Reference : Modeled according to kinetics derived from Magistretti and Alonso 1999
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="Nap_Et2.inf.png"><img alt="Nap_Et2 steady state" src="Nap_Et2.inf.png" height="220"/></a>
</td>
<td>
<a href="Nap_Et2.tau.png"><img alt="Nap_Et2 time course" src="Nap_Et2.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>NaTs2_t</b><br/>
            <a href="../NaTs2_t.channel.nml">NaTs2_t.channel.nml</a><br/>
            <b>Ion: na</b><br/>
            <i>g = gmax * m<sup>3</sup> * h </i><br/>
            Fast inactivating Na+ current. Comment from mod file (NaTs2_t.mod): took the NaTa and shifted both activation/inactivation by 6 mv</sup>
</td>
<td>
<a href="NaTs2_t.inf.png"><img alt="NaTs2_t steady state" src="NaTs2_t.inf.png" height="220"/></a>
</td>
<td>
<a href="NaTs2_t.tau.png"><img alt="NaTs2_t time course" src="NaTs2_t.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>K_Tst</b><br/>
            <a href="../K_Tst.channel.nml">K_Tst.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m<sup>4</sup> * h </i><br/>
            Fast inactivating K+ current
            
Comment from original mod file: 
:Comment : The transient component of the K current
:Reference : :		Voltage-gated K+ channels in layer 5 neocortical pyramidal neurones from young rats:subtypes and gradients,Korngreen and Sakmann, J. Physiology, 2000
:Comment : shifted -10 mv to correct for junction potential
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="K_Tst.inf.png"><img alt="K_Tst steady state" src="K_Tst.inf.png" height="220"/></a>
</td>
<td>
<a href="K_Tst.tau.png"><img alt="K_Tst time course" src="K_Tst.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>K_Pst</b><br/>
            <a href="../K_Pst.channel.nml">K_Pst.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m<sup>2</sup> * h </i><br/>
            Slow inactivating K+ current
            
Comment from original mod file: 
:Comment : The persistent component of the K current
:Reference : :		Voltage-gated K+ channels in layer 5 neocortical pyramidal neurones from young rats:subtypes and gradients,Korngreen and Sakmann, J. Physiology, 2000
:Comment : shifted -10 mv to correct for junction potential
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="K_Pst.inf.png"><img alt="K_Pst steady state" src="K_Pst.inf.png" height="220"/></a>
</td>
<td>
<a href="K_Pst.tau.png"><img alt="K_Pst time course" src="K_Pst.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>SKv3_1</b><br/>
            <a href="../SKv3_1.channel.nml">SKv3_1.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m </i><br/>
            Fast, non inactivating K+ current
            
Comment from original mod file: 
:Reference : :		Characterization of a Shaw-related potassium channel family in rat brain, The EMBO Journal, vol.11, no.7,2473-2486 (1992)</sup>
</td>
<td>
<a href="SKv3_1.inf.png"><img alt="SKv3_1 steady state" src="SKv3_1.inf.png" height="220"/></a>
</td>
<td>
<a href="SKv3_1.tau.png"><img alt="SKv3_1 time course" src="SKv3_1.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>SK_E2</b><br/>
            <a href="../SK_E2.channel.nml">SK_E2.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * z </i><br/>
            Small-conductance, Ca2+ activated K+ current
            
Comment from original mod file: 
: SK-type calcium-activated potassium current
: Reference : Kohler et al. 1996</sup>
</td>
<td>
<a href="SK_E2.inf.png"><img alt="SK_E2 steady state" src="SK_E2.inf.png" height="220"/></a>
</td>
<td>
<a href="SK_E2.tau.png"><img alt="SK_E2 time course" src="SK_E2.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Ca_LVAst</b><br/>
            <a href="../Ca_LVAst.channel.nml">Ca_LVAst.channel.nml</a><br/>
            <b>Ion: ca</b><br/>
            <i>g = gmax * m<sup>2</sup> * h </i><br/>
            Low voltage activated Ca2+ current
            
Comment from original mod file: 
Note: mtau is an approximation from the plots
:Reference : :		Avery and Johnston 1996, tau from Randall 1997
:Comment: shifted by -10 mv to correct for junction potential
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="Ca_LVAst.inf.png"><img alt="Ca_LVAst steady state" src="Ca_LVAst.inf.png" height="220"/></a>
</td>
<td>
<a href="Ca_LVAst.tau.png"><img alt="Ca_LVAst time course" src="Ca_LVAst.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Ca_HVA</b><br/>
            <a href="../Ca_HVA.channel.nml">Ca_HVA.channel.nml</a><br/>
            <b>Ion: ca</b><br/>
            <i>g = gmax * m<sup>2</sup> * h </i><br/>
            High voltage activated Ca2+ current. 
            
Comment from original mod file: 
Reuveni, Friedman, Amitai, and Gutnick, J.Neurosci. 1993</sup>
</td>
<td>
<a href="Ca_HVA.inf.png"><img alt="Ca_HVA steady state" src="Ca_HVA.inf.png" height="220"/></a>
</td>
<td>
<a href="Ca_HVA.tau.png"><img alt="Ca_HVA time course" src="Ca_HVA.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Ih</b><br/>
            <a href="../Ih.channel.nml">Ih.channel.nml</a><br/>
            <b>Ion: hcn</b><br/>
            <i>g = gmax * m </i><br/>
            Non-specific cation current
            
Comment from original mod file: 
Reference : :		Kole,Hallermann,and Stuart, J. Neurosci. 2006</sup>
</td>
<td>
<a href="Ih.inf.png"><img alt="Ih steady state" src="Ih.inf.png" height="220"/></a>
</td>
<td>
<a href="Ih.tau.png"><img alt="Ih time course" src="Ih.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>KdShu2007</b><br/>
            <a href="../KdShu2007.channel.nml">KdShu2007.channel.nml</a><br/>
            <b>Ion: kdshu</b><br/>
            <i>g = gmax * m * h </i><br/>
            K-D current for prefrontal cortical neuron - Yuguo Yu 2007</sup>
</td>
<td>
<a href="KdShu2007.inf.png"><img alt="KdShu2007 steady state" src="KdShu2007.inf.png" height="220"/></a>
</td>
<td>
<a href="KdShu2007.tau.png"><img alt="KdShu2007 time course" src="KdShu2007.tau.png" height="220"/></a>
</td>
</tr>
</table>

