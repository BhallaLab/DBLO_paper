/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 static void _difusfunc(ldifusfunc2_t, NrnThread*);
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__cal4
#define _nrn_initial _nrn_initial__cal4
#define nrn_cur _nrn_cur__cal4
#define _nrn_current _nrn_current__cal4
#define nrn_jacob _nrn_jacob__cal4
#define nrn_state _nrn_state__cal4
#define _net_receive _net_receive__cal4 
#define factors factors__cal4 
#define state state__cal4 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 static double *_p; static Datum *_ppvar;
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gamma _p[0]
#define gamma_columnindex 0
#define sites _p[1]
#define sites_columnindex 1
#define alpha _p[2]
#define alpha_columnindex 2
#define beta _p[3]
#define beta_columnindex 3
#define DCa _p[4]
#define DCa_columnindex 4
#define cip3 _p[5]
#define cip3_columnindex 5
#define jip3 _p[6]
#define jip3_columnindex 6
#define ca1 _p[7]
#define ca1_columnindex 7
#define ca2 _p[8]
#define ca2_columnindex 8
#define ca3 _p[9]
#define ca3_columnindex 9
#define ica_pmp _p[10]
#define ica_pmp_columnindex 10
#define ip3ca _p[11]
#define ip3ca_columnindex 11
#define ca (_p + 12)
#define ca_columnindex 12
#define hc (_p + 16)
#define hc_columnindex 16
#define ho (_p + 20)
#define ho_columnindex 20
#define bufs (_p + 24)
#define bufs_columnindex 24
#define cabufs (_p + 28)
#define cabufs_columnindex 28
#define bufm (_p + 32)
#define bufm_columnindex 32
#define cabufm (_p + 36)
#define cabufm_columnindex 36
#define bapta (_p + 40)
#define bapta_columnindex 40
#define cabapta (_p + 44)
#define cabapta_columnindex 44
#define ip3cas (_p + 48)
#define ip3cas_columnindex 48
#define ica _p[52]
#define ica_columnindex 52
#define cai _p[53]
#define cai_columnindex 53
#define ica_pmp_last _p[54]
#define ica_pmp_last_columnindex 54
#define parea _p[55]
#define parea_columnindex 55
#define sump _p[56]
#define sump_columnindex 56
#define cao _p[57]
#define cao_columnindex 57
#define jchnl _p[58]
#define jchnl_columnindex 58
#define L (_p + 59)
#define L_columnindex 59
#define adjusted _p[63]
#define adjusted_columnindex 63
#define so _p[64]
#define so_columnindex 64
#define that _p[65]
#define that_columnindex 65
#define bufs_0 _p[66]
#define bufs_0_columnindex 66
#define bufm_0 _p[67]
#define bufm_0_columnindex 67
#define bapta_0 _p[68]
#define bapta_0_columnindex 68
#define Dca (_p + 69)
#define Dca_columnindex 69
#define Dhc (_p + 73)
#define Dhc_columnindex 73
#define Dho (_p + 77)
#define Dho_columnindex 77
#define Dbufs (_p + 81)
#define Dbufs_columnindex 81
#define Dcabufs (_p + 85)
#define Dcabufs_columnindex 85
#define Dbufm (_p + 89)
#define Dbufm_columnindex 89
#define Dcabufm (_p + 93)
#define Dcabufm_columnindex 93
#define Dbapta (_p + 97)
#define Dbapta_columnindex 97
#define Dcabapta (_p + 101)
#define Dcabapta_columnindex 101
#define Dip3cas (_p + 105)
#define Dip3cas_columnindex 105
#define _g _p[109]
#define _g_columnindex 109
#define _ion_cao	*_ppvar[0]._pval
#define _ion_ica	*_ppvar[1]._pval
#define _ion_cai	*_ppvar[2]._pval
#define _ion_dicadv	*_ppvar[3]._pval
#define _style_ca	*((int*)_ppvar[4]._pvoid)
#define diam	*_ppvar[5]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_factors(void);
 static void _hoc_u(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _p = _prop->param; _ppvar = _prop->dparam;
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 "setdata_cal4", _hoc_setdata,
 "factors_cal4", _hoc_factors,
 "u_cal4", _hoc_u,
 0, 0
};
#define u u_cal4
 extern double u( double , double );
 /* declare global and static user variables */
#define DBufm DBufm_cal4
 double DBufm = 0.05;
#define Kp Kp_cal4
 double Kp = 0.00027;
#define Kinh Kinh_cal4
 double Kinh = 0.0006;
#define Kact Kact_cal4
 double Kact = 0.0007;
#define Kip3 Kip3_cal4
 double Kip3 = 0.0008;
#define KDBAPTA KDBAPTA_cal4
 double KDBAPTA = 0.2;
#define KDm KDm_cal4
 double KDm = 0.24;
#define KDs KDs_cal4
 double KDs = 10;
#define TBufBAPTA TBufBAPTA_cal4
 double TBufBAPTA = 0;
#define TBufm TBufm_cal4
 double TBufm = 0.075;
#define TBufs TBufs_cal4
 double TBufs = 0.45;
#define caer caer_cal4
 double caer = 0.4;
#define cath cath_cal4
 double cath = 0.0002;
#define cai0 cai0_cal4
 double cai0 = 5e-05;
#define ip3i ip3i_cal4
 double ip3i = 0.01;
#define jmax jmax_cal4
 double jmax = 0.0035;
#define kfm kfm_cal4
 double kfm = 1000;
#define kfBAPTA kfBAPTA_cal4
 double kfBAPTA = 500;
#define kfs kfs_cal4
 double kfs = 1000;
#define kon kon_cal4
 double kon = 2.7;
#define vmax vmax_cal4
 double vmax = 0.0001;
