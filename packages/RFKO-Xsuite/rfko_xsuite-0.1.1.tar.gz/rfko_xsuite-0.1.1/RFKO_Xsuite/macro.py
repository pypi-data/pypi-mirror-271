



def macro_def(mad):


    mad.input('''ptc_twiss_macro(order, dp, slice_flag): macro = {
      ptc_create_universe;
      ptc_create_layout, time=false, model=2, exact=true, method=6, nst=3;
      IF (slice_flag == 1){
        select, flag=ptc_twiss, clear;
        select, flag=ptc_twiss, column=name,keyword,s,l,x,px,beta11,beta22,disp1,k1l;
        ptc_twiss, closed_orbit, icase=56, no=order, deltap=dp, table=ptc_twiss, summary_table=ptc_twiss_summary, slice_magnets=true;
      }
      ELSE{
        select, flag=ptc_twiss, clear;
        select, flag=ptc_twiss, column=name,keyword,s,x,px,beta11,alfa11,beta22,alfa22,disp1,disp2,mu1,mu2,energy,l,angle,K1L,K2L,K3L,HKICK,SLOT_ID;    
        ptc_twiss, closed_orbit, icase=56, no=order, deltap=dp, table=ptc_twiss, summary_table=ptc_twiss_summary, normal;
      }
      ptc_end;
    };

    ''')

    mad.input(''' 
    write_ptc_twiss(filename) : macro = {
        write, table=ptc_twiss, file=filename;
    };
    ''')

    mad.input('''match_tunes(qx, qy, dqx, dqy) : macro = {

      match, sequence=ps;
              vary, name = kf, step=0.00001;
              vary, name = kd, step=0.00001;
              constraint, range = #E, mux = qx + dqx, muy = qy + dqy;
      jacobian,calls=50000,bisec=3, tolerance = 1E-20;
      ENDMATCH;

    };

    ''')

    mad.input('''tunes_leq_knob(): macro = {

      kf := kf_0 + dkf_x * qx_leq + dkf_y * qy_leq;
      kd := kd_0 + dkd_x * qx_leq + dkd_y * qy_leq;

    };

    ''')

    mad.input('''tunes_leq_knob_factors(qx0, qy0): macro = {

      kf_0 = kf; 
      kd_0 = kd;

      dq = 1E-2;

      qx0 = qx0 ; ! lef out a +6
      qy0 = qy0 ; ! lef out a +6 because in the code  it is actually already there

      exec, match_tunes(qx0, qy0, 0, 0);

      kf_1 = kf; 
      kd_1 = kd;

      exec, match_tunes(qx0, qy0, dq, 0);

      dkf_x = (kf - kf_1) / dq;
      dkd_x = (kd - kd_1) / dq;

      exec, match_tunes(qx0, qy0, 0, dq);

      dkf_y = (kf - kf_1) / dq;
      dkd_y = (kd - kd_1) / dq;  

      qx_leq = 0;
      qy_leq = 0;

      exec, tunes_leq_knob;

    };
    ''')

    mad.input('''write_str_file(filename): macro = {
      assign, echo = filename;
      print, text = "/**********************************************************************************";
      print, text = "*                             SBENDs and MULTIPOLES in MUs";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, k1PRBHF, k1PRBHD, k2PRBHF, k2PRBHD, k2PRMP, k2PRMPJ, k3PRMPF, k3PRMPD;
      print, text = "";
      print, text = "/**********************************************************************************";
      print, text = "*                                    PFW and F8L";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, k1PRPFWF, k1PRPFWD, k2PRPFWF, k2PRPFWD, k3PRPFWF, k3PRPFWD, k1PRF8L;
      print, text = "";
      print, text = "/**********************************************************************************";
      print, text = "*                                    Injection dipoles";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, kPIBSW26;
      value, kPIBSW40, kPIBSW41, kPIBSW42, kPIBSW43, kPIBSW44;
      print, text = "";
      print, text = "/**********************************************************************************";
      print, text = "*                                    Extraction dipoles";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, kPEBSW12, kPEBSW14, kPEBSW20, kPEBSW22;
      value, kPEBSW23, kPEBSW57;
      print, text = ""; 
      print, text = "/**********************************************************************************";
      print, text = "*                                      Quadrupoles";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, kF, kD, kPRQSE, kPEQKE16, kPIQLB;
      print, text = "";
      print, text = "/**********************************************************************************";
      print, text = "*                                       Sextupoles";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, kPRXNO39, kPRXNO55, kPRXNO, kPRXSE;
      print, text = "";
      print, text = "/**********************************************************************************";
      print, text = "*                                       Octupoles";
      print, text = "***********************************************************************************/";
      print, text = "";
      value, kPRONO39, kPRONO55, kPRODN;
      print, text = "";
      print, text = "/**********************************************************************************";
      print, text = "*                                   KNOBS";
      print, text = "***********************************************************************************/";
      IF (dkPIBSW40_x <> 0.) {
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Proton injection bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = "";  
        print, text = "bsw42_x_mm_abs_active  =              1 ;";         
        printf, text = "bsw42_x_mm_abs     = %F ;", value = x0*1e3;
        print, text = "bsw42_x_mm         =       0.0000000000 ;";
        print, text = "bsw42_px_mrad      =       0.0000000000 ;";
        print,  text = "";      

        IF (second_injection == 1){
          printf, text = "bsw42.2_x_mm_abs   = %F ;", value = x0*1e3;
          print, text = "bsw42.2_x_mm       =       0.0000000000 ;";
          print, text = "bsw42.2_px_mrad    =       0.0000000000 ;";
          print,  text = "";  
        }

        printf, text = "dkPIBSW40_x_abs    = %F ;", value = dkPIBSW40_x_abs;
        printf, text = "dkPIBSW41_x_abs    = %F ;", value = dkPIBSW41_x_abs;
        printf, text = "dkPIBSW42_x_abs    = %F ;", value = dkPIBSW42_x_abs;
        printf, text = "dkPIBSW43_x_abs    = %F ;", value = dkPIBSW43_x_abs;
        printf, text = "dkPIBSW44_x_abs    = %F ;", value = dkPIBSW44_x_abs;
        print,  text = "";      
        printf, text = "dkPIBSW40_x        = %F ;", value = dkPIBSW40_x;
        printf, text = "dkPIBSW41_x        = %F ;", value = dkPIBSW41_x;
        printf, text = "dkPIBSW42_x        = %F ;", value = dkPIBSW42_x;
        printf, text = "dkPIBSW43_x        = %F ;", value = dkPIBSW43_x;
        printf, text = "dkPIBSW44_x        = %F ;", value = dkPIBSW44_x;
        print,  text = "";      
        printf, text = "dkPIBSW40_px       = %F ;", value = dkPIBSW40_px;
        printf, text = "dkPIBSW41_px       = %F ;", value = dkPIBSW41_px;
        printf, text = "dkPIBSW42_px       = %F ;", value = dkPIBSW42_px;
        printf, text = "dkPIBSW43_px       = %F ;", value = dkPIBSW43_px;
        printf, text = "dkPIBSW44_px       = %F ;", value = dkPIBSW44_px;
        print,  text = "";      
        print, text = "kPIBSW40 := dkPIBSW40_x_abs * bsw42_x_mm_abs + dkPIBSW40_x * bsw42_x_mm + dkPIBSW40_px * bsw42_px_mrad;";
        print, text = "kPIBSW41 := dkPIBSW41_x_abs * bsw42_x_mm_abs + dkPIBSW41_x * bsw42_x_mm + dkPIBSW41_px * bsw42_px_mrad;";
        print, text = "kPIBSW42 := dkPIBSW42_x_abs * bsw42_x_mm_abs + dkPIBSW42_x * bsw42_x_mm + dkPIBSW42_px * bsw42_px_mrad;";
        print, text = "kPIBSW43 := dkPIBSW43_x_abs * bsw42_x_mm_abs + dkPIBSW43_x * bsw42_x_mm + dkPIBSW43_px * bsw42_px_mrad;";
        print, text = "kPIBSW44 := dkPIBSW44_x_abs * bsw42_x_mm_abs + dkPIBSW44_x * bsw42_x_mm + dkPIBSW44_px * bsw42_px_mrad;";
        print,  text = "";  

        IF (second_injection == 1){

          print, text = "kPI2BSW40 := dkPIBSW40_x_abs * bsw42.2_x_mm_abs + dkPIBSW40_x * bsw42.2_x_mm + dkPIBSW40_px * bsw42.2_px_mrad;";
          print, text = "kPI2BSW41 := dkPIBSW41_x_abs * bsw42.2_x_mm_abs + dkPIBSW41_x * bsw42.2_x_mm + dkPIBSW41_px * bsw42.2_px_mrad;";
          print, text = "kPI2BSW42 := dkPIBSW42_x_abs * bsw42.2_x_mm_abs + dkPIBSW42_x * bsw42.2_x_mm + dkPIBSW42_px * bsw42.2_px_mrad;";
          print, text = "kPI2BSW43 := dkPIBSW43_x_abs * bsw42.2_x_mm_abs + dkPIBSW43_x * bsw42.2_x_mm + dkPIBSW43_px * bsw42.2_px_mrad;";
          print, text = "kPI2BSW44 := dkPIBSW44_x_abs * bsw42.2_x_mm_abs + dkPIBSW44_x * bsw42.2_x_mm + dkPIBSW44_px * bsw42.2_px_mrad;";
          print,  text = "";  

        }

      }
      ELSE{
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Proton injection bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = "";   
        print, text = "bsw42_x_mm_abs_active  =              0 ;";
        print,  text = "";   
      }

      IF (dkPISMH26_x_abs <> 0.) {
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Ion injection bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = "";           
        print, text = "smh26_x_mm_abs_active  =              1 ;";
        printf, text = "smh26_x_mm_abs      = %F ;", value = x0*1e3;
        print,  text = "";      
        printf, text = "dkPISMH26_x_abs     = %F ;", value = dkPISMH26_x_abs;
        print,  text = "";      
        print, text = "kPIBSW26 := dkPISMH26_x_abs * smh26_x_mm_abs;";
        print,  text = "";  
      } 
      ELSE{
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Ion injection bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = ""; 
        print, text = "smh26_x_mm_abs_active  =              0 ;";
        print,  text = ""; 
      }

      IF (dkf_x <> 0.) {  
        IF (wo_PRQDN90 == 1) {
           print,  text = "";   
           print,  text = "!------------------------------------------------------------------------------------------------------------";      
           print,  text = "! Tune knobs using the low energy quadrupoles without the PR.QDN90 (for LHC-type beams with long flat bottom)"; 
           print,  text = "!------------------------------------------------------------------------------------------------------------"; 
           print,  text = ""; 
           print,  text = "kPRQDN90 = 0.;"; 
           print,  text = "";      
           print,  text = "qx_leq             =       0.0000000000 ;";
           print,  text = "qy_leq             =       0.0000000000 ;";  
           print,  text = "";      
           printf, text = "dkf_x              = %F ;", value = dkf_x;
           printf, text = "dkd_x              = %F ;", value = dkd_x;
           print,  text = ""; 
           printf, text = "dkf_y              = %F ;", value = dkf_y;
           printf, text = "dkd_y              = %F ;", value = dkd_y;
           print,  text = "";           
           printf, text = "kf := %F + dkf_x * qx_leq + dkf_y * qy_leq;", value = kf_0;
           printf, text = "kd := %F + dkd_x * qx_leq + dkd_y * qy_leq;", value = kd_0;
           print,  text = "";
        } 
        ELSE {  
           print,  text = "";   
           print,  text = "!-------------------------------------------------";      
           print,  text = "! Tune knobs using the low energy quadrupoles"; 
           print,  text = "!-------------------------------------------------"; 
           print,  text = "";      
           print,  text = "kPRQDN90 := kd;"; 
           print,  text = "";  
           print,  text = "qx_leq             =       0.0000000000 ;";
           print,  text = "qy_leq             =       0.0000000000 ;";  
           print,  text = "";      
           printf, text = "dkf_x              = %F ;", value = dkf_x;
           printf, text = "dkd_x              = %F ;", value = dkd_x;
           print,  text = ""; 
           printf, text = "dkf_y              = %F ;", value = dkf_y;
           printf, text = "dkd_y              = %F ;", value = dkd_y;
           print,  text = "";           
           printf, text = "kf := %F + dkf_x * qx_leq + dkf_y * qy_leq;", value = kf_0;
           printf, text = "kd := %F + dkd_x * qx_leq + dkd_y * qy_leq;", value = kd_0;
           print,  text = "";
        }
      }

      IF (zero_disp_knobs <> 0.) {
           print,  text = "";   
           print,  text = "!-------------------------------------------------";      
           print,  text = "! Zero dispersion knobs"; 
           print,  text = "!-------------------------------------------------"; 
           print,  text = "";      
           print,  text = "Dx_bwsh54_leq    =       0.0000000000 ;";
           print,  text = "Dx_bwsh65_leq    =       0.0000000000 ;";  
           print,  text = "Dx_bwsh68_leq    =       0.0000000000 ;"; 
           print,  text = "Dx_bgi82_leq     =       0.0000000000 ;"; 
           print,  text = ""; 

           printf, text = "bwsh54_dkN05     = %F ;", value = bwsh54_dkN05;
           printf, text = "bwsh54_dkN21     = %F ;", value = bwsh54_dkN21;
           printf, text = "bwsh54_dkW27     = %F ;", value = bwsh54_dkW27;
           printf, text = "bwsh54_dkW28     = %F ;", value = bwsh54_dkW28;
           printf, text = "bwsh54_dkN35     = %F ;", value = bwsh54_dkN35;
           printf, text = "bwsh54_dkN36     = %F ;", value = bwsh54_dkN36;
           printf, text = "bwsh54_dkN45     = %F ;", value = bwsh54_dkN45;
           printf, text = "bwsh54_dkN55     = %F ;", value = bwsh54_dkN55;
           printf, text = "bwsh54_dkW56     = %F ;", value = bwsh54_dkW56;
           printf, text = "bwsh54_dkN71     = %F ;", value = bwsh54_dkN71;
           printf, text = "bwsh54_dkN72     = %F ;", value = bwsh54_dkN72;
           printf, text = "bwsh54_dkN81     = %F ;", value = bwsh54_dkN81;
           printf, text = "bwsh54_dkN89     = %F ;", value = bwsh54_dkN89;
           printf, text = "bwsh54_dkN95     = %F ;", value = bwsh54_dkN95;
           printf, text = "bwsh54_dkN96     = %F ;", value = bwsh54_dkN96;
           print,  text = "";
           printf, text = "bwsh65_dkN05     = %F ;", value = bwsh65_dkN05;
           printf, text = "bwsh65_dkN09     = %F ;", value = bwsh65_dkN09;
           printf, text = "bwsh65_dkW17     = %F ;", value = bwsh65_dkW17;
           printf, text = "bwsh65_dkN21     = %F ;", value = bwsh65_dkN21;
           printf, text = "bwsh65_dkW31     = %F ;", value = bwsh65_dkW31;
           printf, text = "bwsh65_dkN39     = %F ;", value = bwsh65_dkN39;
           printf, text = "bwsh65_dkN45     = %F ;", value = bwsh65_dkN45;
           printf, text = "bwsh65_dkN49     = %F ;", value = bwsh65_dkN49;
           printf, text = "bwsh65_dkN55     = %F ;", value = bwsh65_dkN55;
           printf, text = "bwsh65_dkN67     = %F ;", value = bwsh65_dkN67;
           printf, text = "bwsh65_dkN77     = %F ;", value = bwsh65_dkN77;
           printf, text = "bwsh65_dkN81     = %F ;", value = bwsh65_dkN81;
           printf, text = "bwsh65_dkN85     = %F ;", value = bwsh65_dkN85;
           printf, text = "bwsh65_dkN89     = %F ;", value = bwsh65_dkN89;
           printf, text = "bwsh65_dkN99     = %F ;", value = bwsh65_dkN99;
           print,  text = "";   
           printf, text = "bwsh68_dkN09     = %F ;", value = bwsh68_dkN09;
           printf, text = "bwsh68_dkW17     = %F ;", value = bwsh68_dkW17;
           printf, text = "bwsh68_dkW18     = %F ;", value = bwsh68_dkW18;
           printf, text = "bwsh68_dkW27     = %F ;", value = bwsh68_dkW27;
           printf, text = "bwsh68_dkN35     = %F ;", value = bwsh68_dkN35;
           printf, text = "bwsh68_dkN49     = %F ;", value = bwsh68_dkN49;
           printf, text = "bwsh68_dkN50     = %F ;", value = bwsh68_dkN50;
           printf, text = "bwsh68_dkW59     = %F ;", value = bwsh68_dkW59;
           printf, text = "bwsh68_dkN67     = %F ;", value = bwsh68_dkN67;
           printf, text = "bwsh68_dkN71     = %F ;", value = bwsh68_dkN71;
           printf, text = "bwsh68_dkN77     = %F ;", value = bwsh68_dkN77;
           printf, text = "bwsh68_dkN78     = %F ;", value = bwsh68_dkN78;
           printf, text = "bwsh68_dkN85     = %F ;", value = bwsh68_dkN85;
           printf, text = "bwsh68_dkN86     = %F ;", value = bwsh68_dkN86;
           printf, text = "bwsh68_dkN95     = %F ;", value = bwsh68_dkN95;
           print,  text = "";           
           printf, text = "bgi82_dkN09      = %F ;", value = bgi82_dkN09;
           printf, text = "bgi82_dkW17      = %F ;", value = bgi82_dkW17;
           printf, text = "bgi82_dkW31      = %F ;", value = bgi82_dkW31;
           printf, text = "bgi82_dkW32      = %F ;", value = bgi82_dkW32;
           printf, text = "bgi82_dkN39      = %F ;", value = bgi82_dkN39;
           printf, text = "bgi82_dkN40      = %F ;", value = bgi82_dkN40;
           printf, text = "bgi82_dkN49      = %F ;", value = bgi82_dkN49;
           printf, text = "bgi82_dkN55      = %F ;", value = bgi82_dkN55;
           printf, text = "bgi82_dkW56      = %F ;", value = bgi82_dkW56;
           printf, text = "bgi82_dkN71      = %F ;", value = bgi82_dkN71;
           printf, text = "bgi82_dkN72      = %F ;", value = bgi82_dkN72;
           printf, text = "bgi82_dkN81      = %F ;", value = bgi82_dkN81;
           printf, text = "bgi82_dkN85      = %F ;", value = bgi82_dkN85;
           printf, text = "bgi82_dkN99      = %F ;", value = bgi82_dkN99;
           printf, text = "bgi82_dkN00      = %F ;", value = bgi82_dkN00;
           print,  text = "";           
           print,  text = "kPRQFN05 := kf + bwsh54_dkN05 * Dx_bwsh54_leq + bwsh65_dkN05 * Dx_bwsh65_leq;"; 
           print,  text = "kPRQFN09 := kf + bwsh65_dkN09 * Dx_bwsh65_leq + bwsh68_dkN09 * Dx_bwsh68_leq + bgi82_dkN09 * Dx_bgi82_leq;"; 
           print,  text = "kPRQFW17 := kf + bwsh65_dkW17 * Dx_bwsh65_leq + bwsh68_dkW17 * Dx_bwsh68_leq + bgi82_dkW17 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDW18 := kd + bwsh68_dkW18 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQFN21 := kf + bwsh54_dkN21 * Dx_bwsh54_leq + bwsh65_dkN21 * Dx_bwsh65_leq;"; 
           print,  text = "kPRQFW27 := kf + bwsh54_dkW27 * Dx_bwsh54_leq + bwsh68_dkW27 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQDW28 := kd + bwsh54_dkW28 * Dx_bwsh54_leq;"; 
           print,  text = "kPRQFW31 := kf + bwsh65_dkW31 * Dx_bwsh65_leq + bgi82_dkW31 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDW32 := kd + bgi82_dkW32 * Dx_bgi82_leq;";
           print,  text = "kPRQFN35 := kf + bwsh54_dkN35 * Dx_bwsh54_leq + bwsh68_dkN35 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQDN36 := kd + bwsh54_dkN36 * Dx_bwsh54_leq;"; 
           print,  text = "kPRQFN39 := kf + bwsh65_dkN39 * Dx_bwsh65_leq + bgi82_dkN39 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDN40 := kd + bgi82_dkN40 * Dx_bgi82_leq;"; 
           print,  text = "kPRQFN45 := kf + bwsh54_dkN45 * Dx_bwsh54_leq + bwsh65_dkN45 * Dx_bwsh65_leq;"; 
           print,  text = "kPRQFN49 := kf + bwsh65_dkN49 * Dx_bwsh65_leq + bwsh68_dkN49 * Dx_bwsh68_leq + bgi82_dkN49 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDN50 := kd + bwsh68_dkN50 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQFN55 := kf + bwsh54_dkN55 * Dx_bwsh54_leq + bwsh65_dkN55 * Dx_bwsh65_leq + bgi82_dkN55 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDW56 := kd + bwsh54_dkW56 * Dx_bwsh54_leq + bgi82_dkW56 * Dx_bgi82_leq;"; 
           print,  text = "kPRQFW59 := kf + bwsh68_dkW59 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQFN67 := kf + bwsh65_dkN67 * Dx_bwsh65_leq + bwsh68_dkN67 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQFN71 := kf + bwsh54_dkN71 * Dx_bwsh54_leq + bwsh68_dkN71 * Dx_bwsh68_leq + bgi82_dkN71 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDN72 := kd + bwsh54_dkN72 * Dx_bwsh54_leq + bgi82_dkN72 * Dx_bgi82_leq;"; 
           print,  text = "kPRQFN77 := kf + bwsh65_dkN77 * Dx_bwsh65_leq + bwsh68_dkN77 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQDN78 := kd + bwsh68_dkN78 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQFN81 := kf + bwsh54_dkN81 * Dx_bwsh54_leq + bwsh65_dkN81 * Dx_bwsh65_leq + bgi82_dkN81 * Dx_bgi82_leq;";        
           print,  text = "kPRQFN85 := kf + bwsh65_dkN85 * Dx_bwsh65_leq + bwsh68_dkN85 * Dx_bwsh68_leq + bgi82_dkN85 * Dx_bgi82_leq;";        
           print,  text = "kPRQDN86 := kd + bwsh68_dkN86 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQFN89 := kf + bwsh54_dkN89 * Dx_bwsh54_leq + bwsh65_dkN89 * Dx_bwsh65_leq;"; 
           print,  text = "kPRQFN95 := kf + bwsh54_dkN95 * Dx_bwsh54_leq + bwsh68_dkN95 * Dx_bwsh68_leq;"; 
           print,  text = "kPRQDN96 := kd + bwsh54_dkN96 * Dx_bwsh54_leq;"; 
           print,  text = "kPRQFN99 := kf + bwsh65_dkN99 * Dx_bwsh65_leq + bgi82_dkN99 * Dx_bgi82_leq;"; 
           print,  text = "kPRQDN00 := kd + bgi82_dkN00 * Dx_bgi82_leq;"; 
           print,  text = ""; 
      }

      IF (dkPEBSW14_x_abs <> 0.) {
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Extraction bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = "";  
        print, text = "smh16_x_mm_abs_active  =                  1 ;";         
        printf, text = "smh16_x_mm_abs         = %F ;", value = smh16_x_mm_abs;
        print, text = "smh16_x_mm             =       0.0000000000 ;";
        print, text = "smh16_px_urad          =       0.0000000000 ;";
        print, text = "tps15_ortho_x_mm       =       0.0000000000 ;";    
        print, text = "smh16_ortho_x_mm       =       0.0000000000 ;";    
        print,  text = "";      
        printf, text = "dkPEBSW12_x_abs        = %F ;", value = dkPEBSW12_x_abs;
        printf, text = "dkPEBSW14_x_abs        = %F ;", value = dkPEBSW14_x_abs;
        printf, text = "dkPEBSW20_x_abs        = %F ;", value = dkPEBSW20_x_abs;
        printf, text = "dkPEBSW22_x_abs        = %F ;", value = dkPEBSW22_x_abs;
        print,  text = "";      
        printf, text = "dkPEBSW12_x            = %F ;", value = dkPEBSW12_x;
        printf, text = "dkPEBSW14_x            = %F ;", value = dkPEBSW14_x;
        printf, text = "dkPEBSW20_x            = %F ;", value = dkPEBSW20_x;
        printf, text = "dkPEBSW22_x            = %F ;", value = dkPEBSW22_x;
        print,  text = "";      
        printf, text = "dkPEBSW12_px           = %F ;", value = dkPEBSW12_px;
        printf, text = "dkPEBSW14_px           = %F ;", value = dkPEBSW14_px;
        printf, text = "dkPEBSW20_px           = %F ;", value = dkPEBSW20_px;
        printf, text = "dkPEBSW22_px           = %F ;", value = dkPEBSW22_px;
        print,  text = "";   
        printf, text = "dkPEBSW12_ortho_x15    = %F ;", value = dkPEBSW12_ortho_x15;
        printf, text = "dkPEBSW14_ortho_x15    = %F ;", value = dkPEBSW14_ortho_x15;
        printf, text = "dkPEBSW20_ortho_x15    = %F ;", value = dkPEBSW20_ortho_x15;
        printf, text = "dkPEBSW22_ortho_x15    = %F ;", value = dkPEBSW22_ortho_x15;
        print,  text = ""; 
        printf, text = "dkPEBSW12_ortho_x16    = %F ;", value = dkPEBSW12_ortho_x16;
        printf, text = "dkPEBSW14_ortho_x16    = %F ;", value = dkPEBSW14_ortho_x16;
        printf, text = "dkPEBSW20_ortho_x16    = %F ;", value = dkPEBSW20_ortho_x16;
        printf, text = "dkPEBSW22_ortho_x16    = %F ;", value = dkPEBSW22_ortho_x16;
        print,  text = "";          
        print, text = "kPEBSW12 := dkPEBSW12_x_abs * smh16_x_mm_abs + dkPEBSW12_x * smh16_x_mm + dkPEBSW12_px * smh16_px_urad + dkPEBSW12_ortho_x15 * tps15_ortho_x_mm + dkPEBSW12_ortho_x16 * smh16_ortho_x_mm;";
        print, text = "kPEBSW14 := dkPEBSW14_x_abs * smh16_x_mm_abs + dkPEBSW14_x * smh16_x_mm + dkPEBSW14_px * smh16_px_urad + dkPEBSW14_ortho_x15 * tps15_ortho_x_mm + dkPEBSW14_ortho_x16 * smh16_ortho_x_mm;";
        print, text = "kPEBSW20 := dkPEBSW20_x_abs * smh16_x_mm_abs + dkPEBSW20_x * smh16_x_mm + dkPEBSW20_px * smh16_px_urad + dkPEBSW20_ortho_x15 * tps15_ortho_x_mm + dkPEBSW20_ortho_x16 * smh16_ortho_x_mm;";
        print, text = "kPEBSW22 := dkPEBSW22_x_abs * smh16_x_mm_abs + dkPEBSW22_x * smh16_x_mm + dkPEBSW22_px * smh16_px_urad + dkPEBSW22_ortho_x15 * tps15_ortho_x_mm + dkPEBSW22_ortho_x16 * smh16_ortho_x_mm;";
        print,  text = "";  
      } 
      ELSEIF (dkpeseh23_x_abs <> 0.){
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Extraction bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = ""; 
        print, text = "seh23_x_mm_abs_active  =              1 ;";
        print, text = "smh57_x_mm_abs_active  =              1 ;";
        print,  text = "";      
        printf, text = "seh23_x_mm_abs      = %F ;", value = x_SEH23*1e3;
        printf, text = "smh57_x_mm_abs      = %F ;", value = x_SMH57*1e3;
        print,  text = "";      
        printf, text = "dkPESEH23_x_abs     = %F ;", value = dkPESEH23_x_abs;
        printf, text = "dkPESMH57_x_abs     = %F ;", value = dkPESMH57_x_abs;
        print,  text = "";      
        print, text = "kPEBSW23 := dkPESEH23_x_abs * seh23_x_mm_abs;";
        print, text = "kPEBSW57 := dkPESMH57_x_abs * smh57_x_mm_abs;";
        print,  text = "";  
      }
      ELSE{
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! Extraction bump"; 
        print,  text = "!-------------------------------------------------";
        print,  text = "";  
        print, text = "smh16_x_mm_abs_active  =              0 ;";
        print, text = "seh23_x_mm_abs_active  =              1 ;";
        print, text = "seh23_x_mm_abs         =              0 ;";
        print, text = "smh57_x_mm_abs_active  =              1 ;";
        print, text = "smh57_x_mm_abs         =              0 ;";
        print,  text = "";   
      }

      IF (dkPRDHZOC05_SMH16_x <> 0.) {
        print,  text = "";   
        print,  text = "!-------------------------------------------------";      
        print,  text = "! High-energy corrector knobs"; 
        print,  text = "!-------------------------------------------------";
        print,  text = "";  
        print,  text = "dhzoc_smh16_x_mm     =                    0 ;";
        print,  text = "dhzoc_qsk19_x_mm     =                    0 ;";
        print,  text = "dhzoc_smh16_px_urad  =                    0 ;";
        print,  text = "dhzoc_qsk19_px_urad  =                    0 ;";
        print,  text = "";      
        printf, text = "dkPRDHZOC05_SMH16_x      = %F ;", value = dkPRDHZOC05_SMH16_x;
        printf, text = "dkPRDHZOC18_SMH16_x      = %F ;", value = dkPRDHZOC18_SMH16_x;
        printf, text = "dkPRDHZOC60_SMH16_x      = %F ;", value = dkPRDHZOC60_SMH16_x;
        print,  text = "";   
        printf, text = "dkPRDHZOC05_QSK19_x      = %F ;", value = dkPRDHZOC05_QSK19_x;
        printf, text = "dkPRDHZOC18_QSK19_x      = %F ;", value = dkPRDHZOC18_QSK19_x;
        printf, text = "dkPRDHZOC60_QSK19_x      = %F ;", value = dkPRDHZOC60_QSK19_x;
        print,  text = "";   
        printf, text = "dkPRDHZOC05_SMH16_px     = %F ;", value = dkPRDHZOC05_SMH16_px;
        printf, text = "dkPRDHZOC18_SMH16_px     = %F ;", value = dkPRDHZOC18_SMH16_px;
        printf, text = "dkPRDHZOC60_SMH16_px     = %F ;", value = dkPRDHZOC60_SMH16_px;
        print,  text = "";  
        printf, text = "dkPRDHZOC05_QSK19_px     = %F ;", value = dkPRDHZOC05_QSK19_px;
        printf, text = "dkPRDHZOC18_QSK19_px     = %F ;", value = dkPRDHZOC18_QSK19_px;
        printf, text = "dkPRDHZOC60_QSK19_px     = %F ;", value = dkPRDHZOC60_QSK19_px;
        print,  text = "";    
        print, text = "kPRDHZOC05 := dkPRDHZOC05_SMH16_x * dhzoc_smh16_x_mm + dkPRDHZOC05_QSK19_x * dhzoc_qsk19_x_mm + dkPRDHZOC05_SMH16_px * dhzoc_smh16_px_urad + dkPRDHZOC05_QSK19_px * dhzoc_qsk19_px_urad;";
        print, text = "kPRDHZOC18 := dkPRDHZOC18_SMH16_x * dhzoc_smh16_x_mm + dkPRDHZOC18_QSK19_x * dhzoc_qsk19_x_mm + dkPRDHZOC18_SMH16_px * dhzoc_smh16_px_urad + dkPRDHZOC18_QSK19_px * dhzoc_qsk19_px_urad;";
        print, text = "kPRDHZOC60 := dkPRDHZOC60_SMH16_x * dhzoc_smh16_x_mm + dkPRDHZOC60_QSK19_x * dhzoc_qsk19_x_mm + dkPRDHZOC60_SMH16_px * dhzoc_smh16_px_urad + dkPRDHZOC60_QSK19_px * dhzoc_qsk19_px_urad;";
        print,  text = "";  
      } 

      assign, echo = terminal;
    };


    ''')

