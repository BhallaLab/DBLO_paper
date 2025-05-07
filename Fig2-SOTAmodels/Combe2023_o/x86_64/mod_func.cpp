#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;
#if defined(__cplusplus)
extern "C" {
#endif

extern void _CurrentClamp_reg(void);
extern void _Kv2like_reg(void);
extern void _Nav16_a_reg(void);
extern void _PotassiumInwardRectifier_reg(void);
extern void _cad_reg(void);
extern void _cagk_reg(void);
extern void _cal_reg(void);
extern void _cal4_reg(void);
extern void _calH_reg(void);
extern void _car_reg(void);
extern void _cat_reg(void);
extern void _d3_reg(void);
extern void _exp2i_reg(void);
extern void _h_reg(void);
extern void _ican_reg(void);
extern void _ican_nov_reg(void);
extern void _icand_reg(void);
extern void _kadist_reg(void);
extern void _kaprox_reg(void);
extern void _kca_reg(void);
extern void _kcasimple_reg(void);
extern void _kd_reg(void);
extern void _kdr_reg(void);
extern void _km_reg(void);
extern void _kv1_reg(void);
extern void _na3_reg(void);
extern void _na3dend_reg(void);
extern void _na3notrunk_reg(void);
extern void _nap_reg(void);
extern void _nax_reg(void);
extern void _netstims_reg(void);
extern void _nmdanet_reg(void);
extern void _somacar_reg(void);
extern void _stim2_reg(void);

void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"CurrentClamp.mod\"");
    fprintf(stderr, " \"Kv2like.mod\"");
    fprintf(stderr, " \"Nav16_a.mod\"");
    fprintf(stderr, " \"PotassiumInwardRectifier.mod\"");
    fprintf(stderr, " \"cad.mod\"");
    fprintf(stderr, " \"cagk.mod\"");
    fprintf(stderr, " \"cal.mod\"");
    fprintf(stderr, " \"cal4.mod\"");
    fprintf(stderr, " \"calH.mod\"");
    fprintf(stderr, " \"car.mod\"");
    fprintf(stderr, " \"cat.mod\"");
    fprintf(stderr, " \"d3.mod\"");
    fprintf(stderr, " \"exp2i.mod\"");
    fprintf(stderr, " \"h.mod\"");
    fprintf(stderr, " \"ican.mod\"");
    fprintf(stderr, " \"ican_nov.mod\"");
    fprintf(stderr, " \"icand.mod\"");
    fprintf(stderr, " \"kadist.mod\"");
    fprintf(stderr, " \"kaprox.mod\"");
    fprintf(stderr, " \"kca.mod\"");
    fprintf(stderr, " \"kcasimple.mod\"");
    fprintf(stderr, " \"kd.mod\"");
    fprintf(stderr, " \"kdr.mod\"");
    fprintf(stderr, " \"km.mod\"");
    fprintf(stderr, " \"kv1.mod\"");
    fprintf(stderr, " \"na3.mod\"");
    fprintf(stderr, " \"na3dend.mod\"");
    fprintf(stderr, " \"na3notrunk.mod\"");
    fprintf(stderr, " \"nap.mod\"");
    fprintf(stderr, " \"nax.mod\"");
    fprintf(stderr, " \"netstims.mod\"");
    fprintf(stderr, " \"nmdanet.mod\"");
    fprintf(stderr, " \"somacar.mod\"");
    fprintf(stderr, " \"stim2.mod\"");
    fprintf(stderr, "\n");
  }
  _CurrentClamp_reg();
  _Kv2like_reg();
  _Nav16_a_reg();
  _PotassiumInwardRectifier_reg();
  _cad_reg();
  _cagk_reg();
  _cal_reg();
  _cal4_reg();
  _calH_reg();
  _car_reg();
  _cat_reg();
  _d3_reg();
  _exp2i_reg();
  _h_reg();
  _ican_reg();
  _ican_nov_reg();
  _icand_reg();
  _kadist_reg();
  _kaprox_reg();
  _kca_reg();
  _kcasimple_reg();
  _kd_reg();
  _kdr_reg();
  _km_reg();
  _kv1_reg();
  _na3_reg();
  _na3dend_reg();
  _na3notrunk_reg();
  _nap_reg();
  _nax_reg();
  _netstims_reg();
  _nmdanet_reg();
  _somacar_reg();
  _stim2_reg();
}

#if defined(__cplusplus)
}
#endif