#define vrat vrat_cal4
 double vrat[4];
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "ip3i_cal4", "mM",
 "cai0_cal4", "mM",
 "cath_cal4", "mM",
 "jmax_cal4", "mM/ms",
 "caer_cal4", "mM",
 "Kip3_cal4", "mM",
 "Kact_cal4", "mM",
 "kon_cal4", "/mM-ms",
 "Kinh_cal4", "mM",
 "vmax_cal4", "mM/ms",
 "Kp_cal4", "mM",
 "TBufs_cal4", "mM",
 "kfs_cal4", "/mM-ms",
 "KDs_cal4", "uM",
 "TBufBAPTA_cal4", "mM",
 "kfBAPTA_cal4", "/mM-ms",
 "KDBAPTA_cal4", "uM",
 "TBufm_cal4", "mM",
 "kfm_cal4", "/mM-ms",
 "KDm_cal4", "uM",
 "DBufm_cal4", "um2/ms",
 "vrat_cal4", "1",
 "gamma_cal4", "um/s",
 "alpha_cal4", "1",
 "beta_cal4", "1",
 "DCa_cal4", "um2/ms",
 "ca_cal4", "mM",
 "bufs_cal4", "mM",
 "cabufs_cal4", "mM",
 "bufm_cal4", "mM",
 "cabufm_cal4", "mM",
 "bapta_cal4", "mM",
 "cabapta_cal4", "mM",
 "ip3cas_cal4", "mM",
 "cip3_cal4", "mA/cm2",
 "jip3_cal4", "mM/ms",
 "ca1_cal4", "mM",
 "ca2_cal4", "mM",
 "ca3_cal4", "mM",
 "ica_pmp_cal4", "mA/cm2",
 "ip3ca_cal4", "mM",
 0,0
};
 static double bapta0 = 0;
 static double bufm0 = 0;
 static double bufs0 = 0;
 static double cabapta0 = 0;
 static double cabufm0 = 0;
 static double cabufs0 = 0;
 static double ca0 = 0;
 static double delta_t = 0.01;
 static double ho0 = 0;
 static double hc0 = 0;
 static double ip3cas0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "ip3i_cal4", &ip3i_cal4,
 "cai0_cal4", &cai0_cal4,
 "cath_cal4", &cath_cal4,
 "jmax_cal4", &jmax_cal4,
 "caer_cal4", &caer_cal4,
 "Kip3_cal4", &Kip3_cal4,
 "Kact_cal4", &Kact_cal4,
 "kon_cal4", &kon_cal4,
 "Kinh_cal4", &Kinh_cal4,
 "vmax_cal4", &vmax_cal4,
 "Kp_cal4", &Kp_cal4,
 "TBufs_cal4", &TBufs_cal4,
 "kfs_cal4", &kfs_cal4,
 "KDs_cal4", &KDs_cal4,
 "TBufBAPTA_cal4", &TBufBAPTA_cal4,
 "kfBAPTA_cal4", &kfBAPTA_cal4,
 "KDBAPTA_cal4", &KDBAPTA_cal4,
 "TBufm_cal4", &TBufm_cal4,
 "kfm_cal4", &kfm_cal4,
 "KDm_cal4", &KDm_cal4,
 "DBufm_cal4", &DBufm_cal4,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 "vrat_cal4", vrat_cal4, 4,
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(NrnThread*, _Memb_list*, int);
static void nrn_state(NrnThread*, _Memb_list*, int);
 static void nrn_cur(NrnThread*, _Memb_list*, int);
static void  nrn_jacob(NrnThread*, _Memb_list*, int);
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(NrnThread*, _Memb_list*, int);
static void _ode_matsol(NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[6]._i
 static void _ode_synonym(int, double**, Datum**);
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"cal4",
 "gamma_cal4",
 "sites_cal4",
 "alpha_cal4",
 "beta_cal4",
 "DCa_cal4",
 0,
 "cip3_cal4",
 "jip3_cal4",
 "ca1_cal4",
 "ca2_cal4",
 "ca3_cal4",
 "ica_pmp_cal4",
 "ip3ca_cal4",
 0,
 "ca_cal4[4]",
 "hc_cal4[4]",
 "ho_cal4[4]",
 "bufs_cal4[4]",
 "cabufs_cal4[4]",
 "bufm_cal4[4]",
 "cabufm_cal4[4]",
 "bapta_cal4[4]",
 "cabapta_cal4[4]",
 "ip3cas_cal4[4]",
 0,
 0};
 static Symbol* _morphology_sym;
 static Symbol* _ca_sym;
 static int _type_ica;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 110, _prop);
 	/*initialize range parameters*/
 	gamma = 8;
 	sites = 3;
 	alpha = 1;
 	beta = 1;
 	DCa = 0.22;
 	_prop->param = _p;
 	_prop->param_size = 110;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 7, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[5]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_ca_sym);
  _type_ica = prop_ion->_type;
 nrn_check_conc_write(_prop, prop_ion, 1);
 nrn_promote(prop_ion, 3, 0);
 	_ppvar[0]._pval = &prop_ion->param[2]; /* cao */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ica */
 	_ppvar[2]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[3]._pval = &prop_ion->param[4]; /* _ion_dicadv */
 	_ppvar[4]._pvoid = (void*)(&(prop_ion->dparam[0]._i)); /* iontype for ca */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 "ca_cal4", 1e-07,
 "bufs_cal4", 0.001,
 "cabufs_cal4", 1e-07,
 "bufm_cal4", 0.0001,
 "cabufm_cal4", 1e-08,
 "bapta_cal4", 0.001,
 "cabapta_cal4", 1e-07,
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _cal4_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
 	_morphology_sym = hoc_lookup("morphology");
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 110, 7);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "#ca_ion");
  hoc_register_dparam_semantics(_mechtype, 6, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 5, "diam");
 	nrn_writes_conc(_mechtype, 0);
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_synonym(_mechtype, _ode_synonym);
 	hoc_register_ldifus1(_difusfunc);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 cal4 /mnt/h/Thesis work/Compilations/ExistingModels/Combe2023/267599/cholinergic_shift_generalize/cal4.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 
#define FARADAY _nrnunit_FARADAY[_nrnunit_use_legacy_]
static double _nrnunit_FARADAY[2] = {0x1.34c0c8b92a9b7p+3, 9.64853}; /* 9.64853321233100125 */
 
#define PI _nrnunit_PI[_nrnunit_use_legacy_]
static double _nrnunit_PI[2] = {0x1.921fb54442d18p+1, 3.14159}; /* 3.14159265358979312 */
 static double volo = 1e10;
 static double _zfactors_done , _zjx ;
 static double _zfrat [ 4 ] ;
 static double _zdsq , _zdsqvol ;
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int factors();
 extern double *_getelm();
 
#define _MATELM1(_row,_col)	*(_getelm(_row + 1, _col + 1))
 
#define _RHS1(_arg) _coef1[_arg + 1]
 static double *_coef1;
 
#define _linmat1  0
 static void* _sparseobj1;
 static void* _cvsparseobj1;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[32], _dlist1[32]; static double *_temp1;
 static int state();
 
static int  factors (  ) {
   double _lr , _ldr2 ;
 _lr = 1.0 / 2.0 ;
   _ldr2 = _lr / ( 4.0 - 1.0 ) / 2.0 ;
   vrat [ 0 ] = 0.0 ;
   _zfrat [ 0 ] = 2.0 * _lr ;
   {int  _li ;for ( _li = 0 ; _li <= 4 - 2 ; _li ++ ) {
     vrat [ _li ] = vrat [ _li ] + PI * ( _lr - _ldr2 / 2.0 ) * 2.0 * _ldr2 ;
     _lr = _lr - _ldr2 ;
     _zfrat [ _li + 1 ] = 2.0 * PI * _lr / ( 2.0 * _ldr2 ) ;
     _lr = _lr - _ldr2 ;
     vrat [ _li + 1 ] = PI * ( _lr + _ldr2 / 2.0 ) * 2.0 * _ldr2 ;
     } }
    return 0; }
 
static void _hoc_factors(void) {
  double _r;
   _r = 1.;
 factors (  );
 hoc_retpushx(_r);
}
 
