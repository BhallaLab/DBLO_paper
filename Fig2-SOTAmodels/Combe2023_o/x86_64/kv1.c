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
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__Kv1
#define _nrn_initial _nrn_initial__Kv1
#define nrn_cur _nrn_cur__Kv1
#define _nrn_current _nrn_current__Kv1
#define nrn_jacob _nrn_jacob__Kv1
#define nrn_state _nrn_state__Kv1
#define _net_receive _net_receive__Kv1 
#define rates rates__Kv1 
#define states states__Kv1 
 
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
#define gbar _p[0]
#define gbar_columnindex 0
#define ik _p[1]
#define ik_columnindex 1
#define gk _p[2]
#define gk_columnindex 2
#define n _p[3]
#define n_columnindex 3
#define ek _p[4]
#define ek_columnindex 4
#define alphan _p[5]
#define alphan_columnindex 5
#define betan _p[6]
#define betan_columnindex 6
#define qt _p[7]
#define qt_columnindex 7
#define Dn _p[8]
#define Dn_columnindex 8
#define _g _p[9]
#define _g_columnindex 9
#define _ion_ek	*_ppvar[0]._pval
#define _ion_ik	*_ppvar[1]._pval
#define _ion_dikdv	*_ppvar[2]._pval
 
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
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_alphanfkt(void);
 static void _hoc_betanfkt(void);
 static void _hoc_rates(void);
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
 "setdata_Kv1", _hoc_setdata,
 "alphanfkt_Kv1", _hoc_alphanfkt,
 "betanfkt_Kv1", _hoc_betanfkt,
 "rates_Kv1", _hoc_rates,
 0, 0
};
#define alphanfkt alphanfkt_Kv1
#define betanfkt betanfkt_Kv1
 extern double alphanfkt( double );
 extern double betanfkt( double );
 /* declare global and static user variables */
#define ninf ninf_Kv1
 double ninf = 0;
#define taun taun_Kv1
 double taun = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "gbar_Kv1", 0, 1e+09,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "taun_Kv1", "ms",
 "gbar_Kv1", "mho/cm2",
 "ik_Kv1", "mA/cm2",
 "gk_Kv1", "mho/cm2",
 0,0
};
 static double delta_t = 0.01;
 static double n0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "ninf_Kv1", &ninf_Kv1,
 "taun_Kv1", &taun_Kv1,
 0,0
};
 static DoubVec hoc_vdoub[] = {
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
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"Kv1",
 "gbar_Kv1",
 0,
 "ik_Kv1",
 "gk_Kv1",
 0,
 "n_Kv1",
 0,
 0};
 static Symbol* _k_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 10, _prop);
 	/*initialize range parameters*/
 	gbar = 0.011;
 	_prop->param = _p;
 	_prop->param_size = 10;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0]._pval = &prop_ion->param[0]; /* ek */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ik */
 	_ppvar[2]._pval = &prop_ion->param[4]; /* _ion_dikdv */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _kv1_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("k", -10000.);
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 10, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 Kv1 /mnt/h/Thesis work/Compilations/ExistingModels/Combe2023/267599/cholinergic_shift_generalize/kv1.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double q10 = 3;
 static double ca = 0.12889;
 static double cva = 45;
 static double cka = -33.90877;
 static double cb = 0.12889;
 static double cvb = 45;
 static double ckb = 12.42101;
static int _reset;
static char *modelname = "Voltage-gated low threshold potassium current from Kv1 subunits";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[1], _dlist1[1];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
   Dn = ( ninf - n ) / taun ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 rates ( _threadargscomma_ v ) ;
 Dn = Dn  / (1. - dt*( ( ( ( - 1.0 ) ) ) / taun )) ;
  return 0;
}
 /*END CVODE*/
 static int states () {_reset=0;
 {
   rates ( _threadargscomma_ v ) ;
    n = n + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / taun)))*(- ( ( ( ninf ) ) / taun ) / ( ( ( ( - 1.0 ) ) ) / taun ) - n) ;
   }
  return 0;
}
 
