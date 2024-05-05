# -*- coding: utf-8 -*-
# 2018 to present - Copyright Microchip Technology Inc. and its subsidiaries.

# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.

# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR
# PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL,
# PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY
# KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP
# HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO THE
# FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN
# ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
# THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.

import os
import cryptoauthlib as cal
from pathlib import Path
from tpds.resource_generation import TFLXResources, TFLXSlotConfig
from tpds.tp_utils import TPSymmetricKey
from tpds.flash_program import FlashProgram
from tpds.secure_element import ECC608A
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils.tp_print import print
from tpds.tp_utils.tp_utils import pretty_print_hex
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KDF_MODE_ALG_AES = 0x20
KDF_MODE_SOURCE_SLOT = 0x02
KDF_MODE_TARGET_OUTPUT = 0x10


class AesMessageEncryption():
    """
    Use case to showcase message encryption on HOST MCU(PC in this case).
    Uses master symmetric key in ECC608 to derive a ephemeral key that will
    be used to encrypt and decrypt messages
    """

    def __init__(self, boards, symm_key_slot):
        self.boards = boards
        self.shared_secret_slot = symm_key_slot

    def __connect_to_SE(self, b=None):
        print('Connecting to Secure Element: ', canvas=b)
        if self.boards is None:
            print('Prototyping board MUST be selected!', canvas=b)
            return
        assert self.boards.get_selected_board(), \
            'Select board to run an Usecase'

        kit_parser = FlashProgram()
        print(kit_parser.check_board_status())
        assert kit_parser.is_board_connected(), \
            'Check the Kit parser board connections'
        factory_hex = self.boards.get_kit_hex()
        if not kit_parser.is_factory_programmed():
            assert factory_hex, \
                'Factory hex is unavailable to program'
            print('Programming factory hex...', canvas=b)
            tp_settings = TPSettings()
            path = os.path.join(
                tp_settings.get_tpds_core_path(),
                'assets', 'Factory_Program.X',
                factory_hex)
            print(f'Programming {path} file')
            kit_parser.load_hex_image(path)
        self.element = ECC608A(address=0x6C)
        print('OK', canvas=b)
        print('Device details: {}'.format(self.element.get_device_details()))

    def generate_resources(self, b=None):
        self.__connect_to_SE(b)

        print('Generating crypto assets for Usecase...', canvas=b)
        resources = TFLXResources()
        tflex_slot_config = TFLXSlotConfig().tflex_slot_config

        symm_slot = self.shared_secret_slot
        symm_key_slot_config = tflex_slot_config.get(symm_slot)
        assert symm_key_slot_config.get('type') == 'secret', \
            "Invalid Slot, It is expected to be secret"

        enc_slot = symm_key_slot_config.get('enc_key', None)
        enc_key = Path('slot_{}_secret_key.pem'.format(
            enc_slot)) if enc_slot else None

        # Load encrypted Key
        if enc_key is not None:
            secret_key = Path('slot_{}_secret_key.pem'.format(enc_slot))
            assert resources.load_secret_key(
                enc_slot, enc_key, None,
                None) == cal.Status.ATCA_SUCCESS, \
                "Loading encrypted key into slot{} failed".format(enc_slot)

        # Load symmetric Key
        secret_key = Path('slot_{}_secret_key.pem'.format(symm_slot))
        assert resources.load_secret_key(
            symm_slot, secret_key, enc_slot,
            enc_key) == cal.Status.ATCA_SUCCESS, \
            "Loading secret key into slot{} failed".format(symm_slot)
        print('OK', canvas=b)

        sym_key = TPSymmetricKey(key=secret_key)
        self.sym_key_bytes = sym_key.get_bytes()[0:16]
        print("\nMaster Symmetric key:")
        print(pretty_print_hex(self.sym_key_bytes, li=8, indent='') + '\n')

    def derive_ephemeral_key(self, b=None):
        print('Generating ephemeral key using KDF ...', canvas=b)

        # Salt for key derivation, new salt can be used to get a new ephemeral key
        print('Generating salt for key derivation...', canvas=b)
        self.salt = os.urandom(16)
        print("Generated Salt:")
        print(pretty_print_hex(self.salt, li=8, indent='') + '\n')

        out_kdf_aes = bytearray(32)
        out_nonce = bytearray(32)

        # Begin KDF operation
        # Running KDF in AES mode, slot 5 as source key and output in plaintext to MCU
        # Addition data is 0 as the first key location in Slot 5 is used
        # Out_nonce is not required as output is read as plain text
        status = cal.atcab_kdf(KDF_MODE_ALG_AES | KDF_MODE_SOURCE_SLOT | KDF_MODE_TARGET_OUTPUT,
                               0x0005,
                               0,
                               self.salt,
                               out_kdf_aes,
                               out_nonce
                               )
        assert (
            status == cal.Status.ATCA_SUCCESS
        ), f"atcab_kdf has failed with: {status: 02X}"
        self.ephemeral_key_mcu = out_kdf_aes[0:16]
        print('Derived key on embedded side:', canvas=b)
        print(pretty_print_hex(self.ephemeral_key_mcu, li=8, indent=''))
        print('Generated using SALT and Master symmetric key' + '\n')

    def encrypt_msg_on_host(self, b=None):
        print('Generating random message to encrypt...', canvas=b)
        self.random_message = os.urandom(16)
        print("Generated message:")
        print(pretty_print_hex(self.random_message, li=8, indent=''))

        # Using AES functions from Cryptography module to encrypt
        cipher = Cipher(algorithms.AES(self.ephemeral_key_mcu), modes.ECB())
        encryptor = cipher.encryptor()
        self.encrypted_msg = encryptor.update(self.random_message) + encryptor.finalize()

        print('\nEncrypting message using ephemeral key...', canvas=b)
        print("Encrypted message:")
        print(pretty_print_hex(self.encrypted_msg, li=8, indent='') + '\n')

    def derive_decrypt_msg(self, b=None):
        print('Deriving key on HOST side...', canvas=b)
        # Using AES functions from Cryptography module to derive key on host
        cipher = Cipher(algorithms.AES(self.sym_key_bytes), modes.ECB())
        encryptor = cipher.encryptor()
        ephemeral_key = encryptor.update(self.salt) + encryptor.finalize()
        print('\nKey derived on HOST side:', canvas=b)
        print(pretty_print_hex(ephemeral_key, li=8, indent=''))

        print('\nRecieved encrypted message:', canvas=b)
        print(pretty_print_hex(self.encrypted_msg, li=8, indent=''))

        # Using AES functions from Cryptography module to decrypt
        print('\nDecrypting the message recieved', canvas=b)
        cipher = Cipher(algorithms.AES(ephemeral_key), modes.ECB())
        decryptor = cipher.decryptor()
        decrypted_msg = decryptor.update(self.encrypted_msg) + decryptor.finalize()
        print("Decrypted message:")
        print(pretty_print_hex(decrypted_msg, li=8, indent=''))

        print('\nComparing the generated message and the decrypted message', canvas=b)
        assert (self.random_message == decrypted_msg[0:16])
        print('\nThe messages match - Decryption successfull')