static int state ()
 {_reset=0;
 {
   double b_flux, f_flux, _term; int _i;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<32;_i++){
  	_RHS1(_i) = -_dt1*(_p[_slist1[_i]] - _p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
} 
for (_i=0; _i < 4; _i++) {
  	_RHS1(_i + 4) *= ( diam * diam * vrat [ ((int) _i ) ]) ;
_MATELM1(_i + 4, _i + 4) *= ( diam * diam * vrat [ ((int) _i ) ]);  } 
for (_i=0; _i < 4; _i++) {
  	_RHS1(_i + 12) *= ( diam * diam * vrat [ ((int) _i ) ]) ;
_MATELM1(_i + 12, _i + 12) *= ( diam * diam * vrat [ ((int) _i ) ]);  } 
for (_i=0; _i < 4; _i++) {
  	_RHS1(_i + 16) *= ( diam * diam * vrat [ ((int) _i ) ]) ;
_MATELM1(_i + 16, _i + 16) *= ( diam * diam * vrat [ ((int) _i ) ]);  } }
 /* COMPARTMENT _li , diam * diam * vrat [ ((int) _i ) ] {
     ca bufs cabufs bufm cabufm }
   */
 /* COMPARTMENT volo {
     }
   */
 /* LONGITUDINAL_DIFFUSION _li , DCa * diam * diam * vrat [ ((int) _i ) ] {
     ca }
   */
 /* LONGITUDINAL_DIFFUSION _li , DBufm * diam * diam * vrat [ ((int) _i ) ] {
     bufm cabufm }
   */
 /* ~ ca [ 0 ] <-> sump ( ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) , ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) )*/
 f_flux =  ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) * ca [ 0] ;
 b_flux =  ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) * sump ;
 _RHS1( 16 +  0) -= (f_flux - b_flux);
 
 _term =  ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) ;
 _MATELM1( 16 +  0 ,16 +  0)  += _term;
 /*REACTION*/
  ica_pmp = 2.0 * FARADAY * ( f_flux - b_flux ) / parea ;
   /* ~ ca [ 0 ] < < ( - ( ica - ica_pmp_last ) * PI * diam / ( 2.0 * FARADAY ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 16 +  0) += (b_flux =   ( - ( ica - ica_pmp_last ) * PI * diam / ( 2.0 * FARADAY ) ) );
 /*FLUX*/
  {int  _li ;for ( _li = 0 ; _li <= 4 - 2 ; _li ++ ) {
     /* ~ ca [ _li ] <-> ca [ _li + 1 ] ( DCa * _zfrat [ _li + 1 ] , DCa * _zfrat [ _li + 1 ] )*/
 f_flux =  DCa * _zfrat [ _li + 1 ] * ca [ _li] ;
 b_flux =  DCa * _zfrat [ _li + 1 ] * ca [ _li + 1] ;
 _RHS1( 16 +  _li) -= (f_flux - b_flux);
 _RHS1( 16 +  _li + 1) += (f_flux - b_flux);
 
 _term =  DCa * _zfrat [ _li + 1 ] ;
 _MATELM1( 16 +  _li ,16 +  _li)  += _term;
 _MATELM1( 16 +  _li + 1 ,16 +  _li)  -= _term;
 _term =  DCa * _zfrat [ _li + 1 ] ;
 _MATELM1( 16 +  _li ,16 +  _li + 1)  -= _term;
 _MATELM1( 16 +  _li + 1 ,16 +  _li + 1)  += _term;
 /*REACTION*/
  } }
   _zdsq = diam * diam ;
   {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
     _zdsqvol = _zdsq * vrat [ _li ] ;
     /* ~ ca [ _li ] + bufs [ _li ] <-> cabufs [ _li ] ( kfs * _zdsqvol , ( 0.001 ) * KDs * kfs * _zdsqvol )*/
 f_flux =  kfs * _zdsqvol * bufs [ _li] * ca [ _li] ;
 b_flux =  ( 0.001 ) * KDs * kfs * _zdsqvol * cabufs [ _li] ;
 _RHS1( 4 +  _li) -= (f_flux - b_flux);
 _RHS1( 16 +  _li) -= (f_flux - b_flux);
 _RHS1( 12 +  _li) += (f_flux - b_flux);
 
 _term =  kfs * _zdsqvol * ca [ _li] ;
 _MATELM1( 4 +  _li ,4 +  _li)  += _term;
 _MATELM1( 16 +  _li ,4 +  _li)  += _term;
 _MATELM1( 12 +  _li ,4 +  _li)  -= _term;
 _term =  kfs * _zdsqvol * bufs [ _li] ;
 _MATELM1( 4 +  _li ,16 +  _li)  += _term;
 _MATELM1( 16 +  _li ,16 +  _li)  += _term;
 _MATELM1( 12 +  _li ,16 +  _li)  -= _term;
 _term =  ( 0.001 ) * KDs * kfs * _zdsqvol ;
 _MATELM1( 4 +  _li ,12 +  _li)  -= _term;
 _MATELM1( 16 +  _li ,12 +  _li)  -= _term;
 _MATELM1( 12 +  _li ,12 +  _li)  += _term;
 /*REACTION*/
  /* ~ ca [ _li ] + bapta [ _li ] <-> cabapta [ _li ] ( kfBAPTA * _zdsqvol , ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol )*/
 f_flux =  kfBAPTA * _zdsqvol * bapta [ _li] * ca [ _li] ;
 b_flux =  ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol * cabapta [ _li] ;
 _RHS1( 0 +  _li) -= (f_flux - b_flux);
 _RHS1( 16 +  _li) -= (f_flux - b_flux);
 _RHS1( 8 +  _li) += (f_flux - b_flux);
 
 _term =  kfBAPTA * _zdsqvol * ca [ _li] ;
 _MATELM1( 0 +  _li ,0 +  _li)  += _term;
 _MATELM1( 16 +  _li ,0 +  _li)  += _term;
 _MATELM1( 8 +  _li ,0 +  _li)  -= _term;
 _term =  kfBAPTA * _zdsqvol * bapta [ _li] ;
 _MATELM1( 0 +  _li ,16 +  _li)  += _term;
 _MATELM1( 16 +  _li ,16 +  _li)  += _term;
 _MATELM1( 8 +  _li ,16 +  _li)  -= _term;
 _term =  ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol ;
 _MATELM1( 0 +  _li ,8 +  _li)  -= _term;
 _MATELM1( 16 +  _li ,8 +  _li)  -= _term;
 _MATELM1( 8 +  _li ,8 +  _li)  += _term;
 /*REACTION*/
  } }
   {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
     _zdsqvol = _zdsq * vrat [ _li ] ;
     /* ~ ca [ _li ] < < ( - _zdsqvol * beta * vmax * pow( ca [ _li ] , 2.0 ) / ( pow( ca [ _li ] , 2.0 ) + pow( Kp , 2.0 ) ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 16 +  _li) += (b_flux =   ( - _zdsqvol * beta * vmax * pow( ca [ _li ] , 2.0 ) / ( pow( ca [ _li ] , 2.0 ) + pow( Kp , 2.0 ) ) ) );
 /*FLUX*/
  /* ~ hc [ _li ] <-> ho [ _li ] ( kon * Kinh , kon * ca [ _li ] )*/
 f_flux =  kon * Kinh * hc [ _li] ;
 b_flux =  kon * ca [ _li ] * ho [ _li] ;
 _RHS1( 24 +  _li) -= (f_flux - b_flux);
 _RHS1( 20 +  _li) += (f_flux - b_flux);
 
 _term =  kon * Kinh ;
 _MATELM1( 24 +  _li ,24 +  _li)  += _term;
 _MATELM1( 20 +  _li ,24 +  _li)  -= _term;
 _term =  kon * ca [ _li ] ;
 _MATELM1( 24 +  _li ,20 +  _li)  -= _term;
 _MATELM1( 20 +  _li ,20 +  _li)  += _term;
 /*REACTION*/
  /* ~ ca [ _li ] < < ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 16 +  _li) += (b_flux =   ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) ) );
 /*FLUX*/
  /* ~ ca [ _li ] < < ( _zdsqvol * beta * L [ _li ] * ( 1.0 - ( ca [ _li ] / caer ) ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 16 +  _li) += (b_flux =   ( _zdsqvol * beta * L [ _li ] * ( 1.0 - ( ca [ _li ] / caer ) ) ) );
 /*FLUX*/
  /* ~ ip3cas [ _li ] < < ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) )*/
 f_flux = b_flux = 0.;
 _RHS1( 28 +  _li) += (b_flux =   ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) ) );
 /*FLUX*/
  } }
   jip3 = ( jmax * ( 1.0 - ( ca [ 0 ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ 0 ] / ( ca [ 0 ] + Kact ) ) * ho [ 0 ] ) , sites ) ) ;
   cip3 = ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ 0 ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ 0 ] / ( ca [ 0 ] + Kact ) ) * ho [ 0 ] ) , sites ) ) * ( 2.0 * FARADAY ) / ( PI * ( diam ) ) ;
   ip3ca = ip3cas [ 0 ] ;
   cai = ca [ 0 ] ;
   ca1 = ca [ 1 ] ;
   ca2 = ca [ 2 ] ;
   ca3 = ca [ 3 ] ;
     } return _reset;
 }
 