static int  rates (  double _lv ) {
   alphan = alphanfkt ( _threadargscomma_ _lv ) ;
   betan = betanfkt ( _threadargscomma_ _lv ) ;
   ninf = alphan / ( alphan + betan ) ;
   taun = 1.0 / ( qt * ( alphan + betan ) ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
   _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double alphanfkt (  double _lv ) {
   double _lalphanfkt;
 _lalphanfkt = ca * exp ( - ( _lv + cva ) / cka ) ;
   
return _lalphanfkt;
 }
 
static void _hoc_alphanfkt(void) {
  double _r;
   _r =  alphanfkt (  *getarg(1) );
 hoc_retpushx(_r);
}
 
double betanfkt (  double _lv ) {
   double _lbetanfkt;
 _lbetanfkt = cb * exp ( - ( _lv + cvb ) / ckb ) ;
   
return _lbetanfkt;
 }
 
static void _hoc_betanfkt(void) {
  double _r;
   _r =  betanfkt (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 1;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  ek = _ion_ek;
     _ode_spec1 ();
  }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 1; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 ();
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
  ek = _ion_ek;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_k_sym, _ppvar, 0, 0);
   nrn_update_ion_pointer(_k_sym, _ppvar, 1, 3);
   nrn_update_ion_pointer(_k_sym, _ppvar, 2, 4);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  n = n0;
 {
   qt = pow( q10 , ( ( celsius - 22.0 ) / 10.0 ) ) ;
   rates ( _threadargscomma_ v ) ;
   n = ninf ;
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
  ek = _ion_ek;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   gk = gbar * pow( n , 4.0 ) ;
   ik = gk * ( v - ek ) ;
   }
 _current += ik;

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
  ek = _ion_ek;
 _g = _nrn_current(_v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g - _rhs)/.001;
  _ion_ik += ik ;
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
  ek = _ion_ek;
 { error =  states();
 if(error){fprintf(stderr,"at line 90 in file kv1.mod:\n	SOLVE states METHOD cnexp\n"); nrn_complain(_p); abort_run(error);}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = n_columnindex;  _dlist1[0] = Dn_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/mnt/h/Thesis work/Compilations/ExistingModels/Combe2023/267599/cholinergic_shift_generalize/kv1.mod";
static const char* nmodl_file_text = 
  "TITLE Voltage-gated low threshold potassium current from Kv1 subunits\n"
  "\n"
  "COMMENT\n"
  "\n"
  "NEURON implementation of a potassium channel from Kv1.1 subunits\n"
  "Kinetical scheme: Hodgkin-Huxley m^4, no inactivation\n"
  "\n"
  "Kinetic data taken from: Zerr et al., J.Neurosci. 18 (1998) 2842\n"
  "Vhalf = -28.8 +/- 2.3 mV; k = 8.1 +/- 0.9 mV\n"
  "\n"
  "The voltage dependency of the rate constants was approximated by:\n"
  "\n"
  "alpha = ca * exp(-(v+cva)/cka)\n"
  "beta = cb * exp(-(v+cvb)/ckb)\n"
  "\n"
  "Parameters ca, cva, cka, cb, cvb, ckb\n"
  "are defined in the CONSTANT block.\n"
  "\n"
  "Laboratory for Neuronal Circuit Dynamics\n"
  "RIKEN Brain Science Institute, Wako City, Japan\n"
  "http://www.neurodynamics.brain.riken.jp\n"
  "\n"
  "Reference: Akemann and Knoepfel, J.Neurosci. 26 (2006) 4602\n"
  "Date of Implementation: April 2005\n"
  "Contact: akemann@brain.riken.jp\n"
  "\n"
  "ENDCOMMENT\n"
  "\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX Kv1\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gk, gbar, ik\n"
  "	GLOBAL ninf, taun\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mV) = (millivolt)\n"
  "	(mA) = (milliamp)\n"
  "	(nA) = (nanoamp)\n"
  "	(pA) = (picoamp)\n"
  "	(S)  = (siemens)\n"
  "	(nS) = (nanosiemens)\n"
  "	(pS) = (picosiemens)\n"
  "	(um) = (micron)\n"
  "	(molar) = (1/liter)\n"
  "	(mM) = (millimolar)		\n"
  "}\n"
  "\n"
  "CONSTANT {\n"
  "	q10 = 3\n"
  "\n"
  "	ca = 0.12889 (1/ms)\n"
  "	cva = 45 (mV)\n"
  "	cka = -33.90877 (mV)\n"
  "\n"
  "	cb = 0.12889 (1/ms)\n"
  "      cvb = 45 (mV)\n"
  "	ckb = 12.42101 (mV)         \n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	v (mV)\n"
  "	celsius (degC)\n"
  "	\n"
  "	gbar = 0.011 (mho/cm2)   <0,1e9>\n"
  "}\n"
  "\n"
  "\n"
  "ASSIGNED {\n"
  " 	ik (mA/cm2) \n"
  "	ek (mV)\n"
  "	gk  (mho/cm2)\n"
  "	ninf\n"
  "	taun (ms)\n"
  "	alphan (1/ms)\n"
  "	betan (1/ms)\n"
  "	qt\n"
  "}\n"
  "\n"
  "STATE { n }\n"
  "\n"
  "INITIAL {\n"
  "	qt = q10^((celsius-22 (degC))/10 (degC))\n"
  "	rates(v)\n"
  "	n = ninf\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states METHOD cnexp\n"
  "      gk = gbar * n^4 \n"
  "	ik = gk * (v - ek)\n"
  "}\n"
  "\n"
  "DERIVATIVE states {\n"
  "	rates(v)\n"
  "	n' = (ninf-n)/taun \n"
  "}\n"
  "\n"
  "PROCEDURE rates(v (mV)) {\n"
  "	alphan = alphanfkt(v)\n"
  "	betan = betanfkt(v)\n"
  "	ninf = alphan/(alphan+betan) \n"
  "	taun = 1/(qt*(alphan + betan))       \n"
  "}\n"
  "\n"
  "FUNCTION alphanfkt(v (mV)) (1/ms) {\n"
  "	alphanfkt = ca * exp(-(v+cva)/cka) \n"
  "}\n"
  "\n"
  "FUNCTION betanfkt(v (mV)) (1/ms) {\n"
  "	betanfkt = cb * exp(-(v+cvb)/ckb)\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
