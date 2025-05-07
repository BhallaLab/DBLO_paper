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
 
#define nrn_init _nrn_init__ican
#define _nrn_initial _nrn_initial__ican
#define nrn_cur _nrn_cur__ican
#define _nrn_current _nrn_current__ican
#define nrn_jacob _nrn_jacob__ican
#define nrn_state _nrn_state__ican
#define _net_receive _net_receive__ican 
#define evaluate_fct evaluate_fct__ican 
#define states states__ican 
 
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
#define depth _p[0]
#define depth_columnindex 0
#define taur _p[1]
#define taur_columnindex 1
#define erev _p[2]
#define erev_columnindex 2
#define gbar _p[3]
#define gbar_columnindex 3
#define taumin _p[4]
#define taumin_columnindex 4
#define concrelease _p[5]
#define concrelease_columnindex 5
#define itrpm4 _p[6]
#define itrpm4_columnindex 6
#define can _p[7]
#define can_columnindex 7
#define Po _p[8]
#define Po_columnindex 8
#define cai _p[9]
#define cai_columnindex 9
#define ica _p[10]
#define ica_columnindex 10
#define Dcan _p[11]
#define Dcan_columnindex 11
#define DPo _p[12]
#define DPo_columnindex 12
#define ican _p[13]
#define ican_columnindex 13
#define drive_channel _p[14]
#define drive_channel_columnindex 14
#define Po_inf _p[15]
#define Po_inf_columnindex 15
#define Tau _p[16]
#define Tau_columnindex 16
#define _g _p[17]
#define _g_columnindex 17
#define _ion_cai	*_ppvar[0]._pval
#define _ion_ica	*_ppvar[1]._pval
#define jip3p	*_ppvar[2]._pval
#define _p_jip3p	_ppvar[2]._pval
#define diam	*_ppvar[3]._pval
 
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
 static int hoc_nrnpointerindex =  2;
 /* external NEURON variables */
 /* declaration of user functions */
 static void _hoc_MyExp(void);
 static void _hoc_evaluate_fct(void);
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
 "setdata_ican", _hoc_setdata,
 "MyExp_ican", _hoc_MyExp,
 "evaluate_fct_ican", _hoc_evaluate_fct,
 0, 0
};
#define MyExp MyExp_ican
 extern double MyExp( double );
 /* declare global and static user variables */
#define Kd Kd_ican
 double Kd = 0.087;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Kd_ican", "mM",
 "depth_ican", "um",
 "taur_ican", "ms",
 "erev_ican", "mV",
 "gbar_ican", "mho/cm2",
 "taumin_ican", "ms",
 "can_ican", "mM",
 "itrpm4_ican", "mA/cm2",
 "jip3p_ican", "mM/ms",
 0,0
};
 static double Po0 = 0;
 static double can0 = 0;
 static double delta_t = 1;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "Kd_ican", &Kd_ican,
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
 