double u (  double _lx , double _lth ) {
   double _lu;
 if ( _lx > _lth ) {
     _lu = 1.0 ;
     }
   else {
     _lu = 0.0 ;
     }
   
return _lu;
 }
 
static void _hoc_u(void) {
  double _r;
   _r =  u (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
/*CVODE ode begin*/
 static int _ode_spec1() {_reset=0;{
 double b_flux, f_flux, _term; int _i;
 {int _i; for(_i=0;_i<32;_i++) _p[_dlist1[_i]] = 0.0;}
 /* COMPARTMENT _li , diam * diam * vrat [ ((int) _i ) ] {
   ca bufs cabufs bufm cabufm }
 */
 /* COMPARTMENT volo {
   }
 */
 /* LONGITUDINAL_DIFFUSION _li , DCa * diam * diam * vrat [ ((int) _i ) ] {
   ca }
 */
 /* LONGITUDINAL_DIFFUSION _li , DBufm * diam * diam * vrat [ ((int) _i ) ] {
   bufm cabufm }
 */
 /* ~ ca [ 0 ] <-> sump ( ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) , ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) )*/
 f_flux =  ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) * ca [ 0] ;
 b_flux =  ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) * sump ;
 Dca [ 0] -= (f_flux - b_flux);
 
 /*REACTION*/
  ica_pmp = 2.0 * FARADAY * ( f_flux - b_flux ) / parea ;
 /* ~ ca [ 0 ] < < ( - ( ica - ica_pmp_last ) * PI * diam / ( 2.0 * FARADAY ) )*/
 f_flux = b_flux = 0.;
 Dca [ 0] += (b_flux =   ( - ( ica - ica_pmp_last ) * PI * diam / ( 2.0 * FARADAY ) ) );
 /*FLUX*/
  {int  _li ;for ( _li = 0 ; _li <= 4 - 2 ; _li ++ ) {
   /* ~ ca [ _li ] <-> ca [ _li + 1 ] ( DCa * _zfrat [ _li + 1 ] , DCa * _zfrat [ _li + 1 ] )*/
 f_flux =  DCa * _zfrat [ _li + 1 ] * ca [ _li] ;
 b_flux =  DCa * _zfrat [ _li + 1 ] * ca [ _li + 1] ;
 Dca [ _li] -= (f_flux - b_flux);
 Dca [ _li + 1] += (f_flux - b_flux);
 
 /*REACTION*/
  } }
 _zdsq = diam * diam ;
 {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
   _zdsqvol = _zdsq * vrat [ _li ] ;
   /* ~ ca [ _li ] + bufs [ _li ] <-> cabufs [ _li ] ( kfs * _zdsqvol , ( 0.001 ) * KDs * kfs * _zdsqvol )*/
 f_flux =  kfs * _zdsqvol * bufs [ _li] * ca [ _li] ;
 b_flux =  ( 0.001 ) * KDs * kfs * _zdsqvol * cabufs [ _li] ;
 Dbufs [ _li] -= (f_flux - b_flux);
 Dca [ _li] -= (f_flux - b_flux);
 Dcabufs [ _li] += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ ca [ _li ] + bapta [ _li ] <-> cabapta [ _li ] ( kfBAPTA * _zdsqvol , ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol )*/
 f_flux =  kfBAPTA * _zdsqvol * bapta [ _li] * ca [ _li] ;
 b_flux =  ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol * cabapta [ _li] ;
 Dbapta [ _li] -= (f_flux - b_flux);
 Dca [ _li] -= (f_flux - b_flux);
 Dcabapta [ _li] += (f_flux - b_flux);
 
 /*REACTION*/
  } }
 {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
   _zdsqvol = _zdsq * vrat [ _li ] ;
   /* ~ ca [ _li ] < < ( - _zdsqvol * beta * vmax * pow( ca [ _li ] , 2.0 ) / ( pow( ca [ _li ] , 2.0 ) + pow( Kp , 2.0 ) ) )*/
 f_flux = b_flux = 0.;
 Dca [ _li] += (b_flux =   ( - _zdsqvol * beta * vmax * pow( ca [ _li ] , 2.0 ) / ( pow( ca [ _li ] , 2.0 ) + pow( Kp , 2.0 ) ) ) );
 /*FLUX*/
  /* ~ hc [ _li ] <-> ho [ _li ] ( kon * Kinh , kon * ca [ _li ] )*/
 f_flux =  kon * Kinh * hc [ _li] ;
 b_flux =  kon * ca [ _li ] * ho [ _li] ;
 Dhc [ _li] -= (f_flux - b_flux);
 Dho [ _li] += (f_flux - b_flux);
 
 /*REACTION*/
  /* ~ ca [ _li ] < < ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) )*/
 f_flux = b_flux = 0.;
 Dca [ _li] += (b_flux =   ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) ) );
 /*FLUX*/
  /* ~ ca [ _li ] < < ( _zdsqvol * beta * L [ _li ] * ( 1.0 - ( ca [ _li ] / caer ) ) )*/
 f_flux = b_flux = 0.;
 Dca [ _li] += (b_flux =   ( _zdsqvol * beta * L [ _li ] * ( 1.0 - ( ca [ _li ] / caer ) ) ) );
 /*FLUX*/
  /* ~ ip3cas [ _li ] < < ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) )*/
 f_flux = b_flux = 0.;
 Dip3cas [ _li] += (b_flux =   ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) ) );
 /*FLUX*/
  } }
 jip3 = ( jmax * ( 1.0 - ( ca [ 0 ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ 0 ] / ( ca [ 0 ] + Kact ) ) * ho [ 0 ] ) , sites ) ) ;
 cip3 = ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ 0 ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ 0 ] / ( ca [ 0 ] + Kact ) ) * ho [ 0 ] ) , sites ) ) * ( 2.0 * FARADAY ) / ( PI * ( diam ) ) ;
 ip3ca = ip3cas [ 0 ] ;
 cai = ca [ 0 ] ;
 ca1 = ca [ 1 ] ;
 ca2 = ca [ 2 ] ;
 ca3 = ca [ 3 ] ;
 for (_i=0; _i < 4; _i++) { _p[_dlist1[_i + 4]] /= ( diam * diam * vrat [ ((int) _i ) ]);}
 for (_i=0; _i < 4; _i++) { _p[_dlist1[_i + 12]] /= ( diam * diam * vrat [ ((int) _i ) ]);}
 for (_i=0; _i < 4; _i++) { _p[_dlist1[_i + 16]] /= ( diam * diam * vrat [ ((int) _i ) ]);}
   } return _reset;
 }
 
