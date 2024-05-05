
import numpy as np
from scipy.linalg import expm
from typing import Literal

from rcwa_tlv.utils.convmat import convmat
from rcwa_tlv.utils.normal_vector import calc_nv_fields
from rcwa_tlv import Device, Source


class RCWA:
    def __init__(
            self,
            device: Device,
            source: Source,
            gamma: float = 1.,
            apply_nv: bool = False,
            dtype: Literal['np.float32', 'np.float64'] = np.float32,
            renormalize: bool = False,
    ):
        self.source = source
        self.device = device
        self.gamma = gamma
        self.apply_nv = apply_nv
        self.renormalize = renormalize
        self.result = None

        self.dtype = dtype
        self.cdtype = np.complex128 if dtype == np.float64 else np.complex64
        self.idtype = np.int64 if dtype == np.float64 else np.int32

    def __call__(self, *args, apply_nv=None, verbose=True, **kwargs) -> dict:
        ur1 = self.device.ur1
        er1 = self.device.er1
        ur2 = self.device.ur2
        er2 = self.device.er2
        gamma = self.gamma
        polarization_vec = self.source.polarization_vec
        self.apply_nv = apply_nv if apply_nv is not None else self.apply_nv

        if self.apply_nv:
            for layer in self.device.layers:
                layer['nv_x'], layer['nv_y'] = calc_nv_fields(layer['er'])

        n_layers = len(self.device.layers)
        num_of_m = 1 + 2 * self.device.p  # x/width axis
        num_of_n = 1 + 2 * self.device.q  # y/height axis

        # Compute k0 and incident wavevector
        k0 = 2 * np.pi / self.source.lam0
        k_inc = np.array([
            np.sqrt(self.device.er1 * self.device.ur1) * np.sin(self.source.theta) * np.cos(self.source.phi),
            np.sqrt(self.device.er1 * self.device.ur1) * np.sin(self.source.theta) * np.sin(self.source.phi),
            np.sqrt(self.device.er1 * self.device.ur1) * np.cos(self.source.theta)
        ])

        # Compute kx and ky
        m = np.arange(-self.device.p, self.device.p + 1)  # x/width axis
        n = np.arange(-self.device.q, self.device.q + 1)  # y/height axis
        kx = k_inc[0] - 2 * np.pi * m / (k0 * self.device.period_x)
        ky = k_inc[1] - 2 * np.pi * n / (k0 * self.device.period_y)
        # kx, ky = np.meshgrid(kx.astype(self.cdtype), ky.astype(self.cdtype))
        ky, kx = np.meshgrid(ky.astype(self.cdtype), kx.astype(self.cdtype))

        # Compute kz in reflection and transmission regions
        kz_ref = np.conj((ur1 * er1 - kx ** 2 - ky ** 2).astype(self.cdtype) ** 0.5)
        kz_trn = np.conj((ur2 * er2 - kx ** 2 - ky ** 2).astype(self.cdtype) ** 0.5)

        # m_vec, n_vec = np.meshgrid(m.astype(self.idtype), n.astype(self.idtype))
        n_vec, m_vec = np.meshgrid(n.astype(self.idtype), m.astype(self.idtype))

        # Truncate k vectors
        shape = (np.abs(m_vec / self.device.p) ** (2 * gamma) + np.abs(n_vec / self.device.q) ** (2 * gamma)) <= 1
        non_zero_rows, non_zero_cols = np.nonzero(shape)
        inxs = np.ravel_multi_index((non_zero_rows, non_zero_cols), shape.shape)
        n_nonzero = np.count_nonzero(shape)

        kx[np.logical_not(shape)] = 0
        ky[np.logical_not(shape)] = 0
        kz_ref[np.logical_not(shape)] = 0
        kz_trn[np.logical_not(shape)] = 0

        # Compute convolution matrices and truncate
        er_c_mat = np.zeros((n_layers, n_nonzero, n_nonzero), dtype=self.cdtype)
        er_inv_mat = np.zeros((n_layers, n_nonzero, n_nonzero), dtype=self.cdtype)
        delta_mat = np.zeros((n_layers, n_nonzero, n_nonzero), dtype=self.cdtype)

        nvx_c = np.zeros((n_layers, n_nonzero, n_nonzero), dtype=self.cdtype) if self.apply_nv else None
        nvy_c = np.zeros((n_layers, n_nonzero, n_nonzero), dtype=self.cdtype) if self.apply_nv else None
        nvxy_c = np.zeros((n_layers, n_nonzero, n_nonzero), dtype=self.cdtype) if self.apply_nv else None

        for i_layer in range(n_layers):
            er_temp = convmat(
                self.device.layers[i_layer]['er'].astype(self.cdtype), num_of_m, num_of_n, dtype=self.cdtype
            )
            er_c_mat[i_layer, :, :] = er_temp[inxs, :][:, inxs]

            er_inv = convmat(1 / self.device.layers[i_layer]['er'], num_of_m, num_of_n, dtype=self.cdtype)
            er_inv_mat[i_layer, :, :] = np.linalg.inv(er_inv[inxs, :][:, inxs])

            delta_mat[i_layer, :, :] = er_c_mat[i_layer, :, :] - er_inv_mat[i_layer, :, :]

            if self.apply_nv:
                nvxtemp = convmat(self.device.layers[i_layer]['nv_x'] ** 2, num_of_m, num_of_n)
                nvytemp = convmat(self.device.layers[i_layer]['nv_y'] ** 2, num_of_m, num_of_n)
                nvxytemp = convmat(
                    self.device.layers[i_layer]['nv_x'] * self.device.layers[i_layer]['nv_y'], num_of_m, num_of_n
                )

                nvx_c[i_layer, :, :] = nvxtemp[inxs, :][:, inxs]
                nvy_c[i_layer, :, :] = nvytemp[inxs, :][:, inxs]
                nvxy_c[i_layer, :, :] = nvxytemp[inxs, :][:, inxs]

        kx_mat = np.diag(kx[non_zero_rows, non_zero_cols]).astype(self.cdtype)
        ky_mat = np.diag(ky[non_zero_rows, non_zero_cols]).astype(self.cdtype)
        kz_ref_mat = np.diag(kz_ref[non_zero_rows, non_zero_cols])
        kz_trn_mat = np.diag(kz_trn[non_zero_rows, non_zero_cols])

        # EMT RCWA
        delta = np.zeros(n_nonzero)
        delta[len(delta) // 2] = 1
        s_mat = np.concatenate([
            polarization_vec[0] * delta,
            polarization_vec[1] * delta,
            1j * (k_inc[2] * polarization_vec[1] - k_inc[1] * polarization_vec[2]) * delta / self.device.ur1,
            1j * (k_inc[0] * polarization_vec[2] - k_inc[2] * polarization_vec[0]) * delta / self.device.ur1
        ]).astype(self.cdtype)

        # Initialize matrices
        i_mat = np.diag(np.ones(n_nonzero, dtype=self.cdtype))
        o_mat = np.diag(np.zeros(n_nonzero, dtype=self.cdtype))

        # prepare mid-way calculations to save time
        kxky_mat = kx_mat @ ky_mat
        kykx_mat = ky_mat @ kx_mat
        kxkx_mat = kx_mat @ kx_mat
        kyky_mat = ky_mat @ ky_mat
        j_kxky_mat = 1j * kxky_mat
        kx_sqr_mat = kx_mat ** 2
        ky_sqr_mat = ky_mat ** 2
        kz_ref_sqr_mat = kz_ref_mat ** 2
        kz_trn_sqr_mat = kz_trn_mat ** 2

        a_mat = self._a_mat(
            ur1, i_mat, o_mat, j_kxky_mat, kz_ref_mat, ky_sqr_mat, kx_sqr_mat, kz_ref_sqr_mat, verbose=verbose
        )
        b_mat = self._b_mat(
            ur2, i_mat, o_mat, j_kxky_mat, kz_trn_mat, ky_sqr_mat, kx_sqr_mat, kz_trn_sqr_mat, verbose=verbose
        )

        f_mat = np.zeros((4 * n_nonzero, 4 * n_nonzero, n_layers), dtype=self.cdtype)
        x_mat = np.zeros((2 * n_nonzero, 2 * n_nonzero, n_layers), dtype=self.cdtype)
        p_mat = np.zeros((2 * n_nonzero, 2 * n_nonzero, n_layers), dtype=self.cdtype)
        q_mat = np.zeros((2 * n_nonzero, 2 * n_nonzero, n_layers), dtype=self.cdtype)

        # Compute matrices for each layer
        if n_layers > 0:
            for i_layer in range(n_layers):
                erky = np.linalg.solve(er_c_mat[i_layer], ky_mat)
                erkx = np.linalg.solve(er_c_mat[i_layer], kx_mat)

                p_mat[:, :, i_layer] = np.block([  # type:ignore
                    [kx_mat @ erky, i_mat - kx_mat @ erkx],
                    [ky_mat @ erky - i_mat, -ky_mat @ erkx]
                ])
                if self.apply_nv:
                    delta_nxy = delta_mat[i_layer] @ nvxy_c[i_layer]
                    q_mat[:, :, i_layer] = np.block([  # type:ignore
                        [
                            kxky_mat - delta_nxy,
                            er_c_mat[i_layer] - delta_mat[i_layer] @ nvy_c[i_layer] - kxkx_mat
                        ],
                        [
                            kyky_mat - er_c_mat[i_layer] + delta_mat[i_layer] @ nvx_c[i_layer],
                            -kykx_mat + delta_nxy
                        ]
                    ])
                else:
                    q_mat[:, :, i_layer] = np.block([  # type:ignore
                        [kxky_mat, er_c_mat[i_layer] - kxkx_mat],
                        [kyky_mat - er_c_mat[i_layer], -kykx_mat]
                    ])
                omega_2 = p_mat[:, :, i_layer] @ q_mat[:, :, i_layer]
                lam, w_mat = np.linalg.eig(omega_2)
                lam = np.diag(np.sqrt(lam))
                x_mat[:, :, i_layer] = expm(-lam * k0 * self.device.layers[i_layer]['length_z'])
                v_mat = q_mat[:, :, i_layer] @ w_mat @ np.linalg.inv(lam)
                f_mat[:, :, i_layer] = np.block([  # type:ignore
                    [w_mat, w_mat],
                    [-v_mat, v_mat]
                ])

        # Compute a_i and b_i matrices
        a = np.zeros((2 * n_nonzero, 2 * n_nonzero, n_layers), dtype=self.cdtype)
        b = np.zeros((2 * n_nonzero, 2 * n_nonzero, n_layers), dtype=self.cdtype)

        i2_mat = np.diag(np.ones(2 * n_nonzero, dtype=self.cdtype))
        o2_mat = np.diag(np.zeros(2 * n_nonzero, dtype=self.cdtype))

        if n_layers > 0:
            an_bn = np.linalg.solve(f_mat[:, :, -1], b_mat)
            a[:, :, -1] = an_bn[:2 * n_nonzero, :]
            b[:, :, -1] = an_bn[2 * n_nonzero:, :]

            for i_layer in range(n_layers - 2, -1, -1):
                temp1 = np.block([  # type:ignore
                    [i2_mat, o2_mat],
                    [o2_mat, x_mat[:, :, i_layer + 1]]
                ])
                temp2 = np.block([  # type:ignore
                    [i2_mat],
                    [b[:, :, i_layer + 1] @ np.linalg.solve(a[:, :, i_layer + 1], x_mat[:, :, i_layer + 1])]
                ])
                an_bn = np.linalg.solve(f_mat[:, :, i_layer], f_mat[:, :, i_layer + 1] @ temp1 @ temp2)
                a[:, :, i_layer] = an_bn[:2 * n_nonzero, :]
                b[:, :, i_layer] = an_bn[2 * n_nonzero:, :]

        # Compute B'
        temp1 = np.block([  # type:ignore
            [i2_mat, o2_mat],
            [o2_mat, x_mat[:, :, 0]]
        ])
        temp2 = np.block([  # type:ignore
            [i2_mat],
            [b[:, :, 0] @ np.linalg.solve(a[:, :, 0], x_mat[:, :, 0])]
        ])
        b_tag_mat = f_mat[:, :, 0] @ temp1 @ temp2

        # Compute reflected and transmitted field amplitudes
        rt1 = np.linalg.solve(np.block([[-a_mat, b_tag_mat]]), s_mat)  # type:ignore
        rxy = rt1[:2 * n_nonzero]
        t1 = rt1[2 * n_nonzero:]

        # Initialize E field amplitudes
        r = np.zeros((n_nonzero, 3), dtype=self.cdtype)
        t = np.zeros((n_nonzero, 3), dtype=self.cdtype)

        # Compute r and t
        txy = t1
        for i_layer in range(n_layers):
            txy = np.linalg.solve(a[:, :, i_layer], x_mat[:, :, i_layer]) @ txy

        r[:, 0] = rxy[:n_nonzero]
        r[:, 1] = rxy[n_nonzero:]

        try:
            r[:, 2] = -np.linalg.solve(kz_ref_mat, kx_mat @ r[:, 0] + ky_mat @ r[:, 1])
        except np.linalg.linalg.LinAlgError:
            if verbose:
                print('failed: -np.linalg.solve(kz_ref_mat, kx_mat @ r[:, 0] + ky_mat @ r[:, 1]), trying lstsq')
            r[:, 2] = -np.linalg.lstsq(kz_ref_mat, kx_mat @ r[:, 0] + ky_mat @ r[:, 1], rcond=None)[0]

        t[:, 0] = txy[:n_nonzero]
        t[:, 1] = txy[n_nonzero:]

        try:
            t[:, 2] = -np.linalg.solve(kz_trn_mat, kx_mat @ t[:, 0] + ky_mat @ t[:, 1])
        except np.linalg.linalg.LinAlgError:
            if verbose:
                print('failed: -np.linalg.solve(kz_trn_mat, kx_mat @ t[:, 0] + ky_mat @ t[:, 1]), trying lstsq')
            t[:, 2] = -np.linalg.lstsq(kz_trn_mat, kx_mat @ t[:, 0] + ky_mat @ t[:, 1], rcond=None)[0]

        # Compute diffraction efficiency
        r_squared = np.abs(r[:, 0]) ** 2 + np.abs(r[:, 1]) ** 2 + np.abs(r[:, 2]) ** 2
        t_squared = np.abs(t[:, 0]) ** 2 + np.abs(t[:, 1]) ** 2 + np.abs(t[:, 2]) ** 2

        reflectance = np.real(kz_ref_mat / ur1) / np.real(k_inc[2] / ur1) @ r_squared
        transmittance = np.real(kz_trn_mat / ur2) / np.real(k_inc[2] / ur1) @ t_squared

        tot_r = np.sum(reflectance)
        tot_t = np.sum(transmittance)
        tot = tot_t + tot_r

        if self.renormalize:
            reflectance /= tot
            transmittance /= tot

            tot_r = np.sum(reflectance)
            tot_t = np.sum(transmittance)
            tot = tot_t + tot_r

        self.result = {
            'reflectance': reflectance,
            'transmittance': transmittance,
            'tot_r': tot_r,
            'tot_t': tot_t,
        }

        return self.result

    @staticmethod
    def _a_mat(ur1, i_mat, o_mat, j_kxky_mat, kz_ref_mat, ky_sqr_mat, kx_sqr_mat, kz_ref_sqr_mat, verbose=True):
        """
        a_mat = np.block([  # type:ignore
            [i_mat, o_mat],
            [o_mat, i_mat],
            [
                -(1j * kx_mat @ ky_mat) @ np.linalg.inv(ur1 * kz_ref_mat),
                -(1j * (ky_mat ** 2 + kz_ref_mat ** 2)) @ np.linalg.inv(ur1 * kz_ref_mat)
            ],
            [
                (1j * (kx_mat ** 2 + kz_ref_mat ** 2)) @ np.linalg.inv(ur1 * kz_ref_mat),
                (1j * kx_mat @ ky_mat) @ np.linalg.inv(ur1 * kz_ref_mat)
            ]
        ])
        :param ur1:
        :param i_mat:
        :param o_mat:
        :param j_kxky_mat:
        :param kz_ref_mat:
        :param ky_sqr_mat:
        :param kx_sqr_mat:
        :param kz_ref_sqr_mat:
        :param verbose:
        :return:
        """
        ur1_kz_ref_mat = ur1 * kz_ref_mat

        try:
            kz_inv_mat = np.linalg.inv(ur1_kz_ref_mat)
            j_kxky_kz_inv_mat = j_kxky_mat @ kz_inv_mat

            a_mat = np.block([  # type:ignore
                [i_mat, o_mat],
                [o_mat, i_mat],
                [-j_kxky_kz_inv_mat, -(1j * (ky_sqr_mat + kz_ref_sqr_mat)) @ kz_inv_mat],
                [(1j * (kx_sqr_mat + kz_ref_sqr_mat)) @ kz_inv_mat, j_kxky_kz_inv_mat]
            ])
        except np.linalg.linalg.LinAlgError:
            try:
                if verbose:
                    print(f'direct inversion of ur1 * kz_ref_mat failed, trying to use np.linalg.solve...')

                a_mat = np.block([  # type:ignore
                    [i_mat, o_mat],
                    [o_mat, i_mat],
                    [
                        np.linalg.solve(ur1_kz_ref_mat.T, -j_kxky_mat.T).T,
                        np.linalg.solve(ur1_kz_ref_mat.T, -(1j * (ky_sqr_mat + kz_ref_sqr_mat)).T).T
                    ],
                    [
                        np.linalg.solve(ur1_kz_ref_mat.T, (1j * (kx_sqr_mat + kz_ref_sqr_mat)).T).T,
                        np.linalg.solve(ur1_kz_ref_mat.T, j_kxky_mat.T).T
                    ]
                ])
            except np.linalg.linalg.LinAlgError:
                try:
                    if verbose:
                        print(f'np.linalg.solve failed, trying np.linalg.lstsq...')
                    a_mat = np.block([  # type:ignore
                        [i_mat, o_mat],
                        [o_mat, i_mat],
                        [
                            np.linalg.lstsq(ur1_kz_ref_mat.T, -j_kxky_mat.T, rcond=None)[0].T,
                            np.linalg.lstsq(ur1_kz_ref_mat.T, -(1j * (ky_sqr_mat + kz_ref_sqr_mat)).T, rcond=None)[0].T
                        ],
                        [
                            np.linalg.lstsq(ur1_kz_ref_mat.T, (1j * (kx_sqr_mat + kz_ref_sqr_mat)).T, rcond=None)[0].T,
                            np.linalg.lstsq(ur1_kz_ref_mat.T, j_kxky_mat.T, rcond=None)[0].T
                        ]
                    ])
                except np.linalg.linalg.LinAlgError:
                    raise np.linalg.linalg.LinAlgError('all methods to evaluate a_mat failed')

        return a_mat

    @staticmethod
    def _b_mat(ur2, i_mat, o_mat, j_kxky_mat, kz_trn_mat, ky_sqr_mat, kx_sqr_mat, kz_trn_sqr_mat, verbose=True):
        """
        b_mat = np.block([  # type:ignore
            [i_mat, o_mat],
            [o_mat, i_mat],
            [
                j_kxky_mat @ np.linalg.inv(ur2 * kz_trn_mat),
                (1j * (ky_sqr_mat + kz_trn_sqr_mat)) @ np.linalg.inv(ur2 * kz_trn_mat)
            ],
            [
                -(1j * (kx_sqr_mat + kz_trn_sqr_mat)) @ np.linalg.inv(ur2 * kz_trn_mat),
                -j_kxky_mat @ np.linalg.inv(ur2 * kz_trn_mat)
            ]
        ])
        :param ur2:
        :param i_mat:
        :param o_mat:
        :param j_kxky_mat:
        :param kz_trn_mat:
        :param ky_sqr_mat:
        :param kx_sqr_mat:
        :param kz_trn_sqr_mat:
        :param verbose:
        :return:
        """

        ur2_kz_trn_mat = ur2 * kz_trn_mat

        try:
            kz_inv_mat = np.linalg.inv(ur2_kz_trn_mat)
            j_kxky_kz_inv_mat = j_kxky_mat @ kz_inv_mat

            b_mat = np.block([  # type:ignore
                [i_mat, o_mat],
                [o_mat, i_mat],
                [j_kxky_kz_inv_mat, (1j * (ky_sqr_mat + kz_trn_sqr_mat)) @ kz_inv_mat],
                [-(1j * (kx_sqr_mat + kz_trn_sqr_mat)) @ kz_inv_mat, -j_kxky_kz_inv_mat]
            ])
        except np.linalg.linalg.LinAlgError:
            try:
                if verbose:
                    print(f'direct inversion of ur1 * kz_ref_mat failed, trying to use np.linalg.solve...')

                b_mat = np.block([  # type:ignore
                    [i_mat, o_mat],
                    [o_mat, i_mat],
                    [
                        np.linalg.solve(ur2_kz_trn_mat.T, j_kxky_mat.T).T,
                        np.linalg.solve(ur2_kz_trn_mat.T, (1j * (ky_sqr_mat + kz_trn_sqr_mat)).T).T
                    ],
                    [
                        np.linalg.solve(ur2_kz_trn_mat.T, -(1j * (kx_sqr_mat + kz_trn_sqr_mat)).T).T,
                        np.linalg.solve(ur2_kz_trn_mat.T, -j_kxky_mat.T).T
                    ]
                ])
            except np.linalg.linalg.LinAlgError:
                try:
                    if verbose:
                        print(f'np.linalg.solve failed, trying np.linalg.lstsq...')
                    b_mat = np.block([  # type:ignore
                        [i_mat, o_mat],
                        [o_mat, i_mat],
                        [
                            np.linalg.lstsq(ur2_kz_trn_mat.T, j_kxky_mat.T, rcond=None)[0].T,
                            np.linalg.lstsq(ur2_kz_trn_mat.T, (1j * (ky_sqr_mat + kz_trn_sqr_mat)).T, rcond=None)[0].T
                        ],
                        [
                            np.linalg.lstsq(ur2_kz_trn_mat.T, -(1j * (kx_sqr_mat + kz_trn_sqr_mat)).T, rcond=None)[0].T,
                            np.linalg.lstsq(ur2_kz_trn_mat.T, -j_kxky_mat.T, rcond=None)[0].T
                        ]
                    ])
                except np.linalg.linalg.LinAlgError:
                    raise np.linalg.linalg.LinAlgError('all methods to evaluate b_mat failed')

        return b_mat


if __name__ == '__main__':
    from time import perf_counter
    from rcwa_tlv.devices.shapes import add_circle

    n_height = 800
    n_width = 800
    period = 900
    nm2pixels = n_width / period

    # reflexion region
    er1 = 1.5 ** 2
    ur1 = 1.0

    # transmission region
    er2 = 1.0
    ur2 = 1.0

    layer_1 = {
        'er': 1.0 * np.ones((n_height, n_width)),
        # 'ur': 1.0 * np.ones((n_height, n_width)),
        'length_z': 21,
    }

    layer_2 = {
        'er': 7.0 * np.ones((n_height, n_width)),
        # 'ur': 1.0 * np.ones((n_height, n_width)),
        'length_z': 54,
    }

    # layers = [layer_1, layer_2, layer_2, layer_2, layer_1, layer_2, layer_2, layer_2]
    layers = [layer_1]
    add_circle(layers[0]['er'], (n_height // 2, n_width // 2), 300 * nm2pixels, 36.)
    # add_circle(layers[1]['er'], (n_height // 4, n_width // 2), 200 * nm2pixels, er1)

    device_1 = Device(layers, period_x=period, period_y=period, er1=1.445 ** 2, ur1=1.0, er2=1.0, ur2=1.0, p=9, q=9)
    source_1 = Source(0.0, 0.0, 400, 1., 0.)

    rcwa = RCWA(device_1, source_1, gamma=1.0, apply_nv=True, dtype=np.float32)

    t1 = perf_counter()
    result = rcwa()
    t2 = perf_counter()

    print(f'rcwa time: {t2 - t1:0.4f}, r: {result["tot_r"]}, t: {result["tot_t"]}')

    b = 1
