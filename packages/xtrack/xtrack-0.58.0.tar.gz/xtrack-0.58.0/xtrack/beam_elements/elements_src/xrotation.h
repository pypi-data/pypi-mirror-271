// copyright ############################### //
// This file is part of the Xtrack Package.  //
// Copyright (c) CERN, 2021.                 //
// ######################################### //

#ifndef XTRACK_XROTATION_H
#define XTRACK_XROTATION_H


/*gpufun*/
void XRotation_single_particle(LocalParticle* part, double sin_angle, double cos_angle, double tan_angle){

    double const beta0 = LocalParticle_get_beta0(part);
    double const beta = LocalParticle_get_rvv(part)*beta0;
    double const x  = LocalParticle_get_x(part);
    double const y  = LocalParticle_get_y(part);
    double const px = LocalParticle_get_px(part);
    double const py = LocalParticle_get_py(part);
    double const t = LocalParticle_get_zeta(part)/beta0;
    double const pt = LocalParticle_get_pzeta(part)*beta0;

    double pz = sqrt(1.0 + 2.0*pt/beta + pt*pt - px*px - py*py);
    double ptt = 1.0 - tan_angle*py/pz;
    double x_hat = x + tan_angle*y*px/(pz*ptt);
    double y_hat = y/(cos_angle*ptt);
    double py_hat = cos_angle*py + sin_angle*pz;
    double t_hat = t - tan_angle*y*(1.0/beta+pt)/(pz*ptt);

    LocalParticle_set_x(part, x_hat);
    LocalParticle_set_y(part, y_hat);
    LocalParticle_set_py(part, py_hat);
    LocalParticle_set_zeta(part,t_hat*beta0);

}


/*gpufun*/
void XRotation_track_local_particle(XRotationData el, LocalParticle* part0){

    double sin_angle = XRotationData_get_sin_angle(el);
    double cos_angle = XRotationData_get_cos_angle(el);
    double tan_angle = XRotationData_get_tan_angle(el);

    #ifdef XSUITE_BACKTRACK
        sin_angle = -sin_angle;
        tan_angle = -tan_angle;
    #endif

    //start_per_particle_block (part0->part)
        XRotation_single_particle(part, sin_angle, cos_angle, tan_angle);
    //end_per_particle_block

}


#endif /* XTRACK_XROTATION_H */