/*CVODE matsol*/
 static int _ode_matsol1() {_reset=0;{
 double b_flux, f_flux, _term; int _i;
   b_flux = f_flux = 0.;
 {int _i; double _dt1 = 1.0/dt;
for(_i=0;_i<32;_i++){
  	_RHS1(_i) = _dt1*(_p[_dlist1[_i]]);
	_MATELM1(_i, _i) = _dt1;
      
} 
for (_i=0; _i < 4; _i++) {
  	_RHS1(_i + 4) *= ( diam * diam * vrat [ ((int) _i ) ]) ;
_MATELM1(_i + 4, _i + 4) *= ( diam * diam * vrat [ ((int) _i ) ]);  } 
for (_i=0; _i < 4; _i++) {
  	_RHS1(_i + 12) *= ( diam * diam * vrat [ ((int) _i ) ]) ;
_MATELM1(_i + 12, _i + 12) *= ( diam * diam * vrat [ ((int) _i ) ]);  } 
for (_i=0; _i < 4; _i++) {
  	_RHS1(_i + 16) *= ( diam * diam * vrat [ ((int) _i ) ]) ;
_MATELM1(_i + 16, _i + 16) *= ( diam * diam * vrat [ ((int) _i ) ]);  } }
 /* COMPARTMENT _li , diam * diam * vrat [ ((int) _i ) ] {
 ca bufs cabufs bufm cabufm }
 */
 /* COMPARTMENT volo {
 }
 */
 /* LONGITUDINAL_DIFFUSION _li , DCa * diam * diam * vrat [ ((int) _i ) ] {
 ca }
 */
 /* LONGITUDINAL_DIFFUSION _li , DBufm * diam * diam * vrat [ ((int) _i ) ] {
 bufm cabufm }
 */
 /* ~ ca [ 0 ] <-> sump ( ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) , ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) )*/
 _term =  ( 0.001 ) * parea * gamma * u ( _threadargscomma_ ca [ 0 ] / ( 1.0 ) , cath / ( 1.0 ) ) ;
 _MATELM1( 16 +  0 ,16 +  0)  += _term;
 /* ~ ca [ 0 ] < < ( - ( ica - ica_pmp_last ) * PI * diam / ( 2.0 * FARADAY ) )*/
 /*FLUX*/
  {int  _li ;for ( _li = 0 ; _li <= 4 - 2 ; _li ++ ) {
 /* ~ ca [ _li ] <-> ca [ _li + 1 ] ( DCa * _zfrat [ _li + 1 ] , DCa * _zfrat [ _li + 1 ] )*/
 _term =  DCa * _zfrat [ _li + 1 ] ;
 _MATELM1( 16 +  _li ,16 +  _li)  += _term;
 _MATELM1( 16 +  _li + 1 ,16 +  _li)  -= _term;
 _term =  DCa * _zfrat [ _li + 1 ] ;
 _MATELM1( 16 +  _li ,16 +  _li + 1)  -= _term;
 _MATELM1( 16 +  _li + 1 ,16 +  _li + 1)  += _term;
 /*REACTION*/
  } }
 _zdsq = diam * diam ;
 {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
 _zdsqvol = _zdsq * vrat [ _li ] ;
 /* ~ ca [ _li ] + bufs [ _li ] <-> cabufs [ _li ] ( kfs * _zdsqvol , ( 0.001 ) * KDs * kfs * _zdsqvol )*/
 _term =  kfs * _zdsqvol * ca [ _li] ;
 _MATELM1( 4 +  _li ,4 +  _li)  += _term;
 _MATELM1( 16 +  _li ,4 +  _li)  += _term;
 _MATELM1( 12 +  _li ,4 +  _li)  -= _term;
 _term =  kfs * _zdsqvol * bufs [ _li] ;
 _MATELM1( 4 +  _li ,16 +  _li)  += _term;
 _MATELM1( 16 +  _li ,16 +  _li)  += _term;
 _MATELM1( 12 +  _li ,16 +  _li)  -= _term;
 _term =  ( 0.001 ) * KDs * kfs * _zdsqvol ;
 _MATELM1( 4 +  _li ,12 +  _li)  -= _term;
 _MATELM1( 16 +  _li ,12 +  _li)  -= _term;
 _MATELM1( 12 +  _li ,12 +  _li)  += _term;
 /*REACTION*/
  /* ~ ca [ _li ] + bapta [ _li ] <-> cabapta [ _li ] ( kfBAPTA * _zdsqvol , ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol )*/
 _term =  kfBAPTA * _zdsqvol * ca [ _li] ;
 _MATELM1( 0 +  _li ,0 +  _li)  += _term;
 _MATELM1( 16 +  _li ,0 +  _li)  += _term;
 _MATELM1( 8 +  _li ,0 +  _li)  -= _term;
 _term =  kfBAPTA * _zdsqvol * bapta [ _li] ;
 _MATELM1( 0 +  _li ,16 +  _li)  += _term;
 _MATELM1( 16 +  _li ,16 +  _li)  += _term;
 _MATELM1( 8 +  _li ,16 +  _li)  -= _term;
 _term =  ( 0.001 ) * KDBAPTA * kfBAPTA * _zdsqvol ;
 _MATELM1( 0 +  _li ,8 +  _li)  -= _term;
 _MATELM1( 16 +  _li ,8 +  _li)  -= _term;
 _MATELM1( 8 +  _li ,8 +  _li)  += _term;
 /*REACTION*/
  } }
 {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
 _zdsqvol = _zdsq * vrat [ _li ] ;
 /* ~ ca [ _li ] < < ( - _zdsqvol * beta * vmax * pow( ca [ _li ] , 2.0 ) / ( pow( ca [ _li ] , 2.0 ) + pow( Kp , 2.0 ) ) )*/
 /*FLUX*/
  /* ~ hc [ _li ] <-> ho [ _li ] ( kon * Kinh , kon * ca [ _li ] )*/
 _term =  kon * Kinh ;
 _MATELM1( 24 +  _li ,24 +  _li)  += _term;
 _MATELM1( 20 +  _li ,24 +  _li)  -= _term;
 _term =  kon * ca [ _li ] ;
 _MATELM1( 24 +  _li ,20 +  _li)  -= _term;
 _MATELM1( 20 +  _li ,20 +  _li)  += _term;
 /*REACTION*/
  /* ~ ca [ _li ] < < ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) )*/
 /*FLUX*/
  /* ~ ca [ _li ] < < ( _zdsqvol * beta * L [ _li ] * ( 1.0 - ( ca [ _li ] / caer ) ) )*/
 /*FLUX*/
  /* ~ ip3cas [ _li ] < < ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) )*/
 /*FLUX*/
  } }
 jip3 = ( jmax * ( 1.0 - ( ca [ 0 ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ 0 ] / ( ca [ 0 ] + Kact ) ) * ho [ 0 ] ) , sites ) ) ;
 cip3 = ( _zdsqvol * alpha * jmax * ( 1.0 - ( ca [ 0 ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ 0 ] / ( ca [ 0 ] + Kact ) ) * ho [ 0 ] ) , sites ) ) * ( 2.0 * FARADAY ) / ( PI * ( diam ) ) ;
 ip3ca = ip3cas [ 0 ] ;
 cai = ca [ 0 ] ;
 ca1 = ca [ 1 ] ;
 ca2 = ca [ 2 ] ;
 ca3 = ca [ 3 ] ;
   } return _reset;
 }
 