#define _cvode_ieq _ppvar[4]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"ican",
 "depth_ican",
 "taur_ican",
 "erev_ican",
 "gbar_ican",
 "taumin_ican",
 "concrelease_ican",
 0,
 "itrpm4_ican",
 0,
 "can_ican",
 "Po_ican",
 0,
 "jip3p_ican",
 0};
 static Symbol* _morphology_sym;
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
 	_p = nrn_prop_data_alloc(_mechtype, 18, _prop);
 	/*initialize range parameters*/
 	depth = 0.0125;
 	taur = 80;
 	erev = 0;
 	gbar = 0.0001;
 	taumin = 0.1;
 	concrelease = 500;
 	_prop->param = _p;
 	_prop->param_size = 18;
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_morphology_sym);
 	_ppvar[3]._pval = &prop_ion->param[0]; /* diam */
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0]._pval = &prop_ion->param[1]; /* cai */
 	_ppvar[1]._pval = &prop_ion->param[3]; /* ica */
 
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

 void _ican_reg() {
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
  hoc_register_prop_size(_mechtype, 18, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "pointer");
  hoc_register_dparam_semantics(_mechtype, 4, "cvodeieq");
  hoc_register_dparam_semantics(_mechtype, 3, "diam");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ican /mnt/h/Thesis work/Compilations/ExistingModels/Combe2023/267599/cholinergic_shift_generalize/ican.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 
#define FARADAY _nrnunit_FARADAY[_nrnunit_use_legacy_]
static double _nrnunit_FARADAY[2] = {0x1.78e555060882cp+16, 96485.3}; /* 96485.3321233100141 */
 
#define PI _nrnunit_PI[_nrnunit_use_legacy_]
static double _nrnunit_PI[2] = {0x1.921fb54442d18p+1, 3.14159}; /* 3.14159265358979312 */
static int _reset;
static char *modelname = "Slow Ca-dependent cation current";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int evaluate_fct(double, double);
 static int _deriv1_advance = 0;
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist2[2]; static double _dlist2[2];
 static double _savstate1[2], *_temp1 = _savstate1;
 static int _slist1[2], _dlist1[2];
 static int states(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 () {_reset=0;
 {
   evaluate_fct ( _threadargscomma_ v , can ) ;
   DPo = ( Po_inf - Po ) / ( Tau ) ;
   drive_channel = - ( concrelease ) * ica / ( 2.0 * FARADAY * depth ) ;
   if ( drive_channel <= 0.0 ) {
     drive_channel = 0.0 ;
     }
   Dcan = drive_channel + ( cai - can ) / ( taur ) ;
   }
 return _reset;
}
 static int _ode_matsol1 () {
 evaluate_fct ( _threadargscomma_ v , can ) ;
 DPo = DPo  / (1. - dt*( ( ( ( - 1.0 ) ) ) / ( Tau ) )) ;
 drive_channel = - ( concrelease ) * ica / ( 2.0 * FARADAY * depth ) ;
 if ( drive_channel <= 0.0 ) {
   drive_channel = 0.0 ;
   }
 Dcan = Dcan  / (1. - dt*( ( ( ( - 1.0 ) ) ) / ( taur ) )) ;
  return 0;
}
 /*END CVODE*/
 
static int states () {_reset=0;
 { static int _recurse = 0;
 int _counte = -1;
 if (!_recurse) {
 _recurse = 1;
 {int _id; for(_id=0; _id < 2; _id++) { _savstate1[_id] = _p[_slist1[_id]];}}
 error = newton(2,_slist2, _p, states, _dlist2);
 _recurse = 0; if(error) {abort_run(error);}}
 {
   evaluate_fct ( _threadargscomma_ v , can ) ;
   DPo = ( Po_inf - Po ) / ( Tau ) ;
   drive_channel = - ( concrelease ) * ica / ( 2.0 * FARADAY * depth ) ;
   if ( drive_channel <= 0.0 ) {
     drive_channel = 0.0 ;
     }
   Dcan = drive_channel + ( cai - can ) / ( taur ) ;
   {int _id; for(_id=0; _id < 2; _id++) {
if (_deriv1_advance) {
 _dlist2[++_counte] = _p[_dlist1[_id]] - (_p[_slist1[_id]] - _savstate1[_id])/dt;
 }else{
_dlist2[++_counte] = _p[_slist1[_id]] - _savstate1[_id];}}}
 } }
 return _reset;}
 
double MyExp (  double _lx ) {
   double _lMyExp;
 if ( _lx < - 50.0 ) {
     _lMyExp = 0.0 ;
     }
   else if ( _lx > 50.0 ) {
     _lMyExp = exp ( 50.0 ) ;
     }
   else {
     _lMyExp = exp ( _lx ) ;
     }
   
return _lMyExp;
 }
 
static void _hoc_MyExp(void) {
  double _r;
   _r =  MyExp (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static int  evaluate_fct (  double _lv , double _lcai ) {
   double _lalpha , _lalpha2 , _lbeta ;
 _lalpha = 0.0057 * MyExp ( _threadargscomma_ 0.0060 * _lv ) ;
   _lbeta = 0.033 * MyExp ( _threadargscomma_ - 0.019 * _lv ) ;
   _lalpha2 = _lalpha / ( 1.0 + ( Kd / _lcai ) ) ;
   Po_inf = _lalpha2 / ( _lalpha2 + _lbeta ) ;
   Tau = 1.0 / ( _lalpha2 + _lbeta ) ;
   if ( Tau < taumin ) {
     Tau = taumin ;
     }
    return 0; }
 
static void _hoc_evaluate_fct(void) {
  double _r;
   _r = 1.;
 evaluate_fct (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(NrnThread* _nt, _Memb_list* _ml, int _type) {
   Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  cai = _ion_cai;
  ica = _ion_ica;
     _ode_spec1 ();
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
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
  cai = _ion_cai;
  ica = _ion_ica;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_ca_sym, _ppvar, 0, 1);
   nrn_update_ion_pointer(_ca_sym, _ppvar, 1, 3);
 }

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  Po = Po0;
  can = can0;
 {
   can = cai ;
   evaluate_fct ( _threadargscomma_ v , can ) ;
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
  cai = _ion_cai;
  ica = _ion_ica;
 initmodel();
}}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   itrpm4 = gbar * Po * ( v - erev ) ;
   }
 _current += itrpm4;

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
  cai = _ion_cai;
  ica = _ion_ica;
 _g = _nrn_current(_v + .001);
 	{ _rhs = _nrn_current(_v);
 	}
 _g = (_g - _rhs)/.001;
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
  cai = _ion_cai;
  ica = _ion_ica;
 { error = _deriv1_advance = 1;
 derivimplicit(_ninits, 2, _slist1, _dlist1, _p, &t, dt, states, &_temp1);
_deriv1_advance = 0;
 if(error){fprintf(stderr,"at line 64 in file ican.mod:\n    SOLVE states METHOD derivimplicit\n"); nrn_complain(_p); abort_run(error);}
    if (secondorder) {
    int _i;
    for (_i = 0; _i < 2; ++_i) {
      _p[_slist1[_i]] += dt*_p[_dlist1[_i]];
    }}
 }}}
 dt = _dtsav;
}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = Po_columnindex;  _dlist1[0] = DPo_columnindex;
 _slist1[1] = can_columnindex;  _dlist1[1] = Dcan_columnindex;
 _slist2[0] = Po_columnindex;
 _slist2[1] = can_columnindex;
