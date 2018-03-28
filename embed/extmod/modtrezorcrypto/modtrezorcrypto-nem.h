/*
 * This file is part of the TREZOR project, https://trezor.io/
 *
 * Copyright (c) SatoshiLabs
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "py/objstr.h"
#include "nem.h"

/// def validate_address(address: str, network: int) -> bool:
///     '''
///     Validate a NEM address
///     '''
STATIC mp_obj_t mod_trezorcrypto_nem_validate_address(mp_obj_t address, mp_obj_t network) {

    mp_buffer_info_t addr;
    mp_get_buffer_raise(address, &addr, MP_BUFFER_READ);

    uint32_t n = mp_obj_get_int_truncated(network);
    return mp_obj_new_bool(nem_validate_address(addr.buf, n));
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(mod_trezorcrypto_nem_validate_address_obj, mod_trezorcrypto_nem_validate_address);

// objects definition
STATIC const mp_rom_map_elem_t mod_trezorcrypto_nem_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR_validate_address), MP_ROM_PTR(&mod_trezorcrypto_nem_validate_address_obj) },
};
STATIC MP_DEFINE_CONST_DICT(mod_trezorcrypto_nem_globals, mod_trezorcrypto_nem_globals_table);

// module definition
STATIC const mp_obj_module_t mod_trezorcrypto_nem_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&mod_trezorcrypto_nem_globals,
};