/*CVODE end*/
 
static int _ode_count(int _type){ return 32;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cao = _ion_cao;
  ica = _ion_ica;
  cai = _ion_cai;
     _ode_spec1 ();
  _ion_cai = cai;
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 32; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 static void _ode_synonym(int _cnt, double** _pp, Datum** _ppd) { 
 	int _i; 
	for (_i=0; _i < _cnt; ++_i) {_p = _pp[_i]; _ppvar = _ppd[_i];
 _ion_cai =  ca [ 0 ] ;
 }}
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _cvode_sparse(&_cvsparseobj1, 32, _dlist1, _p, _ode_matsol1, &_coef1);
 }
 
static void _ode_matsol(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cao = _ion_cao;
  ica = _ion_ica;
  cai = _ion_cai;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_ca_sym, _ppvar, 0, 2);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 2, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 3, 4);
 }
 static void* _difspace1;
extern double nrn_nernst_coef();
static double _difcoef1(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, NrnThread* _nt) {
   *_pdvol =  diam * diam * vrat [ ((int) _i ) ] ;
 if (_i ==  0) {
  *_pdfcdc = nrn_nernst_coef(_type_ica)*( ( - ( _ion_dicadv  - ica_pmp_last ) * PI * diam / ( 2.0 * FARADAY ) ));
 }else{ *_pdfcdc=0.;}
   return DCa * diam * diam * vrat [ ((int) _i ) ] ;
}
 static void* _difspace2;
extern double nrn_nernst_coef();
static double _difcoef2(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, NrnThread* _nt) {
   *_pdvol =  diam * diam * vrat [ ((int) _i ) ] ; *_pdfcdc=0.;
   return DBufm * diam * diam * vrat [ ((int) _i ) ] ;
}
 static void* _difspace3;
extern double nrn_nernst_coef();
static double _difcoef3(int _i, double* _p, Datum* _ppvar, double* _pdvol, double* _pdfcdc, Datum* _thread, NrnThread* _nt) {
   *_pdvol =  diam * diam * vrat [ ((int) _i ) ] ; *_pdfcdc=0.;
   return DBufm * diam * diam * vrat [ ((int) _i ) ] ;
}
 static void _difusfunc(ldifusfunc2_t _f, NrnThread* _nt) {int _i;
  for (_i=0; _i < 4; ++_i) (*_f)(_mechtype, _difcoef1, &_difspace1, _i,  12, 69 , _nt);
  for (_i=0; _i < 4; ++_i) (*_f)(_mechtype, _difcoef2, &_difspace2, _i,  32, 89 , _nt);
  for (_i=0; _i < 4; ++_i) (*_f)(_mechtype, _difcoef3, &_difspace3, _i,  36, 93 , _nt);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
 for (_i=0; _i<4; _i++) bapta[_i] = bapta0;
 for (_i=0; _i<4; _i++) bufm[_i] = bufm0;
 for (_i=0; _i<4; _i++) bufs[_i] = bufs0;
 for (_i=0; _i<4; _i++) cabapta[_i] = cabapta0;
 for (_i=0; _i<4; _i++) cabufm[_i] = cabufm0;
 for (_i=0; _i<4; _i++) cabufs[_i] = cabufs0;
 for (_i=0; _i<4; _i++) ca[_i] = ca0;
 for (_i=0; _i<4; _i++) ho[_i] = ho0;
 for (_i=0; _i<4; _i++) hc[_i] = hc0;
 for (_i=0; _i<4; _i++) ip3cas[_i] = ip3cas0;
 {
   if ( _zfactors_done  == 0.0 ) {
     _zfactors_done = 1.0 ;
     factors ( _threadargs_ ) ;
     }
   cai = cai0 ;
   jip3 = 0.0 ;
   bufs_0 = KDs * TBufs / ( KDs + ( 1000.0 ) * cai0 ) ;
   bufm_0 = KDm * TBufm / ( KDm + ( 1000.0 ) * cai0 ) ;
   bapta_0 = KDBAPTA * TBufBAPTA / ( KDBAPTA + ( 1000.0 ) * cai0 ) ;
   {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
     ca [ _li ] = cai ;
     bufs [ _li ] = bufs_0 ;
     cabufs [ _li ] = TBufs - bufs_0 ;
     bapta [ _li ] = bapta_0 ;
     cabapta [ _li ] = TBufBAPTA - bapta_0 ;
     bufm [ _li ] = bufm_0 ;
     cabufm [ _li ] = TBufm - bufm_0 ;
     } }
   ica = 0.0 ;
   ica_pmp = 0.0 ;
   ica_pmp_last = 0.0 ;
   {int  _li ;for ( _li = 0 ; _li <= 4 - 1 ; _li ++ ) {
     ho [ _li ] = Kinh / ( ca [ _li ] + Kinh ) ;
     hc [ _li ] = 1.0 - ho [ _li ] ;
     _zjx = ( - vmax * pow( ca [ _li ] , 2.0 ) / ( pow( ca [ _li ] , 2.0 ) + pow( Kp , 2.0 ) ) ) ;
     _zjx = _zjx + jmax * ( 1.0 - ( ca [ _li ] / caer ) ) * pow( ( ( ip3i / ( ip3i + Kip3 ) ) * ( ca [ _li ] / ( ca [ _li ] + Kact ) ) * ho [ _li ] ) , sites ) ;
     L [ _li ] = - _zjx / ( 1.0 - ( ca [ _li ] / caer ) ) ;
     } }
   sump = cath ;
   parea = PI * diam ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
  cao = _ion_cao;
  ica = _ion_ica;
  cai = _ion_cai;
 initmodel();
  _ion_cai = cai;
   nrn_wrote_conc(_ca_sym, (&(_ion_cai)) - 1, _style_ca);
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ica_pmp_last = ica_pmp ;
   ica = ica_pmp ;
   }
 _current += ica;

} return _current;
}

static void nrn_cur(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
  cao = _ion_cao;
  ica = _ion_ica;
  cai = _ion_cai;
if (_nt->_vcv) { _ode_spec1(); }
 _g = _nrn_current(_v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_cai = cai;
  _ion_ica += ica ;
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}}

static void nrn_jacob(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}}