_first = 0;
}

#if NMODL_TEXT
static const char* nmodl_filename = "/mnt/h/Thesis work/Compilations/ExistingModels/Combe2023/267599/cholinergic_shift_generalize/ican.mod";
static const char* nmodl_file_text = 
  "TITLE Slow Ca-dependent cation current\n"
  ":\n"
  ":   We've moved to the Model described by Nillus in 2004, while keeping the description of the nanodomain\n"
  ": modified by Canavier too include separate pool for ICan calcium microdomain\n"
  ": at this point ican doesn't activate other pools of calcium need to declare a new ion species\n"
  ": because at this point the code requires pools for SK+BK+T inactivation and ICAN that decay at different rates\n"
  "\n"
  "INDEPENDENT {\n"
  "    t FROM 0 TO 1 WITH 1 (ms)\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "    SUFFIX ican\n"
  "    USEION ca READ cai, ica \n"
  "    RANGE depth,taur,erev\n"
  "    RANGE gbar,itrpm4, concrelease\n"
  "    RANGE beta,taumin\n"
  "    POINTER jip3p\n"
  "    NONSPECIFIC_CURRENT itrpm4\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "    (mA)=(milliamp)\n"
  "    (mV)=(millivolt)\n"
  "    (molar)=(1/liter)\n"
  "    (mM)=(millimolar)\n"
  "    (um)=(micron)\n"
  "    (msM)=(ms mM)\n"
  "    FARADAY=(faraday) (coulomb)\n"
  "	PI      = (pi)       (1)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "    v (mV)\n"
  "    depth=0.0125 (um)         : depth of shell 0.0125 for pc1a\n"
  "    taur=80 (ms)           : rate of calcium removal	100\n"
  "    erev=0 (mV)             : reversal potential\n"
  "    cai (mM)                : will now decay to bulk cai\n"
  "	ica       (mA/cm2)\n"
  "    gbar=0.0001 (mho/cm2)\n"
  "    : middle point of activation fct, for ip3 as somacar, for current injection\n"
  "    taumin=0.1 (ms)         : minimal value of time constant\n"
  "    concrelease=500\n"
  "    Kd = 87e-3 (mM)		:87e-3\n"
  "}\n"
  "\n"
  "STATE {\n"
  "    can (mM) \n"
  "    Po\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	jip3p (mM/ms)\n"
  "    ican (mA/cm2)\n"
  "    drive_channel (mM/ms)\n"
  "    itrpm4 (mA/cm2)\n"
  "    Po_inf\n"
  "    Tau (ms)\n"
  "	diam      (um)\n"
  "    :cai (mM) \n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "    SOLVE states METHOD derivimplicit\n"
  "    itrpm4=gbar*Po*(v-erev)\n"
  "}\n"
  "\n"
  "DERIVATIVE states {\n"
  "    evaluate_fct(v,can)\n"
  "    Po'=(Po_inf-Po)/(Tau)\n"
  "	drive_channel =  - (concrelease) * ica / (2 * FARADAY * depth)\n"
  "    if (drive_channel<=0.0) {drive_channel=0.0}             : cannot pump inward \n"
  "    can'=drive_channel+(cai-can)/(taur)\n"
  "}\n"
  "\n"
  "FUNCTION MyExp(x) {\n"
  "    if (x<-50) {MyExp=0}\n"
  "    else if (x>50) {MyExp=exp(50)}\n"
  "    else {MyExp=exp(x)}\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "\n"
  "INITIAL {\n"
  "    : activation kinetics are assumed to be at 22 deg. C\n"
  "    : Q10 is assumed to be 3\n"
  "    can=cai\n"
  "    evaluate_fct(v,can)\n"
  "}\n"
  "\n"
  "PROCEDURE evaluate_fct(v(mV),cai(mM)) {\n"
  "    LOCAL alpha, alpha2, beta\n"
  "    alpha=0.0057*MyExp(0.0060*v)\n"
  "    beta=0.033*MyExp(-0.019*v)\n"
  "    \n"
  "    :alpha=0.0057*MyExp(0.0060*-60) uncomment these and comment out top if you want the voltage independent model\n"
  "    :beta=0.033*MyExp(-0.019*-60)\n"
  "\n"
  "    alpha2=alpha/(1+(Kd/cai))\n"
  "    Po_inf=alpha2/(alpha2+beta)\n"
  "    Tau=1/(alpha2+beta)\n"
  "    if (Tau<taumin) {Tau=taumin}                        : min value of time cst\n"
  "}\n"
  "\n"
  "UNITSON\n"
  ;
#endif