static void nrn_state(NrnThread* _nt, _Memb_list* _ml, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
double _dtsav = dt;
if (secondorder) { dt *= 0.5; }
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
  cao = _ion_cao;
  ica = _ion_ica;
  cai = _ion_cai;
 { error = sparse(&_sparseobj1, 32, _slist1, _dlist1, _p, &t, dt, state,&_coef1, _linmat1);
 if(error){fprintf(stderr,"at line 104 in file cal4.mod:\n     	SOLVE state METHOD sparse\n"); nrn_complain(_p); abort_run(error);}
    if (secondorder) {
    int _i;
    for (_i = 0; _i < 32; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }  _ion_cai = cai;
 }}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 for(_i=0;_i<4;_i++){_slist1[0+_i] = bapta_columnindex + _i;  _dlist1[0+_i] = Dbapta_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[4+_i] = bufs_columnindex + _i;  _dlist1[4+_i] = Dbufs_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[8+_i] = cabapta_columnindex + _i;  _dlist1[8+_i] = Dcabapta_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[12+_i] = cabufs_columnindex + _i;  _dlist1[12+_i] = Dcabufs_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[16+_i] = ca_columnindex + _i;  _dlist1[16+_i] = Dca_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[20+_i] = ho_columnindex + _i;  _dlist1[20+_i] = Dho_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[24+_i] = hc_columnindex + _i;  _dlist1[24+_i] = Dhc_columnindex + _i;}
 for(_i=0;_i<4;_i++){_slist1[28+_i] = ip3cas_columnindex + _i;  _dlist1[28+_i] = Dip3cas_columnindex + _i;}
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/mnt/h/Thesis work/Compilations/ExistingModels/Combe2023/267599/cholinergic_shift_generalize/cal4.mod";
static const char* nmodl_file_text = 
  ":Modified from NEURON implementation of Fink et al., 2000\n"
  "\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX cal4\n"
  "	USEION ca READ cao,  ica WRITE cai, ica\n"
  "	:USEION ip3 READ ip3i VALENCE 1\n"
  "	RANGE ica_pmp,ca1, ca2,alpha,beta,ca3,gamma,ip3ca, DCa,jip3, cip3, sites\n"
  " 	GLOBAL vrat, TBufs, KDs, TBufs, TBufm, KDm, KDBAPTA, TBufBAPTA\n"
  "}\n"
  "\n"
  "DEFINE Nannuli 4\n"
  "\n"
  "UNITS {\n"
  "	(mol)	= (1)\n"
  " 	(molar) = (1/liter)\n"
  "  	(uM)    = (micromolar)\n"
  "  	(mM)    = (millimolar)\n"
  "  	(um)    = (micron)\n"
  "  	(mA)    = (milliamp)\n"
  "  	FARADAY = (faraday)  (10000 coulomb)\n"
  "  	PI      = (pi)       (1)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	ip3i = 10e-3 (mM):10e-3 for cal wave 0.16 baseline 16 for noND\n"
  "	cai0 = 50e-6(mM)\n"
  "	:caoc = 2 (mM)\n"
  "	cath = 0.2e-3 (mM) : threshold for ca pump activity\n"
  "	gamma = 8 (um/s) : ca pump flux density\n"
  "	jmax = 3.5e-3 (mM/ms) :3.5e-3\n"
  "	caer = 0.400 (mM)\n"
  "	Kip3 = 0.8e-3 (mM)\n"
  "	Kact = 0.7e-3 (mM)\n"
  "	kon = 2.7 (/mM-ms) :2.7\n"
  "	Kinh = 0.6e-3 (mM)\n"
  "	sites=3\n"
  "	alpha = 1 (1) : relative abundance of ER mechanisms : alpha only specific for ip3 receptor,\n"
  "	beta  = 1(1)           :introducing beta to take care of other ER mechanisms(SERCA and leak channel density)\n"
  "\n"
  "	vmax =1e-4   (mM/ms) :1e-4 revised\n"
  "	Kp = 0.27e-3 (mM)	:0.27e-3\n"
  "	DCa = 0.22 (um2/ms) :Fink et al 2000\n"
  "	TBufs = 0.45 (mM)\n"
  "        kfs = 1000 (/mM-ms) : try these for now\n"
  "        KDs = 10 (uM)\n"
  "    TBufBAPTA = 0 (mM) :10 uM for concentration of BAPTA\n"
  "        kfBAPTA = 500 (/mM-ms) : try these for now\n"
  "        KDBAPTA = 0.2 (uM)	:KD is 0.2uM\n"
  "	TBufm = 0.075 (mM)\n"
  "	kfm = 1000 (/mM-ms) : try these for now\n"
  "        KDm = 0.24 (uM)\n"
  "        DBufm = 0.050 (um2/ms)\n"
  "\n"
  "\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	diam      (um)\n"
  "	cip3		(mA/cm2)\n"
  "  	ica       (mA/cm2)\n"
  "        cai       (mM)\n"
  "	jip3	  (mM/ms)\n"
  "        ca1	  (mM)\n"
  "        ca2       (mM)\n"
  "        ca3       (mM)\n"
  "        ica_pmp   (mA/cm2)\n"
  "	ica_pmp_last   (mA/cm2)\n"
  "        parea     (um)    :pump area peer unit length\n"
  "        sump      (mM)\n"
  "        cao       (mM)\n"
  "        :ip3i      (mM)\n"
  "        jchnl    (mM/ms)\n"
  "        vrat[Nannuli]  (1)\n"
  "	L[Nannuli] (mM/ms)  adjusted so that\n"
  "                         : jchnl + jpump + jleak = 0  when  ca = 0.05 uM and h = Kinh/(ca + Kinh)\n"
  "        bufs_0 (mM)\n"
  "	bufm_0 (mM)\n"
  "	bapta_0 (mM)\n"
  "	\n"
  "	ip3ca	(mM)\n"
  "} \n"
  "\n"
  "\n"
  "CONSTANT { volo = 1e10 (um2) }\n"
  "\n"
  "STATE {\n"
  "     	ca[Nannuli]     (mM) <1e-7>\n"
  "     	hc[Nannuli]    \n"
  "     	ho[Nannuli]\n"
  "     	bufs[Nannuli]    (mM) <1e-3>\n"
  "     	cabufs[Nannuli]  (mM) <1e-7>\n"
  "	bufm[Nannuli]    (mM) <1e-4>\n"
  "        cabufm[Nannuli]  (mM) <1e-8>\n"
  "        bapta[Nannuli]    (mM) <1e-3>\n"
  "     	cabapta[Nannuli]  (mM) <1e-7>\n"
  "	ip3cas [Nannuli] (mM)\n"
  "\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "BREAKPOINT {\n"
  "     	SOLVE state METHOD sparse\n"
  "     	ica_pmp_last = ica_pmp\n"
  "     	ica = ica_pmp\n"
  "\n"
  "}\n"
  "LOCAL factors_done, jx\n"
  "INITIAL {\n"
  "	\n"
  "    	if (factors_done==0) {\n"
  "		factors_done= 1\n"
  "		factors()\n"
  "    	}\n"
  " \n"
  "        cai = cai0\n"
  "	jip3=0\n"
  "	bufs_0 = KDs*TBufs/(KDs + (1000)*cai0)\n"
  "	bufm_0 = KDm*TBufm/(KDm + (1000)*cai0)\n"
  "	bapta_0 = KDBAPTA*TBufBAPTA/(KDBAPTA + (1000)*cai0)\n"
  "\n"
  "	FROM i=0 TO Nannuli-1 {    \n"
  "     		ca[i] = cai\n"
  "		bufs[i] = bufs_0\n"
  "       		cabufs[i] = TBufs - bufs_0\n"
  "       	bapta[i] = bapta_0\n"
  "       		cabapta[i] = TBufBAPTA - bapta_0\n"
  "		bufm[i] = bufm_0\n"
  "    		cabufm[i] = TBufm - bufm_0\n"
  "\n"
  "   	}\n"
  "	\n"
  "   	ica=0\n"
  "   	ica_pmp = 0 \n"
  "   	ica_pmp_last = 0\n"
  "\n"
  "\n"
  "	FROM i=0 TO Nannuli-1 {\n"
  "    		ho[i] = Kinh/(ca[i]+Kinh)\n"
  "    		hc[i] = 1-ho[i]\n"
  "    		jx = (-vmax*ca[i]^2 / (ca[i]^2 + Kp^2))\n"
  "    		jx = jx + jmax*(1-(ca[i]/caer)) * ( (ip3i/(ip3i+Kip3)) * (ca[i]/(ca[i]+Kact)) * ho[i] )^sites\n"
  "     	   	L[i] = -jx/(1 - (ca[i]/caer))\n"
  "    	}\n"
  "\n"
  "    	sump = cath\n"
  "    	parea = PI*diam   \n"
  "}\n"
  "\n"
  "LOCAL frat[Nannuli]\n"
  "\n"
  "PROCEDURE factors() {\n"
  "	LOCAL r, dr2\n"
  "  	r = 1/2                : starts at edge (half diam)\n"
  "  	dr2 = r/(Nannuli-1)/2  : full thickness of outermost annulus,\n"
  "                               : half thickness of all other annuli\n"
  "  	vrat[0] = 0\n"
  "  	frat[0] = 2*r\n"
  "\n"
  "  	FROM i=0 TO Nannuli-2 {\n"
  "    		vrat[i] = vrat[i] + PI*(r-dr2/2)*2*dr2  : interior half\n"
  "   		 r = r - dr2\n"
  "   		 frat[i+1] = 2*PI*r/(2*dr2)  : outer radius of annulus\n"
  "                                             : div by distance between centers\n"
  "   		 r = r - dr2\n"
  "    		vrat[i+1] = PI*(r+dr2/2)*2*dr2  : outer half of annulus\n"
  "  	}\n"
  "}\n"
  "\n"
  "\n"
  "LOCAL dsq, dsqvol\n"
  "\n"
  "KINETIC state {\n"
  "  	COMPARTMENT i, diam*diam*vrat[i] {ca  bufs cabufs bufm cabufm sump}\n"
  "  	COMPARTMENT volo {cao}\n"
  "  	LONGITUDINAL_DIFFUSION i, DCa*diam*diam*vrat[i] {ca}\n"
  "  	LONGITUDINAL_DIFFUSION i, DBufm*diam*diam*vrat[i] {bufm cabufm}\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "        :cell membrane ca pump\n"
  "  	~ ca[0] <-> sump  ((0.001)*parea*gamma*u(ca[0]/(1 (mM)), cath/(1 (mM))), (0.001)*parea*gamma*u(ca[0]/(1 (mM)), cath/(1 (mM))))\n"
  "  	ica_pmp = 2*FARADAY*(f_flux - b_flux)/parea\n"
  "\n"
  "  	: all currents except cell membrane ca pump\n"
  "  	~ ca[0] << (-(ica - ica_pmp_last)*PI*diam/(2*FARADAY))  : ica is Ca efflux\n"
  "\n"
  " 	 : radial diffusion\n"
  "   	FROM i=0 TO Nannuli-2 {\n"
  "   		~ ca[i] <-> ca[i+1] (DCa*frat[i+1], DCa*frat[i+1])\n"
  " 	}\n"
  "\n"
  "	: buffering\n"
  "   	dsq = diam*diam\n"
  "   \n"
  "   	FROM i=0 TO Nannuli-1 {\n"
  "	 	dsqvol = dsq*vrat[i]\n"
  "     	 	~ ca[i] + bufs[i] <-> cabufs[i]  (kfs*dsqvol, (0.001)*KDs*kfs*dsqvol)\n"
  "     	 	~ ca[i] + bapta[i] <-> cabapta[i]  (kfBAPTA*dsqvol, (0.001)*KDBAPTA*kfBAPTA*dsqvol)\n"
  "		:~ ca[i] + bufm[i] <-> cabufm[i]  (kfm*dsqvol, (0.001)*KDm*kfm*dsqvol) :to simulate high affinity dyes, used only for the simplified 3 cylinder model in the paper\n"
  "\n"
  "    	}\n"
  "\n"
  "\n"
  "       	:SERCA pump, channel\n"
  "  	FROM i=0 TO Nannuli-1 {\n"
  "    		dsqvol = dsq*vrat[i]\n"
  "\n"
  "   	 	: pump\n"
  "   	 	~ ca[i] << (-dsqvol*beta*vmax*ca[i]^2 / (ca[i]^2 + Kp^2))\n"
  "\n"
  "    		: channel\n"
  "   	 	~ hc[i] <-> ho[i]  (kon*Kinh, kon*ca[i])\n"
  "   	 	~ ca[i] << ( dsqvol*alpha*jmax*(1-(ca[i]/caer)) * ( (ip3i/(ip3i+Kip3)) * (ca[i]/(ca[i]+Kact)) * ho[i] )^sites )\n"
  " 	 	: leak\n"
  "   	 	~ ca[i] << (dsqvol*beta*L[i]*(1 - (ca[i]/caer)))\n"
  "		~ ip3cas[i] << (dsqvol*alpha*jmax*(1-(ca[i]/caer)) * ( (ip3i/(ip3i+Kip3)) * (ca[i]/(ca[i]+Kact)) * ho[i] )^sites )\n"
  "  	}\n"
  "	\n"
  "	jip3 = (jmax*(1-(ca[0]/caer)) * ( (ip3i/(ip3i+Kip3)) * (ca[0]/(ca[0]+Kact)) * ho[0] )^sites ) \n"
  "	: turn this into a current ican can read\n"
  "	:make the diam small assuming its only being released into certain parts\n"
  "	cip3 = ( dsqvol*alpha*jmax*(1-(ca[0]/caer)) * ( (ip3i/(ip3i+Kip3)) * (ca[0]/(ca[0]+Kact)) * ho[0] )^sites )*(2*FARADAY)/(PI*(diam))\n"
  "\n"
  ":	ip3ca=0\n"
  ":	FROM i=0 TO Nannuli-1 {\n"
  ":		ip3ca=ip3ca+ip3cas[i]\n"
  ":	}\n"
  "\n"
  "	ip3ca=ip3cas[0]\n"
  "\n"
  "  	cai = ca[0]\n"
  "  	ca1 = ca[1]\n"
  "  	ca2 = ca[2]\n"
  "  	ca3 = ca[3]\n"
  "}\n"
  "\n"
  "\n"
  "FUNCTION u (x, th) {\n"
  "  	if (x>th) {\n"
  "    		u = 1\n"
  "  	} else {\n"
  "    		u = 0\n"
  "  	}\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
